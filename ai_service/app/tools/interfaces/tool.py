from abc import ABC, abstractmethod
from app.tools.models.tool_request import ToolRequest
from app.tools.models.tool_response import ToolResponse

class ITool(ABC):
    """
    Contract for all concrete tool implementations.
    
    Responsibilities:
        Implement the specific business logic for a single capability.
        Integrate with external APIs securely via Infrastructure.
        
    Must Do:
        - Return a strictly normalized ToolResponse.
        - Handle internal state cleanly (be thread/async safe).
        
    Must Never Do:
        - Never execute synchronously.
        - Never mutate the ToolRequest.
        - Never catch asyncio.CancelledError.
        - Never log sensitive arguments or credentials.
        
    Architecture Invariants:
        1. Chat API MUST communicate only with IToolService.
        2. Every Tool MUST implement ITool.
        3. Every Tool MUST return ToolResponse.
        4. Tool execution MUST be asynchronous.
        5. All external communication MUST go through Infrastructure.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the unique name of the tool."""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """Returns the description of the tool."""
        pass
        
    @abstractmethod
    async def initialize(self) -> None:
        """
        Lifecycle hook called after instantiation but before the tool is registered.
        Useful for setting up database connections, MCP clients, or downloading heavy assets.
        """
        pass
        
    @abstractmethod
    async def shutdown(self) -> None:
        """
        Lifecycle hook called when the application is shutting down.
        Useful for cleaning up resources, closing connections, etc.
        """
        pass

    @abstractmethod
    async def execute(self, request: ToolRequest) -> ToolResponse:
        """
        Executes the tool asynchronously with the given request.
        
        Args:
            request (ToolRequest): The execution request containing arguments and context.
            
        Returns:
            ToolResponse: The standardized response containing success status, result, or error.
        """
        pass
