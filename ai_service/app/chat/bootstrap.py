import logging
from app.chat.interfaces.i_chat_service import IChatService
from app.chat.service import ChatService
from app.chat.orchestrator import ChatOrchestrator
from app.chat.pipeline.memory_stage import MemoryLoadStage
from app.chat.pipeline.intent_stage import IntentAnalysisStage
from app.chat.pipeline.planning_stage import RoutePlanningStage
from app.chat.pipeline.execution_stage import EngineExecutionStage
from app.chat.pipeline.composition_stage import CompositionStage
from app.chat.pipeline.persistence_stage import PersistenceStage
from app.chat.pipeline.suggested_courses_stage import SuggestedCoursesStage
from app.chat.pipeline.cache_stage import CacheStage

from app.chat.pipeline.adaptive_stage import AdaptiveContextStage, AdaptivePersistenceStage
from app.chat.pipeline.page_context_stage import PageContextStage
from app.chat.pipeline.attachment_parse_stage import AttachmentParseStage
from app.chat.pipeline.guardrails_stage import InputGuardrailsStage, OutputGuardrailsStage
from app.chat.pipeline.persona_stage import PersonaLoadStage
from app.chat.pipeline.platform_context_stage import PlatformContextLoadStage
from app.multilingual.stage import LanguageContextStage
from app.multilingual.dependencies import get_language_detector, get_language_preference_store
from app.adaptive.store import SQLiteLearnerStore
from app.adaptive.engine import AdaptiveLearningEngine
from app.adaptive.session_memory import SessionMemoryManager
from app.adaptive.service import AdaptiveLearningService
from app.conversations.dependencies import get_conversation_service

from app.chat.engines.registry import ExecutionEngineRegistry, ExecutionEngineFactory
from app.chat.engines.general_engine import GeneralExecutionEngine
from app.chat.engines.rag_engine import RagExecutionEngine
from app.chat.engines.tool_engine import ToolExecutionEngine
from app.chat.engines.learning_engines import NotesGenerationEngine, TopicSummaryEngine
from app.chat.engines.specialist_engines import (
    ThreatIntelExecutionEngine,
    InvestigationExecutionEngine,
)
from app.chat.engines.soc_engines import (
    WazuhLabEngine,
    PracticeLabEngine,
    InvestigationGuidanceEngine,
    WindowsEventLogEngine,
    LinuxLogEngine,
    IocAnalysisEngine,
    MitreGuidanceEngine,
    DetectionRuleEngine,
)
from app.chat.policies.runtime_policy import RuntimePolicyProxy
from app.agents.executors.agent_executor import AgentExecutor
from app.planning.resolvers.engine_resolver import CapabilityEngineResolver
from app.agents.schedulers.sequential_scheduler import SequentialScheduler

from app.mcp.resolvers.tool_provider_resolver import ToolProviderResolver
from app.mcp.providers.legacy_provider import LegacyToolProvider
from app.mcp.provider_registry.provider_registry import ProviderRegistry
from app.mcp.catalog.tool_catalog import ToolCatalog

# LLM: Factory + Adapter bridging BaseLLMProvider -> ILLMService
from app.llm.factory import LLMFactory
from app.llm.adapter import LLMProviderAdapter

# Intent Intelligence Pipeline components
from app.chat.intent.intent_service import IntentIntelligenceService
from app.chat.intent.pipeline.orchestrator import IntentOrchestrator
from app.chat.intent.pipeline.stages.extraction_stage import EntityExtractionStage
from app.chat.intent.pipeline.stages.classification_stage import IntentClassificationStage
from app.chat.intent.pipeline.stages.confidence_stage import ConfidenceEvaluationStage
from app.chat.intent.pipeline.stages.policy_stage import PolicyEvaluationStage
from app.chat.intent.pipeline.stages.planning_stage import ExecutionPlanningStage
from app.chat.intent.classifiers.rule_classifier import RuleIntentClassifier
from app.chat.intent.extractors.regex_extractor import RegexEntityExtractor
from app.chat.intent.confidence.rule_evaluator import RuleConfidenceEvaluator
from app.chat.intent.policies.fallback_policy import FallbackPolicy
from app.chat.intent.policies.ambiguity_policy import AmbiguityPolicy
from app.chat.intent.planners.route_planner import RuleRoutePlanner

# Remaining dependencies
from app.prompt_builder.simple_prompt_builder import SimplePromptBuilder
from app.memory.dependencies import get_memory_service
from app.memory.default_manager import DefaultMemoryManager
from app.embeddings.dependencies import get_embedding_service
from app.vector_store.dependencies import get_vector_store_service
from app.retrieval.dependencies import get_reranker
from app.retrieval.service import RetrievalService
from app.tools.executors.local_executor import LocalToolExecutor
from app.cache.dependencies import get_cache_service
from app.core.config import settings

logger = logging.getLogger(__name__)


def _threat_intel_tools():
    """Instantiates the available (mock) external threat-intelligence tools.

    Best-effort: if the tool classes are unavailable, returns an empty list so
    the Threat Intel engine still falls back to the LLM's own knowledge.
    """
    tools = []
    try:
        from app.tools.implementations.cybersecurity.indicator_fetcher_tool import IndicatorFetcherTool
        tools.append(IndicatorFetcherTool())
    except Exception as e:
        logger.warning(f"IndicatorFetcherTool unavailable: {e}")
    try:
        from app.tools.implementations.cybersecurity.mitre_tool import MITRETool
        tools.append(MITRETool())
    except Exception as e:
        logger.warning(f"MITRETool unavailable: {e}")
    return tools


def _build_intent_service() -> IntentIntelligenceService:
    """
    Assembles the full Intent Intelligence pipeline.

    Pipeline:
      EntityExtractionStage -> IntentClassificationStage -> ConfidenceEvaluationStage
      -> PolicyEvaluationStage -> ExecutionPlanningStage
    """
    intent_pipeline_stages = [
        EntityExtractionStage(RegexEntityExtractor()),
        IntentClassificationStage(RuleIntentClassifier()),
        ConfidenceEvaluationStage(RuleConfidenceEvaluator()),
        PolicyEvaluationStage([FallbackPolicy(), AmbiguityPolicy()]),
        ExecutionPlanningStage(RuleRoutePlanner()),
    ]
    intent_orchestrator = IntentOrchestrator(intent_pipeline_stages)
    return IntentIntelligenceService(intent_orchestrator)


def get_chat_service() -> IChatService:
    """
    Composition root for the Chat Service.

    Request flow:
      ChatService -> ChatOrchestrator -> [CacheStage, MemoryLoadStage,
      IntentAnalysisStage, RoutePlanningStage, EngineExecutionStage,
      CompositionStage, PersistenceStage]

    Engine routing (via IntentAnalysisStage -> RoutePlanningStage):
      GENERAL_CHAT / GREETING -> GeneralExecutionEngine -> LLMProvider
      RAG_QUERY               -> RagExecutionEngine -> FAISSRetriever + LLMProvider
      TOOL_REQUEST            -> ToolExecutionEngine -> LocalToolExecutor
      * (any other)           -> AgentExecutor (walks the plan DAG)
    """
    logger.info("Initializing ChatService dependencies via composition root")

    # 1. LLM: wrap BaseLLMProvider as ILLMService.
    provider = LLMFactory.get_provider()
    llm = LLMProviderAdapter(provider)
    prompt_builder = SimplePromptBuilder()

    # 2. Pipeline infrastructure
    from app.observability.dependencies import get_observability_service
    obs_service = get_observability_service()

    # Guardrails service (input/output safety). Fully wired through
    # app.guardrails.dependencies; used by the pipeline stages below.
    from app.guardrails.dependencies import get_guardrails_service
    guardrails_service = get_guardrails_service(obs_service)

    # Cache Service manual resolution
    from app.cache.dependencies import get_cache_store
    from app.cache.default_manager import DefaultCacheManager
    cache_store = get_cache_store()
    cache_service = DefaultCacheManager(cache_store)

    # Memory Service manual resolution
    from app.memory.dependencies import get_memory_store
    memory_store = get_memory_store()
    memory_service = get_memory_service(store=memory_store, obs=obs_service)
    memory_manager = DefaultMemoryManager(memory_service)
    
    # Embedding Service manual resolution
    from app.embeddings.dependencies import get_embedding_provider
    embedding_provider = get_embedding_provider()
    embedding_service = get_embedding_service(provider=embedding_provider)

    # Vector Store Service manual resolution
    from app.vector_store.dependencies import get_vector_store, get_metadata_store
    vector_store_provider = get_vector_store()
    vector_meta_store = get_metadata_store()
    vector_store = get_vector_store_service(
        provider=vector_store_provider,
        metadata_store=vector_meta_store,
        embedding_provider=embedding_provider
    )

    # Retrieval Service manual resolution
    from app.retrieval.faiss_retriever import FAISSRetriever
    reranker = get_reranker()
    retrieval_service = RetrievalService(embedding_service, vector_store, reranker)
    retriever = FAISSRetriever(retrieval_service)
    
    intent_service = _build_intent_service()

    # 3. Tool Execution
    from app.tools.dependencies import get_tool_service
    from app.mcp.registry.mcp_registry import MCPRegistry
    
    tool_service = get_tool_service()
    tool_executor = LocalToolExecutor(tool_service)
    legacy_provider = LegacyToolProvider(tool_executor)
    
    mcp_registry = MCPRegistry()
    catalog = ToolCatalog(mcp_registry)
    
    provider_registry = ProviderRegistry()
    provider_registry.register(legacy_provider)
    tool_resolver = ToolProviderResolver(catalog=catalog, provider_registry=provider_registry)

    # 4. Engine Registry & Factory
    registry = ExecutionEngineRegistry()
    registry.register("GENERAL", GeneralExecutionEngine)
    registry.register("RAG", RagExecutionEngine)
    registry.register("TOOL", ToolExecutionEngine)
    registry.register("AGENT", AgentExecutor)
    registry.register("NOTES", NotesGenerationEngine)
    registry.register("SUMMARY", TopicSummaryEngine)
    registry.register("THREAT_INTEL", ThreatIntelExecutionEngine)
    registry.register("WAZUH_LAB", WazuhLabEngine)
    registry.register("PRACTICE_LAB", PracticeLabEngine)
    registry.register("INVESTIGATION", InvestigationExecutionEngine)
    registry.register("INVESTIGATION_GUIDANCE", InvestigationGuidanceEngine)
    registry.register("WINDOWS_EVENT_LOG", WindowsEventLogEngine)
    registry.register("LINUX_LOG", LinuxLogEngine)
    registry.register("IOC_ANALYSIS", IocAnalysisEngine)
    registry.register("MITRE_GUIDANCE", MitreGuidanceEngine)
    registry.register("DETECTION_RULE", DetectionRuleEngine)
    
    from app.chat.engines.platform_engine import PlatformExecutionEngine
    from app.platform.services.platform_client import platform_client
    from app.platform.repositories.django_repository import DjangoPlatformRepository
    from app.platform.context.user_context import UserContextBuilder
    from app.platform.services.recommendation_service import RecommendationService
    
    platform_repo = DjangoPlatformRepository(platform_client)
    user_context_builder = UserContextBuilder(platform_repo)
    recommendation_service = RecommendationService(platform_repo)
    
    registry.register("PLATFORM", PlatformExecutionEngine)

    class RealEngineFactory(ExecutionEngineFactory):
        def create_engine(self, name: str, **kwargs):
            if name == "GENERAL":
                engine = GeneralExecutionEngine(llm, prompt_builder)
            elif name == "RAG":
                engine = RagExecutionEngine(retriever, llm, prompt_builder, platform_repo=platform_repo)
            elif name == "AGENT":
                engine = AgentExecutor(self, CapabilityEngineResolver(), SequentialScheduler())
            elif name == "TOOL":
                engine = ToolExecutionEngine(tool_resolver)
            elif name == "PLATFORM":
                engine = PlatformExecutionEngine(platform_repo, user_context_builder, recommendation_service, retriever, llm, prompt_builder)
            elif name == "NOTES":
                engine = NotesGenerationEngine(retriever, llm, prompt_builder, platform_repo=platform_repo)
            elif name == "SUMMARY":
                engine = TopicSummaryEngine(retriever, llm, prompt_builder, platform_repo=platform_repo)
            elif name == "THREAT_INTEL":
                engine = ThreatIntelExecutionEngine(retriever, llm, prompt_builder, external_tools=_threat_intel_tools())
            elif name == "WAZUH_LAB":
                engine = WazuhLabEngine(retriever, llm, prompt_builder, platform_repo=platform_repo)
            elif name == "PRACTICE_LAB":
                engine = PracticeLabEngine(retriever, llm, prompt_builder, platform_repo=platform_repo)
            elif name == "INVESTIGATION":
                engine = InvestigationExecutionEngine(retriever, llm, prompt_builder)
            elif name == "INVESTIGATION_GUIDANCE":
                engine = InvestigationGuidanceEngine(retriever, llm, prompt_builder, platform_repo=platform_repo)
            elif name == "WINDOWS_EVENT_LOG":
                engine = WindowsEventLogEngine(retriever, llm, prompt_builder, platform_repo=platform_repo)
            elif name == "LINUX_LOG":
                engine = LinuxLogEngine(retriever, llm, prompt_builder, platform_repo=platform_repo)
            elif name == "IOC_ANALYSIS":
                engine = IocAnalysisEngine(retriever, llm, prompt_builder, platform_repo=platform_repo)
            elif name == "MITRE_GUIDANCE":
                engine = MitreGuidanceEngine(retriever, llm, prompt_builder, platform_repo=platform_repo)
            elif name == "DETECTION_RULE":
                engine = DetectionRuleEngine(retriever, llm, prompt_builder, platform_repo=platform_repo)
            else:
                raise ValueError(f"Unknown engine type: {name}")
            return RuntimePolicyProxy(engine)

    factory = RealEngineFactory(registry)

    # 5. Pipeline Stages (ordered)
    adaptive_store = SQLiteLearnerStore()
    adaptive_service = AdaptiveLearningService(
        engine=AdaptiveLearningEngine(adaptive_store),
        session_memory=SessionMemoryManager(adaptive_store),
        store=adaptive_store,
    )
    stages = [
        # Input guardrails FIRST: validate the raw user query (prompt-injection
        # heuristics, length cap) before any downstream stage processes it.
        InputGuardrailsStage(guardrails_service),
        # Sprint 7 (multilingual): resolve the response language FIRST so the
        # cache key and every downstream stage operate on the resolved code.
        LanguageContextStage(
            detector=get_language_detector(),
            store=get_language_preference_store(),
        ),
        CacheStage(cache_service),
        MemoryLoadStage(memory_manager),
        # Uploaded files/images are parsed here so their content is injected
        # into the query before routing/execution — the LLM can then analyze
        # the actual data instead of seeing only the user's text.
        AttachmentParseStage(),
        # Platform + persona (Sprint 5 wiring): load the user's live platform
        # context, then inject the BlueTeamers persona + learner level so every
        # engine inherits the mentor persona in its system prompt.
        PlatformContextLoadStage(user_context_builder),
        PersonaLoadStage(),
        PageContextStage(),
        AdaptiveContextStage(adaptive_service),
        IntentAnalysisStage(intent_service),
        RoutePlanningStage(registry),
        EngineExecutionStage(factory),
        CompositionStage(),
        # Output guardrails: validate the composed answer before it is returned
        # (length cap + leakage heuristics), short-circuiting to a graceful
        # refusal when a violation is flagged.
        OutputGuardrailsStage(guardrails_service),
        SuggestedCoursesStage(platform_repo),
        PersistenceStage(memory_manager, conversation_service=get_conversation_service()),
        AdaptivePersistenceStage(adaptive_service),
    ]

    orchestrator = ChatOrchestrator(stages)
    return ChatService(
        orchestrator,
        memory_manager=memory_manager,
        conversation_service=get_conversation_service(),
    )
