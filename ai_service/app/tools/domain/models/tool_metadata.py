from typing import List, Optional
from pydantic import BaseModel, Field
from app.tools.discovery.metadata.enums import ToolCategory, ToolState
from app.tools.domain.models.tool_capabilities import ToolCapabilities
from app.tools.domain.models.tool_permissions import ToolPermissions
from app.tools.domain.models.tool_version import ToolVersion

class ToolMetadata(BaseModel):
    name: str = Field(..., description="Unique identifier for the tool")
    description: str = Field(..., description="Description of the tool for the LLM")
    category: ToolCategory = Field(default=ToolCategory.CUSTOM, description="Categorization for grouping")
    aliases: List[str] = Field(default_factory=list, description="Alternative names for the tool")
    state: ToolState = Field(default=ToolState.ACTIVE, description="Lifecycle state of the tool")
    timeout: Optional[int] = Field(default=30, description="Execution timeout in seconds")
    tags: List[str] = Field(default_factory=list, description="Searchable tags")
    
    # Nested Domain Concepts
    version: ToolVersion = Field(default_factory=ToolVersion, description="Versioning information")
    capabilities: ToolCapabilities = Field(default_factory=ToolCapabilities, description="Execution capabilities")
    permissions: ToolPermissions = Field(default_factory=ToolPermissions, description="Access requirements")
    
    model_config = {"frozen": True}
