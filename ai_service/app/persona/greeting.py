"""Template-based greeting responses for the BlueTeamers AI Workspace.

Greetings and small talk don't need the LLM: answering them with a generated
system message saves tokens while still being persona-aware and level-aware.
The GreetingResponseBuilder composes a short, professional opening from the
active persona, the learner's detected level, and any available platform
context (name, enrollments).
"""
import logging
import re
from typing import Any, Optional

from app.persona.levels import LEVEL_PROFILES, LearnerLevel, get_level
from app.persona.registry import PersonaRegistry, get_persona_registry

logger = logging.getLogger("app.persona.greeting")

# Intents that can be answered without the LLM.
TEMPLATE_INTENTS = {"GREETING", "SMALL_TALK"}


def _extract_name(platform_context: Optional[str]) -> Optional[str]:
    """Pulls 'Name: ...' out of the user platform context block."""
    if not platform_context:
        return None
    m = re.search(r"^Name:\s*(.+)$", platform_context, re.MULTILINE)
    if not m:
        return None
    name = m.group(1).strip()
    if name in ("Not available.", "None.", ""):
        return None
    return name


def _extract_courses(platform_context: Optional[str]) -> Optional[str]:
    """Pulls 'Active Enrollments: ...' out of the user platform context block."""
    if not platform_context:
        return None
    m = re.search(r"^Active Enrollments:\s*(.+)$", platform_context, re.MULTILINE)
    if not m:
        return None
    courses = m.group(1).strip()
    if courses in ("None.", "Not available.", ""):
        return None
    return courses


class GreetingResponseBuilder:
    """Builds a templated, persona-aware greeting without calling the LLM."""

    def __init__(self, registry: Optional[PersonaRegistry] = None):
        self._registry = registry or get_persona_registry()

    @staticmethod
    def supports(query: str, intent: str) -> bool:
        """True if this query can be answered with a template (no LLM)."""
        return (intent or "").upper() in TEMPLATE_INTENTS

    def build(
        self,
        query: str,
        intent: str,
        memory: Optional[dict[str, Any]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        """Builds the greeting response for the given intent and context."""
        memory = memory or {}
        persona = self._registry.active((metadata or {}).get("persona"))
        level = get_level(memory.get("learner_level"))
        name = _extract_name(memory.get("platform_context"))
        courses = _extract_courses(memory.get("platform_context"))

        if intent.upper() == "SMALL_TALK":
            body = self._small_talk_line()
        else:
            body = self._greeting_line(level, name, courses)
        return body

    def _opening(self, name: Optional[str]) -> str:
        if name:
            return (
                f"Welcome back to the BlueTeamers AI Workspace, {name}. "
                f"I'm your AI assistant, supported by a team of specialized "
                f"agents ready to help you."
            )
        return (
            "Welcome to the BlueTeamers AI Workspace. I'm your AI assistant, "
            "supported by a team of specialized agents ready to help you."
        )

    def _level_offer(self, level: LearnerLevel) -> str:
        offers = {
            LearnerLevel.BEGINNER: (
                "I can walk you through the fundamentals — how a SOC operates, "
                "phishing basics, or how SIEM detections are built — one step at "
                "a time, with clear explanations."
            ),
            LearnerLevel.INTERMEDIATE: (
                "We can go straight to practical work: log correlation, detection "
                "logic, or a full investigation workflow."
            ),
            LearnerLevel.ADVANCED: (
                "We can go deeper: detection engineering, MITRE ATT&CK mapping, "
                "threat hunting, or an advanced incident response scenario."
            ),
            LearnerLevel.PROFESSIONAL: (
                "We can tackle enterprise-grade topics: detection strategy, SOC "
                "architecture, false-positive tuning, or production runbooks."
            ),
            LearnerLevel.INSTRUCTOR: (
                "I can help you build teaching material: lesson plans, quiz "
                "questions, labs, and assessments for your learners."
            ),
        }
        return offers.get(level, offers[LearnerLevel.BEGINNER])

    _AGENT_LIST = (
        "**My specialized agents**\n"
        "- **Knowledge Assistant** — explains cybersecurity concepts and answers questions from our knowledge base.\n"
        "- **Learning Coach** — builds study plans, roadmaps, and skill-gap analyses.\n"
        "- **Threat Intelligence** — provides insight on threat actors, TTPs, IOCs, and campaigns.\n"
        "- **Investigation Assistant** — guides incident triage, evidence correlation, and investigation timelines.\n"
        "- **SOC Analyst** — performs tool-backed analysis such as log and alert review.\n"
        "- **Lab Mentor** — guides you through hands-on labs without giving away solutions.\n"
        "- **Assessment Coach** — prepares you for quizzes, assessments, and certifications.\n"
        "- **Platform Assistant** — answers questions about your courses, progress, and certificates."
    )

    def _greeting_line(
        self, level: LearnerLevel, name: Optional[str], courses: Optional[str]
    ) -> str:
        # Short greeting: opening + a brief tailored offer + a question.
        # (The previous long agent-list is intentionally removed so "hi"/"hello"
        # gets a concise reply instead of a wall of text.)
        return (
            f"{self._opening(name)} "
            f"{self._level_offer(level)} "
            "How can I help you today?"
        )

    def _small_talk_line(self) -> str:
        return (
            "Copy that. I'm focused on getting you sharp at security operations. "
            "Want to dig into a concept, a lab, or a course topic?"
        )
