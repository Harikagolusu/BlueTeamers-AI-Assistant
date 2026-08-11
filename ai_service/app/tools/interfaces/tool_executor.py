from abc import ABC, abstractmethod
from app.tools.models.tool_request import ToolRequest
from app.tools.models.tool_response import ToolResponse

class IToolExecutor(ABC):
    """
    Contract for executing tools. 
    
    Responsibilities:
        - Mechanical invocation of a tool's execute method.
        - Isolating failures by trapping raw exceptions.
        
    Must Do:
        - Normalize all raw exceptions (Network errors, Timeouts) into a failed ToolResponse.
        - Look up the tool via IToolRegistry.
        - Enforce execution timeouts.
        
    Must Never Do:
        - Never contain business logic (e.g., checking user permissions).
        - Never propagate raw exceptions up to the Service layer (except CancelledError).
        
    Architecture Invariants:
        1. ToolExecutor MUST NEVER contain business logic.
        2. Tool execution MUST be asynchronous.
        3. ToolExecutor MUST NEVER return raw exceptions.
    """
    
    @abstractmethod
    async def execute_tool(self, request: ToolRequest) -> ToolResponse:
        """
        Locates and executes a tool asynchronously.
        
        Args:
            request (ToolRequest): The request containing the tool name and arguments.
            
        Returns:
            ToolResponse: The standardized response. Must return a failed ToolResponse 
                          instead of propagating raw exceptions.
        """
        pass
