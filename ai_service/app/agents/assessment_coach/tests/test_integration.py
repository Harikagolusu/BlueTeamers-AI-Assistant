import pytest
from app.agents.assessment_coach.agent import AssessmentCoachAgent
from app.agents.registry.agent_registry import AgentRegistry
from app.agents.assessment_coach.registry import register_agent

@pytest.mark.asyncio
async def test_capability_registration():
    registry = AgentRegistry()
    register_agent(registry)
    
    agent_info = registry.get("assessment_coach")
    assert agent_info is not None
    assert "ASSESSMENT" in agent_info.manifest.capabilities
    assert "READINESS_ASSESSMENT" in agent_info.manifest.capabilities
    assert "ADAPTIVE_ASSESSMENT" in agent_info.manifest.capabilities
