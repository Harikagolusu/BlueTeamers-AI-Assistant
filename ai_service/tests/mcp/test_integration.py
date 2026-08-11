import pytest
import asyncio
from app.mcp.registry.mcp_registry import MCPRegistry
from app.mcp.catalog.tool_catalog import ToolCatalog
from app.mcp.provider_registry.provider_registry import ProviderRegistry
from app.mcp.resolvers.tool_provider_resolver import ToolProviderResolver
from app.mcp.discovery.discovery_service import DiscoveryService
from app.mcp.models import MCPTool
from app.mcp.providers.mcp_provider import MCPToolProvider
from app.mcp.client.mcp_client import MCPClient
from app.mcp.transport.stdio_transport import StdioTransport
from app.chat.engines.tool_engine import ToolExecutionEngine
from app.chat.context.execution_context import ExecutionContext

@pytest.mark.asyncio
async def test_full_pipeline_cache_miss():
    # 1. Initialize Subsystems
    registry = MCPRegistry()
    catalog = ToolCatalog(registry)
    provider_registry = ProviderRegistry()
    discovery = DiscoveryService(registry, catalog)
    resolver = ToolProviderResolver(catalog, provider_registry)
    engine = ToolExecutionEngine(resolver)

    # 2. Simulate Discovery Refresh
    # Suppose a server adds a tool
    tool = MCPTool(
        name="weather_tool",
        description="Get weather",
        input_schema={},
        provider_id="weather_mcp"
    )
    catalog.add_tool(tool)
    
    # 3. Simulate Provider Registration
    # In real world, LifecycleManager would create client and provider after discovery
    class DummyClient:
        async def call_tool(self, name, args):
            from app.mcp.models import MCPResponse
            return MCPResponse(id="1", result={"result_message": f"Weather for {args.get('location')}"})
            
    provider = MCPToolProvider("weather_mcp", DummyClient())
    provider_registry.register(provider)

    # 4. Engine Execution
    context = ExecutionContext(
        session_id="123",
        metadata={"target_tool": "weather_tool", "tool_args": {"location": "London"}},
        permissions={}
    )
    
    result = await engine.execute(context)
    
    assert result.success
    assert "Weather for London" in result.message
    assert result.tool_outputs[0]["provider"] == "weather_mcp"
