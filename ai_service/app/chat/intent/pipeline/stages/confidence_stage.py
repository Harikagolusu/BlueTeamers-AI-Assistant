from app.chat.intent.pipeline.i_intent_stage import IIntentPipelineStage
from app.chat.intent.pipeline.context import IntentPipelineContext
from app.chat.intent.interfaces import IConfidenceEvaluator
import logging

logger = logging.getLogger("app.chat.intent.confidence")

class ConfidenceEvaluationStage(IIntentPipelineStage):
    def __init__(self, evaluator: IConfidenceEvaluator):
        self._evaluator = evaluator

    @property
    def name(self) -> str:
        return "ConfidenceEvaluation"

    async def execute(self, context: IntentPipelineContext) -> IntentPipelineContext:
        if not context.candidate_intents:
            return context
            
        evaluated_intents = await self._evaluator.evaluate(
            intents=context.candidate_intents,
            query=context.query
        )
        
        # Sort by confidence descending
        evaluated_intents.sort(key=lambda i: i.confidence, reverse=True)

        if evaluated_intents:
            top = evaluated_intents[0]
            logger.info(
                f"Intent decision query={context.query!r} -> {top.type.value} "
                f"(confidence={top.confidence:.2f}, features={top.matched_features})"
            )

        return context.copy_with(candidate_intents=evaluated_intents)
