from abc import ABC, abstractmethod
from typing import List, Optional, Any
from app.agents.manifests.skill_manifest import SkillManifest

class ISkillRegistry(ABC):
    @abstractmethod
    def register_skill(self, manifest: SkillManifest) -> None: pass
    @abstractmethod
    def remove_skill(self, skill_id: str) -> None: pass
    @abstractmethod
    def get_skill(self, skill_id: str) -> Optional[SkillManifest]: pass

class ICapabilityIndex(ABC):
    @abstractmethod
    def index_skill(self, capability: str, skill_id: str) -> None: pass
    @abstractmethod
    def get_skills_for_capability(self, capability: str) -> List[str]: pass
    @abstractmethod
    def remove_skill(self, skill_id: str) -> None: pass

class ICapabilityResolver(ABC):
    @abstractmethod
    def resolve_candidates(self, capability: str, context: dict) -> List[str]: 
        """Returns ordered skill_ids based on priority, cost, health, compatibility."""
        pass

class ISkillMatcher(ABC):
    @abstractmethod
    def match_skill(self, capability: str, context: dict) -> Optional[SkillManifest]: pass

class ISkillExecutor(ABC):
    @abstractmethod
    def execute_skill(self, skill_id: str, inputs: dict) -> Any: pass
