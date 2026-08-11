from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.chat.intent.models.entities import EntityCollection
from app.chat.intent.models.intent_types import IntentType
from app.chat.intent.models.analysis_result import DetectedIntent
from app.chat.intent.pipeline.context import IntentPipelineContext

class IEntityExtractor(ABC):
    @abstractmethod
    async def extract(self, query: str, context: Dict[str, Any]) -> EntityCollection:
        pass

class IIntentClassifier(ABC):
    @abstractmethod
    async def classify(self, query: str, context: Dict[str, Any], entities: EntityCollection) -> List[DetectedIntent]:
        pass

class IConfidenceEvaluator(ABC):
    @abstractmethod
    async def evaluate(self, intents: List[DetectedIntent], query: str) -> List[DetectedIntent]:
        pass

class IIntentPolicy(ABC):
    @abstractmethod
    async def apply(self, context: IntentPipelineContext) -> IntentPipelineContext:
        pass

class IExecutionPlanner(ABC):
    @abstractmethod
    async def plan(self, context: IntentPipelineContext) -> IntentPipelineContext:
        pass

class IIntentService(ABC):
    from app.chat.intent.models.analysis_result import IntentAnalysisResult
    @abstractmethod
    async def analyze_intent(self, query: str, conversation_context: Dict[str, Any]) -> 'IntentAnalysisResult':
        pass
