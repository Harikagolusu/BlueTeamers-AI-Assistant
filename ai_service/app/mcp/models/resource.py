from pydantic import BaseModel, Field
from typing import Optional

class MCPResource(BaseModel):
    uri: str
    name: str
    description: Optional[str] = None
    mimeType: Optional[str] = None
    provider_id: str
