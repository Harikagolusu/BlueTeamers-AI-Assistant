import pytest
import asyncio
from typing import AsyncGenerator
from fastapi.responses import StreamingResponse

from app.rag.schemas import RAGRequest, RAGResponse, PipelineMetrics
from app.memory.memory_store import InMemoryStore
from app.memory.memory_service import MemoryService
from app.streaming.streaming_service import StreamingService
from app.streaming.exceptions import StreamCancellationException

class MockRAGService:
    def __init__(self, should_fail=False):
        self.should_fail = should_fail
        
    async def stream_answer(self, request: RAGRequest):
        if self.should_fail == "cancel":
            yield "Fail"
            raise asyncio.CancelledError()
        elif self.should_fail:
            yield "Fail"
            raise Exception("Mock provider error")
        else:
            yield "Hello"
            yield " World"
            yield RAGResponse(
                query=request.query,
                answer="Hello World",
                citations=[],
                metrics=PipelineMetrics()
            )

@pytest.fixture
def memory_service():
    store = InMemoryStore()
    return MemoryService(store=store, enabled=True, max_messages=10)

@pytest.fixture
def rag_service():
    return MockRAGService()

@pytest.fixture
def streaming_service(rag_service, memory_service):
    return StreamingService(rag_service=rag_service, memory_service=memory_service)

@pytest.mark.asyncio
async def test_streaming_success(streaming_service, memory_service):
    request = RAGRequest(query="Test", request_id=None)
    session_id = "test-session-1"
    
    events = []
    async for chunk in streaming_service.stream_chat(request, session_id):
        events.append(chunk)
        
    assert len(events) == 3
    # Verify SSE format
    assert events[0].startswith("data: ")
    assert events[0].endswith("\n\n")
    assert "token" in events[0]
    
    # Check memory persistence
    msgs = await memory_service.get_recent_messages(session_id)
    assert len(msgs) == 2
    assert msgs[0].content == "Test"
    assert msgs[1].content == "Hello World"

@pytest.mark.asyncio
async def test_streaming_failure(memory_service):
    rag_service = MockRAGService(should_fail=True)
    streaming_service = StreamingService(rag_service=rag_service, memory_service=memory_service)
    
    request = RAGRequest(query="Fail Query", request_id=None)
    session_id = "test-session-2"
    
    events = []
    with pytest.raises(Exception):
        async for chunk in streaming_service.stream_chat(request, session_id):
            events.append(chunk)
            
    assert len(events) == 2 # 1 token and 1 error event before raising
    assert "error" in events[-1]
    
    # Ensure memory was not persisted
    msgs = await memory_service.get_recent_messages(session_id)
    assert len(msgs) == 0

@pytest.mark.asyncio
async def test_streaming_cancellation(memory_service):
    rag_service = MockRAGService(should_fail="cancel")
    streaming_service = StreamingService(rag_service=rag_service, memory_service=memory_service)
    
    request = RAGRequest(query="Cancel Me", request_id=None)
    session_id = "test-session-3"
    
    events = []
    with pytest.raises(StreamCancellationException):
        async for chunk in streaming_service.stream_chat(request, session_id):
            events.append(chunk)

    # Memory should be empty
    msgs = await memory_service.get_recent_messages(session_id)
    assert len(msgs) == 0

@pytest.mark.asyncio
async def test_health_check(streaming_service):
    from app.streaming.health import StreamingHealthService
    health = StreamingHealthService(streaming_service)
    res = await health.check_health()
    assert res["status"] == "healthy"
