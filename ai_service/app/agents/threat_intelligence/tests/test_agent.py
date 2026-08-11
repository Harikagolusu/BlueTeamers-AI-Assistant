import pytest
from unittest.mock import AsyncMock, MagicMock
from app.agents.threat_intelligence.agent import ThreatIntelligenceAgent
from app.agents.manifests.models import AgentManifest

from app.agents.models.agent_models import AgentState

@pytest.fixture
def manifest():
    return AgentManifest(
        name="threat_intelligence",
        prompt_template="threat_intelligence_system",
        model="test-model",
        tools=["ioc_lookup_tool"]
    )

@pytest.fixture
def context():
    ctx = MagicMock()
    ctx.conversation.session_id = "test-session"
    valid_json = '''{
        "executive_summary": "Test summary",
        "indicator_details": [],
        "threat_assessment": {"risk_level": "HIGH", "summary": "Bad", "affected_assets": []},
        "threat_intelligence": {"threat_actors": [], "campaigns": [], "related_malware": []},
        "mitre_attack_mapping": [],
        "evidence": [],
        "confidence_score": 90,
        "recommended_next_steps": [],
        "references": []
    }'''
    ctx.runtime.runtime_manager.llm_provider.generate = AsyncMock(return_value=MagicMock(text=valid_json))
    return ctx

@pytest.mark.asyncio
async def test_agent_lifecycle(manifest, context):
    agent = ThreatIntelligenceAgent(manifest)
    result = await agent.execute(context)
    
    assert result.success is True
    assert agent.state == AgentState.COMPLETED
    assert "Test summary" in str(result.response)
    
    # Verify that the LLM was called
    context.runtime.runtime_manager.llm_provider.generate.assert_called_once()
