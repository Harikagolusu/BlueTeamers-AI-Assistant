import pytest
import asyncio
from app.memory.memory_store import InMemoryStore
from app.memory.memory_service import MemoryService
from app.memory.models import MessageRole
from app.memory.exceptions import SessionNotFound

@pytest.fixture
def store():
    return InMemoryStore()

@pytest.fixture
def service(store):
    return MemoryService(store=store, enabled=True, max_messages=5)

@pytest.mark.asyncio
async def test_session_creation(service):
    session_id = "test-session-1"
    
    # Exists should be false
    assert not await service.session_exists(session_id)
    
    # Create session
    session = await service.create_session(session_id)
    assert session.session_id == session_id
    assert await service.session_exists(session_id)
    
    # Messages should be empty
    msgs = await service.get_recent_messages(session_id)
    assert len(msgs) == 0

@pytest.mark.asyncio
async def test_append_message_and_retrieve(service):
    session_id = "test-session-2"
    
    await service.append_message(session_id, MessageRole.USER, "Hello AI")
    await service.append_message(session_id, MessageRole.ASSISTANT, "Hello Human")
    
    msgs = await service.get_recent_messages(session_id)
    assert len(msgs) == 2
    assert msgs[0].role == MessageRole.USER
    assert msgs[0].content == "Hello AI"
    assert msgs[1].role == MessageRole.ASSISTANT
    assert msgs[1].content == "Hello Human"

@pytest.mark.asyncio
async def test_window_trimming(service):
    session_id = "test-session-3"
    
    # Service max_messages is 5
    for i in range(10):
        await service.append_message(session_id, MessageRole.USER, f"Msg {i}")
        
    msgs = await service.get_recent_messages(session_id)
    assert len(msgs) == 5
    # The last 5 messages should be 5, 6, 7, 8, 9
    assert msgs[0].content == "Msg 5"
    assert msgs[-1].content == "Msg 9"

@pytest.mark.asyncio
async def test_clear_session(service):
    session_id = "test-session-4"
    
    await service.append_message(session_id, MessageRole.USER, "Msg")
    msgs = await service.get_recent_messages(session_id)
    assert len(msgs) == 1
    
    await service.clear_conversation(session_id)
    msgs = await service.get_recent_messages(session_id)
    assert len(msgs) == 0

@pytest.mark.asyncio
async def test_delete_session(service):
    session_id = "test-session-5"
    
    await service.append_message(session_id, MessageRole.USER, "Msg")
    assert await service.session_exists(session_id)
    
    success = await service.delete_session(session_id)
    assert success is True
    assert not await service.session_exists(session_id)

@pytest.mark.asyncio
async def test_concurrent_sessions(service):
    session_1 = "test-session-6"
    session_2 = "test-session-7"
    
    await service.append_message(session_1, MessageRole.USER, "S1 M1")
    await service.append_message(session_2, MessageRole.USER, "S2 M1")
    
    msgs_1 = await service.get_recent_messages(session_1)
    msgs_2 = await service.get_recent_messages(session_2)
    
    assert len(msgs_1) == 1
    assert msgs_1[0].content == "S1 M1"
    
    assert len(msgs_2) == 1
    assert msgs_2[0].content == "S2 M1"

@pytest.mark.asyncio
async def test_disabled_memory(store):
    disabled_service = MemoryService(store=store, enabled=False, max_messages=5)
    session_id = "test-session-disabled"
    
    await disabled_service.append_message(session_id, MessageRole.USER, "Msg")
    
    msgs = await disabled_service.get_recent_messages(session_id)
    assert len(msgs) == 0
    assert not await disabled_service.session_exists(session_id)

@pytest.mark.asyncio
async def test_health_check(store):
    from app.memory.health import MemoryHealthService
    health_service = MemoryHealthService(store=store, enabled=True)
    
    status = await health_service.check_health()
    assert status["status"] == "healthy"
    assert status["enabled"] is True
    assert status["store"]["backend"] == "in_memory"
