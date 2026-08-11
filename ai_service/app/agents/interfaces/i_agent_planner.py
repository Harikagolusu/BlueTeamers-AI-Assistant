from abc import ABC, abstractmethod
from app.planning.models.plan import ExecutionPlan
from app.agents.models.orchestration_models import MultiAgentExecutionPlan

class IAgentPlanner(ABC):
    @abstractmethod
    def create_multi_agent_plan(self, plan: ExecutionPlan) -> MultiAgentExecutionPlan:
        """
        Transforms a standard ExecutionPlan into a MultiAgentExecutionPlan, preserving the original.
        """
        pass
