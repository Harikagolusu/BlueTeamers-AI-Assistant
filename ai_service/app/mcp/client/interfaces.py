from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from app.mcp.models.mcp_models import MCPTool, MCPResource, MCPPrompt, MCPResponse

class IMCPClient(ABC):
    @abstractmethod
    async def initialize(self) -> None:
        pass
        
    @abstractmethod
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> MCPResponse:
        pass
        
    @abstractmethod
    async def read_resource(self, uri: str) -> MCPResponse:
        pass
        
    @abstractmethod
    async def fetch_prompt(self, prompt_name: str, arguments: Dict[str, Any]) -> MCPResponse:
        pass
        
    @abstractmethod
    async def list_tools(self) -> List[MCPTool]:
        pass
        
    @abstractmethod
    async def list_resources(self) -> List[MCPResource]:
        pass
        
    @abstractmethod
    async def list_prompts(self) -> List[MCPPrompt]:
        pass
