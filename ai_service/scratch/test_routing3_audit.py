import asyncio, sys
sys.path.insert(0, "/home/harika/BlueTeamers-AI-Assistant/ai_service")
from app.chat.bootstrap import _build_intent_service

queries = ["sigma rule example", "show me a detection rule", "SIEM vs SOC"]
async def main():
    svc = _build_intent_service()
    for q in queries:
        res = await svc.analyze_intent(q, {})
        print(f"QUERY: {q!r}")
        for c in res.candidate_intents if hasattr(res, 'candidate_intents') else []:
            pass
        # dump via pipeline directly
        from app.chat.intent.pipeline.context import IntentPipelineContext
        # easier: re-run orchestrator manually
    # manual: use orchestrator
    from app.chat.intent.pipeline.orchestrator import IntentOrchestrator
    from app.chat.intent.pipeline.context import IntentPipelineContext
    import app.chat.bootstrap as b
    # rebuild stages like bootstrap
    from app.chat.intent.extractors.regex_extractor import RegexEntityExtractor
    from app.chat.intent.classifiers.rule_classifier import RuleIntentClassifier
    from app.chat.intent.confidence.rule_evaluator import RuleConfidenceEvaluator
    from app.chat.intent.policies.fallback_policy import FallbackPolicy
    from app.chat.intent.policies.ambiguity_policy import AmbiguityPolicy
    from app.chat.intent.planners.route_planner import RuleRoutePlanner
    from app.chat.intent.pipeline.stages.extraction_stage import EntityExtractionStage
    from app.chat.intent.pipeline.stages.classification_stage import IntentClassificationStage
    from app.chat.intent.pipeline.stages.confidence_stage import ConfidenceEvaluationStage
    from app.chat.intent.pipeline.stages.policy_stage import PolicyEvaluationStage
    from app.chat.intent.pipeline.stages.planning_stage import ExecutionPlanningStage
    stages = [EntityExtractionStage(RegexEntityExtractor()), IntentClassificationStage(RuleIntentClassifier()), ConfidenceEvaluationStage(RuleConfidenceEvaluator()), PolicyEvaluationStage([FallbackPolicy(), AmbiguityPolicy()]), ExecutionPlanningStage(RuleRoutePlanner())]
    orch = IntentOrchestrator(stages)
    for q in queries:
        ctx = await orch.execute_pipeline(IntentPipelineContext(query=q, conversation_context={}))
        print(f"\nQUERY: {q!r}")
        for c in ctx.candidate_intents:
            print(f"   {c.type.value:<22} conf={c.confidence:.2f} feats={c.matched_features}")
asyncio.run(main())
