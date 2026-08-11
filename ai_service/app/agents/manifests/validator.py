from typing import Dict, Any
from app.agents.interfaces.i_manifest_validator import IManifestValidator
from app.agents.manifests.agent_manifest import AgentManifest
from app.agents.manifests.plugin_manifest import PluginManifest
from app.agents.manifests.skill_manifest import SkillManifest

class ManifestValidator(IManifestValidator):
    def validate_agent_manifest(self, manifest_data: Dict[str, Any]) -> bool:
        try:
            AgentManifest(**manifest_data)
            return True
        except Exception:
            return False

    def validate_plugin_manifest(self, manifest_data: Dict[str, Any]) -> bool:
        try:
            PluginManifest(**manifest_data)
            return True
        except Exception:
            return False

    def validate_skill_manifest(self, manifest_data: Dict[str, Any]) -> bool:
        try:
            SkillManifest(**manifest_data)
            return True
        except Exception:
            return False
