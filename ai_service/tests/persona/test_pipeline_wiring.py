"""Pipeline wiring tests: the persona must reach the system prompt end-to-end.

Regression guard for the "missing persona" issue — PersonaLoadStage and
PlatformContextLoadStage must be present in the pipeline and their output must
reach SimplePromptBuilder.
"""
import pytest

from app.chat.context.execution_context import ExecutionContext
from app.chat.pipeline.cache_stage import CacheStage
from app.chat.pipeline.memory_stage import MemoryLoadStage
from app.chat.pipeline.persona_stage import PersonaLoadStage
from app.chat.pipeline.platform_context_stage import PlatformContextLoadStage
from app.memory.default_manager import DefaultMemoryManager
from app.prompt_builder.simple_prompt_builder import SimplePromptBuilder


class _NoopCache:
    async def get(self, query):
        return None

    async def store(self, *args, **kwargs):
        return None


class _FakePlatform:
    async def build(self, token):
        return (
            "### User Platform Context ###\n"
            "Name: Test Learner\n"
            "Active Enrollments: SIEM Fundamentals"
        )


def _build_wired_context():
    memory_manager = DefaultMemoryManager(memory_service=_NoopCache())
    stages = [
        CacheStage(_NoopCache()),
        MemoryLoadStage(memory_manager),
        PlatformContextLoadStage(_FakePlatform()),
        PersonaLoadStage(),
    ]
    return stages


@pytest.mark.asyncio
async def test_persona_reaches_system_prompt_end_to_end():
    context = ExecutionContext(
        metadata={"query": "siem", "token": "test-token"}, memory={}
    )
    for stage in _build_wired_context():
        context = await stage.execute(context)

    assert "persona_block" in context.memory
    assert "learner_level" in context.memory
    assert "platform_context" in context.memory

    _prompt, system_prompt = SimplePromptBuilder().build_prompt(
        "siem", dict(context.memory)
    )
    assert "[Persona]" in system_prompt
    assert "[User Platform Context]" in system_prompt
    assert "cybersecurity" in system_prompt


@pytest.mark.asyncio
async def test_persona_stage_preserves_memory_keys():
    stage = PersonaLoadStage()
    context = ExecutionContext(
        metadata={"query": "hi"},
        memory={
            "recent_context": "User: hello\nAssistant: hi",
            "messages": [{"role": "user", "content": "hello"}],
        },
    )
    result = await stage.execute(context)
    assert result.memory["recent_context"].startswith("User: hello")
    assert result.memory["messages"] == [{"role": "user", "content": "hello"}]
    assert "[Persona]" in result.memory["persona_block"]
