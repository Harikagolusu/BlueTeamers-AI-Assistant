from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class MCPPromptArgument(BaseModel):
    name: str
    description: Optional[str] = None
    required: bool = False

class MCPPrompt(BaseModel):
    name: str
    description: str
    arguments: List[MCPPromptArgument] = Field(default_factory=list)
    provider_id: str
