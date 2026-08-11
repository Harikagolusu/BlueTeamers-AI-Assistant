import pytest
import asyncio
from app.tools.executor.tool_executor import ToolExecutor
from app.tools.registry.tool_registry import ToolRegistry
from app.tools.interfaces.tool import ITool
from app.tools.models.tool_request import ToolRequest
from app.tools.models.tool_response import ToolResponse
from app.tools.domain.exceptions import ToolExecutionError
from app.tools.config import tool_config

class SuccessTool(ITool):

    async def initialize(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    @property
    def name(self) -> str: return "success_tool"
    @property
    def description(self) -> str: return "desc"
    async def execute(self, request: ToolRequest) -> ToolResponse:
        return ToolResponse(success=True, result="ok")

class ErrorTool(ITool):

    async def initialize(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    @property
    def name(self) -> str: return "error_tool"
    @property
    def description(self) -> str: return "desc"
    async def execute(self, request: ToolRequest) -> ToolResponse:
        raise ToolExecutionError("Intentional domain error")

class UnexpectedErrorTool(ITool):

    async def initialize(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    @property
    def name(self) -> str: return "unexpected_error_tool"
    @property
    def description(self) -> str: return "desc"
    async def execute(self, request: ToolRequest) -> ToolResponse:
        raise ValueError("Raw exception")

class TimeoutTool(ITool):

    async def initialize(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    @property
    def name(self) -> str: return "timeout_tool"
    @property
    def description(self) -> str: return "desc"
    async def execute(self, request: ToolRequest) -> ToolResponse:
        await asyncio.sleep(0.5)
        return ToolResponse(success=True)
        
class InvalidResponseTool(ITool):

    async def initialize(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    @property
    def name(self) -> str: return "invalid_response_tool"
    @property
    def description(self) -> str: return "desc"
    async def execute(self, request: ToolRequest) -> ToolResponse:
        return {"success": True} # Invalid, should be ToolResponse

class CancelledTool(ITool):

    async def initialize(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    @property
    def name(self) -> str: return "cancelled_tool"
    @property
    def description(self) -> str: return "desc"
    async def execute(self, request: ToolRequest) -> ToolResponse:
        raise asyncio.CancelledError()

@pytest.fixture
def registry():
    reg = ToolRegistry()
    reg.register_tool(SuccessTool())
    reg.register_tool(ErrorTool())
    reg.register_tool(UnexpectedErrorTool())
    reg.register_tool(TimeoutTool())
    reg.register_tool(CancelledTool())
    reg.register_tool(InvalidResponseTool())
    reg.freeze()
    return reg

@pytest.mark.asyncio
async def test_executor_success(registry):
    executor = ToolExecutor(registry)
    req = ToolRequest(tool_name="success_tool")
    res = await executor.execute_tool(req)
    assert res.success is True
    assert res.result == "ok"
    assert "execution_duration_ms" in res.metadata
    assert res.metadata["tool_name"] == "success_tool"
    assert res.metadata["execution_status"] == "success"

@pytest.mark.asyncio
async def test_executor_tool_not_found(registry):
    executor = ToolExecutor(registry)
    req = ToolRequest(tool_name="missing_tool")
    res = await executor.execute_tool(req)
    assert res.success is False
    assert "not found" in res.error

@pytest.mark.asyncio
async def test_executor_domain_error(registry):
    executor = ToolExecutor(registry)
    req = ToolRequest(tool_name="error_tool")
    res = await executor.execute_tool(req)
    assert res.success is False
    assert res.error == "Intentional domain error"

@pytest.mark.asyncio
async def test_executor_unexpected_error(registry):
    executor = ToolExecutor(registry)
    req = ToolRequest(tool_name="unexpected_error_tool")
    res = await executor.execute_tool(req)
    assert res.success is False
    assert "Unexpected error" in res.error

@pytest.mark.asyncio
async def test_executor_timeout(registry, monkeypatch):
    monkeypatch.setattr(tool_config, "TOOL_GLOBAL_EXECUTION_TIMEOUT_SEC", 0.1)
    executor = ToolExecutor(registry)
    req = ToolRequest(tool_name="timeout_tool")
    res = await executor.execute_tool(req)
    assert res.success is False
    assert "timed out" in res.error
    assert res.metadata["timed_out"] is True
    assert "execution_duration_ms" in res.metadata
    assert res.metadata["execution_status"] == "timeout"

@pytest.mark.asyncio
async def test_executor_invalid_response(registry):
    executor = ToolExecutor(registry)
    req = ToolRequest(tool_name="invalid_response_tool")
    res = await executor.execute_tool(req)
    assert res.success is False
    assert "violated contract" in res.error
    assert "execution_duration_ms" in res.metadata
    assert res.metadata["execution_status"] == "tool_error"

@pytest.mark.asyncio
async def test_executor_cancelled(registry):
    executor = ToolExecutor(registry)
    req = ToolRequest(tool_name="cancelled_tool")
    with pytest.raises(asyncio.CancelledError):
        await executor.execute_tool(req)
