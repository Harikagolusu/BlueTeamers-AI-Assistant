from typing import Optional, Dict
import threading
from app.agents.interfaces.i_skills import ISkillRegistry
from app.agents.manifests.skill_manifest import SkillManifest

class SkillRegistry(ISkillRegistry):
    def __init__(self):
        self._skills: Dict[str, SkillManifest] = {}
        self._lock = threading.RLock()

    def register_skill(self, manifest: SkillManifest) -> None:
        with self._lock:
            self._skills[manifest.skill_id] = manifest

    def remove_skill(self, skill_id: str) -> None:
        with self._lock:
            if skill_id in self._skills:
                del self._skills[skill_id]

    def get_skill(self, skill_id: str) -> Optional[SkillManifest]:
        with self._lock:
            return self._skills.get(skill_id)
