from abc import ABC, abstractmethod
from typing import List

class IVersionManager(ABC):
    @abstractmethod
    def get_latest_version(self, component_id: str) -> str: pass
    @abstractmethod
    def is_update_available(self, component_id: str, current_version: str) -> bool: pass

class ICompatibilityResolver(ABC):
    @abstractmethod
    def check_compatibility(self, required_version: str, current_version: str) -> bool: pass
    @abstractmethod
    def validate_platform_compatibility(self, package_metadata: dict) -> bool: pass
