from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum

class TransportType(str, Enum):
    STDIO = "stdio"
    HTTP = "http"
    WEBSOCKET = "websocket"
    SSE = "sse"

class MCPServerConfig(BaseModel):
    name: str
    transport_type: TransportType
    transport_config: Dict[str, Any] = Field(default_factory=dict)
    version: str = "1.0.0"

class MCPServerStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    CONNECTING = "connecting"

class MCPServer(BaseModel):
    config: MCPServerConfig
    status: MCPServerStatus = MCPServerStatus.DISCONNECTED
    protocol_version: str = "2.0"
    server_version: Optional[str] = None
    supported_transports: List[TransportType] = Field(default_factory=list)
    capabilities: Dict[str, Any] = Field(default_factory=dict)
