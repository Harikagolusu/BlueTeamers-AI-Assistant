"""Registry of available personas.

Personas are registered by name and resolved per request so the active persona
can be switched without changing the chat pipeline. Future personas can be
added by registering a new Persona instance.
"""
import logging
from typing import Optional

from app.persona.personas import Persona, CYBERSECURITY_MENTOR_PERSONA

logger = logging.getLogger("app.persona.registry")


class PersonaRegistry:
    def __init__(self, personas: Optional[list[Persona]] = None):
        self._personas: dict[str, Persona] = {}
        for persona in personas or []:
            self.register(persona)
        if CYBERSECURITY_MENTOR_PERSONA.name not in self._personas:
            self.register(CYBERSECURITY_MENTOR_PERSONA)

    def register(self, persona: Persona) -> None:
        self._personas[persona.name] = persona

    def get(self, name: Optional[str]) -> Optional[Persona]:
        if not name:
            return None
        return self._personas.get(name)

    def active(self, name: Optional[str]) -> Persona:
        persona = self.get(name)
        if persona is None:
            if name:
                logger.warning(
                    "Unknown persona '%s', falling back to '%s'",
                    name,
                    CYBERSECURITY_MENTOR_PERSONA.name,
                )
            return CYBERSECURITY_MENTOR_PERSONA
        return persona

    def names(self) -> list[str]:
        return list(self._personas.keys())


_default_registry: Optional[PersonaRegistry] = None


def get_persona_registry() -> PersonaRegistry:
    global _default_registry
    if _default_registry is None:
        _default_registry = PersonaRegistry()
    return _default_registry
