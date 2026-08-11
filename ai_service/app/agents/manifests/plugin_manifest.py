from pydantic import BaseModel, Field
from typing import List

class PluginManifest(BaseModel):
    plugin_id: str
    name: str
    version: str
    entry_point: str
    description: str = ""
    dependencies: List[str] = Field(default_factory=list)
    allowed_imports: List[str] = Field(default_factory=list)
    allowed_filesystem_paths: List[str] = Field(default_factory=list)
    allowed_env_vars: List[str] = Field(default_factory=list)
    allowed_networks: List[str] = Field(default_factory=list)
