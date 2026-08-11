from typing import List, Dict
from app.agents.manifests.plugin_manifest import PluginManifest

class PluginDependencyResolver:
    """
    Resolves dependency order for loading plugins.
    """
    def resolve(self, plugins: List[PluginManifest]) -> List[PluginManifest]:
        # Simple topological sort for dependencies
        resolved = []
        pending = {p.plugin_id: p for p in plugins}
        
        while pending:
            # Find a plugin with no unresolved dependencies
            ready = None
            for pid, plugin in pending.items():
                if all(dep not in pending for dep in plugin.dependencies):
                    ready = plugin
                    break
            
            if not ready:
                raise ValueError("Circular dependency detected in plugins")
                
            resolved.append(ready)
            del pending[ready.plugin_id]
            
        return resolved
