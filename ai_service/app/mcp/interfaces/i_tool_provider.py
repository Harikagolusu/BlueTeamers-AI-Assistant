from abc import ABC, abstractmethod
from typing import Dict, Any

class IToolProvider(ABC):
    @property
    @abstractmethod
    def provider_id(self) -> str:
        pass
        
    @property
    @abstractmethod
    def provider_type(self) -> str:
        pass

    @abstractmethod
    async def execute(self, tool_name: str, arguments: Dict[str, Any], permissions: Dict[str, bool]) -> Dict[str, Any]:
        """Execute a tool request."""
        pass

class IMCPToolProvider(IToolProvider):
    @abstractmethod
    async def refresh_tools(self) -> None:
        """Refresh the tools provided by the MCP server."""
        pass
