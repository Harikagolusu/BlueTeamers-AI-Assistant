from typing import Optional, List
from app.tools.registry.tool_registry import ToolRegistry
from app.tools.interfaces.tool import ITool

class RegistryFactory:
    """
    Factory responsible for creating, initializing, and freezing the singleton registry.
    """
    _instance: Optional[ToolRegistry] = None
    
    @classmethod
    def create_registry(cls, tools_to_register: Optional[List[ITool]] = None) -> ToolRegistry:
        """
        Creates and returns the singleton ToolRegistry.
        If tools are provided, registers them and freezes the registry.
        """
        if cls._instance is not None:
            return cls._instance
            
        registry = ToolRegistry()
        
        if tools_to_register:
            for tool in tools_to_register:
                registry.register_tool(tool)
            # Only freeze if we actually registered the built-in tools.
            # In a real app, this is called during startup.
            registry.freeze()
            
        cls._instance = registry
        return cls._instance
        
    @classmethod
    def reset(cls) -> None:
        """For testing purposes only. Resets the singleton."""
        cls._instance = None
