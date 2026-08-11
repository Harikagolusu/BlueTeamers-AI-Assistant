from app.chat.intent.pipeline.i_intent_stage import IIntentPipelineStage
from app.chat.intent.pipeline.context import IntentPipelineContext
from app.chat.intent.interfaces import IEntityExtractor

class EntityExtractionStage(IIntentPipelineStage):
    def __init__(self, extractor: IEntityExtractor):
        self._extractor = extractor

    @property
    def name(self) -> str:
        return "EntityExtraction"

    async def execute(self, context: IntentPipelineContext) -> IntentPipelineContext:
        entities = await self._extractor.extract(context.query, context.conversation_context)
        return context.copy_with(entities=entities)
