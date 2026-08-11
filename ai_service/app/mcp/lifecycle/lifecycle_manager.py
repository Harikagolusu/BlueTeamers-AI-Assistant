import logging
from typing import Dict, Any
from app.mcp.discovery.discovery_service import DiscoveryService
from app.mcp.sessions.session_manager import SessionManager
from app.mcp.interfaces.i_tool_catalog import IToolCatalog
from app.mcp.interfaces.i_provider_registry import IProviderRegistry

logger = logging.getLogger(__name__)

class MCPLifecycleManager:
    """
    Operational entry point for the MCP subsystem.
    """
    def __init__(self, 
                 discovery_service: DiscoveryService, 
                 session_manager: SessionManager,
                 catalog: IToolCatalog,
                 provider_registry: IProviderRegistry):
        self._discovery_service = discovery_service
        self._session_manager = session_manager
        self._catalog = catalog
        self._provider_registry = provider_registry
        self._is_running = False

    async def startup(self, config: Dict[str, Any] = None) -> None:
        logger.info("Starting MCP Lifecycle Manager")
        self._is_running = True
        await self._discovery_service.startup_discovery(config)
        # In a real startup, iterate registry, create clients, register them, initialize sessions

    async def shutdown(self) -> None:
        logger.info("Shutting down MCP Lifecycle Manager")
        self._is_running = False
        # Disconnect all clients in session manager

    async def refresh_registry(self) -> None:
        await self._discovery_service.manual_refresh()

    async def refresh_catalog(self) -> None:
        self._catalog.refresh()
        
    async def refresh_providers(self) -> None:
        for provider in self._provider_registry.list_providers():
            if hasattr(provider, 'refresh_tools'):
                await provider.refresh_tools()

    async def cleanup_sessions(self) -> None:
        await self._session_manager.cleanup_idle_sessions()
        
    async def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "providers": len(self._provider_registry.list_providers())}
