from typing import Optional
from app.mcp.interfaces.i_tool_provider_resolver import IToolProviderResolver
from app.mcp.interfaces.i_tool_provider import IToolProvider
from app.mcp.interfaces.i_tool_catalog import IToolCatalog
from app.mcp.interfaces.i_provider_registry import IProviderRegistry
import logging

logger = logging.getLogger(__name__)

class ToolProviderResolver(IToolProviderResolver):
    """
    Resolves a tool name to its respective Provider instance.
    Uses ToolCatalog to find Provider ID, then ProviderRegistry to get instance.
    """
    def __init__(self, catalog: IToolCatalog, provider_registry: IProviderRegistry):
        self._catalog = catalog
        self._provider_registry = provider_registry

    def resolve(self, tool_name: str) -> Optional[IToolProvider]:
        tool = self._catalog.get_tool(tool_name)
        if not tool:
            logger.warning(f"Tool {tool_name} not found in catalog.")
            return None
            
        provider = self._provider_registry.resolve(tool.provider_id)
        if not provider:
            logger.error(f"Provider {tool.provider_id} for tool {tool_name} not found in registry.")
            return None
            
        return provider
