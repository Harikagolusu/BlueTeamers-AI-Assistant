import time
from typing import Callable, Type
from app.tools.interfaces.tool import ITool
from app.tools.discovery.interfaces.discovery_interfaces import (
    IDiscoveryEngine, IModuleLoader, IClassScanner, 
    IMetadataResolver, IToolValidator, IToolFilter, IRegistrationService
)
from app.tools.discovery.config.config import DiscoveryConfig
from app.tools.discovery.metadata.models import DiscoveryReport
from app.tools.discovery.exceptions.exceptions import ToolDiscoveryError

class DiscoveryEngine(IDiscoveryEngine):
    """
    Orchestrates the entire tool discovery pipeline and emits lifecycle hooks.
    """
    def __init__(
        self,
        config: DiscoveryConfig,
        loader: IModuleLoader,
        scanner: IClassScanner,
        resolver: IMetadataResolver,
        validator: IToolValidator,
        filter_svc: IToolFilter,
        registration: IRegistrationService,
        di_resolver: Callable[[Type[ITool]], ITool]
    ):
        self._config = config
        self._loader = loader
        self._scanner = scanner
        self._resolver = resolver
        self._validator = validator
        self._filter = filter_svc
        self._registration = registration
        self._di_resolver = di_resolver
        
    def discover_and_register(self) -> DiscoveryReport:
        start_time = time.perf_counter()
        report = DiscoveryReport()
        
        self.before_discovery()
        
        try:
            # 1. Load Packages
            modules = self._loader.load_packages(self._config.tool_packages, self._config.excluded_packages)
            
            # 2. Scan Classes
            tool_classes = self._scanner.scan_classes(modules)
            report.loaded_tools = len(tool_classes)
            
            existing_names = set()
            
            # Process each discovered tool
            for cls in tool_classes:
                try:
                    # 3. Resolve Metadata
                    metadata = self._resolver.resolve(cls)
                    
                    # 4. Filter
                    if not self._filter.should_include(metadata):
                        report.skipped_tools += 1
                        continue
                        
                    # 5. Validate
                    self._validator.validate(metadata, existing_names)
                    
                    existing_names.add(metadata.name)
                    for alias in metadata.aliases:
                        existing_names.add(alias)
                        
                    # 6. Instantiate
                    self.before_registration(metadata.name)
                    tool_instance = self._di_resolver(cls)
                    
                    # 7. Register
                    self._registration.register(tool_instance)
                    self.after_registration(metadata.name)
                    
                    report.registered_tools += 1
                    
                except Exception as e:
                    report.failed_tools += 1
                    report.warnings.append(f"Failed to process {cls.__name__}: {str(e)}")
                    if "Duplicate" in str(e):
                        report.duplicate_tools += 1
                        
        except Exception as e:
            report.warnings.append(f"Critical discovery failure: {e}")
            raise ToolDiscoveryError(f"Discovery pipeline failed: {e}")
            
        finally:
            self.after_discovery()
            report.duration_ms = int((time.perf_counter() - start_time) * 1000)
            
        return report

    # Lifecycle Hooks
    def before_discovery(self) -> None:
        pass
        
    def after_discovery(self) -> None:
        pass
        
    def before_registration(self, tool_name: str) -> None:
        pass
        
    def after_registration(self, tool_name: str) -> None:
        pass
