import pytest
from unittest.mock import AsyncMock, AsyncMock
from app.chat.service import ChatService
from app.chat.orchestrator import ChatOrchestrator
from app.chat.pipeline.memory_stage import MemoryLoadStage
from app.chat.pipeline.intent_stage import IntentAnalysisStage
from app.chat.pipeline.planning_stage import RoutePlanningStage
from app.chat.pipeline.execution_stage import EngineExecutionStage
from app.chat.pipeline.composition_stage import CompositionStage
from app.chat.pipeline.persistence_stage import PersistenceStage
from app.chat.pipeline.cache_stage import CacheStage
from app.chat.engines.registry import ExecutionEngineRegistry, ExecutionEngineFactory
from app.chat.engines.general_engine import GeneralExecutionEngine
from app.chat.engines.rag_engine import RagExecutionEngine
from app.chat.engines.tool_engine import ToolExecutionEngine
from app.mcp.resolvers.tool_provider_resolver import ToolProviderResolver
from app.mcp.providers.legacy_provider import LegacyToolProvider
from app.chat.policies.runtime_policy import RuntimePolicyProxy
from app.chat.middleware.pipeline import ObservabilityMiddleware, GuardrailsMiddleware
from app.models.chat.chat_models import ChatRequest, ExecutionResult
from pydantic_core import ValidationError as PydanticValidationError
from app.chat.exceptions.chat_exceptions import ProviderFailure, TimeoutError, ValidationError

# Configuration to build the stress test pipeline
def build_stress_pipeline(
    mock_llm, mock_retriever, mock_tool_executor, mock_memory, mock_cache, mock_guardrails, mock_observability
):
    from unittest.mock import MagicMock
    mock_prompt_builder = MagicMock()
    mock_prompt_builder.build_prompt.return_value = ("Stress Prompt", "Stress System")

    registry = ExecutionEngineRegistry()
    registry.register("GENERAL", GeneralExecutionEngine)
    registry.register("RAG", RagExecutionEngine)
    registry.register("TOOL", ToolExecutionEngine)
    
    from app.agents.executors.agent_executor import AgentExecutor
    from app.planning.resolvers.engine_resolver import CapabilityEngineResolver
    
    registry.register("AGENT", AgentExecutor)

    class StressFactory(ExecutionEngineFactory):
        def create_engine(self, name: str, **kwargs):
            if name == "GENERAL":
                engine = GeneralExecutionEngine(mock_llm, mock_prompt_builder)
            elif name == "RAG":
                engine = RagExecutionEngine(mock_retriever, mock_llm, mock_prompt_builder)
            elif name == "AGENT":
                # AgentExecutor takes the factory and resolver
                from app.agents.schedulers.sequential_scheduler import SequentialScheduler
                engine = AgentExecutor(self, CapabilityEngineResolver(), SequentialScheduler())
            else:
                class MockCatalog:
                    def get_tool(self, name):
                        return type('MockReg', (), {'provider_id': 'legacy_provider_1'})()
                catalog = MockCatalog()
                legacy_provider = LegacyToolProvider(mock_tool_executor)
                resolver = ToolProviderResolver(catalog=catalog, provider_registry=type('MockProviderRegistry', (), {'resolve': lambda self, p_id: legacy_provider})())
                engine = ToolExecutionEngine(resolver)
            return RuntimePolicyProxy(engine)

    factory = StressFactory(registry)
    
    stages = [
        CacheStage(mock_cache),
        MemoryLoadStage(mock_memory),
        IntentAnalysisStage(AsyncMock()), # We replace this below anyway
        RoutePlanningStage(registry),
        EngineExecutionStage(factory),
        CompositionStage(),
        PersistenceStage(mock_memory)
    ]
    
    class TestCacheStage(CacheStage):
        async def initialize(self): pass
        async def shutdown(self): pass
        async def execute(self, context):
            context = context.model_copy(update={"session_user": "test_user"})
            return await super().execute(context)
            
    stages[0] = TestCacheStage(mock_cache)
    
    orchestrator = ChatOrchestrator(stages)
    service = ChatService(orchestrator)
    
    # We will simulate the middleware execution inside the tests since ChatService doesn't 
    # natively execute middleware (the API route typically does that).
    return service, orchestrator, stages


@pytest.fixture
def mocks():
    return {
        "llm": AsyncMock(),
        "retriever": AsyncMock(),
        "tool_executor": AsyncMock(),
        "memory": AsyncMock(),
        "cache": AsyncMock(),
        "guardrails": AsyncMock(),
        "observability": AsyncMock()
    }


@pytest.fixture
def stress_env(mocks):
    mocks["cache"].get.return_value = None
    mocks["guardrails"].validate.return_value = True
    mocks["memory"].load_history.return_value = {}
    
    # By default, intent stage returns GENERAL. We will inject a mock intent stage or just 
    # use the real one and pass `intent` if we can. Actually IntentAnalysisStage hardcodes "GENERAL".
    # Let's replace the real IntentAnalysisStage with one that uses metadata.get("intent_override")
    class ConfigurableIntentStage(IntentAnalysisStage):
        def __init__(self):
            super().__init__(AsyncMock())
            
        async def initialize(self): pass
        async def shutdown(self): pass
        async def execute(self, context):
            if "execution_result" in context.metadata:
                return context
            query = context.metadata.get("query", "")
            if "rag" in query.lower():
                intent_type = "RAG_CHAT"
                engine = "RAG"
            elif "tool" in query.lower():
                intent_type = "TOOL_CHAT"
                engine = "TOOL"
            else:
                intent_type = "GENERAL_CHAT"
                engine = "GENERAL"

            from app.chat.intent.models.analysis_result import IntentAnalysisResult, DetectedIntent
            from app.chat.intent.models.intent_types import IntentType
            from app.chat.intent.models.recommendations import RouteRecommendation
            from app.chat.intent.models.intent_types import ExecutionMode

            intent_analysis = IntentAnalysisResult(
                primary_intent=DetectedIntent(type=IntentType(intent_type), confidence=0.9, reason="stress override"),
                route_recommendation=RouteRecommendation(
                    engine=engine,
                    confidence=0.9,
                    reasoning="stress override",
                    execution_mode=ExecutionMode.SINGLE,
                ),
            )

            return context.model_copy(update={"metadata": {**context.metadata, "intent_analysis": intent_analysis}, "session_user": "user123"})
    service, orchestrator, stages = build_stress_pipeline(
        mocks["llm"], mocks["retriever"], mocks["tool_executor"], 
        mocks["memory"], mocks["cache"], mocks["guardrails"], mocks["observability"]
    )
    
    # Replace the intent stage
    stages[2] = ConfigurableIntentStage()
    
    return service, mocks

# --- TESTS ---

@pytest.mark.asyncio
async def test_general_chat_non_streaming(stress_env):
    service, mocks = stress_env
    mocks["llm"].generate.return_value = "General OK"
    
    request = ChatRequest(message="hello", stream=False, metadata={"intent_override": "GENERAL"})
    response = await service.process_request(request)
    
    assert "General OK" in response.message
    mocks["llm"].generate.assert_called_once()
    mocks["memory"].save_turn.assert_called_once()


@pytest.mark.asyncio
async def test_general_chat_streaming(stress_env):
    service, mocks = stress_env
    
    async def mock_stream(*args, **kwargs):
        yield "Stream "
        yield "OK"
        
    mocks["llm"].stream = mock_stream
    
    request = ChatRequest(message="hello general", stream=True)
    response_stream = await service.process_request(request)
    
    # Consume the generator
    chunks = [chunk async for chunk in response_stream]
    assert '"token": "Stream "' in chunks[0]
    assert '"token": "OK"' in chunks[1]
    assert "data: [DONE]" in chunks[-1]


@pytest.mark.asyncio
async def test_rag_chat_non_streaming(stress_env):
    service, mocks = stress_env
    mocks["llm"].generate.return_value = "RAG OK"
    from app.rag.interfaces import Document
    mocks["retriever"].search.return_value = [Document(content="doc", metadata={"source": "abc.pdf"})]
    
    request = ChatRequest(message="hello rag", stream=False)
    response = await service.process_request(request)
    
    assert "RAG OK" in response.message
    assert response.metadata["citations"] == [{
        "course": "course",
        "lesson": "lesson",
        "chunk_id": "doc",
        "similarity_score": 0.0,
        "source_title": "course - lesson",
        "source_reference": "abc.pdf",
    }]
    mocks["retriever"].search.assert_called_once()


@pytest.mark.asyncio
async def test_tool_chat_non_streaming(stress_env):
    service, mocks = stress_env
    mocks["tool_executor"].execute.return_value = {"result_message": "Tool OK"}
    
    request = ChatRequest(message="hello tool", stream=False)
    response = await service.process_request(request)
    
    assert "Tool OK" in response.message
    mocks["tool_executor"].execute.assert_called_once()


@pytest.mark.asyncio
async def test_cache_hit_bypasses_execution(stress_env):
    service, mocks = stress_env
    # Cache hit returns a valid ExecutionResult string?
    # Wait, CacheStage wraps the return value in an ExecutionResult
    # so cache.get() should return a string!
    mocks["cache"].get.return_value = "Cached Response"
    request = ChatRequest(message="hello", stream=False)
    response = await service.process_request(request)
    
    assert "Cached Response" in response.message
    
    # Engine logic was bypassed
    mocks["llm"].generate.assert_not_called()
    
    # Persistence was STILL called (proving downstream pipeline runs)
    mocks["memory"].save_turn.assert_called_once()


@pytest.mark.asyncio
async def test_guardrail_rejection(stress_env):
    service, mocks = stress_env
    mocks["guardrails"].validate.return_value = False
    
    middleware = GuardrailsMiddleware(mocks["guardrails"])
    
    # Simulated execution
    from app.chat.context.execution_context import ExecutionContext
    ctx = ExecutionContext(metadata={"query": "bad text"})
    
    with pytest.raises(ValidationError):
        await middleware.execute(ctx)


@pytest.mark.asyncio
async def test_retry_on_provider_failure(stress_env):
    service, mocks = stress_env
    
    # Fail 2 times, succeed on 3rd
    mocks["llm"].generate.side_effect = [ProviderFailure("Fail 1"), ProviderFailure("Fail 2"), "Retry OK"]
    
    request = ChatRequest(message="hello", stream=False, metadata={"intent_override": "GENERAL"})
    response = await service.process_request(request)
    
    assert "Retry OK" in response.message
    assert mocks["llm"].generate.call_count == 3


@pytest.mark.asyncio
async def test_timeout_triggers_retry_and_failure(stress_env):
    service, mocks = stress_env
    
    # Always timeout
    mocks["llm"].generate.side_effect = TimeoutError("Timeout")
    
    request = ChatRequest(message="hello", stream=False, metadata={"intent_override": "GENERAL"})
    
    from app.runtime.resilience.circuit_breaker import CircuitOpenException
    with pytest.raises((TimeoutError, CircuitOpenException)):
        await service.process_request(request)
    
    # Should have retried 3 times (tenacity default in our proxy)
    assert mocks["llm"].generate.call_count == 3


@pytest.mark.asyncio
async def test_cancellation(stress_env):
    service, mocks = stress_env
    
    # Create an orchestrator with a canceled context
    # We'll inject cancellation directly into the context before it reaches the pipeline
    from app.chat.context.execution_context import ExecutionContext
    import uuid
    ctx = ExecutionContext(
        trace_id=uuid.uuid4(),
        correlation_id=uuid.uuid4(),
        cancellation_requested=True
    )
    
    response = await service._orchestrator.execute_pipeline(ctx)
    
    # Result should be failed due to cancellation, and execution stages bypassed
    assert response.status == "FAILED"
    mocks["llm"].generate.assert_not_called()
