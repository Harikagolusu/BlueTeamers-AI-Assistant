from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class MCPTool(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]
    provider_id: str
    provider_type: str = "mcp"
    version: str = "1.0.0"
    permissions: Dict[str, bool] = Field(default_factory=dict)
    health: str = "healthy"
    last_refreshed: Optional[str] = None
