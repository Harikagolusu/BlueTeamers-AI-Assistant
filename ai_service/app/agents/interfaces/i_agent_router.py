from typing import Optional
from abc import ABC, abstractmethod
from app.planning.models.plan import ExecutionStep
from app.agents.models.agent_descriptor import AgentDescriptor

class IAgentRouter(ABC):
    @abstractmethod
    def route_step(self, step: ExecutionStep) -> Optional[AgentDescriptor]:
        """
        Matches an execution step to the best capable agent using discovery and ranking.
        """
        pass
