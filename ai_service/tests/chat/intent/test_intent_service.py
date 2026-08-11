import pytest
from app.chat.intent.extractors.regex_extractor import RegexEntityExtractor
from app.chat.intent.classifiers.rule_classifier import RuleIntentClassifier
from app.chat.intent.confidence.rule_evaluator import RuleConfidenceEvaluator
from app.chat.intent.policies.ambiguity_policy import AmbiguityPolicy
from app.chat.intent.policies.fallback_policy import FallbackPolicy
from app.chat.intent.planners.route_planner import RuleRoutePlanner
from app.chat.intent.pipeline.orchestrator import IntentOrchestrator
from app.chat.intent.pipeline.stages.extraction_stage import EntityExtractionStage
from app.chat.intent.pipeline.stages.classification_stage import IntentClassificationStage
from app.chat.intent.pipeline.stages.confidence_stage import ConfidenceEvaluationStage
from app.chat.intent.pipeline.stages.policy_stage import PolicyEvaluationStage
from app.chat.intent.pipeline.stages.planning_stage import ExecutionPlanningStage
from app.chat.intent.intent_service import IntentIntelligenceService
from app.chat.intent.models.intent_types import IntentType, ExecutionMode

def build_test_service():
    stages = [
        EntityExtractionStage(RegexEntityExtractor()),
        IntentClassificationStage(RuleIntentClassifier()),
        ConfidenceEvaluationStage(RuleConfidenceEvaluator()),
        PolicyEvaluationStage([AmbiguityPolicy(), FallbackPolicy()]),
        ExecutionPlanningStage(RuleRoutePlanner())
    ]
    orchestrator = IntentOrchestrator(stages)
    return IntentIntelligenceService(orchestrator)

@pytest.mark.asyncio
async def test_full_intent_pipeline_rag():
    service = build_test_service()
    
    # CVE queries now route to the dedicated Threat Intel engine (Sprint 2),
    # which supersedes the generic RAG bucket for security entities.
    res = await service.analyze_intent("explain CVE-2023-1234 to me", {})
    
    assert res.primary_intent.type == IntentType.THREAT_INTEL
    assert res.entities.has("CVE")
    assert res.route_recommendation.engine == "THREAT_INTEL"
    # THREAT_INTEL (0.93) is primary with a strong RAG secondary (0.9), so the
    # planner legitimately recommends hybrid execution on the THREAT_INTEL engine.
    assert res.route_recommendation.execution_mode == ExecutionMode.HYBRID

@pytest.mark.asyncio
async def test_full_intent_pipeline_ambiguous():
    service = build_test_service()
    
    res = await service.analyze_intent("run it", {})
    
    # Pronoun 'it' should trigger ambiguity policy
    assert res.clarification_request is not None
    assert res.route_recommendation.execution_mode == ExecutionMode.CLARIFICATION_REQUIRED
