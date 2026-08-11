from pydantic import BaseModel
from typing import List
from app.platform.platform_agent_orchestrator.repositories.agent_health import AgentHealth

class CandidateAgent(BaseModel):
    agent_id: str
    capability_score: float
    confidence: float = 0.9

class RankingStrategy:
    @staticmethod
    def rank_candidates(candidates: List[CandidateAgent], health_data: List[AgentHealth]) -> List[CandidateAgent]:
        health_map = {h.agent_id: h for h in health_data}
        
        def score_candidate(candidate: CandidateAgent) -> float:
            health = health_map.get(candidate.agent_id)
            if not health or not health.availability:
                return -1.0 # unavailable
            
            # Combine capability score with health, latency and load
            base_score = candidate.capability_score * candidate.confidence * health.health_score
            latency_penalty = health.latency / 1000.0 # simple penalty
            load_penalty = health.active_workflows * 0.1
            
            return base_score - latency_penalty - load_penalty

        ranked = sorted(candidates, key=score_candidate, reverse=True)
        # Filter out unavailable
        return [r for r in ranked if score_candidate(r) > 0]
