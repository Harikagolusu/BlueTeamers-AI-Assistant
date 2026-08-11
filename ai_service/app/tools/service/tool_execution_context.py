from typing import Optional, Dict, Any
import time
from pydantic import BaseModel, Field, ConfigDict
from app.tools.models.tool_request import ToolRequest
from app.tools.models.tool_response import ToolResponse

class ToolExecutionContext(BaseModel):
    """
    Internal orchestration state model for ToolService.
    
    Purpose:
        Encapsulates the entire lifecycle of a tool request through the orchestration layer.
        Provides a stable interface for hooks (_pre_execute, _post_execute) to inspect and 
        modify execution state without altering method signatures in the future.
        
    Immutability:
        The request is frozen and immutable. The response, metadata, and timestamps can be updated
        by the orchestration pipeline.
        
    Usage:
        Used exclusively within ToolService. Never exposed outside the orchestration layer.
    """
    request: ToolRequest = Field(..., description="The original immutable execution request")
    response: Optional[ToolResponse] = Field(default=None, description="The populated response if execution succeeded or failed")
    
    execution_start_time: float = Field(default_factory=time.perf_counter, description="High-resolution start time")
    execution_end_time: Optional[float] = Field(default=None, description="High-resolution end time")
    execution_duration_ms: Optional[int] = Field(default=None, description="Duration of the entire orchestration pipeline")
    
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Mutable dictionary for hooks to share state (e.g. cache keys)")
    execution_state: str = Field(default="initialized", description="Current phase of the pipeline (e.g. pre_hook, executing, post_hook, complete)")
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def mark_complete(self):
        """Calculates final duration."""
        self.execution_end_time = time.perf_counter()
        self.execution_duration_ms = int((self.execution_end_time - self.execution_start_time) * 1000)
