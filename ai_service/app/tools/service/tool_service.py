import asyncio
import time
from app.tools.interfaces.tool_service import IToolService
from app.tools.interfaces.tool_executor import IToolExecutor
from app.tools.interfaces.registry import IToolRegistry
from app.tools.models.tool_request import ToolRequest
from app.tools.models.tool_response import ToolResponse
from app.tools.domain.exceptions import ToolValidationError, ToolNotFoundError, ToolError
from app.tools.service.tool_execution_context import ToolExecutionContext

class ToolService(IToolService):
    """
    Orchestration layer for tool execution.
    
    Responsibilities:
        - Validate incoming requests.
        - Trigger pre/post execution hooks.
        - Delegate execution to IToolExecutor.
        - Normalize all failures into ToolResponses.
        
    Sequence Diagram:
        Validate Request
                ↓
        Registry Lookup
                ↓
        Pre Execute Hook
                ↓
        Executor
                ↓
        Post Execute Hook
                ↓
        Normalize Response
                ↓
        Return ToolResponse
        
    Extension Points:
        - _pre_execute: Override for Cache lookup, Guardrails pre-validation, Auth, Audit.
        - _post_execute: Override for Cache storage, Guardrails post-validation, Metrics.
        
    Architecture Invariants:
        1. Chat API MUST communicate only with IToolService.
        2. ToolService MUST NEVER execute tools directly.
        3. All external communication MUST go through Infrastructure (not Service).
        4. ToolRequest.context must NEVER be inspected or modified by Service.
    """
    def __init__(self, executor: IToolExecutor, registry: IToolRegistry):
        self._executor = executor
        self._registry = registry
        
    async def _pre_execute(self, context: ToolExecutionContext) -> None:
        """
        Hook executed before delegation. 
        
        Must:
            - Validate and Prepare execution.
        Must NOT:
            - Execute tools.
            - Call providers.
            - Modify ToolRequest.
        May raise:
            - ToolValidationError
            - ToolAuthorizationError
            
        Future Integration Points:
            - Cache Lookup
            - Input Guardrails
            - Authorization
            - Rate Limiting
        """
        context.execution_state = "pre_execute"
        
    async def _post_execute(self, context: ToolExecutionContext) -> None:
        """
        Hook executed after delegation. 
        
        Must:
            - Inspect response
            - Enrich metadata
            - Normalize response
        Must NOT:
            - Re-execute tools
            - Access providers
            - Modify ToolRequest
            
        Future Integration Points:
            - Cache Store
            - Output Guardrails
            - Metrics
            - Audit
            - Tracing
        """
        context.execution_state = "post_execute"
        
    def _build_error_response(
        self, 
        tool_name: str, 
        error_msg: str, 
        status: str, 
        start_time: float
    ) -> ToolResponse:
        """Centralized helper to build standardized error responses."""
        execution_duration_ms = int((time.perf_counter() - start_time) * 1000)
        return ToolResponse(
            success=False,
            error=error_msg,
            metadata={
                "execution_status": status,
                "tool_name": tool_name,
                "execution_duration_ms": execution_duration_ms,
                "timed_out": status == "timeout"
            }
        )

    def _validate_final_response(self, response: ToolResponse, context: ToolExecutionContext) -> ToolResponse:
        """Strengthen Response Validation before returning."""
        if not isinstance(response, ToolResponse):
            return self._build_error_response(
                tool_name=getattr(context.request, "tool_name", "unknown") if hasattr(context.request, "tool_name") else "unknown",
                error_msg=f"Post-hook violated contract. Expected ToolResponse, got {type(response).__name__}",
                status="unexpected_error",
                start_time=context.execution_start_time
            )
            
        # Ensure critical metadata fields exist
        meta = dict(response.metadata)
        if "execution_status" not in meta:
            meta["execution_status"] = "success" if response.success else "error"
        if "execution_duration_ms" not in meta:
            meta["execution_duration_ms"] = context.execution_duration_ms
            
        return response.model_copy(update={"metadata": meta})

    async def handle_tool_call(self, request: ToolRequest) -> ToolResponse:
        start_time = time.perf_counter()
        tool_name = getattr(request, "tool_name", "unknown") if hasattr(request, "tool_name") else "unknown"
        
        try:
            if not isinstance(request, ToolRequest):
                return self._build_error_response(tool_name, "Request must be an instance of ToolRequest.", "validation_error", start_time)
                
            if not request.tool_name:
                return self._build_error_response(tool_name, "ToolRequest must contain a valid tool_name.", "validation_error", start_time)
                
            # Verify existence quickly to avoid unnecessary hook execution if tool doesn't exist
            self._registry.get_tool(request.tool_name)
            
            # Initialize context
            context = ToolExecutionContext(request=request)
            context.execution_start_time = start_time
                
            # Pre-execution hooks
            await self._pre_execute(context)
            
            # Mechanical execution delegation
            context.execution_state = "executing"
            response = await self._executor.execute_tool(request)
            
            if not isinstance(response, ToolResponse):
                return self._build_error_response(tool_name, f"Executor violated contract. Expected ToolResponse, got {type(response).__name__}", "tool_error", start_time)
                
            context.response = response
                
            # Post-execution hooks
            await self._post_execute(context)
            
            context.mark_complete()
            
            # Use the possibly mutated response from context
            final_response = context.response if context.response else response
            
            return self._validate_final_response(final_response, context)
            
        except asyncio.CancelledError:
            # Architecture Invariant: Never catch CancelledError, let FastAPI abort cleanly
            raise
        except ToolValidationError as e:
            return self._build_error_response(tool_name, str(e), "validation_error", start_time)
        except ToolNotFoundError as e:
            return self._build_error_response(tool_name, str(e), "not_found", start_time)
        except ToolError as e:
            return self._build_error_response(tool_name, str(e), "tool_error", start_time)
        except Exception as e:
            return self._build_error_response(tool_name, f"Unexpected orchestration error: {str(e)}", "unexpected_error", start_time)
