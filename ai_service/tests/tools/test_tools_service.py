import pytest
import asyncio
from app.tools.service.tool_service import ToolService
from app.tools.interfaces.tool_executor import IToolExecutor
from app.tools.interfaces.registry import IToolRegistry
from app.tools.models.tool_request import ToolRequest
from app.tools.models.tool_response import ToolResponse
from app.tools.domain.exceptions import ToolValidationError, ToolNotFoundError, ToolExecutionError
from app.tools.service.tool_execution_context import ToolExecutionContext

class MockRegistry(IToolRegistry):
    def register_tool(self, tool): pass
    def get_registered_tools(self): return tuple()
    @property
    def tool_count(self): return 1
    def get_tool(self, name: str):
        if name == "missing":
            raise ToolNotFoundError("Not found")
        return True # Just needs to not raise

class MockExecutor(IToolExecutor):
    def __init__(self):
        self.called = False
        
    async def execute_tool(self, request: ToolRequest) -> ToolResponse:
        self.called = True
        if request.tool_name == "error_tool":
            raise ToolExecutionError("Executor failure")
        if request.tool_name == "bad_response_tool":
            return {"not_a": "response"}
        if request.tool_name == "cancelled_tool":
            raise asyncio.CancelledError()
        if request.tool_name == "crash_tool":
            raise ValueError("Raw crash")
            
        return ToolResponse(success=True, result="success", metadata={"executor_called": True})

class TrackedToolService(ToolService):
    def __init__(self, executor, registry):
        super().__init__(executor, registry)
        self.pre_called = False
        self.post_called = False
        self.abort_pre = False
        self.last_context = None
        
    async def _pre_execute(self, context: ToolExecutionContext) -> None:
        self.pre_called = True
        context.execution_state = "pre_hook_custom"
        self.last_context = context
        if self.abort_pre:
            raise ToolValidationError("Aborted by pre-hook")
            
    async def _post_execute(self, context: ToolExecutionContext) -> None:
        self.post_called = True
        context.execution_state = "post_hook_custom"
        if context.response:
            new_meta = dict(context.response.metadata)
            new_meta["post_called"] = True
            context.response = context.response.model_copy(update={"metadata": new_meta})

@pytest.fixture
def service():
    return TrackedToolService(MockExecutor(), MockRegistry())

@pytest.mark.asyncio
async def test_service_successful_flow(service):
    req = ToolRequest(tool_name="valid_tool")
    res = await service.handle_tool_call(req)
    
    assert res.success is True
    assert service.pre_called is True
    assert service._executor.called is True
    assert service.post_called is True
    assert res.metadata.get("post_called") is True
    assert res.metadata.get("executor_called") is True

@pytest.mark.asyncio
async def test_service_invalid_request_type(service):
    res = await service.handle_tool_call({"tool_name": "test"})
    assert res.success is False
    assert res.metadata["execution_status"] == "validation_error"
    assert service.pre_called is False
    assert service._executor.called is False

@pytest.mark.asyncio
async def test_service_missing_tool_name(service):
    req = ToolRequest(tool_name="")
    res = await service.handle_tool_call(req)
    assert res.success is False
    assert res.metadata["execution_status"] == "validation_error"
    assert service.pre_called is False

@pytest.mark.asyncio
async def test_service_tool_not_found(service):
    req = ToolRequest(tool_name="missing")
    res = await service.handle_tool_call(req)
    assert res.success is False
    assert res.metadata["execution_status"] == "not_found"
    assert service.pre_called is False

@pytest.mark.asyncio
async def test_service_pre_hook_abort(service):
    service.abort_pre = True
    req = ToolRequest(tool_name="valid_tool")
    res = await service.handle_tool_call(req)
    assert res.success is False
    assert res.metadata["execution_status"] == "validation_error"
    assert service._executor.called is False

@pytest.mark.asyncio
async def test_service_executor_returns_bad_type(service):
    req = ToolRequest(tool_name="bad_response_tool")
    res = await service.handle_tool_call(req)
    assert res.success is False
    assert "Executor violated contract" in res.error
    assert res.metadata["execution_status"] == "tool_error"

@pytest.mark.asyncio
async def test_service_executor_raises_tool_error(service):
    req = ToolRequest(tool_name="error_tool")
    res = await service.handle_tool_call(req)
    assert res.success is False
    assert res.metadata["execution_status"] == "tool_error"

@pytest.mark.asyncio
async def test_service_executor_raises_raw_exception(service):
    req = ToolRequest(tool_name="crash_tool")
    res = await service.handle_tool_call(req)
    assert res.success is False
    assert res.metadata["execution_status"] == "unexpected_error"
    assert "orchestration error" in res.error

@pytest.mark.asyncio
async def test_service_cancelled_error(service):
    req = ToolRequest(tool_name="cancelled_tool")
    with pytest.raises(asyncio.CancelledError):
        await service.handle_tool_call(req)

@pytest.mark.asyncio
async def test_service_hook_ordering_and_context_propagation(service):
    req = ToolRequest(tool_name="valid_tool")
    res = await service.handle_tool_call(req)
    
    context = service.last_context
    assert context is not None
    assert context.execution_state == "post_hook_custom"
    assert context.execution_duration_ms is not None
    assert context.execution_start_time > 0
    assert context.execution_end_time > context.execution_start_time

@pytest.mark.asyncio
async def test_service_bad_post_hook_response():
    # If a post hook sets response to a dict instead of ToolResponse
    class BadPostHookService(ToolService):
        async def _post_execute(self, context: ToolExecutionContext) -> None:
            context.response = {"not_a": "response"}
            
    bad_service = BadPostHookService(MockExecutor(), MockRegistry())
    req = ToolRequest(tool_name="valid_tool")
    res = await bad_service.handle_tool_call(req)
    
    assert res.success is False
    assert res.metadata["execution_status"] == "unexpected_error"
    assert "Expected ToolResponse" in res.error
