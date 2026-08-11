from abc import ABC, abstractmethod
from typing import Any, List, Type, Dict, Callable
from app.tools.interfaces.tool import ITool
from app.tools.discovery.metadata.models import DiscoveryReport, ToolMetadata

class IModuleLoader(ABC):
    @abstractmethod
    def load_packages(self, packages: List[str], excluded: List[str]) -> List[Any]:
        pass

class IClassScanner(ABC):
    @abstractmethod
    def scan_classes(self, modules: List[Any]) -> List[Type[ITool]]:
        pass

class IMetadataResolver(ABC):
    @abstractmethod
    def resolve(self, tool_class: Type[ITool]) -> ToolMetadata:
        pass

class IToolValidator(ABC):
    @abstractmethod
    def validate(self, metadata: ToolMetadata, existing_names: set) -> None:
        pass

class IToolFilter(ABC):
    @abstractmethod
    def should_include(self, metadata: ToolMetadata) -> bool:
        pass

class IRegistrationService(ABC):
    @abstractmethod
    def register(self, tool: ITool) -> None:
        pass

class IDiscoveryEngine(ABC):
    @abstractmethod
    def discover_and_register(self) -> DiscoveryReport:
        pass
