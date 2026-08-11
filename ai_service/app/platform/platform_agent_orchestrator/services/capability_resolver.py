from typing import List, Optional
from app.platform.platform_agent_orchestrator.policies.capability_matcher import CapabilityMatcher, MetadataCapabilityMatcher
from app.platform.platform_agent_orchestrator.policies.ranking_strategy import RankingStrategy, CandidateAgent
from app.platform.platform_agent_orchestrator.repositories.agent_health import AgentHealth

class CapabilityResolverService:
    def __init__(self, matcher: Optional[CapabilityMatcher] = None, ranking: Optional[RankingStrategy] = None):
        self.matcher = matcher or MetadataCapabilityMatcher()
        self.ranking = ranking or RankingStrategy()
        
    def resolve_capabilities(self, capabilities: List[str], registry=None) -> dict:
        """
        Resolves a list of required capabilities into assigned target agents.
        Returns a dict mapping capability -> agent_id.
        """
        resolved_map = {}
        for cap in capabilities:
            # 1. Match
            matches = self.matcher.match(cap, registry)
            if not matches:
                resolved_map[cap] = None
                continue
            
            # 2. Map to CandidateAgents for ranking
            candidates = []
            for m in matches:
                candidates.append(
                    CandidateAgent(
                        agent_id=m.agent_id,
                        capability_score=m.score,
                        health_score=m.metadata.get("health", 1.0),
                        latency_ms=m.metadata.get("latency", 100.0),
                        confidence=m.metadata.get("confidence", 0.9)
                    )
                )
                
            # 3. Rank and Select
            mock_health = [
                AgentHealth(
                    agent_id=c.agent_id, 
                    availability=True, 
                    health_score=1.0, 
                    latency=10.0, 
                    success_rate=1.0, 
                    failure_rate=0.0, 
                    active_workflows=0, 
                    last_heartbeat="now"
                ) 
                for c in candidates
            ]
            ranked = self.ranking.rank_candidates(candidates, health_data=mock_health)
            if ranked:
                resolved_map[cap] = ranked[0].agent_id
            else:
                resolved_map[cap] = None
                
        return resolved_map
