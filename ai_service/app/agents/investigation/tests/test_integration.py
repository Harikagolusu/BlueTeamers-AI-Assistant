import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from app.agents.investigation.agent import InvestigationAgent
from app.agents.manifests.models import AgentManifest
from app.agents.models.agent_models import AgentState
from app.shared.models.communication import AgentExecutionResult, AgentResponse
from app.services.orchestration.service import AgentOrchestrationService

from app.agents.investigation.tools import (
    EvidenceCollectionTool,
    EvidenceCorrelationTool,
    InvestigationPlanningTool,
    IncidentTimelineTool,
    InvestigationSummaryTool
)

@pytest.fixture
def manifest():
    return AgentManifest(
        name="investigation_agent",
        prompt_template="investigation_agent_system",
        model="test-model",
        tools=[
            "evidence_collection_tool",
            "evidence_correlation_tool",
            "investigation_planning_tool",
            "incident_timeline_tool",
            "investigation_summary_tool"
        ]
    )

@pytest.fixture
def context():
    ctx = MagicMock()
    ctx.conversation.session_id = "test-integration"
    
    valid_json = '''{
        "executive_summary": "Integration test summary",
        "evidence_collected": {"items": [], "total_count": 0},
        "evidence_correlation": {"correlated_entities": {}, "process_trees": [], "network_sessions": []},
        "soc_findings": [{"status": "success"}],
        "threat_intelligence_findings": [{"status": "partial"}],
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
async def test_integration_expert_agent_unavailable(manifest, context):
    """
    Test where SOC Analyst succeeds but Threat Intel fails/unavailable.
    Validates graceful degradation.
    """
    orchestration_service = MagicMock(spec=AgentOrchestrationService)
    
    # Mock concurrent invocation to simulate SOC Analyst success and Threat Intel failure
    async def mock_invoke(invocations, ctx):
        results = {}
        for inv in invocations:
            if inv.target_agent == "soc_analyst":
                results["soc_analyst"] = AgentExecutionResult(
                    execution_id="1", agent_name="soc_analyst", success=True, 
                    response=AgentResponse(request_id="1", success=True, data='{"status": "success"}')
                )
            if inv.target_agent == "threat_intelligence":
                results["threat_intelligence"] = AgentExecutionResult(
                    execution_id="2", agent_name="threat_intelligence", success=False,
                    response=AgentResponse(request_id="2", success=False, errors=["Agent timeout"])
                )
        return results
        
    orchestration_service.invoke_agents_concurrently = mock_invoke
    
    agent = InvestigationAgent(manifest, orchestration_service)
    agent.set_tools([
        EvidenceCollectionTool(),
        EvidenceCorrelationTool(),
        InvestigationPlanningTool(),
        IncidentTimelineTool(),
        InvestigationSummaryTool()
    ])
    
    agent.raw_evidence = [{"type": "log", "content": "test log"}, {"type": "ioc", "content": "1.1.1.1"}]
    
    result = await agent.execute(context)
    
    assert result.success is True
    assert agent.state == AgentState.COMPLETED
    
    response_dict = json.loads(result.response)
    assert response_dict["executive_summary"] == "Integration test summary"
