import pytest
import json
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
        tools=[
            "ioc_lookup_tool", "reputation_tool", "threat_actor_tool", 
            "campaign_lookup_tool", "indicator_correlation_tool", "mitre_mapping_tool"
        ]
    )

@pytest.mark.asyncio
async def test_integration_mixed_iocs(manifest):
    context = MagicMock()
    context.conversation.session_id = "test-session-mixed"
    
    mock_response = {
        "executive_summary": "Analysis of mixed indicators.",
        "indicator_details": [
            {"value": "8.8.8.8", "type": "ip", "description": "Google Public DNS", "confidence": 100},
            {"value": "44d88612fea8a8f36de82e1278abb02f", "type": "hash", "description": "Known Malicious", "confidence": 95}
        ],
        "threat_assessment": {"risk_level": "HIGH", "summary": "Found malicious hash.", "affected_assets": []},
        "threat_intelligence": {"threat_actors": [], "campaigns": [], "related_malware": []},
        "mitre_attack_mapping": [],
        "evidence": ["Hash matched known malware database."],
        "confidence_score": 90,
        "recommended_next_steps": ["Block the hash on endpoints."],
        "references": []
    }
    
    context.runtime.runtime_manager.llm_provider.generate = AsyncMock(
        return_value=MagicMock(text=json.dumps(mock_response))
    )
    
    agent = ThreatIntelligenceAgent(manifest)
    # Simulate setting the context manually
    agent.investigation_context = {"iocs": ["8.8.8.8", "44d88612fea8a8f36de82e1278abb02f", "example.com"]}
    
    result = await agent.execute(context)
    assert result.success is True
    assert agent.state == AgentState.COMPLETED
    response_dict = json.loads(result.response)
    assert response_dict["threat_assessment"]["risk_level"] == "HIGH"

@pytest.mark.asyncio
async def test_integration_threat_actor_query(manifest):
    context = MagicMock()
    context.conversation.session_id = "test-session-actor"
    
    mock_response = {
        "executive_summary": "Analysis of APT29.",
        "indicator_details": [],
        "threat_assessment": {"risk_level": "CRITICAL", "summary": "Advanced persistent threat actor.", "affected_assets": []},
        "threat_intelligence": {"threat_actors": ["APT29"], "campaigns": ["SolarWinds"], "related_malware": []},
        "mitre_attack_mapping": [{"tactic": "Initial Access", "technique_id": "T1566", "technique_name": "Phishing", "description": "Spearphishing"}],
        "evidence": ["Actor is known to target government."],
        "confidence_score": 100,
        "recommended_next_steps": ["Hunt for T1566.", "Hunt for T1078."],
        "references": []
    }
    
    context.runtime.runtime_manager.llm_provider.generate = AsyncMock(
        return_value=MagicMock(text=json.dumps(mock_response))
    )
    
    agent = ThreatIntelligenceAgent(manifest)
    agent.investigation_context = {"actor_query": "APT29"}
    
    result = await agent.execute(context)
    assert result.success is True
    response_dict = json.loads(result.response)
    assert "APT29" in response_dict["threat_intelligence"]["threat_actors"]

@pytest.mark.asyncio
async def test_integration_unknown_ioc(manifest):
    context = MagicMock()
    context.conversation.session_id = "test-session-unknown"
    
    mock_response = {
        "executive_summary": "Analysis of unknown indicator.",
        "indicator_details": [
            {"value": "192.168.1.1", "type": "ip", "description": "No intelligence available", "confidence": 0}
        ],
        "threat_assessment": {"risk_level": "UNKNOWN", "summary": "No intelligence available", "affected_assets": []},
        "threat_intelligence": {"threat_actors": [], "campaigns": [], "related_malware": []},
        "mitre_attack_mapping": [],
        "evidence": [],
        "confidence_score": 0,
        "recommended_next_steps": ["Monitor traffic to/from IP."],
        "references": []
    }
    
    context.runtime.runtime_manager.llm_provider.generate = AsyncMock(
        return_value=MagicMock(text=json.dumps(mock_response))
    )
    
    agent = ThreatIntelligenceAgent(manifest)
    agent.investigation_context = {"ioc_query": "192.168.1.1"}
    
    result = await agent.execute(context)
    assert result.success is True
    response_dict = json.loads(result.response)
    assert response_dict["threat_assessment"]["risk_level"] == "UNKNOWN"
