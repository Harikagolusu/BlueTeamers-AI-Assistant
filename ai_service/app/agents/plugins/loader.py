import importlib.util
import sys
from typing import Any
from app.agents.interfaces.i_plugins import IPluginLoader, IPluginSandbox
from app.agents.manifests.plugin_manifest import PluginManifest

class PluginLoader(IPluginLoader):
    def __init__(self, sandbox: IPluginSandbox):
        self._sandbox = sandbox
        self._loaded_modules = {}

    def load_plugin(self, manifest: PluginManifest, source_path: str) -> Any:
        # 1. Sandbox Validation
        if not self._sandbox.validate_plugin(manifest, source_path):
            raise ValueError(f"Plugin {manifest.plugin_id} failed sandbox validation.")

        # 2. Dynamic loading
        module_name = f"plugin_{manifest.plugin_id.replace('-', '_')}"
        spec = importlib.util.spec_from_file_location(module_name, source_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load plugin from {source_path}")
            
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        self._loaded_modules[manifest.plugin_id] = module
        
        # Expecting an entry_point class
        entry_point_class = getattr(module, manifest.entry_point)
        return entry_point_class()

    def unload_plugin(self, plugin_id: str) -> None:
        module_name = f"plugin_{plugin_id.replace('-', '_')}"
        if module_name in sys.modules:
            del sys.modules[module_name]
        if plugin_id in self._loaded_modules:
            del self._loaded_modules[plugin_id]
