from abc import ABC, abstractmethod
from app.chat.interfaces.i_execution_engine import IExecutionEngine
from app.agents.models.agent_descriptor import AgentDescriptor

class IAgentExecutorFactory(ABC):
    @abstractmethod
    def create_executor(self, agent: AgentDescriptor) -> IExecutionEngine:
        """
        Instantiates an execution engine configured for the specific agent.
        """
        pass
