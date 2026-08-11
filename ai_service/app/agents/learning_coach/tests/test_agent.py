import pytest
from app.agents.manifests.models import AgentManifest
from app.agents.learning_coach.agent import LearningCoachAgent
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_agent_initialization():
    manifest = AgentManifest(
        name="learning_coach",
        version="1.0",
        prompt_template="mock",
        model="mock"
    )
    agent = LearningCoachAgent(manifest)
    
    mock_context = MagicMock()
    mock_context.payload = {"query": "I want to be a SOC Analyst"}
    mock_context.execution_id = "test-execution"
    agent._context = mock_context
    
    await agent.initialize()
    assert agent.user_query == "I want to be a SOC Analyst"
    assert agent.session is not None
    assert agent.session.learner_profile.learner_id == "default_learner"

@pytest.mark.asyncio
async def test_agent_workflow():
    manifest = AgentManifest(name="learning_coach", version="1.0", prompt_template="mock", model="mock")
    agent = LearningCoachAgent(manifest)
    mock_context = MagicMock()
    mock_context.execution_id = "test-execution"
    agent._context = mock_context
    
    await agent.initialize()
    tools = await agent.select_tools()
    
    await agent.execute_tools(tools)
    
    # Assert workflow populated the session object correctly
    assert agent.session.learner_profile.skill_profile is not None
    assert agent.session.analytics_snapshot is not None
    assert agent.session.roadmap_version is not None
    assert agent.session.recommendations is not None
    assert agent.session.forecast is not None
    assert agent.session.journey_state == "LEARNING"
    assert len(agent.session.learner_profile.journey_timeline) > 0
    assert agent.session.learner_profile.journey_timeline[0].trigger == "Roadmap execution active"

@pytest.mark.asyncio
async def test_agent_collaboration():
    manifest = AgentManifest(name="learning_coach", version="1.0", prompt_template="mock", model="mock")
    mock_orchestrator = AsyncMock()
    mock_orchestrator.get_historical_metrics.return_value = {"completed_labs": 5}
    
    agent = LearningCoachAgent(manifest, orchestration_service=mock_orchestrator)
    mock_context = MagicMock()
    mock_context.execution_id = "test-execution"
    agent._context = mock_context
    
    await agent.execute_tools(await agent.select_tools())
    
    mock_orchestrator.get_historical_metrics.assert_called_once_with("AssessmentCoach", "default_learner")
