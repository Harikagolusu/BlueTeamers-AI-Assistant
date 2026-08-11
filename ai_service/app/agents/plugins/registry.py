from typing import Dict, Any, Optional
from app.agents.interfaces.i_plugins import IPluginRegistry

class PluginRegistry(IPluginRegistry):
    def __init__(self):
        self._plugins: Dict[str, Any] = {}

    def register_plugin(self, plugin_id: str, instance: Any) -> None:
        self._plugins[plugin_id] = instance

    def unregister_plugin(self, plugin_id: str) -> None:
        if plugin_id in self._plugins:
            del self._plugins[plugin_id]

    def get_plugin(self, plugin_id: str) -> Optional[Any]:
        return self._plugins.get(plugin_id)
