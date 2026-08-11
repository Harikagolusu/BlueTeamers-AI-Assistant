from typing import Protocol, List, Optional
from pydantic import BaseModel

class AgentHealth(BaseModel):
    agent_id: str
    availability: bool
    health_score: float
    latency: float
    success_rate: float
    failure_rate: float
    active_workflows: int
    last_heartbeat: str

class AgentHealthRepository(Protocol):
    def save(self, health: AgentHealth) -> None:
        ...
    def get(self, agent_id: str) -> Optional[AgentHealth]:
        ...
    def list(self) -> List[AgentHealth]:
        ...

class InMemoryAgentHealthRepository:
    def __init__(self):
        self._store = {}
        
    def save(self, health: AgentHealth) -> None:
        self._store[health.agent_id] = health
        
    def get(self, agent_id: str) -> Optional[AgentHealth]:
        return self._store.get(agent_id)
        
    def list(self) -> List[AgentHealth]:
        return list(self._store.values())
