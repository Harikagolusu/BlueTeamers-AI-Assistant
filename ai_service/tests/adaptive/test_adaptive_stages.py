"""Tests for the adaptive + memory pipeline stages (Sprint 4 wiring)."""
import pytest

from app.adaptive.engine import AdaptiveLearningEngine
from app.adaptive.service import AdaptiveLearningService
from app.adaptive.session_memory import SessionMemoryManager
from app.adaptive.store import SQLiteLearnerStore
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult
from app.chat.pipeline.adaptive_stage import AdaptiveContextStage, AdaptivePersistenceStage
from app.chat.pipeline.memory_stage import MemoryLoadStage


@pytest.fixture
def service(tmp_path):
    store = SQLiteLearnerStore(db_path=str(tmp_path / "stages.db"))
    return AdaptiveLearningService(
        engine=AdaptiveLearningEngine(store),
        session_memory=SessionMemoryManager(store),
        store=store,
    ), store


def _context(**overrides):
    defaults = {
        "session_user": "user@example.com",
        "metadata": {
            "query": "Explain Wazuh decoders",
            "conversation_id": "conv-1",
        },
    }
    defaults.update(overrides)
    return ExecutionContext(**defaults)


@pytest.mark.asyncio
async def test_adaptive_context_stage_injects_blocks(service):
    adaptive, _ = service
    context = await AdaptiveContextStage(adaptive).execute(_context())
    assert "adaptive_learning" in context.memory
    assert context.memory["adaptive_learning"]["primary_topic"] == "wazuh"
    assert "session_memory" in context.memory
    assert context.memory["session_memory"]["conversation_id"] == "conv-1"


@pytest.mark.asyncio
async def test_adaptive_context_skips_anonymous(service):
    adaptive, _ = service
    context = await AdaptiveContextStage(adaptive).execute(
        ExecutionContext(metadata={"query": "hi"})
    )
    assert "adaptive_learning" not in context.memory


@pytest.mark.asyncio
async def test_adaptive_persistence_updates_profile_and_session(service, tmp_path):
    adaptive, store = service
    context = await AdaptiveContextStage(adaptive).execute(_context())
    result = ExecutionResult.success(engine="RAG", message="Wazuh decoders parse log lines")
    context = context.model_copy(update={
        "metadata": {**context.metadata, "execution_result": result},
    })
    await AdaptivePersistenceStage(adaptive).execute(context)

    profile = await store.load_profile("user@example.com")
    assert profile.topic_confidences["wazuh"].evidence_count == 1
    session = await store.load_session("user@example.com", "conv-1")
    assert "Wazuh" in session.summary
    assert session.facts


@pytest.mark.asyncio
async def test_adaptive_persistence_never_breaks_on_missing_adaptation(service):
    adaptive, _ = service
    context = _context(metadata={"query": "hi", "conversation_id": "conv-1"})
    result = ExecutionResult.success(engine="GENERAL", message="hi")
    context = context.model_copy(update={"metadata": {**context.metadata, "execution_result": result}})
    out = await AdaptivePersistenceStage(adaptive).execute(context)
    assert out is not None


class _RecordingMemoryManager:
    def __init__(self):
        self.loaded_for = None
        self.saved_for = None

    async def load_history(self, session_user, tenant_id):
        self.loaded_for = session_user
        return {"recent_context": "", "messages": []}

    async def save_turn(self, session_user, tenant_id, turn_data):
        self.saved_for = session_user


@pytest.mark.asyncio
async def test_memory_load_stage_scopes_per_conversation():
    memory = _RecordingMemoryManager()
    stage = MemoryLoadStage(memory)
    await stage.execute(_context(metadata={"query": "q", "conversation_id": "conv-9"}))
    assert memory.loaded_for == "user@example.com::conv-9"


@pytest.mark.asyncio
async def test_memory_load_stage_keeps_user_scope_without_conversation():
    memory = _RecordingMemoryManager()
    stage = MemoryLoadStage(memory)
    await stage.execute(_context(metadata={"query": "q"}))
    assert memory.loaded_for == "user@example.com"
