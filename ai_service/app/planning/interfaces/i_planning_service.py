from abc import ABC, abstractmethod
from typing import Dict, Any
from app.planning.models.context import PlanningContext

class IPlanningService(ABC):
    @abstractmethod
    async def create_plan(self, intent_analysis: Any, conversation_context: Dict[str, Any]) -> PlanningContext:
        """
        Receives an IntentAnalysisResult (Any here to avoid circular dependencies),
        builds, validates, estimates, and returns a fully formed PlanningContext.
        """
        pass
