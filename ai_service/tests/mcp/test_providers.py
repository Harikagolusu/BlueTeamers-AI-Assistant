import pytest
import asyncio
from typing import Dict, Any
from app.mcp.providers.local_provider import LocalProvider
from app.mcp.providers.mcp_provider import MCPToolProvider
from app.tools.interfaces.i_tool_executor import IToolExecutor
from app.mcp.interfaces.i_mcp_client import IMCPClient
from app.mcp.models import MCPResponse, SessionState

class MockToolExecutor(IToolExecutor):
    async def execute(self, tool_name: str, arguments: Dict[str, Any], permissions: Dict[str, bool]) -> Dict[str, Any]:
        return {"result_message": f"Ran {tool_name}"}

class MockMCPClient(IMCPClient):
    async def connect(self) -> None: pass
    async def disconnect(self) -> None: pass
    async def initialize_session(self): pass
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> MCPResponse:
        return MCPResponse(id="1", result={"result_message": f"Ran MCP {tool_name}"})
    async def read_resource(self, uri: str): pass
    async def fetch_prompt(self, name: str, arguments: Dict[str, str]): pass

@pytest.mark.asyncio
async def test_local_provider():
    executor = MockToolExecutor()
    provider = LocalProvider(executor)
    
    assert provider.provider_id == "local"
    assert provider.provider_type == "local"
    
    result = await provider.execute("test_tool", {}, {})
    assert result["result_message"] == "Ran test_tool"

@pytest.mark.asyncio
async def test_mcp_provider():
    client = MockMCPClient()
    provider = MCPToolProvider("remote_mcp", client)
    
    assert provider.provider_id == "remote_mcp"
    assert provider.provider_type == "mcp"
    
    result = await provider.execute("test_tool", {}, {})
    assert result["result_message"] == "Ran MCP test_tool"
