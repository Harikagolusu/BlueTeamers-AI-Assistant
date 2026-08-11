from typing import Callable, Type
from app.tools.interfaces.tool import ITool
from app.tools.interfaces.registry import IToolRegistry
from app.tools.discovery.config.config import DiscoveryConfig
from app.tools.discovery.loader.module_loader import ModuleLoader
from app.tools.discovery.scanner.class_scanner import ClassScanner
from app.tools.discovery.resolver.metadata_resolver import MetadataResolver
from app.tools.discovery.validators.tool_validator import ToolValidator
from app.tools.discovery.filters.tool_filter import ToolFilter
from app.tools.discovery.registration.registration_service import RegistrationService
from app.tools.discovery.engine.discovery_engine import DiscoveryEngine
from app.tools.discovery.metadata.models import DiscoveryReport

def default_di_resolver(cls: Type[ITool]) -> ITool:
    """Fallback no-arg instantiation if no DI container is provided."""
    return cls()

def run_discovery(
    registry: IToolRegistry, 
    config: DiscoveryConfig = None, 
    di_resolver: Callable[[Type[ITool]], ITool] = default_di_resolver
) -> DiscoveryReport:
    """
    Wires up the discovery pipeline components and runs the orchestration engine.
    """
    config = config or DiscoveryConfig()
    
    loader = ModuleLoader()
    scanner = ClassScanner()
    resolver = MetadataResolver()
    validator = ToolValidator()
    tool_filter = ToolFilter(config)
    registration = RegistrationService(registry)
    
    engine = DiscoveryEngine(
        config=config,
        loader=loader,
        scanner=scanner,
        resolver=resolver,
        validator=validator,
        filter_svc=tool_filter,
        registration=registration,
        di_resolver=di_resolver
    )
    
    return engine.discover_and_register()
