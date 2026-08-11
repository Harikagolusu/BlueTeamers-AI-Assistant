import pytest
import json
import os
from unittest.mock import Mock, AsyncMock
from app.agents.soc_analyst import SOCAnalystAgent
from app.agents.manifests.loader import ManifestLoader
from app.agents.context import AgentContext, ExecutionContext, UserContext, ConversationContext, RuntimeContext

@pytest.fixture
def agent():
    manifest_path = os.path.join(os.path.dirname(__file__), "../../../app/agents/manifests/files/soc_analyst.yaml")
    manifest = ManifestLoader.load_from_file(manifest_path)
    return SOCAnalystAgent(manifest)

@pytest.fixture
def mock_context():
    mock_llm = AsyncMock()
    mock_llm.generate.return_value = Mock(text=json.dumps({
        "summary": "Test Summary", 
        "severity": "HIGH", 
        "confidence": 0.9, 
        "analysis": "Test Analysis",
        "mitre_mapping": ["T1059"],
        "evidence": [],
        "investigation_steps": [],
        "containment_recommendations": [],
        "detection_recommendations": [],
        "references": [],
        "warnings": []
    }))
    
    mock_runtime = Mock()
    mock_runtime.llm_provider = mock_llm
    
    return AgentContext(
        execution=ExecutionContext(execution_id="e-1"),
        user=UserContext(user_id="u-1"),
        conversation=ConversationContext(session_id="s-1"),
        runtime=RuntimeContext()
    )

@pytest.mark.asyncio
async def test_soc_analyst_initialization(agent):
    assert agent.manifest.name == "SOC Analyst"
    assert "INVESTIGATION" in agent.manifest.capabilities

@pytest.mark.asyncio
async def test_soc_analyst_execution_success(agent, mock_context):
    mock_context.runtime.runtime_manager = Mock()
    mock_context.runtime.runtime_manager.llm_provider = AsyncMock()
    mock_context.runtime.runtime_manager.llm_provider.generate.return_value = Mock(text=json.dumps({
        "summary": "Test Summary", 
        "severity": "HIGH", 
        "confidence": 0.9, 
        "analysis": "Test Analysis",
        "mitre_mapping": ["T1059"],
        "evidence": [],
        "investigation_steps": [],
        "containment_recommendations": [],
        "detection_recommendations": [],
        "references": [],
        "warnings": []
    }))

    mock_context.knowledge.retrieved_documents = [{"alert": "test alert"}]
    
    result = await agent.execute(mock_context)
    
    assert result.success is True
    parsed_response = json.loads(result.response)
    assert parsed_response.get("severity") == "HIGH"

@pytest.mark.asyncio
async def test_soc_analyst_fallback_on_malformed_json(agent, mock_context):
    mock_context.runtime.runtime_manager = Mock()
    mock_context.runtime.runtime_manager.llm_provider = AsyncMock()
    mock_context.runtime.runtime_manager.llm_provider.generate.return_value = Mock(text="not json")
    
    result = await agent.execute(mock_context)
    
    assert result.success is True  # Agent completes successfully but response contains parsing fallbacks
    parsed_response = json.loads(result.response)
    assert parsed_response.get("severity") == "UNKNOWN"
    assert "Invalid JSON output" in parsed_response.get("warnings", [])
