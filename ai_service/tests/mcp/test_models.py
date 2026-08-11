import pytest
from app.mcp.models import MCPServer, MCPServerConfig, TransportType, MCPServerStatus

def test_mcp_server_model():
    config = MCPServerConfig(name="test_server", transport_type=TransportType.STDIO)
    server = MCPServer(config=config)
    
    assert server.config.name == "test_server"
    assert server.status == MCPServerStatus.DISCONNECTED
    assert server.protocol_version == "2.0"
