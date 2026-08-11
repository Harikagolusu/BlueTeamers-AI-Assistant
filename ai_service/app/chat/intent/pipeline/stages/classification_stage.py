from app.chat.intent.pipeline.i_intent_stage import IIntentPipelineStage
from app.chat.intent.pipeline.context import IntentPipelineContext
from app.chat.intent.interfaces import IIntentClassifier
import logging

logger = logging.getLogger("app.chat.intent.classification")

class IntentClassificationStage(IIntentPipelineStage):
    def __init__(self, classifier: IIntentClassifier):
        self._classifier = classifier

    @property
    def name(self) -> str:
        return "IntentClassification"

    async def execute(self, context: IntentPipelineContext) -> IntentPipelineContext:
        # Classifier returns baseline DetectedIntents (confidence might be naive or 0 at this stage)
        candidate_intents = await self._classifier.classify(
            query=context.query,
            context=context.conversation_context,
            entities=context.entities
        )
        logger.debug(
            f"Classified query={context.query!r} -> "
            f"{[i.type.value for i in candidate_intents]}"
        )
        return context.copy_with(candidate_intents=candidate_intents)
