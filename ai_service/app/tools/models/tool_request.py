from pydantic import BaseModel, Field
from app.tools.models.types import ToolArguments
from app.tools.models.execution_context import ExecutionContext

class ToolRequest(BaseModel):
    """
    Represents a request to execute a specific tool.
    
    Purpose:
        Acts as the standard DTO passed from the Chat API down to the concrete tools.
        
    Immutability:
        Frozen. Must never be altered by the ToolService or ToolExecutor.
        
    Expected lifecycle:
        Created upstream, routed through the Service and Executor, consumed by the Tool.
        
    Usage:
        Read-only container for tool arguments and enterprise execution context.
    """
    tool_name: str = Field(..., description="The name of the tool to execute")
    arguments: ToolArguments = Field(default_factory=dict, description="The arguments to pass to the tool")
    context: ExecutionContext = Field(default_factory=ExecutionContext, description="The strictly-typed execution context")
    
    model_config = {
        "frozen": True
    }
