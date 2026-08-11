"""PersonaPromptBuilder: assembles the persona + level instruction block.

The block is injected into the system prompt by SimplePromptBuilder so every
engine (general, RAG, platform, specialist) inherits the BlueTeamers persona
and the learner's detected level.
"""
from typing import Any, Optional

from app.persona.detector import LearnerLevelDetector
from app.persona.levels import LEVEL_PROFILES, LearnerLevel, get_level
from app.persona.personas import Persona
from app.persona.registry import PersonaRegistry, get_persona_registry


class PersonaPromptBuilder:
    def __init__(
        self,
        detector: Optional[LearnerLevelDetector] = None,
        registry: Optional[PersonaRegistry] = None,
    ):
        self._detector = detector or LearnerLevelDetector()
        self._registry = registry or get_persona_registry()

    def detect_level(
        self,
        memory: Optional[dict[str, Any]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> LearnerLevel:
        return self._detector.detect(memory=memory, metadata=metadata)

    def build_persona_block(
        self,
        memory: Optional[dict[str, Any]] = None,
        metadata: Optional[dict[str, Any]] = None,
        persona_name: Optional[str] = None,
    ) -> str:
        """Builds the full persona system-instruction block."""
        persona = self._registry.active(persona_name)
        level = self.detect_level(memory=memory, metadata=metadata)
        level_profile = LEVEL_PROFILES.get(level, LEVEL_PROFILES[LearnerLevel.BEGINNER])

        parts = [
            "[Persona]",
            persona.identity,
            "",
            "[Expertise]",
            "Your areas of expertise include: " + ", ".join(persona.expertise),
            "",
            "[Communication Style]",
            persona.style,
            "",
            "[Teaching Level]",
            level_profile.teaching_guidance,
            "",
            "[Response Format]",
            persona.response_format,
            "",
            "[Domain Priority]",
            persona.domain_priority,
            "",
            "[Personality]",
            persona.personality,
        ]

        return "\n".join(parts)

    def build_context_block(
        self,
        memory: Optional[dict[str, Any]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        """Builds a context-awareness block from current learning context."""
        context_bits = []

        platform_context = (memory or {}).get("platform_context")
        if platform_context:
            context_bits.append(platform_context)

        current_course = (metadata or {}).get("course_title") or (metadata or {}).get("course")
        if current_course:
            context_bits.append(f"Current course: {current_course}")

        current_lesson = (metadata or {}).get("lesson_title") or (metadata or {}).get("lesson")
        if current_lesson:
            context_bits.append(f"Current lesson: {current_lesson}")

        current_lab = (metadata or {}).get("lab_title") or (metadata or {}).get("lab")
        if current_lab:
            context_bits.append(f"Current practice lab: {current_lab}")

        if not context_bits:
            return ""

        return "[Learning Context]\n" + "\n".join(context_bits)
