import pytest
from app.agents.knowledge_assistant.agent import KnowledgeAssistantAgent
from app.agents.manifests.models import AgentManifest
from unittest.mock import MagicMock, AsyncMock
from app.agents.context import AgentContext

@pytest.mark.asyncio
async def test_integration_ambiguous_query():
    manifest = AgentManifest(name="knowledge_assistant", version="1.0", prompt_template="mock", model="mock")
    agent = KnowledgeAssistantAgent(manifest)
    
    mock_context = MagicMock()
    mock_context.payload = {"query": "security", "learner_profile": {"experience_level": "ELI5"}}
    mock_context.execution_id = "ambiguous-test"
    
    agent._context = mock_context
    await agent.initialize()
    await agent.retrieve()
    await agent.execute_tools(list(agent.tools_dict.values()))
    response = await agent.reason()
    
    # Even with ambiguous query, agent should produce a valid ELI5 response structure
    assert "ELI5" in response.summary
    assert response.knowledge_check is not None

@pytest.mark.asyncio
async def test_integration_missing_knowledge():
    manifest = AgentManifest(name="knowledge_assistant", version="1.0", prompt_template="mock", model="mock")
    agent = KnowledgeAssistantAgent(manifest)
    
    mock_context = MagicMock()
    mock_context.payload = {"query": "NonExistentConcept", "learner_profile": {"experience_level": "Intermediate"}}
    mock_context.execution_id = "missing-test"
    
    agent._context = mock_context
    await agent.initialize()
    
    # Mock retrieval to return empty
    agent.tools_dict["knowledge_retrieval"].execute = AsyncMock(return_value=[])
    
    await agent.retrieve()
    await agent.execute_tools(list(agent.tools_dict.values()))
    response = await agent.reason()
    
    # Graceful degradation logic should handle it
    assert response.summary != ""
