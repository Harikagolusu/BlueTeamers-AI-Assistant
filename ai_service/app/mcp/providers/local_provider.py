from typing import Dict, Any
from app.mcp.interfaces.i_tool_provider import IToolProvider
from app.tools.interfaces.i_tool_executor import IToolExecutor

class LocalProvider(IToolProvider):
    """
    Wraps the existing Enterprise Tool Framework IToolExecutor 
    to act as a standard IToolProvider, ensuring backwards compatibility
    with Modules 1-6.
    """
    def __init__(self, tool_executor: IToolExecutor):
        self._tool_executor = tool_executor

    @property
    def provider_id(self) -> str:
        return "local"

    @property
    def provider_type(self) -> str:
        return "local"

    async def execute(self, tool_name: str, arguments: Dict[str, Any], permissions: Dict[str, bool]) -> Dict[str, Any]:
        return await self._tool_executor.execute(
            tool_name=tool_name,
            arguments=arguments,
            permissions=permissions
        )
