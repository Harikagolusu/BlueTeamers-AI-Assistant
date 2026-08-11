import os
import yaml
from typing import List
from app.agents.interfaces.i_plugins import IPluginDiscovery
from app.agents.manifests.plugin_manifest import PluginManifest

class PluginDiscovery(IPluginDiscovery):
    def discover_plugins(self, paths: List[str]) -> List[PluginManifest]:
        manifests = []
        for path in paths:
            if not os.path.exists(path):
                continue
            
            for root, _, files in os.walk(path):
                if "plugin_manifest.yaml" in files:
                    manifest_path = os.path.join(root, "plugin_manifest.yaml")
                    with open(manifest_path, 'r') as f:
                        data = yaml.safe_load(f)
                        manifest = PluginManifest(**data)
                        manifests.append(manifest)
        return manifests
