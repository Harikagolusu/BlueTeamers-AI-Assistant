from typing import Optional, Dict, Any
from app.agents.interfaces.i_skills import ISkillMatcher, ICapabilityResolver, ISkillRegistry
from app.agents.manifests.skill_manifest import SkillManifest

class SkillMatcher(ISkillMatcher):
    def __init__(self, resolver: ICapabilityResolver, registry: ISkillRegistry):
        self._resolver = resolver
        self._registry = registry

    def match_skill(self, capability: str, context: Dict[str, Any]) -> Optional[SkillManifest]:
        candidates = self._resolver.resolve_candidates(capability, context)
        if not candidates:
            return None
            
        # Top candidate based on resolver's sorting
        best_candidate_id = candidates[0]
        return self._registry.get_skill(best_candidate_id)
