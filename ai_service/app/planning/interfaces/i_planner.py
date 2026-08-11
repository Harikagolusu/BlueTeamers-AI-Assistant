from abc import ABC, abstractmethod
from typing import Dict, Any
from app.planning.models.plan import ExecutionPlan

class IExecutionPlanner(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @abstractmethod
    async def build_plan(self, intent_analysis: Any, conversation_context: Dict[str, Any]) -> ExecutionPlan:
        pass
