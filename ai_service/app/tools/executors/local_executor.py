from typing import Dict, Any
from app.tools.interfaces.i_tool_executor import IToolExecutor
from app.tools.interfaces.tool_service import IToolService
from app.tools.models.tool_request import ToolRequest

class LocalToolExecutor(IToolExecutor):
    """
    Concrete implementation of the legacy IToolExecutor interface.
    Bridges the legacy MCP Tool Providers to the modern ToolService.
    """
    def __init__(self, tool_service: IToolService):
        self.tool_service = tool_service

    async def execute(self, tool_name: str, arguments: Dict[str, Any], permissions: Dict[str, bool] = None) -> Dict[str, Any]:
        request = ToolRequest(
            tool_name=tool_name,
            arguments=arguments,
            context={}
        )
        response = await self.tool_service.handle_tool_call(request)
        
        return {
            "success": response.success,
            "result": response.result if response.success else None,
            "error": response.error if not response.success else None,
            "metadata": response.metadata
        }
