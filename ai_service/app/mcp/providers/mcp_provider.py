from typing import Dict, Any
from app.mcp.interfaces.i_tool_provider import IMCPToolProvider
from app.mcp.interfaces.i_mcp_client import IMCPClient

class MCPToolProvider(IMCPToolProvider):
    def __init__(self, provider_id: str, client: IMCPClient):
        self._provider_id = provider_id
        self._client = client

    @property
    def provider_id(self) -> str:
        return self._provider_id

    @property
    def provider_type(self) -> str:
        return "mcp"

    async def execute(self, tool_name: str, arguments: Dict[str, Any], permissions: Dict[str, bool]) -> Dict[str, Any]:
        response = await self._client.call_tool(tool_name, arguments)
        if response.is_error:
            raise Exception(f"MCP Tool execution failed: {response.error.message}")
        
        # ToolResult format
        return response.result or {}

    async def refresh_tools(self) -> None:
        # Client requests list of tools from server
        pass
