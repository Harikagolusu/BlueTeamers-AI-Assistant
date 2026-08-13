"""Guest conversational-memory coverage.

Guests (no JWT, persistent ``client_id``) must get the same short-term
conversation memory window as authenticated users — keyed under the namespaced
``guest:<client_id>::<conversation_id>`` scope — but their turns must NOT be
recorded into the authenticated user's Recent Conversations store.
"""
import pytest

from app.chat.context.execution_context import ExecutionContext
from app.chat.pipeline.memory_stage import MemoryLoadStage, _memory_session_user
from app.chat.pipeline.persistence_stage import PersistenceStage
from app.chat.service import GUEST_ID_PREFIX, _resolve_user
from app.models.chat.chat_models import (
    ChatResponse,
    ExecutionResult,
    ExecutionStatus,
)


class FakeMemory:
    def __init__(self):
        self.turns = []
        self.saved_keys = []

    async def save_turn(self, session_user, tenant_id, turn_data):
        self.saved_keys.append(session_user)
        self.turns.append(turn_data)

    async def load_history(self, session_user, tenant_id):
        return {"recent_context": "", "messages": []}


class FakeConversations:
    def __init__(self):
        self.turns = []

    async def record_turn(self, user_id, conversation_id, user_message, ai_message, metadata=None):
        self.turns.append(user_id)


# --------------------------------------------------------------------------- identity


def test_guest_identity_from_client_id():
    session_user, tenant_id = _resolve_user(None, client_id="client-abc")
    assert session_user == f"{GUEST_ID_PREFIX}client-abc"
    assert tenant_id is None


def test_fully_anonymous_has_no_identity():
    session_user, tenant_id = _resolve_user(None, None)
    assert session_user is None
    assert tenant_id is None


def test_invalid_token_with_client_id_falls_back_to_guest():
    session_user, tenant_id = _resolve_user("garbage.token", client_id="client-abc")
    assert session_user == f"{GUEST_ID_PREFIX}client-abc"


def test_guest_memory_scope_is_per_conversation():
    context = ExecutionContext(
        session_user=f"{GUEST_ID_PREFIX}client-abc",
        metadata={"conversation_id": "conv-1"},
    )
    assert _memory_session_user(context) == f"{GUEST_ID_PREFIX}client-abc::conv-1"


# ------------------------------------------------------------------- persistence


@pytest.mark.asyncio
async def test_guest_turn_writes_memory_but_not_conversations():
    memory = FakeMemory()
    conversations = FakeConversations()
    stage = PersistenceStage(memory, conversation_service=conversations)

    context = ExecutionContext(
        session_user=f"{GUEST_ID_PREFIX}client-abc",
        streaming_mode=False,
        metadata={
            "query": "My name is Harika",
            "conversation_id": "conv-1",
            "chat_response": ChatResponse(
                conversation_id="conv-1",
                message="Hello Harika",
                metadata={},
            ),
            "execution_result": ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                engine_name="GENERAL",
                message="Hello Harika",
            ),
        },
    )

    await stage.execute(context)

    assert len(memory.turns) == 1
    assert memory.turns[0]["query"] == "My name is Harika"
    assert memory.turns[0]["response"] == "Hello Harika"
    assert memory.saved_keys == [f"{GUEST_ID_PREFIX}client-abc::conv-1"]
    assert conversations.turns == []


@pytest.mark.asyncio
async def test_guest_streaming_turn_defers_and_excludes_conversations():
    memory = FakeMemory()
    conversations = FakeConversations()
    stage = PersistenceStage(memory, conversation_service=conversations)

    result = ExecutionResult(
        status=ExecutionStatus.SUCCESS,
        engine_name="GENERAL",
        message="[Streaming Generator]",
        metadata={"generator": "some-generator"},
    )
    context = ExecutionContext(
        session_user=f"{GUEST_ID_PREFIX}client-abc",
        streaming_mode=True,
        metadata={
            "query": "say hi",
            "conversation_id": "conv-1",
            "chat_response": ChatResponse(
                conversation_id="conv-1",
                message="[Streaming Generator]",
                metadata={"generator": "some-generator"},
            ),
            "execution_result": result,
        },
    )

    await stage.execute(context)

    assert memory.turns == []
    assert conversations.turns == []
    pending = result.metadata["_pending_turn"]
    assert pending["memory_session_user"] == f"{GUEST_ID_PREFIX}client-abc::conv-1"


# ----------------------------------------------------------------------- load


@pytest.mark.asyncio
async def test_memory_load_stage_runs_for_guests():
    memory = FakeMemory()
    stage = MemoryLoadStage(memory)

    context = ExecutionContext(
        session_user=f"{GUEST_ID_PREFIX}client-abc",
        metadata={"conversation_id": "conv-1"},
    )

    out = await stage.execute(context)
    assert out.memory is not None


@pytest.mark.asyncio
async def test_memory_load_stage_preserves_language_keys():
    """MemoryLoadStage must MERGE history into existing memory, not replace it,
    so upstream keys like the resolved language_block survive."""
    memory = FakeMemory()
    stage = MemoryLoadStage(memory)

    context = ExecutionContext(
        session_user=f"{GUEST_ID_PREFIX}client-abc",
        metadata={"conversation_id": "conv-1"},
        memory={"language": "te+en", "language_block": "[Response Language]..."},
    )

    out = await stage.execute(context)
    assert out.memory["language"] == "te+en"
    assert out.memory["language_block"] == "[Response Language]..."
    assert "recent_context" in out.memory
