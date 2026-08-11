from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.mcp.interfaces.i_tool_catalog import IToolCatalog
from app.mcp.models import MCPTool
from app.mcp.registry.mcp_registry import MCPRegistry

class ToolCatalog(IToolCatalog):
    """
    Single source of truth for tools.
    Stores metadata and Provider ID.
    """
    def __init__(self, registry: MCPRegistry):
        self._registry = registry
        self._tools: Dict[str, MCPTool] = {}
        self._last_refreshed: Optional[datetime] = None

    def get_tool(self, tool_name: str) -> Optional[MCPTool]:
        return self._tools.get(tool_name)

    def list_tools(self) -> List[MCPTool]:
        return list(self._tools.values())

    def add_tool(self, tool: MCPTool) -> None:
        self._tools[tool.name] = tool

    def remove_tool(self, tool_name: str) -> None:
        if tool_name in self._tools:
            del self._tools[tool_name]

    def refresh(self) -> None:
        """
        Pull updates from the registry/providers.
        """
        # In a real implementation, iterate through servers in registry,
        # fetch their tools and update self._tools.
        self._last_refreshed = datetime.now(timezone.utc)
