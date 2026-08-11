from typing import Dict, List, Optional
from pydantic import BaseModel
from app.services.capabilities.capability import Capability
from app.agents.base_interfaces import IAgentRegistry, IAgent

class ProviderRegistration(BaseModel):
    agent_name: str
    priority: int = 100

class CapabilityRegistry:
    """
    Registry for mapping capabilities to multiple agent providers with priority-based resolution.
    """
    def __init__(self, agent_registry: IAgentRegistry):
        self.agent_registry = agent_registry
        # capability -> list of ProviderRegistration sorted by priority
        self._capabilities: Dict[Capability, List[ProviderRegistration]] = {}
        
    def register_provider(self, capability: Capability, agent_name: str, priority: int = 100) -> None:
        if capability not in self._capabilities:
            self._capabilities[capability] = []
            
        # check if already registered
        existing = next((p for p in self._capabilities[capability] if p.agent_name == agent_name), None)
        if existing:
            existing.priority = priority
        else:
            self._capabilities[capability].append(ProviderRegistration(agent_name=agent_name, priority=priority))
            
        # Sort by priority ascending (lower number = higher priority)
        self._capabilities[capability].sort(key=lambda x: x.priority)
        
    def get_providers(self, capability: Capability) -> List[ProviderRegistration]:
        return self._capabilities.get(capability, [])
