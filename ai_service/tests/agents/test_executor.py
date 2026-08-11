import pytest
from unittest.mock import MagicMock, AsyncMock
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult
from app.planning.models.context import PlanningContext
from app.planning.models.plan import ExecutionPlan, ExecutionStep, Capability
from app.agents.executors.agent_executor import AgentExecutor
from app.planning.resolvers.engine_resolver import CapabilityEngineResolver

@pytest.mark.asyncio
async def test_agent_executor_walks_dag():
    step1 = ExecutionStep(name="A", required_capability=Capability.LLM)
    step2 = ExecutionStep(name="B", required_capability=Capability.RAG, dependencies=[step1.step_id])
    plan = ExecutionPlan(goal="Test", steps=[step1, step2])
    
    planning_ctx = PlanningContext(plan=plan)
    ctx = ExecutionContext(metadata={"planning": planning_ctx})
    
    # Mock Factory
    factory = MagicMock()
    mock_llm_engine = AsyncMock()
    mock_llm_engine.execute.return_value = ExecutionResult.success(engine="GENERAL", message="LLM Done")
    
    mock_rag_engine = AsyncMock()
    mock_rag_engine.execute.return_value = ExecutionResult.success(engine="RAG", message="RAG Done")
    
    def side_effect(name):
        if name == "GENERAL": return mock_llm_engine
        if name == "RAG": return mock_rag_engine
        
    factory.create_engine.side_effect = side_effect
    
    from app.agents.schedulers.sequential_scheduler import SequentialScheduler
    executor = AgentExecutor(engine_factory=factory, resolver=CapabilityEngineResolver(), scheduler=SequentialScheduler())
    
    result = await executor.execute(ctx)
    
    assert result.status == "SUCCESS"
    
    # Verify both engines were called in sequence
    mock_llm_engine.execute.assert_called_once()
    mock_rag_engine.execute.assert_called_once()
