import pytest
from app.agents.knowledge_assistant.agent import KnowledgeAssistantAgent
from app.agents.manifests.models import AgentManifest
from app.agents.context import AgentContext
from unittest.mock import MagicMock

@pytest.mark.asyncio
async def test_agent_lifecycle():
    manifest = AgentManifest(name="knowledge_assistant", version="1.0", prompt_template="mock", model="mock")
    agent = KnowledgeAssistantAgent(manifest)
    
    mock_context = MagicMock()
    mock_context.payload = {"query": "Explain MITRE ATT&CK", "learner_profile": {"experience_level": "Beginner"}}
    mock_context.conversation.session_id = "test-session"
    mock_context.execution_id = "test-execution"
    agent._context = mock_context
    
    # Simulate BaseAgent execute flow
    await agent.initialize()
    assert agent.ka_context.profile.experience_level == "Beginner"
    assert agent.ka_context.raw_request.query == "Explain MITRE ATT&CK"
    
    await agent.retrieve()
    assert len(agent.ka_context.retrieved_knowledge) > 0
    
    tools = await agent.select_tools()
    assert len(tools) == 6
    
    # Assuming WorkflowEngine executes the tools and populates context
    await agent.execute_tools(tools)
    assert agent.ka_context.explanation is not None
    assert agent.ka_context.concept_map is not None
    assert agent.ka_context.knowledge_check is not None
    assert agent.ka_context.learning_path is not None
    
    response = await agent.reason()
    assert response.summary != ""
    assert len(response.knowledge_check.options) == 4
    
    await agent.update_memory("")
    assert agent.ka_context.metrics.questions_asked == 1
