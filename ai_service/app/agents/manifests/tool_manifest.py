from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class ToolManifest(BaseModel):
    tool_id: str
    name: str
    version: str
    provider: str
    description: str = ""
    config_schema: Dict[str, Any] = Field(default_factory=dict)
    executable_path: Optional[str] = None
