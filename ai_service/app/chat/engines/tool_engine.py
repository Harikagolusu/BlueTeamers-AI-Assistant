from app.chat.interfaces.i_execution_engine import IExecutionEngine
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult
from app.mcp.interfaces.i_tool_provider_resolver import IToolProviderResolver
import logging

logger = logging.getLogger(__name__)

class ToolExecutionEngine(IExecutionEngine):
    """
    Bridges the Chat Integration Framework to the existing
    Enterprise Tool Calling Framework and MCP Integration Framework.
    """
    def __init__(self, provider_resolver: IToolProviderResolver):
        self._provider_resolver = provider_resolver

    @property
    def name(self) -> str:
        return "TOOL"

    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        target_tool = context.metadata.get("target_tool", "unknown_tool")
        tool_args = context.metadata.get("tool_args", {})
        
        # 1. Resolve Tool Provider (Local Provider or MCP Provider)
        provider = self._provider_resolver.resolve(target_tool)
        if not provider:
            error_msg = f"No provider found for tool {target_tool}."
            logger.error(error_msg)
            return ExecutionResult.failed(engine=self.name, errors=[{"error": error_msg}])
            
        # 2. Execute via the resolved provider
        try:
            tool_response = await provider.execute(
                tool_name=target_tool,
                arguments=tool_args,
                permissions=context.permissions
            )
            
            # 3. Map response
            message = tool_response.get("result_message", f"Executed {target_tool} successfully via {provider.provider_type} provider.")
            
            return ExecutionResult.success(
                engine=self.name,
                message=message,
                tool_outputs=[{"tool": target_tool, "provider": provider.provider_id, "response": tool_response}]
            )
        except Exception as e:
            error_msg = f"Execution failed for tool {target_tool}: {str(e)}"
            logger.error(error_msg)
            return ExecutionResult.failed(engine=self.name, errors=[{"error": error_msg}])
