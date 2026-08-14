"""Tests for LanguageContextStage (Sprint 7 — Features 1, 2, 3, 6)."""
import pytest

from app.chat.context.execution_context import ExecutionContext
from app.multilingual.stage import LanguageContextStage


class _FakeDetector:
    def __init__(self, code="te", confidence=0.95):
        self.code = code
        self.confidence = confidence

    def detect(self, text):
        return self.code, self.confidence


class _FakeStore:
    def __init__(self, stored=None):
        self.stored = stored
        self.saved = []

    async def get(self, user_id):
        return self.stored

    async def set(self, user_id, language):
        self.stored = language
        self.saved.append((user_id, language))

    async def clear(self, user_id):
        self.stored = None


def _context(**kwargs):
    metadata = {"query": "SIEM ante enti", **kwargs.pop("metadata", {})}
    return ExecutionContext(session_user=kwargs.pop("session_user", "user-1"), metadata=metadata, **kwargs)


@pytest.mark.asyncio
async def test_explicit_manual_language_wins_and_persists():
    store = _FakeStore()
    # Detection agrees with the explicit pick -> manual selection is honored.
    stage = LanguageContextStage(detector=_FakeDetector("hi", 0.8), store=store)
    ctx = _context(metadata={"language": "hi"})

    out = await stage.execute(ctx)

    assert out.memory["language"] == "hi"
    assert out.memory["language_source"] == "manual"
    assert "[Response Language]" in out.memory["language_block"]
    assert store.stored == "hi"
    assert ctx.metadata["language"] == "hi"


@pytest.mark.asyncio
async def test_explicit_manual_language_always_wins():
    # A user pinned the selector to Hindi. Even if the query is clearly
    # Tinglish, the manual selection is honored (documented behaviour of a
    # manual override) — it is not silently switched away from.
    store = _FakeStore(stored="hi")
    stage = LanguageContextStage(detector=_FakeDetector("te+en", 0.95), store=store)
    ctx = _context(
        metadata={"query": "siem ante emiti", "language": "hi"},
    )

    out = await stage.execute(ctx)

    assert out.memory["language"] == "hi"
    assert out.memory["language_source"] == "manual"
    assert store.stored == "hi"


@pytest.mark.asyncio
async def test_explicit_manual_language_kept_when_detection_weak():
    # Pinned to Telugu, query is English with low confidence -> manual wins.
    store = _FakeStore()
    stage = LanguageContextStage(detector=_FakeDetector("en", 0.6), store=store)
    ctx = _context(metadata={"language": "te"})

    out = await stage.execute(ctx)

    assert out.memory["language"] == "te"
    assert out.memory["language_source"] == "manual"


@pytest.mark.asyncio
async def test_auto_detects_and_persists():
    store = _FakeStore()
    stage = LanguageContextStage(detector=_FakeDetector("te", 0.95), store=store)
    out = await stage.execute(_context(metadata={"language": "auto"}))

    assert out.memory["language"] == "te"
    assert out.memory["language_source"] == "detected"
    assert store.stored == "te"


@pytest.mark.asyncio
async def test_stored_preference_continues():
    store = _FakeStore(stored="te")
    # Detection returns English at low confidence -> stored preference wins.
    stage = LanguageContextStage(detector=_FakeDetector("en", 0.3), store=store)
    out = await stage.execute(_context())

    assert out.memory["language"] == "te"
    assert out.memory["language_source"] == "stored"


@pytest.mark.asyncio
async def test_high_confidence_script_switch_overrides_stored():
    store = _FakeStore(stored="en")
    stage = LanguageContextStage(detector=_FakeDetector("hi", 0.95), store=store)
    out = await stage.execute(_context())

    assert out.memory["language"] == "hi"
    assert out.memory["language_source"] == "detected"
    assert store.stored == "hi"


@pytest.mark.asyncio
async def test_guest_with_client_id_gets_detection_and_preference():
    store = _FakeStore()
    stage = LanguageContextStage(detector=_FakeDetector("te", 0.95), store=store)
    ctx = ExecutionContext(
        session_user=None,
        metadata={"query": "SIEM ante enti", "client_id": "dev-123"},
    )
    out = await stage.execute(ctx)

    assert out.memory["language"] == "te"
    assert store.stored == "te"


@pytest.mark.asyncio
async def test_no_identity_never_persists():
    store = _FakeStore()
    stage = LanguageContextStage(detector=_FakeDetector("te", 0.95), store=store)
    ctx = ExecutionContext(session_user=None, metadata={"query": "SIEM ante enti"})
    out = await stage.execute(ctx)

    assert out.memory["language"] == "te"
    assert store.saved == []


@pytest.mark.asyncio
async def test_english_produces_no_language_block():
    store = _FakeStore()
    stage = LanguageContextStage(detector=_FakeDetector("en", 0.9), store=store)
    out = await stage.execute(_context(metadata={"language": "en"}))

    assert out.memory["language"] == "en"
    assert out.memory["language_block"] == ""
