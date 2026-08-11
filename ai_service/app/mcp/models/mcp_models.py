from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional
from enum import Enum

class HealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"

class DiscoveryPolicy(str, Enum):
    STATIC = "STATIC"
    ON_DEMAND = "ON_DEMAND"
    PERIODIC = "PERIODIC"

class MCPCapability(BaseModel):
    name: str
    supported: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MCPServer(BaseModel):
    server_id: str
    name: str
    version: str
    protocol_version: str = "2024-11-05"
    supported_transports: List[str] = Field(default_factory=list)
    auth_type: str = "none"
    health_status: HealthStatus = HealthStatus.UNKNOWN
    capabilities: List[MCPCapability] = Field(default_factory=list)
    max_request_size: int = 1048576

class MCPSession(BaseModel):
    session_id: str
    server_id: str
    status: str = "DISCONNECTED"
    connection_time: Optional[float] = None
    last_heartbeat: Optional[float] = None

class MCPTool(BaseModel):
    name: str
    description: str
    inputSchema: Dict[str, Any]
    required_permissions: List[str] = Field(default_factory=list)

class MCPResource(BaseModel):
    uri: str
    name: str
    mimeType: Optional[str] = None
    description: Optional[str] = None

class MCPPrompt(BaseModel):
    name: str
    description: Optional[str] = None
    arguments: List[Dict[str, Any]] = Field(default_factory=list)

class MCPRequest(BaseModel):
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)

class MCPResponse(BaseModel):
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

class ToolMetadata(BaseModel):
    description: str = ""
    schema_def: Dict[str, Any] = Field(default_factory=dict)
    version: str = "1.0.0"
    health: HealthStatus = HealthStatus.UNKNOWN
    permissions: List[str] = Field(default_factory=list)
    ttl: float = 3600.0
    last_refreshed: float = 0.0

class ToolRegistration(BaseModel):
    tool_name: str
    provider_name: str
    provider_type: str = "LOCAL" # LOCAL or MCP
    provider_id: str = ""
    priority: int = 50
    metadata: ToolMetadata = Field(default_factory=ToolMetadata)
