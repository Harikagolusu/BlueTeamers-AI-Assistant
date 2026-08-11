import pytest
from app.chat.context.execution_context import ExecutionContext
from app.agents.executors.agent_executor import AgentExecutor
from app.chat.engines.registry import ExecutionEngineFactory, ExecutionEngineRegistry
from app.chat.engines.general_engine import GeneralExecutionEngine
from app.chat.engines.rag_engine import RagExecutionEngine
from app.chat.engines.tool_engine import ToolExecutionEngine
from app.planning.resolvers.engine_resolver import CapabilityEngineResolver
from app.agents.schedulers.sequential_scheduler import SequentialScheduler
from app.planning.services.planning_service import PlanningService
from app.chat.intent.models.analysis_result import IntentAnalysisResult, DetectedIntent
from app.chat.intent.models.intent_types import IntentType, ExecutionMode
from app.chat.intent.models.recommendations import RouteRecommendation
from app.chat.intent.models.entities import EntityCollection
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_multi_agent_collaboration():
    # 1. Setup mock engines
    mock_llm = AsyncMock()
    mock_llm.generate.return_value = "Mocked LLM Response"
    mock_retriever = AsyncMock()
    mock_prompt = AsyncMock()
    mock_tool = AsyncMock()
    
    registry = ExecutionEngineRegistry()
    registry.register("GENERAL", GeneralExecutionEngine)
    registry.register("RAG", RagExecutionEngine)
    registry.register("TOOL", ToolExecutionEngine)
    
    class TestFactory(ExecutionEngineFactory):
        def create_engine(self, name: str, **kwargs):
            if name == "GENERAL":
                engine = GeneralExecutionEngine(mock_llm, mock_prompt)
            elif name == "RAG":
                engine = RagExecutionEngine(mock_retriever, mock_llm, mock_prompt)
            elif name == "TOOL":
                engine = ToolExecutionEngine(mock_tool)
            else:
                raise ValueError(f"Unknown engine: {name}")
            
            # mock the execute method to avoid actually calling LLMs
            engine.execute = AsyncMock()
            from app.models.chat.chat_models import ExecutionResult
            engine.execute.return_value = ExecutionResult.success(name, f"Response from {name}")
            return engine

    factory = TestFactory(registry)
    resolver = CapabilityEngineResolver()
    scheduler = SequentialScheduler()
    
    executor = AgentExecutor(factory, resolver, scheduler)
    
    # 2. Create Planning Context using MultiAgentPlanner (triggered by INVESTIGATION)
    intent_analysis = IntentAnalysisResult(
        primary_intent=DetectedIntent(type=IntentType.INVESTIGATION, confidence=0.9, reason="", matched_features=[]),
        candidate_intents=[],
        entities=EntityCollection(),
        route_recommendation=RouteRecommendation(engine="AGENT", confidence=0.9, reasoning="Investigation", execution_mode=ExecutionMode.HYBRID),
        clarification_request=None,
        secondary_intents=[]
    )
    
    planning_service = PlanningService()
    planning_context = await planning_service.create_plan(intent_analysis, {})
    
    # Verify the plan has 4 steps
    assert len(planning_context.plan.steps) == 4
    
    # 3. Create Execution Context
    context = ExecutionContext()
    context = context.model_copy(update={"metadata": {"planning": planning_context}})
    
    # 4. Execute the DAG
    result = await executor.execute(context)
    
    # 5. Verify the result
    assert result.success
    # The final message should come from the last step (GENERAL engine response)
    assert result.message == "Response from GENERAL"
