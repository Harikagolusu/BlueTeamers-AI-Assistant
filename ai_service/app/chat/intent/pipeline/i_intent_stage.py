from abc import ABC, abstractmethod
from app.chat.intent.pipeline.context import IntentPipelineContext

class IIntentPipelineStage(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def execute(self, context: IntentPipelineContext) -> IntentPipelineContext:
        """Executes the pipeline stage and returns an updated context."""
        pass
