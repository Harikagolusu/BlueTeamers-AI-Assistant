import pytest
from app.agents.assessment_coach.agent import AssessmentCoachAgent
from app.agents.assessment_coach.models import AssessmentResponse
from unittest.mock import MagicMock, AsyncMock

class MockContext:
    payload = {"query": "evaluate me", "learner_id": "test_learner"}
    execution_id = "test_execution"

@pytest.mark.asyncio
async def test_agent_workflow():
    manifest = {"name": "AssessmentCoach"}
    orchestrator = MagicMock()
    orchestrator.get_historical_metrics = AsyncMock(return_value={"previous_assessments": 5})
    
    agent = AssessmentCoachAgent(manifest=manifest, orchestration_service=orchestrator)
    agent._context = MockContext()
    
    await agent.initialize()
    assert agent.session.context.request.learner_id == "test_learner"
    
    tools = await agent.select_tools()
    assert len(tools) == 10
    
    await agent.execute_tools(tools)
    
    reasoning = await agent.reason()
    assert isinstance(reasoning, AssessmentResponse)
    assert reasoning.result.overall_score == 8.5
