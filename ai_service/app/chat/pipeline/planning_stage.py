from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.chat.engines.registry import ExecutionEngineRegistry
from app.planning.services.planning_service import PlanningService
from app.planning.resolvers.engine_resolver import CapabilityEngineResolver
import logging

logger = logging.getLogger("app.chat.pipeline.planning_stage")

class RoutePlanningStage(IExecutionStage):
    """Maps the analyzed intent to a specific Execution Engine.

    Routing Decision:
    - If a QueryRouter `decide` callable is injected, use it: it deterministically
      classifies the query into exactly one agent -> one engine. This is the
      Phase-X QueryRouter path (no LLM, no response generation in routing).
    - Otherwise fall back to the legacy route_recommendation / AGENT plan walk.
    """

    def __init__(self, registry: ExecutionEngineRegistry, decide=None):
        self._registry = registry
        self._planning_service = PlanningService()
        self._resolver = CapabilityEngineResolver()
        self._decide = decide

    @property
    def name(self) -> str:
        return "RoutePlanning"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        if "execution_result" in context.metadata:
            return context

        intent_analysis = context.metadata.get("intent_analysis")
        query = context.metadata.get("query", "")

        # 1. Phase-X: Query Router decision (deterministic, exactly one agent).
        if self._decide is not None:
            decision = self._decide(query, intent_analysis)
            engine_name = decision.engine
            logger.info(
                f"RoutePlanningStage: QueryRouter routed to agent={decision.agent_id} "
                f"engine={engine_name} domain={decision.domain.value} intent={decision.intent} "
                f"confidence={decision.domain_confidence:.2f}"
            )
            self._registry.get_engine_class(engine_name)
            new_metadata = {
                **context.metadata,
                "selected_engine": engine_name,
                "selected_agent": decision.agent_id,
                "routing_decision": decision,
                "intent": decision.intent,
                "domain": decision.domain.value,
            }
            return context.model_copy(update={"metadata": new_metadata})

        # 2. Ask Planning Layer for a formal Execution Plan (for the AgentExecutor fallback)
        planning_context = await self._planning_service.create_plan(
            intent_analysis,
            context.memory or {}
        )

        # 2. Determine which engine to use:
        #    - Prefer the route_recommendation from IntentIntelligenceService for direct routing.
        #    - Fall back to "AGENT" only for multi-step/hybrid plans.
        engine_name = "AGENT"  # default: use full agent DAG execution

        if intent_analysis and hasattr(intent_analysis, "route_recommendation") and intent_analysis.route_recommendation:
            recommended_engine = intent_analysis.route_recommendation.engine
            if recommended_engine and recommended_engine in [
                "GENERAL", "RAG", "TOOL", "PLATFORM", "NOTES", "SUMMARY",
                "THREAT_INTEL", "WAZUH_LAB", "PRACTICE_LAB",
                "INVESTIGATION", "INVESTIGATION_GUIDANCE", "WINDOWS_EVENT_LOG",
                "LINUX_LOG", "IOC_ANALYSIS", "MITRE_GUIDANCE", "DETECTION_RULE",
            ]:
                engine_name = recommended_engine
                logger.info(
                    f"RoutePlanningStage: Direct routing to {engine_name} "
                    f"(intent={intent_analysis.primary_intent.type.value if intent_analysis.primary_intent else 'unknown'}, "
                    f"confidence={intent_analysis.route_recommendation.confidence:.2f})"
                )
            else:
                logger.info(f"RoutePlanningStage: route_recommendation engine='{recommended_engine}' not recognized, falling back to AGENT")
        else:
            logger.info("RoutePlanningStage: No route_recommendation, falling back to AGENT")

        # 3. Validate the engine exists in registry
        self._registry.get_engine_class(engine_name)

        # 4. Propagate into context metadata
        new_metadata = {
            **context.metadata,
            "selected_engine": engine_name,
            "planning": planning_context
        }
        return context.model_copy(update={"metadata": new_metadata})

