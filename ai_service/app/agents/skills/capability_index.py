from typing import List, Dict, Set
import threading
from app.agents.interfaces.i_skills import ICapabilityIndex

class CapabilityIndex(ICapabilityIndex):
    """
    O(1) capability lookup index.
    """
    def __init__(self):
        self._index: Dict[str, Set[str]] = {}
        self._lock = threading.RLock()

    def index_skill(self, capability: str, skill_id: str) -> None:
        with self._lock:
            if capability not in self._index:
                self._index[capability] = set()
            self._index[capability].add(skill_id)

    def get_skills_for_capability(self, capability: str) -> List[str]:
        with self._lock:
            return list(self._index.get(capability, set()))

    def remove_skill(self, skill_id: str) -> None:
        with self._lock:
            for capability, skills in self._index.items():
                if skill_id in skills:
                    skills.remove(skill_id)
