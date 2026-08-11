from typing import Optional
from app.agents.interfaces.i_agent_router import IAgentRouter
from app.planning.models.plan import ExecutionStep
from app.agents.models.agent_descriptor import AgentDescriptor
from app.agents.discovery.discovery_service import DiscoveryService

class AgentRouter(IAgentRouter):
    """
    Routes an ExecutionStep to the best available AgentDescriptor using the DiscoveryService.
    """
    def __init__(self, discovery_service: DiscoveryService):
        self._discovery_service = discovery_service

    def route_step(self, step: ExecutionStep) -> Optional[AgentDescriptor]:
        # Required capability enum value as string
        capability_str = step.required_capability.value
        
        candidates = self._discovery_service.discover_agents(capability_str)
        if not candidates:
            return None
            
        # Returning the top-ranked candidate
        return candidates[0]
