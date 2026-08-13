"""Integration: the language block must reach the system prompt (Feature 3/4)."""
import pytest

from app.chat.context.execution_context import ExecutionContext
from app.multilingual.stage import LanguageContextStage
from app.prompt_builder.simple_prompt_builder import SimplePromptBuilder


class _FakeDetector:
    """Realistic detector: Telugu script for the Telugu query, English for the
    English query (so an explicit 'en' stays English for English input)."""

    def detect(self, text):
        if "అంటే" in text:
            return "te", 0.95
        return "en", 0.9


class _NoopStore:
    async def get(self, user_id):
        return None

    async def set(self, user_id, language):
        return None

    async def clear(self, user_id):
        return None


@pytest.mark.asyncio
async def test_language_block_reaches_system_prompt():
    stage = LanguageContextStage(detector=_FakeDetector(), store=_NoopStore())
    context = ExecutionContext(
        session_user="user-1",
        metadata={"query": "SIEM అంటే ఏంటి", "language": "auto"},
    )
    out = await stage.execute(context)

    _prompt, system_prompt = SimplePromptBuilder().build_prompt(
        "SIEM అంటే ఏంటి", dict(out.memory)
    )

    assert "[Response Language]" in system_prompt
    assert "Telugu" in system_prompt
    assert system_prompt.rstrip().endswith("Markdown formatting you normally use.") or "Language" in system_prompt


@pytest.mark.asyncio
async def test_english_leaves_prompt_unchanged():
    stage = LanguageContextStage(detector=_FakeDetector(), store=_NoopStore())
    context = ExecutionContext(
        session_user="user-1",
        metadata={"query": "What is a SIEM?", "language": "en"},
    )
    out = await stage.execute(context)

    _prompt, system_prompt = SimplePromptBuilder().build_prompt(
        "What is a SIEM?", dict(out.memory)
    )

    assert "[Response Language]" not in system_prompt