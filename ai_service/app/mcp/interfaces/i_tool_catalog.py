from abc import ABC, abstractmethod
from typing import List, Optional
from app.mcp.models import MCPTool

class IToolCatalog(ABC):
    @abstractmethod
    def get_tool(self, tool_name: str) -> Optional[MCPTool]:
        pass
        
    @abstractmethod
    def list_tools(self) -> List[MCPTool]:
        pass
        
    @abstractmethod
    def add_tool(self, tool: MCPTool) -> None:
        pass
        
    @abstractmethod
    def remove_tool(self, tool_name: str) -> None:
        pass
        
    @abstractmethod
    def refresh(self) -> None:
        """Synchronize with registry or external sources."""
        pass
