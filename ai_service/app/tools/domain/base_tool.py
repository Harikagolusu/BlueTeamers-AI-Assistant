from typing import Dict, Any, Optional
from app.tools.interfaces.tool import ITool
from app.tools.models.tool_request import ToolRequest
from app.tools.models.tool_response import ToolResponse

class BaseTool(ITool):
    """
    Abstract base class providing standard lifecycle implementations and metadata wiring.
    Concrete tools should inherit from this instead of ITool directly.
    """
    
    # This will be injected by the @tool decorator
    __tool_metadata__: Optional[Any] = None 
    
    def __init__(self):
        # We rely on the decorator metadata, which should be normalized to ToolMetadata
        if not hasattr(self, '__tool_metadata__') or not self.__tool_metadata__:
            raise ValueError(f"Tool {self.__class__.__name__} is missing @tool decorator or metadata.")
            
    @property
    def name(self) -> str:
        # Assuming metadata is a ToolMetadata object containing 'name'
        return self.__tool_metadata__.name
        
    @property
    def description(self) -> str:
        return self.__tool_metadata__.description
        
    async def initialize(self) -> None:
        """Default no-op implementation."""
        pass
        
    async def shutdown(self) -> None:
        """Default no-op implementation."""
        pass
        
    # execute() is intentionally left abstract so subclasses MUST implement it.
