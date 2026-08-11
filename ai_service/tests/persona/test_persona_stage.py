import pytest
from unittest.mock import MagicMock

from app.chat.context.execution_context import ExecutionContext
from app.chat.pipeline.persona_stage import PersonaLoadStage


@pytest.fixture
def stage():
    return PersonaLoadStage(persona_builder=MagicMock())


class TestPersonaLoadStage:
    @pytest.mark.asyncio
    async def test_injects_persona_into_memory(self, stage):
        stage._persona_builder.detect_level.return_value = MagicMock(value="advanced")
        stage._persona_builder.build_persona_block.return_value = "[Persona] block"
        stage._persona_builder.build_context_block.return_value = "[Learning Context] ctx"

        ctx = ExecutionContext(metadata={"query": "hi"})
        result = await stage.execute(ctx)

        assert result.memory["learner_level"] == "advanced"
        assert result.memory["persona_block"] == "[Persona] block"
        assert result.memory["persona_context"] == "[Learning Context] ctx"

    @pytest.mark.asyncio
    async def test_preserves_existing_memory(self, stage):
        stage._persona_builder.detect_level.return_value = MagicMock(value="beginner")
        stage._persona_builder.build_persona_block.return_value = "[Persona] block"
        stage._persona_builder.build_context_block.return_value = ""

        ctx = ExecutionContext(
            metadata={"query": "hi"}, memory={"platform_context": "ctx"}
        )
        result = await stage.execute(ctx)

        assert result.memory["platform_context"] == "ctx"
        assert result.memory["learner_level"] == "beginner"
        assert "persona_context" not in result.memory
