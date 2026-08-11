from abc import ABC, abstractmethod
from app.mcp.interfaces.i_tool_provider import IToolProvider

class IToolProviderResolver(ABC):
    @abstractmethod
    def resolve(self, tool_name: str) -> IToolProvider:
        """
        Resolves the appropriate Tool Provider for a given tool name.
        Uses ToolCatalog to find Provider ID and Provider Type,
        then uses ProviderRegistry to fetch the instance.
        """
        pass
