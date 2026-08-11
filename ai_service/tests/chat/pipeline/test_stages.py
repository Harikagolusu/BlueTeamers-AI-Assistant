import pytest
from app.chat.context.execution_context import ExecutionContext
from app.chat.pipeline.intent_stage import IntentAnalysisStage
from app.chat.pipeline.planning_stage import RoutePlanningStage
from app.chat.pipeline.execution_stage import EngineExecutionStage
from app.chat.engines.registry import ExecutionEngineRegistry, ExecutionEngineFactory
from app.chat.engines.general_engine import GeneralExecutionEngine
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_intent_stage():
    from app.chat.intent.intent_service import IntentIntelligenceService
    from app.chat.intent.models.analysis_result import IntentAnalysisResult, DetectedIntent
    from app.chat.intent.models.intent_types import IntentType
    from app.chat.intent.models.recommendations import RouteRecommendation, ExecutionMode
    
    mock_service = AsyncMock(spec=IntentIntelligenceService)
    mock_service.analyze_intent.return_value = IntentAnalysisResult(
        primary_intent=DetectedIntent(type=IntentType.GENERAL_CHAT, confidence=0.9, reason="test"),
        route_recommendation=RouteRecommendation(engine="GENERAL", confidence=0.9, reasoning="test", execution_mode=ExecutionMode.SINGLE)
    )
    
    stage = IntentAnalysisStage(mock_service)
    context = ExecutionContext()
    
    new_context = await stage.execute(context)
    assert new_context.metadata["intent"] == "GENERAL_CHAT"
    assert "intent_analysis" in new_context.metadata
    
    # Bypassed
    bypassed_context = ExecutionContext(metadata={"execution_result": "mock"})
    assert await stage.execute(bypassed_context) == bypassed_context

@pytest.mark.asyncio
async def test_planning_stage():
    from app.chat.intent.models.analysis_result import IntentAnalysisResult, DetectedIntent
    from app.chat.intent.models.intent_types import IntentType
    registry = ExecutionEngineRegistry()
    registry.register("GENERAL", GeneralExecutionEngine)
    registry.register("AGENT", GeneralExecutionEngine)
    stage = RoutePlanningStage(registry)
    
    intent_analysis = IntentAnalysisResult(
        primary_intent=DetectedIntent(type=IntentType.GENERAL_CHAT, confidence=0.9, reason="test"),
        route_recommendation=None
    )
    ctx = ExecutionContext(metadata={"intent": "GENERAL", "intent_analysis": intent_analysis})
    new_ctx = await stage.execute(ctx)
    
    assert "planning" in new_ctx.metadata


@pytest.mark.asyncio
@pytest.mark.parametrize("engine_name", [
    "WAZUH_LAB",
    "PRACTICE_LAB",
    "INVESTIGATION_GUIDANCE",
    "WINDOWS_EVENT_LOG",
    "LINUX_LOG",
    "IOC_ANALYSIS",
    "MITRE_GUIDANCE",
    "DETECTION_RULE",
])
async def test_planning_stage_routes_sprint3_engines_directly(engine_name):
    """Sprint 3 engines must route directly (not fall back to AGENT), matching
    the whitelist in RoutePlanningStage. This guards against the 'Internal
    server error' seen when a specialist intent fell back to the AGENT/tool path."""
    from app.chat.intent.models.analysis_result import IntentAnalysisResult, DetectedIntent
    from app.chat.intent.models.intent_types import IntentType
    from app.chat.intent.models.recommendations import RouteRecommendation, ExecutionMode

    registry = ExecutionEngineRegistry()
    registry.register("AGENT", GeneralExecutionEngine)
    registry.register(engine_name, GeneralExecutionEngine)
    stage = RoutePlanningStage(registry)

    intent_analysis = IntentAnalysisResult(
        primary_intent=DetectedIntent(type=IntentType.RAG_CHAT, confidence=0.9, reason="test"),
        route_recommendation=RouteRecommendation(
            engine=engine_name, confidence=0.95, reasoning="sprint3", execution_mode=ExecutionMode.SINGLE
        ),
    )
    ctx = ExecutionContext(
        metadata={"intent": engine_name, "intent_analysis": intent_analysis}
    )
    new_ctx = await stage.execute(ctx)

    assert new_ctx.metadata["selected_engine"] == engine_name

@pytest.mark.asyncio
async def test_execution_stage():
    registry = ExecutionEngineRegistry()
    registry.register("GENERAL", GeneralExecutionEngine)
    
    mock_llm = AsyncMock()
    mock_llm.generate.return_value = "hello world"
    mock_prompt_builder = MagicMock()
    mock_prompt_builder.build_prompt.return_value = ("hello", "hello system")

    class StubFactory(ExecutionEngineFactory):
        def create_engine(self, name: str, **kwargs):
            return GeneralExecutionEngine(mock_llm, mock_prompt_builder)

    factory = StubFactory(registry)
    stage = EngineExecutionStage(factory)
    
    ctx = ExecutionContext(metadata={"selected_engine": "GENERAL", "query": "hello"})
    new_ctx = await stage.execute(ctx)
    
    result = new_ctx.metadata.get("execution_result")
    assert result is not None
    assert result.engine_name == "GENERAL"
    assert "hello" in result.message
