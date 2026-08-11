from abc import ABC, abstractmethod
from typing import List
from app.agents.context import AgentContext
from app.agents.models.agent_models import AgentResult

class IAgent(ABC):
    """
    Contract for all agents. 
    Defines the entry point for agent execution.
    """
    @abstractmethod
    async def execute(self, context: AgentContext) -> AgentResult:
        pass

class IAgentRegistry(ABC):
    """
    Contract for discovering and instantiating agents.
    """
    @abstractmethod
    def register(self, name: str, agent: IAgent) -> None:
        pass

    @abstractmethod
    def get(self, name: str) -> IAgent:
        pass

    @abstractmethod
    def discover(self) -> List[IAgent]:
        pass

    @abstractmethod
    def list(self) -> List[str]:
        pass

    @abstractmethod
    def filter(self, capabilities: List[str]) -> List[IAgent]:
        pass

    @abstractmethod
    def unregister(self, name: str) -> None:
        pass

    @abstractmethod
    def reload(self) -> None:
        pass
