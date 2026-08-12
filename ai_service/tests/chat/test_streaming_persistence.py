"""Regression tests: streamed assistant replies must be persisted with the
real text, not the "[Streaming Generator]" placeholder.

PersistenceStage defers the turn when a streaming generator is present, then
ChatService persists the actual accumulated text once the stream completes.
"""
import json
from unittest.mock import patch

import pytest

from app.chat.context.execution_context import ExecutionContext
from app.chat.interfaces.i_chat_orchestrator import IChatOrchestrator
from app.chat.pipeline.persistence_stage import PersistenceStage
from app.chat.service import ChatService
from app.models.chat.chat_models import (
    ChatRequest,
    ChatResponse,
    ExecutionResult,
    ExecutionStatus,
)


class FakeMemory:
    def __init__(self):
        self.turns = []

    async def save_turn(self, session_user, tenant_id, turn_data):
        self.turns.append(turn_data)


class FakeConversations:
    def __init__(self):
        self.turns = []

    async def record_turn(self, user_id, conversation_id, user_message, ai_message, metadata=None):
        self.turns.append(
            {
                "user_id": user_id,
                "conversation_id": conversation_id,
                "user_message": user_message,
                "ai_message": ai_message,
                "metadata": metadata or {},
            }
        )


class StreamingOrchestrator(IChatOrchestrator):
    def __init__(self):
        self.context_seen = None

    async def execute_pipeline(self, context: ExecutionContext) -> ExecutionResult:
        self.context_seen = context

        async def gen():
            for tok in ["Hello", " ", "world", "!"]:
                yield tok

        return ExecutionResult(
            status=ExecutionStatus.SUCCESS,
            engine_name="GENERAL",
            message="[Streaming Generator]",
            metadata={
                "generator": gen(),
                "_pending_turn": {
                    "query": "say hi",
                    "session_user": "u1",
                    "tenant_id": "u1",
                    "memory_session_user": "u1::conv-abc",
                    "conversation_id": "conv-abc",
                    "conversation_metadata": {"conversation_type": "chat"},
                    "trace_id": "trace-1",
                },
            },
        )


@pytest.mark.asyncio
async def test_streamed_turn_is_persisted_with_real_text():
    memory = FakeMemory()
    conversations = FakeConversations()
    service = ChatService(
        StreamingOrchestrator(),
        memory_manager=memory,
        conversation_service=conversations,
    )

    request = ChatRequest(
        message="say hi",
        stream=True,
        conversation_id="conv-abc",
        token="fake-token",
    )
    with patch("app.chat.service.resolve_user_identity", return_value=("u1", "u1")):
        stream = await service.process_request(request)
    events = [event async for event in stream]

    assert events, "expected stream events"
    assert events[-1] == "data: [DONE]\n\n"

    assert memory.turns, "expected the deferred turn to be saved to memory"
    assert memory.turns[-1]["response"] == "Hello world!"
    assert memory.turns[-1]["query"] == "say hi"

    assert conversations.turns, "expected the deferred turn to be recorded"
    turn = conversations.turns[-1]
    assert turn["ai_message"] == "Hello world!"
    assert turn["user_message"] == "say hi"
    assert turn["conversation_id"] == "conv-abc"


@pytest.mark.asyncio
async def test_persistence_stage_defers_streaming_placeholder():
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
        session_user="u1",
        streaming_mode=True,
        metadata={
            "query": "say hi",
            "conversation_id": "conv-abc",
            "chat_response": ChatResponse(
                conversation_id="conv-abc",
                message="[Streaming Generator]",
                metadata={"generator": "some-generator"},
            ),
            "execution_result": result,
        },
    )

    await stage.execute(context)

    assert memory.turns == []
    assert conversations.turns == []
    assert result.metadata["_pending_turn"]["query"] == "say hi"
    assert result.metadata["_pending_turn"]["conversation_id"] == "conv-abc"


@pytest.mark.asyncio
async def test_persistence_stage_still_persists_non_streaming():
    memory = FakeMemory()
    conversations = FakeConversations()
    stage = PersistenceStage(memory, conversation_service=conversations)

    context = ExecutionContext(
        session_user="u1",
        streaming_mode=False,
        metadata={
            "query": "say hi",
            "conversation_id": "conv-abc",
            "chat_response": ChatResponse(
                conversation_id="conv-abc",
                message="Real answer",
                metadata={},
            ),
            "execution_result": ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                engine_name="GENERAL",
                message="Real answer",
            ),
        },
    )

    await stage.execute(context)

    assert len(memory.turns) == 1
    assert memory.turns[0]["response"] == "Real answer"
    assert len(conversations.turns) == 1
    assert conversations.turns[0]["ai_message"] == "Real answer"
