from typing import List
from app.agents.interfaces.i_agent_registry import IAgentRegistry
from app.agents.models.agent_descriptor import AgentDescriptor, AgentStatus

class DiscoveryService:
    """
    Discovers and filters agents based on capabilities, priority, and health.
    Implements ranking: Capability Match -> Priority -> Health -> Cost.
    """
    def __init__(self, registry: IAgentRegistry):
        self._registry = registry

    def discover_agents(self, capability: str) -> List[AgentDescriptor]:
        """
        Returns a ranked list of capable agents.
        Ranking weight formula:
        - Must have capability
        - Status must be AVAILABLE or BUSY (penalize BUSY)
        - Sort by Priority (descending)
        - Sort by Cost (ascending)
        """
        candidates = self._registry.get_agents_by_capability(capability)
        
        # Filter out offline/error agents
        valid_candidates = [
            agent for agent in candidates 
            if agent.status in [AgentStatus.AVAILABLE, AgentStatus.BUSY]
        ]
        
        def rank_score(agent: AgentDescriptor) -> float:
            score = float(agent.priority) * 100
            
            # Penalize busy agents
            if agent.status == AgentStatus.BUSY:
                score -= 50
                
            # Confidence of the specific capability match
            cap_confidence = 1.0
            for cap in agent.capabilities:
                if cap.capability_name == capability:
                    cap_confidence = cap.confidence
                    break
                    
            score *= cap_confidence
            
            # Favor lower cost
            score -= agent.cost_weight
            
            return score
            
        return sorted(valid_candidates, key=rank_score, reverse=True)
