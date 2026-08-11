from app.tools.registry.registry_factory import RegistryFactory
from app.tools.interfaces.registry import IToolRegistry
from app.tools.executor.tool_executor import ToolExecutor
from app.tools.interfaces.tool_executor import IToolExecutor
from app.tools.service.tool_service import ToolService
from app.tools.interfaces.tool_service import IToolService

def get_tool_registry() -> IToolRegistry:
    """Returns the singleton ToolRegistry instance."""
    return RegistryFactory.create_registry()

def get_tool_executor(registry: IToolRegistry = None) -> IToolExecutor:
    """Returns a new ToolExecutor instance per request."""
    if registry is None:
        registry = get_tool_registry()
    return ToolExecutor(registry=registry)

def get_tool_service(
    executor: IToolExecutor = None, 
    registry: IToolRegistry = None
) -> IToolService:
    """Returns a new ToolService instance per request."""
    if registry is None:
        registry = get_tool_registry()
    if executor is None:
        executor = get_tool_executor(registry)
    return ToolService(executor=executor, registry=registry)
