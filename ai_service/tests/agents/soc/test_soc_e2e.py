import pytest
import os
import json
from unittest.mock import Mock, AsyncMock
from app.agents.soc_analyst import SOCAnalystAgent
from app.agents.manifests.loader import ManifestLoader
from app.agents.context import AgentContext, ExecutionContext, UserContext, ConversationContext, RuntimeContext

@pytest.fixture
def e2e_agent():
    manifest_path = os.path.join(os.path.dirname(__file__), "../../../app/agents/manifests/files/soc_analyst.yaml")
    manifest = ManifestLoader.load_from_file(manifest_path)
    return SOCAnalystAgent(manifest)

@pytest.fixture
def mock_runtime_context():
    mock_llm = AsyncMock()
    mock_llm.generate.return_value = Mock(text=json.dumps({
        "summary": "Event ID 4625 indicates a Failed Logon attempt.", 
        "severity": "LOW", 
        "confidence": 1.0, 
        "analysis": "This is a standard Windows Event log.",
        "mitre_mapping": [],
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
async def test_scenario_1_event_4625(e2e_agent, mock_runtime_context):
    """
    Scenario 1: User asks 'What is Event ID 4625?'
    """
    mock_runtime_context.runtime.runtime_manager = Mock()
    mock_runtime_context.runtime.runtime_manager.llm_provider = mock_runtime_context.runtime.llm_provider if hasattr(mock_runtime_context.runtime, 'llm_provider') else AsyncMock()
    
    # Setup mock response
    mock_runtime_context.runtime.runtime_manager.llm_provider.generate.return_value = Mock(text=json.dumps({
        "summary": "Event ID 4625 indicates a Failed Logon attempt.", 
        "severity": "LOW", 
        "confidence": 1.0, 
        "analysis": "Standard Windows Event log.",
        "mitre_mapping": [],
        "evidence": [],
        "investigation_steps": [],
        "containment_recommendations": [],
        "detection_recommendations": [],
        "references": [],
        "warnings": []
    }))

    mock_runtime_context.knowledge.retrieved_documents = [{"alert": "What is Event ID 4625?"}]
    result = await e2e_agent.execute(mock_runtime_context)
    
    assert result.success is True
    parsed_response = json.loads(result.response)
    assert "Failed Logon" in parsed_response.get("summary", "")
