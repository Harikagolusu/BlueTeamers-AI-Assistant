from typing import List, Optional
from pydantic import BaseModel, Field
from app.tools.discovery.metadata.enums import ToolCategory, ToolState

class ToolMetadata(BaseModel):
    name: str = Field(..., description="Unique identifier for the tool")
    description: str = Field(..., description="Description of the tool for the LLM")
    category: ToolCategory = Field(default=ToolCategory.CUSTOM, description="Categorization for grouping")
    version: str = Field(default="1.0.0", description="Semantic version of the tool")
    aliases: List[str] = Field(default_factory=list, description="Alternative names for the tool")
    permissions: List[str] = Field(default_factory=list, description="Required permissions to execute this tool")
    state: ToolState = Field(default=ToolState.ACTIVE, description="Lifecycle state of the tool")
    timeout: Optional[int] = Field(default=30, description="Execution timeout in seconds")
    
    model_config = {
        "frozen": True
    }

class DiscoveryReport(BaseModel):
    loaded_tools: int = Field(default=0)
    registered_tools: int = Field(default=0)
    skipped_tools: int = Field(default=0)
    failed_tools: int = Field(default=0)
    duplicate_tools: int = Field(default=0)
    warnings: List[str] = Field(default_factory=list)
    duration_ms: int = Field(default=0)
    
    model_config = {
        "frozen": False # Report is mutable during discovery
    }
