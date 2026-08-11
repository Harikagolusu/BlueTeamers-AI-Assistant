from typing import List, Optional
from abc import ABC, abstractmethod
from app.agents.models.agent_descriptor import AgentDescriptor
from app.agents.models.capability import CapabilityModel

class IAgentRegistry(ABC):
    @abstractmethod
    def register(self, agent: AgentDescriptor) -> None:
        pass

    @abstractmethod
    def unregister(self, agent_id: str) -> None:
        pass

    @abstractmethod
    def get_agent(self, agent_id: str) -> Optional[AgentDescriptor]:
        pass

    @abstractmethod
    def list_agents(self) -> List[AgentDescriptor]:
        pass

    @abstractmethod
    def get_agents_by_capability(self, capability: str) -> List[AgentDescriptor]:
        pass
