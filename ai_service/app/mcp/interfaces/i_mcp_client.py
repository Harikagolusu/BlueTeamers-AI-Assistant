from abc import ABC, abstractmethod
from typing import Dict, Any, List
from app.mcp.models import MCPSession, MCPResponse, MCPTool, MCPResource, MCPPrompt

class IMCPClient(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass
        
    @abstractmethod
    async def disconnect(self) -> None:
        pass
        
    @abstractmethod
    async def initialize_session(self) -> MCPSession:
        pass
        
    @abstractmethod
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> MCPResponse:
        pass
        
    @abstractmethod
    async def read_resource(self, uri: str) -> MCPResponse:
        pass
        
    @abstractmethod
    async def fetch_prompt(self, name: str, arguments: Dict[str, str]) -> MCPResponse:
        pass
