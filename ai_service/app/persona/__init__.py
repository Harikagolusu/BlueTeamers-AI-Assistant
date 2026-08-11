"""Persona system for the BlueTeamers AI Workspace.

Provides configurable personas, learner-level detection, and prompt-block
assembly so the AI behaves as a cybersecurity expert tailored to each learner.
"""
from app.persona.builder import PersonaPromptBuilder
from app.persona.detector import LearnerLevelDetector
from app.persona.levels import LearnerLevel
from app.persona.personas import Persona, CYBERSECURITY_MENTOR_PERSONA
from app.persona.registry import PersonaRegistry, get_persona_registry

__all__ = [
    "PersonaPromptBuilder",
    "LearnerLevelDetector",
    "LearnerLevel",
    "Persona",
    "CYBERSECURITY_MENTOR_PERSONA",
    "PersonaRegistry",
    "get_persona_registry",
]
