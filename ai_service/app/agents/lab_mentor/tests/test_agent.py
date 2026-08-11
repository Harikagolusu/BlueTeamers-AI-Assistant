import pytest
from app.agents.lab_mentor.agent import LabMentorAgent
from app.agents.manifests.models import AgentManifest
from app.services.lab.models import LabState
from unittest.mock import MagicMock

@pytest.mark.asyncio
async def test_agent_lifecycle():
    manifest = AgentManifest(
        name="lab_mentor", 
        version="1.0", 
        prompt_template="mock", 
        model="mock"
    )
    agent = LabMentorAgent(manifest)
    
    mock_context = MagicMock()
    mock_context.payload = {"query": "I am stuck, give me a hint"}
    mock_context.conversation.session_id = "test-session"
    mock_context.execution_id = "test-execution"
    agent._context = mock_context
    
    await agent.initialize()
    agent.session.current_state = LabState.IN_PROGRESS
    assert agent.user_query == "I am stuck, give me a hint"
    
    tools = await agent.select_tools()
    assert len(tools) == 7

    await agent.execute_tools(tools)
    
    reasoning = await agent.reason()
    assert reasoning["state"] == "AWAITING_HINT"
    assert reasoning["hint"] is not None
    assert reasoning["feedback"] is not None
    assert reasoning["reflection"] is not None
    
    await agent.update_memory("Mock final response")
    assert agent.session.attempt_history.reflections_completed == 1
