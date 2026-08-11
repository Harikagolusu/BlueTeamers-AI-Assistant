from app.chat.intent.interfaces import IExecutionPlanner
from app.chat.intent.pipeline.context import IntentPipelineContext
from app.chat.intent.models.recommendations import RouteRecommendation, ExecutionRecommendation
from app.chat.intent.models.intent_types import ExecutionMode, IntentType

class RuleRoutePlanner(IExecutionPlanner):
    async def plan(self, context: IntentPipelineContext) -> IntentPipelineContext:
        if context.clarification_request:
            # If clarification is required, execution is deferred
            return context.copy_with(
                route_recommendation=RouteRecommendation(
                    engine="GENERAL", # Route clarification prompts through general LLM
                    confidence=1.0,
                    reasoning="Clarification required by policy.",
                    execution_mode=ExecutionMode.CLARIFICATION_REQUIRED
                ),
                execution_recommendation=ExecutionRecommendation(
                    action="REQUEST_CLARIFICATION",
                    description=context.clarification_request.reason
                )
            )
            
        if not context.candidate_intents:
            # Fallback (handled by fallback policy, but planner maps it to route)
            return context.copy_with(
                route_recommendation=RouteRecommendation(
                    engine="GENERAL",
                    confidence=0.5,
                    reasoning="No intent detected, falling back.",
                    execution_mode=ExecutionMode.SINGLE
                )
            )
            
        primary = max(
            context.candidate_intents,
            key=lambda i: i.confidence,
        )
        
        # Map IntentType to Engine Name
        engine_map = {
            IntentType.GENERAL_CHAT: "GENERAL",
            IntentType.RAG_CHAT: "RAG",
            IntentType.NOTES_GENERATION: "NOTES",
            IntentType.TOPIC_SUMMARY: "SUMMARY",
            IntentType.THREAT_INTEL: "THREAT_INTEL",
            IntentType.TOOL_CHAT: "TOOL",
            IntentType.IMAGE_CHAT: "GENERAL",
            IntentType.DOCUMENT_CHAT: "INVESTIGATION",
            IntentType.LAB_ASSISTANT: "AGENT",
            IntentType.INVESTIGATION: "INVESTIGATION",
            IntentType.WAZUH_LAB: "WAZUH_LAB",
            IntentType.PRACTICE_LAB: "PRACTICE_LAB",
            IntentType.INVESTIGATION_GUIDANCE: "INVESTIGATION_GUIDANCE",
            IntentType.WINDOWS_EVENT_LOG: "WINDOWS_EVENT_LOG",
            IntentType.LINUX_LOG: "LINUX_LOG",
            IntentType.IOC_ANALYSIS: "IOC_ANALYSIS",
            IntentType.MITRE_GUIDANCE: "MITRE_GUIDANCE",
            IntentType.DETECTION_RULE: "DETECTION_RULE",
            IntentType.PLATFORM_COURSE: "PLATFORM",
            IntentType.PLATFORM_LAB: "PLATFORM",
            IntentType.PLATFORM_PROGRESS: "PLATFORM",
            IntentType.PLATFORM_BADGE: "PLATFORM",
            IntentType.PLATFORM_CERTIFICATE: "PLATFORM",
            IntentType.PLATFORM_LEARNING_PATH: "PLATFORM",
            IntentType.PLATFORM_ASSESSMENT: "PLATFORM",
            IntentType.PLATFORM_DASHBOARD: "PLATFORM",
            IntentType.PLATFORM_PROFILE: "PLATFORM",
            IntentType.GREETING: "GENERAL",
            IntentType.SMALL_TALK: "GENERAL",
            IntentType.FOLLOW_UP: "GENERAL",
            IntentType.OFF_TOPIC: "GENERAL",
            IntentType.SYSTEM_COMMAND: "TOOL",
            IntentType.UNKNOWN: "GENERAL"
        }
        
        target_engine = engine_map.get(primary.type, "GENERAL")
        
        # Check for multi-intent hybrid recommendation
        execution_mode = ExecutionMode.SINGLE
        action = "EXECUTE_SINGLE"
        desc = f"Execute using {target_engine} engine."
        
        if len(context.candidate_intents) > 1 and context.candidate_intents[1].confidence > 0.5:
            # We have a strong secondary intent -> Hybrid potential
            execution_mode = ExecutionMode.HYBRID
            action = "HYBRID_EXECUTION_PLANNED"
            desc = f"Primary: {primary.type.value}, Secondary: {context.candidate_intents[1].type.value}"
            
        return context.copy_with(
            route_recommendation=RouteRecommendation(
                engine=target_engine,
                confidence=primary.confidence,
                reasoning=primary.reason,
                execution_mode=execution_mode
            ),
            execution_recommendation=ExecutionRecommendation(
                action=action,
                description=desc
            )
        )
