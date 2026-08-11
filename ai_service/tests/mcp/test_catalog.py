import pytest
from app.mcp.catalog.tool_catalog import ToolCatalog
from app.mcp.registry.mcp_registry import MCPRegistry
from app.mcp.models import MCPTool

def test_tool_catalog():
    registry = MCPRegistry()
    catalog = ToolCatalog(registry)
    
    tool = MCPTool(
        name="calculator",
        description="A simple calculator",
        input_schema={"type": "object", "properties": {}},
        provider_id="math_provider"
    )
    
    catalog.add_tool(tool)
    fetched = catalog.get_tool("calculator")
    assert fetched.provider_id == "math_provider"
    
    tools = catalog.list_tools()
    assert len(tools) == 1
    
    catalog.remove_tool("calculator")
    assert catalog.get_tool("calculator") is None
