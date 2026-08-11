from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from app.mcp.models.mcp_models import ToolRegistration

class IToolCatalog(ABC):
    @abstractmethod
    async def get_tool(self, tool_name: str) -> Optional[ToolRegistration]:
        pass
        
    @abstractmethod
    async def register_tool(self, registration: ToolRegistration) -> None:
        pass
        
    @abstractmethod
    async def remove_tool(self, tool_name: str) -> None:
        pass
        
    @abstractmethod
    async def refresh_tool(self, tool_name: str) -> bool:
        pass
        
    @abstractmethod
    async def list_tools(self) -> List[ToolRegistration]:
        pass
