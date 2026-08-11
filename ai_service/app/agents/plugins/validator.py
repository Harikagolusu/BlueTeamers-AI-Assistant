from typing import Dict, Any
from app.agents.manifests.plugin_manifest import PluginManifest

class PluginValidator:
    def validate(self, data: Dict[str, Any]) -> PluginManifest:
        # Pydantic validates the schema
        return PluginManifest(**data)
