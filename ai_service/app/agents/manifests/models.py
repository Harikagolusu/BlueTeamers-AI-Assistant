from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class AgentManifest(BaseModel):
    name: str
    version: str = "1.0.0"
    owner: str = "system"
    description: str = ""
    prompt_template: str
    model: str
    tools: List[str] = Field(default_factory=list)
    capabilities: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    supported_inputs: Dict[str, Any] = Field(default_factory=dict)
    supported_outputs: Dict[str, Any] = Field(default_factory=dict)
    policies: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    runtime_options: Dict[str, Any] = Field(default_factory=dict)
