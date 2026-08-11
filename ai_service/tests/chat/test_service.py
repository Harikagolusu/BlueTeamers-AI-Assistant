import pytest
from app.chat.service import ChatService
from app.chat.interfaces.i_chat_orchestrator import IChatOrchestrator
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult, ChatRequest, ChatResponse

class MockOrchestrator(IChatOrchestrator):
    async def execute_pipeline(self, context: ExecutionContext) -> ExecutionResult:
        return ExecutionResult.success(engine="MOCK", message="service mock")

@pytest.mark.asyncio
async def test_chat_service_non_streaming():
    orchestrator = MockOrchestrator()
    service = ChatService(orchestrator)
    
    request = ChatRequest(message="hello", stream=False)
    response = await service.process_request(request)
    
    assert isinstance(response, ChatResponse)
    assert response.message == "service mock"

@pytest.mark.asyncio
async def test_chat_service_streaming():
    orchestrator = MockOrchestrator()
    service = ChatService(orchestrator)
    
    request = ChatRequest(message="hello", stream=True)
    response = await service.process_request(request)
    
    # It should return an AsyncGenerator for streaming
    import collections.abc
    assert isinstance(response, collections.abc.AsyncGenerator)
    
    chunks = [chunk async for chunk in response]
    # Mock orchestrator returns message "service mock" with no generator, so the
    # fallback path emits one event per word + a metadata event + [DONE].
    assert len(chunks) == 4
