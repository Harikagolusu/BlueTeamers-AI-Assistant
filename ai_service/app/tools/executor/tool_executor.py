import asyncio
import time
from app.tools.interfaces.tool_executor import IToolExecutor
from app.tools.interfaces.registry import IToolRegistry
from app.tools.models.tool_request import ToolRequest
from app.tools.models.tool_response import ToolResponse
from app.tools.domain.exceptions import ToolNotFoundError, ToolError, ToolExecutionError
from app.tools.config import tool_config

class ToolExecutor(IToolExecutor):
    """
    Mechanical executor for tools. 
    Handles timeouts and exception normalization.
    """
    def __init__(self, registry: IToolRegistry):
        self._registry = registry
        
    async def execute_tool(self, request: ToolRequest) -> ToolResponse:
        start_time = time.perf_counter()
        tool_name = request.tool_name
        
        try:
            tool = self._registry.get_tool(tool_name)
            
            timeout = tool_config.TOOL_GLOBAL_EXECUTION_TIMEOUT_SEC
            
            # Wrap execution to enforce timeout
            result = await asyncio.wait_for(tool.execute(request), timeout=timeout)
            
            if not isinstance(result, ToolResponse):
                raise ToolExecutionError(f"Tool '{tool_name}' violated contract: Expected ToolResponse, got {type(result).__name__}")
            
            execution_duration_ms = int((time.perf_counter() - start_time) * 1000)
            
            new_metadata = dict(result.metadata)
            new_metadata["execution_duration_ms"] = execution_duration_ms
            new_metadata["tool_name"] = tool_name
            new_metadata["timed_out"] = False
            new_metadata["execution_status"] = "success" if result.success else "error"
            
            return result.model_copy(update={"metadata": new_metadata})
            
        except asyncio.CancelledError:
            # Architecture Invariant: Never catch CancelledError
            raise
        except asyncio.TimeoutError:
            execution_duration_ms = int((time.perf_counter() - start_time) * 1000)
            return ToolResponse(
                success=False,
                error=f"Tool execution timed out after {timeout} seconds.",
                metadata={"timed_out": True, "tool_name": tool_name, "execution_duration_ms": execution_duration_ms, "execution_status": "timeout"}
            )
        except ToolNotFoundError as e:
            execution_duration_ms = int((time.perf_counter() - start_time) * 1000)
            return ToolResponse(
                success=False,
                error=str(e),
                metadata={"timed_out": False, "tool_name": tool_name, "execution_duration_ms": execution_duration_ms, "execution_status": "not_found"}
            )
        except ToolError as e:
            execution_duration_ms = int((time.perf_counter() - start_time) * 1000)
            return ToolResponse(
                success=False,
                error=str(e),
                metadata={"timed_out": False, "tool_name": tool_name, "execution_duration_ms": execution_duration_ms, "execution_status": "tool_error"}
            )
        except Exception as e:
            execution_duration_ms = int((time.perf_counter() - start_time) * 1000)
            return ToolResponse(
                success=False,
                error=f"Unexpected error during execution: {str(e)}",
                metadata={"timed_out": False, "tool_name": tool_name, "execution_duration_ms": execution_duration_ms, "execution_status": "unexpected_error"}
            )
