from typing import Dict, List, Optional
from app.mcp.models import MCPServer

class MCPRegistry:
    """
    Tracks registered MCP servers and their metadata.
    """
    def __init__(self):
        self._servers: Dict[str, MCPServer] = {}

    def register_server(self, server: MCPServer) -> None:
        self._servers[server.config.name] = server

    def get_server(self, name: str) -> Optional[MCPServer]:
        return self._servers.get(name)

    def remove_server(self, name: str) -> None:
        if name in self._servers:
            del self._servers[name]

    def list_servers(self) -> List[MCPServer]:
        return list(self._servers.values())
