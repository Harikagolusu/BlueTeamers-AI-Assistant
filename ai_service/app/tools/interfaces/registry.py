from abc import ABC, abstractmethod
from typing import Tuple
from app.tools.interfaces.tool import ITool

class IToolRegistry(ABC):
    """
    Contract for managing the registration and retrieval of tools.
    
    Responsibilities:
        - Maintain an in-memory or persisted registry of all available tools.
        - Prevent duplicate registrations to avoid ambiguous executions.
        
    Must Do:
        - Throw ToolNotFoundError if a requested tool does not exist.
        - Throw ToolRegistrationError on duplicate names.
        
    Must Never Do:
        - Never call tools directly.
        - Never mutate the registered ITool instances.
        
    Architecture Invariants:
        1. Registry MUST NEVER call tools.
        2. Registry MUST be the single source of truth for tool availability.
    """
    
    @abstractmethod
    def register_tool(self, tool: ITool) -> None:
        """
        Registers a tool.
        
        Args:
            tool (ITool): The concrete tool instance to register.
            
        Raises:
            ToolRegistrationError: If a tool with the same name is already registered.
        """
        pass
        
    @abstractmethod
    def get_tool(self, name: str) -> ITool:
        """
        Retrieves a registered tool by name.
        
        Args:
            name (str): The name of the tool to retrieve.
            
        Returns:
            ITool: The requested tool instance.
            
        Raises:
            ToolNotFoundError: If the tool is not found in the registry.
        """
        pass
        
    @abstractmethod
    def get_registered_tools(self) -> Tuple[ITool, ...]:
        """
        Retrieves a snapshot of all registered tools.
        
        Returns:
            Tuple[ITool, ...]: An immutable collection of available tools.
        """
        pass
        
    @property
    @abstractmethod
    def tool_count(self) -> int:
        """Returns the number of registered tools."""
        pass
