from app.agents.interfaces.i_plugins import IPluginManager, IPluginLoader, IPluginRegistry
from app.agents.manifests.plugin_manifest import PluginManifest

class PluginManager(IPluginManager):
    def __init__(self, loader: IPluginLoader, registry: IPluginRegistry):
        self._loader = loader
        self._registry = registry
        self._manifests = {} # plugin_id -> manifest
        self._paths = {} # plugin_id -> path
        self._enabled = {} # plugin_id -> bool
        
    def add_known_plugin(self, manifest: PluginManifest, path: str):
        self._manifests[manifest.plugin_id] = manifest
        self._paths[manifest.plugin_id] = path
        self._enabled[manifest.plugin_id] = False

    def enable_plugin(self, plugin_id: str) -> None:
        if plugin_id not in self._manifests:
            raise ValueError(f"Plugin {plugin_id} not known")
            
        if self._enabled.get(plugin_id):
            return
            
        instance = self._loader.load_plugin(self._manifests[plugin_id], self._paths[plugin_id])
        self._registry.register_plugin(plugin_id, instance)
        self._enabled[plugin_id] = True

    def disable_plugin(self, plugin_id: str) -> None:
        if not self._enabled.get(plugin_id):
            return
            
        self._registry.unregister_plugin(plugin_id)
        self._loader.unload_plugin(plugin_id)
        self._enabled[plugin_id] = False

    def reload_plugin(self, plugin_id: str) -> None:
        self.disable_plugin(plugin_id)
        self.enable_plugin(plugin_id)
