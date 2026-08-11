"""Course-aware gating for the interactive Assessment Agent.

The Assessment Agent may only offer a quiz when ALL of the following hold:

  - The user is enrolled in a course,
  - The asked topic belongs to that enrolled course,
  - The user has asked a learning-related question, and
  - The user has not recently completed an assessment for that topic.

When enrolment cannot be confirmed (or the topic does not map to an enrolled
course), the agent stays inactive and the chat pipeline delegates to the Course
Recommendation service instead (which is a separate system by design).

This module is intentionally free of recommendation logic: it only decides
*quiz eligibility* from the learner's live enrolment state so the Assessment
Agent stays distinctly separate from the Course Recommendation system.
"""
import logging
import re
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel

from app.platform.models import Course
from app.platform.repositories.interfaces import IPlatformRepository

logger = logging.getLogger("app.agents.assessment.course_context")


class CourseOfferAction(str, Enum):
    """What the chat pipeline should do after a suitable learning answer."""

    OFF = "off"                        # not a learning context -> do nothing
    OFFER_QUIZ = "offer_quiz"          # enrolled & topic matches -> offer a quiz
    RECOMMEND_COURSE = "recommend_course"  # not enrolled -> delegate to Course Recommendation
    RECENTLY_ASSESSED = "recently_assessed"  # assessed recently -> don't interrupt again


class CourseOffer(BaseModel):
    """Course-aware decision for whether to offer / recommend after an answer."""

    action: str = CourseOfferAction.OFF.value
    suitable: bool = False             # keyword-level learning/assessment suitability
    course: Optional[Course] = None
    course_slug: Optional[str] = None
    topic: str = ""
    reason: str = ""


# Controller keywords used to map an asked topic to an enrolled course. These
# mirror the platform catalog so a bare topic like "log analysis" deterministically
# resolves to the enrolled "Log Analysis for Beginners" course without an LLM.
_COURSE_KEYWORDS: Dict[str, tuple] = {
    "blue-team-soc-fundamentals": ("soc", "blue team", "blue-team", "analyst", "monitoring"),
    "log-analysis-for-beginners": ("log analysis", "logs", "log", "parsing", "syslog"),
    "siem-fundamentals": ("siem", "security information", "alert", "correlation", "soc"),
    "network-fundamentals": ("network", "tcp", "ip", "osi", "protocol", "routing"),
    "network-security-monitoring": ("network security", "monitoring", "ids", "ips", "packet"),
    "incident-response-fundamentals": ("incident response", "ir", "containment", "eradication"),
    "threat-hunting-fundamentals": ("threat hunting", "hunting", "hypothesis"),
    "detection-engineering-basics": ("detection engineering", "detection", "sigma", "rule"),
    "malware-analysis-fundamentals": ("malware", "malware analysis", "reverse", "sandbox"),
    "soc-analyst-path": ("soc analyst", "career", "path", "journey"),
}


def _tokens(text: str) -> List[str]:
    return [t for t in re.split(r"[^a-z0-9]+", (text or "").lower()) if len(t) > 1]


class CourseContextService:
    """Resolves quiz eligibility from the learner's live enrolment state."""

    def __init__(self, platform_repo: IPlatformRepository):
        self.platform_repo = platform_repo

    async def enrolled_courses(self, token: Optional[str]) -> List[Course]:
        """Courses the user is currently enrolled in (empty for anonymous)."""
        if not token:
            return []
        try:
            return list(await self.platform_repo.get_enrolled_courses(token) or [])
        except Exception as exc:  # pragma: no cover - defensive against repo outages
            logger.warning("Failed to fetch enrolled courses for assessment gating: %s", exc)
            return []

    def match_course(self, query: str, courses: List[Course]) -> Optional[Course]:
        """Deterministically match an asked topic to one of the given courses."""
        text = (query or "").lower()
        best: Optional[Course] = None
        best_score = 0
        for course in courses:
            score = self._score(text, course)
            if score > best_score:
                best, best_score = course, score
        return best if best_score > 0 else None

    @classmethod
    def _score(cls, text: str, course: Course) -> int:
        slug = (course.id or "").lower()
        title = (course.title or "").lower()
        keywords = list(_COURSE_KEYWORDS.get(slug, ())) + [slug.replace("-", " ")]
        score = 0
        for kw in keywords:
            if kw and kw in text:
                score += 2
        for token in _tokens(title):
            if token in text:
                score += 1
        return score

    def recently_assessed(
        self,
        profile,
        course: Optional[Course],
        window_seconds: int,
    ) -> bool:
        """True if the learner was assessed on this course within the window."""
        if profile is None or not window_seconds:
            return False
        slug = (course.id if course else "").lower()
        history = getattr(profile, "quiz_history", None) or []
        now = datetime.now(timezone.utc)
        for entry in history:
            if slug and str(entry.get("course_slug", "")).lower() != slug:
                continue
            at = entry.get("at")
            if not at:
                continue
            try:
                ts = datetime.fromisoformat(str(at))
            except (TypeError, ValueError):
                continue
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            if (now - ts).total_seconds() < window_seconds:
                return True
        return False
