from typing import Any
from abc import ABC, abstractmethod
from app.agents.models.orchestration_models import MultiAgentExecutionPlan
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult

class IAgentCoordinator(ABC):
    @abstractmethod
    async def coordinate(self, plan: MultiAgentExecutionPlan, context: ExecutionContext) -> ExecutionResult:
        """
        Coordinates the execution of a multi-agent plan, returning the final aggregated result.
        """
        pass
