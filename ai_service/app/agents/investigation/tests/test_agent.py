import pytest
from unittest.mock import AsyncMock, MagicMock
from app.agents.investigation.agent import InvestigationAgent
from app.agents.manifests.models import AgentManifest
from app.agents.models.agent_models import AgentState
from app.services.orchestration.service import AgentOrchestrationService

@pytest.fixture
def manifest():
    return AgentManifest(
        name="investigation_agent",
        prompt_template="investigation_agent_system",
        model="test-model",
        tools=["evidence_collection_tool"]
    )

@pytest.fixture
def orchestration_service():
    service = MagicMock(spec=AgentOrchestrationService)
    service.invoke_agents_concurrently = AsyncMock(return_value={})
    return service

@pytest.fixture
def context():
    ctx = MagicMock()
    ctx.conversation.session_id = "test-session"
    
    valid_json = '''{
        "executive_summary": "Test summary",
        "evidence_collected": {"items": [], "total_count": 0},
        "evidence_correlation": {"correlated_entities": {}, "process_trees": [], "network_sessions": []},
        "soc_findings": [],
        "threat_intelligence_findings": [],
        "mitre_mapping": [],
        "incident_timeline": {"events": []},
        "affected_assets": [],
        "risk_assessment": "HIGH",
        "confidence": 90,
        "recommendations": [],
        "next_investigation_steps": [],
        "learning_guidance": "Test guidance."
    }'''
    
    ctx.runtime.runtime_manager.llm_provider.generate = AsyncMock(return_value=MagicMock(text=valid_json))
    ctx.runtime.prompt_builder.build = MagicMock(return_value="test prompt")
    return ctx

@pytest.mark.asyncio
async def test_agent_lifecycle(manifest, orchestration_service, context):
    agent = InvestigationAgent(manifest, orchestration_service)
    agent.raw_evidence = [{"type": "log", "content": "test"}]
    
    result = await agent.execute(context)
    
    assert result.success is True
    assert agent.state == AgentState.COMPLETED
    assert "Test summary" in str(result.response)
    
    # Verify LLM call
    context.runtime.runtime_manager.llm_provider.generate.assert_called_once()
