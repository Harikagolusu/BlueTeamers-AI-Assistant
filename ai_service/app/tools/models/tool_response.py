from typing import Any, Optional
from pydantic import BaseModel, Field
from app.tools.models.types import ToolMetadata

class ToolResponse(BaseModel):
    """
    Represents the standardized output of a tool execution.
    
    Purpose:
        Ensures the Chat API receives a predictable, normalized response, isolating it from raw exceptions.
        
    Immutability:
        Frozen. Must never be mutated once returned by the Executor or Tool.
        
    Expected lifecycle:
        Created by the ITool implementation (or Executor on failure) and passed up to the Service and Chat API.
        
    Usage:
        Evaluated for `success`. If true, `result` contains the payload. If false, `error` contains the normalized message.
    """
    success: bool = Field(..., description="Whether the tool execution was successful")
    result: Any = Field(None, description="The output data from the tool if successful")
    error: Optional[str] = Field(None, description="Error message if the execution failed")
    metadata: ToolMetadata = Field(default_factory=dict, description="Execution metadata (duration, cache hit, etc.)")
    
    model_config = {
        "frozen": True
    }
