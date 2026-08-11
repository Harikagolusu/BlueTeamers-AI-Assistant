"""Learner level detection.

Determines the learner's proficiency level without requiring the user to
state it. It combines evidence from:

  - The platform user context string (certificates, progress, enrollments)
  - The current conversation history (vocabulary and self-description)
  - Explicit markers in the request metadata (e.g. a course or lab with a
    known difficulty)

Levels are scored independently and the highest-scoring level wins. A stable
'beginner' default keeps first-time users safe until evidence accumulates.
"""
import logging
import re
from typing import Any, Optional

from app.persona.levels import LearnerLevel, get_level

logger = logging.getLogger("app.persona.detector")

# Vocabulary signals per level, matched against the recent conversation text.
_VOCAB = {
    LearnerLevel.BEGINNER: [
        "what is", "how do i start", "i'm new", "im new", "beginner",
        "i don't understand", "i dont understand", "explain simply",
        "noob", "just starting", "first time",
    ],
    LearnerLevel.INTERMEDIATE: [
        "siem", "alert", "log", "event", "ticket", "triaging", "triage",
        "analyst", "false positive", "correlation", "mitre", "technique",
        "investigate", "windows event", "syslog",
    ],
    LearnerLevel.ADVANCED: [
        "threat hunting", "detection engineering", "sigma", "yara",
        "edr", "behavioral", "lateral movement", "privilege escalation",
        "ttps", "indicator of compromise", "ioc", "sandbox", "malware",
        "payload", "command and control", "c2", "root cause",
    ],
    LearnerLevel.PROFESSIONAL: [
        "tuning", "performance", "architecture", "enterprise deployment",
        "soar", "runbook", "playbook", "staffing", "mttr", "mttd",
        "escalation", "severity", "sla", "compliance", "hunt",
    ],
    LearnerLevel.INSTRUCTOR: [
        "teach", "lesson plan", "syllabus", "curriculum", "quiz for",
        "interview question", "assessment", "training material",
        "learning path", "course design", "train",
    ],
}

_COURSE_LEVEL_SIGNALS = {
    "advanced": 4,
    "expert": 5,
    "professional": 5,
    "intermediate": 3,
    "foundation": 2,
    "beginner": 1,
}


class LearnerLevelDetector:
    """Scoring-based detector producing a stable, evidence-driven level."""

    def detect(
        self,
        memory: Optional[dict[str, Any]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> LearnerLevel:
        memory = memory or {}
        metadata = metadata or {}

        explicit = metadata.get("learner_level")
        if explicit:
            return get_level(explicit)

        scores = {level: 0 for level in LearnerLevel}

        self._score_platform_context(scores, memory.get("platform_context", ""))
        self._score_conversation(scores, memory.get("recent_context", ""))
        self._score_course_signal(scores, metadata)

        # Always give beginners a baseline; evidence can push them upward.
        scores[LearnerLevel.BEGINNER] += 1

        best = max(scores, key=lambda lvl: scores[lvl])
        logger.debug("Detected learner level: %s (scores=%s)", best.value, scores)
        return best

    def _score_platform_context(self, scores: dict, platform_context: str) -> None:
        if not platform_context:
            return
        text = platform_context.lower()

        # Certificates are strong evidence of an experienced learner.
        if re.search(r"certificates?:\s*[^n]", text) and "certificates: none" not in text:
            scores[LearnerLevel.PROFESSIONAL] += 4
            scores[LearnerLevel.ADVANCED] += 3

        # Course levels in the enrollment list.
        for keyword, weight in _COURSE_LEVEL_SIGNALS.items():
            if keyword in text:
                scores[LearnerLevel.ADVANCED] += weight
                if keyword in ("advanced", "expert", "professional"):
                    scores[LearnerLevel.PROFESSIONAL] += max(0, weight - 2)

        # Progress percentages: sustained completion of lessons.
        percents = re.findall(r"(\d{1,3})%", text)
        if percents:
            avg = sum(int(p) for p in percents) / len(percents)
            if avg >= 60:
                scores[LearnerLevel.INTERMEDIATE] += 2
            if avg >= 90:
                scores[LearnerLevel.ADVANCED] += 2

    def _score_conversation(self, scores: dict, recent_context: str) -> None:
        if not recent_context:
            return
        text = recent_context.lower()
        for level, signals in _VOCAB.items():
            for signal in signals:
                if signal in text:
                    scores[level] += 2

    def _score_course_signal(self, scores: dict, metadata: dict) -> None:
        # A course/lab explicitly tagged with a difficulty level.
        for key in ("course_level", "lab_difficulty", "difficulty"):
            value = metadata.get(key)
            if not value:
                continue
            lowered = str(value).lower()
            for keyword, weight in _COURSE_LEVEL_SIGNALS.items():
                if keyword in lowered:
                    scores[LearnerLevel.ADVANCED] += weight
