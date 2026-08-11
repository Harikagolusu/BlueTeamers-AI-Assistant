from abc import ABC, abstractmethod
from typing import Dict, Any

class IManifestValidator(ABC):
    @abstractmethod
    def validate_agent_manifest(self, manifest_data: Dict[str, Any]) -> bool: pass
    @abstractmethod
    def validate_plugin_manifest(self, manifest_data: Dict[str, Any]) -> bool: pass
    @abstractmethod
    def validate_skill_manifest(self, manifest_data: Dict[str, Any]) -> bool: pass
