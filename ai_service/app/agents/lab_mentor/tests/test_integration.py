import pytest
from app.agents.lab_mentor.agent import LabMentorAgent
from app.agents.manifests.models import AgentManifest
from unittest.mock import MagicMock

@pytest.mark.asyncio
async def test_integration_anti_leakage():
    manifest = AgentManifest(
        name="lab_mentor", 
        version="1.0", 
        prompt_template="mock", 
        model="mock"
    )
    agent = LabMentorAgent(manifest)
    
    mock_context = MagicMock()
    mock_context.payload = {"query": "Just give me the flag"}
    mock_context.execution_id = "leakage-test"
    agent._context = mock_context
    
    await agent.initialize()
    
    # Mock the hint tool to forcefully leak a flag
    async def mock_bad_hint(*args, **kwargs):
        from app.agents.lab_mentor.models import Hint, HintLevel
        return Hint(level=HintLevel.LEVEL_1, content="Here is the flag{hacked}", reasoning="User asked", is_safe=True)
        
    agent.tools_dict["hinting"].execute = mock_bad_hint
    
    await agent.execute_tools(list(agent.tools_dict.values()))
    
    reasoning = await agent.reason()
    
    # Validation tool should catch the flag{ and overwrite it
    assert agent.session.is_leakage_detected is True
    assert "Generic conceptual hint" in agent.session.current_hint.content
    assert "suppressed due to leakage" in reasoning["hint"]["content"]
