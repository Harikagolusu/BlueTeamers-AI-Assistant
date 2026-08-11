from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class PromptVersion(BaseModel):
    id: str
    name: str
    version: str
    system_prompt: str
    user_prompt: str
    variables: List[str] = Field(default_factory=list)
    parent_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
