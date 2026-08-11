import pytest
import asyncio
from app.mcp.discovery.discovery_service import DiscoveryService
from app.mcp.registry.mcp_registry import MCPRegistry
from app.mcp.catalog.tool_catalog import ToolCatalog

@pytest.mark.asyncio
async def test_startup_discovery():
    registry = MCPRegistry()
    catalog = ToolCatalog(registry)
    service = DiscoveryService(registry, catalog)
    
    config = {
        "servers": {
            "filesystem": {"transport": "stdio", "command": "fs-server"},
            "github": {"transport": "http", "url": "http://localhost:8080"}
        }
    }
    
    await service.startup_discovery(config)
    servers = registry.list_servers()
    assert len(servers) == 2
    
    fs_server = registry.get_server("filesystem")
    assert fs_server.config.transport_type == "stdio"
    
    gh_server = registry.get_server("github")
    assert gh_server.config.transport_type == "http"
