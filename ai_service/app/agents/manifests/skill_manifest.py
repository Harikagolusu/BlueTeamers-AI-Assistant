from pydantic import BaseModel, Field
from typing import List, Dict, Any

class SkillManifest(BaseModel):
    skill_id: str
    name: str
    version: str
    description: str = ""
    capability: str
    required_tools: List[str] = Field(default_factory=list)
    required_permissions: List[str] = Field(default_factory=list)
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
