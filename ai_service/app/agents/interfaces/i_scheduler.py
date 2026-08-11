from abc import ABC, abstractmethod
from typing import Optional
from app.planning.models.plan import ExecutionPlan, ExecutionStep
from app.agents.models.cursor import ExecutionCursor

class IScheduler(ABC):
    """Defines how the next step in an ExecutionPlan is resolved."""

    @abstractmethod
    def get_next_step(self, plan: ExecutionPlan, cursor: ExecutionCursor) -> Optional[ExecutionStep]:
        """
        Returns the next ExecutionStep ready to be executed, or None if:
        - No steps are ready.
        - The agent is currently blocked waiting for dependencies.
        - The execution is completed.
        """
        pass
