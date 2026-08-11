from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from app.agents.models.metadata import PackageMetadata

class AgentManifest(BaseModel):
    id: str
    name: str
    version: str
    description: str = ""
    capabilities: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    
class AgentPackage(BaseModel):
    manifest: AgentManifest
    metadata: PackageMetadata
    
    # Resolvable paths or direct loaded references
    skills_paths: List[str] = Field(default_factory=list)
    plugins_paths: List[str] = Field(default_factory=list)
    templates_paths: List[str] = Field(default_factory=list)
    assets_paths: List[str] = Field(default_factory=list)
    configurations: Dict[str, Any] = Field(default_factory=dict)
    
    signature: Optional[str] = None
