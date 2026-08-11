from app.tools.interfaces.tool import ITool
from app.tools.interfaces.registry import IToolRegistry
from app.tools.discovery.interfaces.discovery_interfaces import IRegistrationService
from app.tools.discovery.exceptions.exceptions import ToolRegistrationError

class RegistrationService(IRegistrationService):
    """
    Acts as a proxy to ToolRegistry and handles plugin lifecycles.
    """
    def __init__(self, registry: IToolRegistry):
        self._registry = registry
        
    def register(self, tool: ITool) -> None:
        try:
            self._registry.register_tool(tool)
        except Exception as e:
            raise ToolRegistrationError(f"Failed to register tool '{tool.name}': {e}")
