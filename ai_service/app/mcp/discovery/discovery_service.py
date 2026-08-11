from typing import Dict, Any
from app.mcp.registry.mcp_registry import MCPRegistry
from app.mcp.interfaces.i_tool_catalog import IToolCatalog
from app.mcp.models import MCPServer, MCPServerConfig, TransportType

class DiscoveryService:
    """
    Handles discovery of new servers and populating the registry.
    Triggers catalog refresh when needed.
    """
    def __init__(self, registry: MCPRegistry, catalog: IToolCatalog):
        self._registry = registry
        self._catalog = catalog

    async def startup_discovery(self, initial_config: Dict[str, Any] = None) -> None:
        """
        Discovers servers based on initial configuration and populates registry.
        """
        if initial_config and "servers" in initial_config:
            for server_name, config_data in initial_config["servers"].items():
                transport_type = TransportType(config_data.get("transport", "stdio"))
                config = MCPServerConfig(
                    name=server_name,
                    transport_type=transport_type,
                    transport_config=config_data
                )
                server = MCPServer(config=config)
                self._registry.register_server(server)

        # Trigger catalog refresh
        self._catalog.refresh()

    async def manual_refresh(self) -> None:
        """
        Force refresh of registry and catalog.
        """
        # Logic to ping endpoints or read updated config
        self._catalog.refresh()
