from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from typing import List

class ToolSupport(str, Enum):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)
    MCP = "MCP"
    LOCAL = "LOCAL"
    REST = "REST"

class CapabilityModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)
    """
    Defines the specific capabilities an agent possesses.
    Matches the Capability enum in ExecutionPlan.
    """
    capability_name: str
    description: str = ""
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    tags: List[str] = Field(default_factory=list)
    supported_tool_types: List[ToolSupport] = Field(default_factory=list)
