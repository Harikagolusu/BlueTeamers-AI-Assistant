import pytest
from app.mcp.resolvers.tool_provider_resolver import ToolProviderResolver
from app.mcp.models.mcp_models import ToolRegistration

class MockCatalog:
    def get_tool(self, tool_name: str):
        if tool_name == "local_tool":
            return ToolRegistration(tool_name="local_tool", provider_name="Local", provider_id="local_prov")
        elif tool_name == "mcp_tool":
            return ToolRegistration(tool_name="mcp_tool", provider_name="MCP", provider_id="mcp_prov")
        return None

class MockProviderRegistry:
    def __init__(self, providers):
        self.providers = providers
    def resolve(self, p_id):
        return self.providers.get(p_id)

class MockProvider:
    def __init__(self, ptype):
        self.ptype = ptype
    def provider_type(self):
        return self.ptype

def test_tool_provider_resolver():
    catalog = MockCatalog()
    providers = {
        "local_prov": MockProvider("LOCAL"),
        "mcp_prov": MockProvider("MCP")
    }
    registry = MockProviderRegistry(providers)
    
    resolver = ToolProviderResolver(catalog=catalog, provider_registry=registry)
    
    p1 = resolver.resolve("local_tool")
    assert p1.provider_type() == "LOCAL"
    
    p2 = resolver.resolve("mcp_tool")
    assert p2.provider_type() == "MCP"
    
    p3 = resolver.resolve("unknown_tool")
    assert p3 is None
