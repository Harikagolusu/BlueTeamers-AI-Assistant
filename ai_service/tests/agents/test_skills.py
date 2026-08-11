import pytest
from app.agents.skills.registry import SkillRegistry
from app.agents.skills.capability_index import CapabilityIndex
from app.agents.skills.resolver import CapabilityResolver
from app.agents.skills.matcher import SkillMatcher
from app.agents.manifests.skill_manifest import SkillManifest

def test_skill_resolution_pipeline():
    registry = SkillRegistry()
    index = CapabilityIndex()
    resolver = CapabilityResolver(index, registry)
    matcher = SkillMatcher(resolver, registry)
    
    manifest1 = SkillManifest(
        skill_id="skill-1",
        name="Skill 1",
        version="1.0",
        capability="SECURITY_SCAN"
    )
    
    manifest2 = SkillManifest(
        skill_id="skill-2",
        name="Skill 2",
        version="1.0",
        capability="SECURITY_SCAN"
    )
    
    registry.register_skill(manifest1)
    registry.register_skill(manifest2)
    
    index.index_skill("SECURITY_SCAN", "skill-1")
    index.index_skill("SECURITY_SCAN", "skill-2")
    
    # Test O(1) index retrieval
    skills = index.get_skills_for_capability("SECURITY_SCAN")
    assert len(skills) == 2
    assert "skill-1" in skills
    assert "skill-2" in skills
    
    # Test Matcher (returns first candidate)
    matched = matcher.match_skill("SECURITY_SCAN", {})
    assert matched is not None
    assert matched.skill_id in ["skill-1", "skill-2"]
    
    # Test removal
    index.remove_skill("skill-1")
    skills = index.get_skills_for_capability("SECURITY_SCAN")
    assert len(skills) == 1
