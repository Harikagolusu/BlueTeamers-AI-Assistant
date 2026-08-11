"""
Environment-aware MCP server configuration.

MCP servers are fully configuration-driven (no hardcoded URLs/hosts). They are
declared either inline (MCP_SERVERS_CONFIG JSON) or in a JSON file
(MCP_SERVERS_CONFIG_PATH). Both values live in app/core/config.py and are loaded
from the environment, so development (local MCP servers) and production (managed
MCP endpoints) differ only by configuration, never by code.

Expected configuration shape:
    {"servers": {
        "filesystem": {
            "transport": "stdio",      # stdio | http | websocket | sse
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
            "url": "http://localhost:3000/mcp"    # http/websocket/sse
        }
    }}

NOTE: The transport layer (app/mcp/transport/*) is currently a scaffold. The
local tool provider (LegacyToolProvider -> LocalToolExecutor) is the functional
tool path in both modes; remote MCP execution requires transport implementations.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

from app.core.config import settings
from app.mcp.models import MCPServer, MCPServerConfig, TransportType

logger = logging.getLogger("app.mcp.config")


def load_mcp_servers_config() -> Dict[str, Any]:
    """
    Resolve the MCP server configuration for the active deployment mode.

    Resolution order:
      1. MCP_SERVERS_CONFIG      - inline JSON string.
      2. MCP_SERVERS_CONFIG_PATH - path to a JSON file.

    Always returns a dict (possibly with an empty "servers" list) so callers can
    rely on the DiscoveryService contract.
    """
    if not settings.MCP_ENABLED:
        logger.info("MCP is disabled (MCP_ENABLED=false); no servers registered.")
        return {"servers": {}}

    if settings.MCP_SERVERS_CONFIG:
        try:
            data = json.loads(settings.MCP_SERVERS_CONFIG)
            logger.info("MCP servers loaded from inline MCP_SERVERS_CONFIG.")
            return data if isinstance(data, dict) else {"servers": {}}
        except json.JSONDecodeError as exc:
            logger.error(f"Invalid MCP_SERVERS_CONFIG JSON: {exc}")
            return {"servers": {}}

    if settings.MCP_SERVERS_CONFIG_PATH:
        path = Path(settings.MCP_SERVERS_CONFIG_PATH)
        if path.is_file():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                logger.info(f"MCP servers loaded from {path}.")
                return data if isinstance(data, dict) else {"servers": {}}
            except (json.JSONDecodeError, OSError) as exc:
                logger.error(f"Failed to load MCP servers config {path}: {exc}")
                return {"servers": {}}
        logger.warning(f"MCP_SERVERS_CONFIG_PATH does not exist: {path}")

    logger.info("No MCP servers configured; using local tools only.")
    return {"servers": {}}


def register_configured_servers(mcp_registry) -> int:
    """
    Register every configured MCP server into the given registry (synchronous,
    defensive). Returns the number of servers registered. A misconfigured server
    is skipped with a warning and never breaks application startup.
    """
    config = load_mcp_servers_config()
    servers = config.get("servers", {})
    count = 0
    for name, data in servers.items():
        try:
            transport_type = TransportType(data.get("transport", "stdio"))
            server_config = MCPServerConfig(
                name=name,
                transport_type=transport_type,
                transport_config=data,
            )
            mcp_registry.register_server(MCPServer(config=server_config))
            count += 1
            logger.info(
                f"Registered MCP server '{name}' "
                f"(transport={transport_type.value}, "
                f"mode={'development' if settings.is_development else 'production'})"
            )
        except Exception as exc:  # noqa: BLE001 - never block startup on bad config
            logger.warning(f"Skipping MCP server '{name}': {exc}")
    return count
