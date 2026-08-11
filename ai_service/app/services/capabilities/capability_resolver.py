from typing import Optional, List
from app.services.capabilities.capability import Capability
from app.services.capabilities.capability_registry import CapabilityRegistry
from app.agents.base_interfaces import IAgent

class CapabilityResolver:
    """
    Resolves a capability to the highest priority available agent instance.
    """
    def __init__(self, capability_registry: CapabilityRegistry):
        self.registry = capability_registry
        
    def resolve(self, capability: Capability) -> Optional[IAgent]:
        """
        Returns the highest priority agent that supports this capability.
        """
        providers = self.registry.get_providers(capability)
        for provider in providers:
            agent = self.registry.agent_registry.get(provider.agent_name)
            if agent:
                return agent
        return None
        
    def resolve_name(self, capability: Capability) -> Optional[str]:
        """
        Returns the name of the highest priority agent that supports this capability.
        """
        providers = self.registry.get_providers(capability)
        for provider in providers:
            # Verify the agent actually exists in the registry
            if self.registry.agent_registry.get(provider.agent_name):
                return provider.agent_name
        return None
