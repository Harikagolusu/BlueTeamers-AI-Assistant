from typing import List, Dict, Any
from app.agents.interfaces.i_skills import ICapabilityResolver, ICapabilityIndex, ISkillRegistry

class CapabilityResolver(ICapabilityResolver):
    def __init__(self, index: ICapabilityIndex, registry: ISkillRegistry):
        self._index = index
        self._registry = registry

    def resolve_candidates(self, capability: str, context: Dict[str, Any]) -> List[str]:
        """
        Resolves multiple candidate skills for a capability based on context (priority, cost, etc).
        """
        skill_ids = self._index.get_skills_for_capability(capability)
        
        # In a real enterprise system, we would score them based on context (token limits, latency thresholds, etc.)
        # For now, return them directly. A future plugin could intercept this sorting.
        return skill_ids
