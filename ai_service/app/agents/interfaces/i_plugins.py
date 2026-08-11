from abc import ABC, abstractmethod
from typing import List, Any
from app.agents.manifests.plugin_manifest import PluginManifest

class IPluginDiscovery(ABC):
    @abstractmethod
    def discover_plugins(self, paths: List[str]) -> List[PluginManifest]: pass

class IPluginSandbox(ABC):
    @abstractmethod
    def validate_plugin(self, manifest: PluginManifest, source_path: str) -> bool: pass

class IPluginLoader(ABC):
    @abstractmethod
    def load_plugin(self, manifest: PluginManifest, source_path: str) -> Any: pass
    @abstractmethod
    def unload_plugin(self, plugin_id: str) -> None: pass

class IPluginRegistry(ABC):
    @abstractmethod
    def register_plugin(self, plugin_id: str, instance: Any) -> None: pass
    @abstractmethod
    def unregister_plugin(self, plugin_id: str) -> None: pass
    @abstractmethod
    def get_plugin(self, plugin_id: str) -> Any: pass

class IPluginManager(ABC):
    @abstractmethod
    def enable_plugin(self, plugin_id: str) -> None: pass
    @abstractmethod
    def disable_plugin(self, plugin_id: str) -> None: pass
    @abstractmethod
    def reload_plugin(self, plugin_id: str) -> None: pass
