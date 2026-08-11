from typing import Dict, Any, List
from app.mcp.interfaces.i_tool_provider import IToolProvider
from app.tools.interfaces.i_tool_executor import IToolExecutor

class LegacyToolProvider(IToolProvider):
    def __init__(self, tool_executor: IToolExecutor):
        self._tool_executor = tool_executor
        
    @property
    def provider_id(self) -> str:
        return "legacy_provider"

    @property
    def provider_type(self) -> str:
        return "LOCAL"

    async def execute(self, tool_name: str, arguments: Dict[str, Any], permissions: Dict[str, bool] = None) -> Dict[str, Any]:
        return await self._tool_executor.execute(
            tool_name=tool_name,
            arguments=arguments,
            permissions=list(permissions.keys()) if permissions else None
        )
        
    def supports(self, capability: str) -> bool:
        return True # Supports whatever the legacy framework supports
