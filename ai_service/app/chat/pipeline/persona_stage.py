"""PersonaLoadStage: injects the BlueTeamers persona + learner level.

Runs after PlatformContextLoadStage so it has access to the user's platform
context (certificates, progress, enrollments) and conversation memory. It
computes the learner's level and attaches the persona instruction blocks to
`context.memory` where SimplePromptBuilder picks them up.
"""
import logging

from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.persona.builder import PersonaPromptBuilder
from app.persona.registry import get_persona_registry

logger = logging.getLogger("app.chat.pipeline.persona_stage")


class PersonaLoadStage(IExecutionStage):
    def __init__(self, persona_builder: PersonaPromptBuilder = None):
        self._persona_builder = persona_builder or PersonaPromptBuilder(
            registry=get_persona_registry()
        )

    @property
    def name(self) -> str:
        return "LoadPersona"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        new_memory = dict(context.memory) if context.memory else {}

        metadata = context.metadata
        level = self._persona_builder.detect_level(
            memory=context.memory, metadata=metadata
        )
        persona_block = self._persona_builder.build_persona_block(
            memory=context.memory,
            metadata=metadata,
            persona_name=metadata.get("persona"),
        )
        context_block = self._persona_builder.build_context_block(
            memory=context.memory, metadata=metadata
        )

        new_memory["learner_level"] = level.value
        new_memory["learner_level_label"] = level.value.capitalize()
        new_memory["persona_block"] = persona_block
        if context_block:
            new_memory["persona_context"] = context_block

        return context.with_memory(new_memory)
