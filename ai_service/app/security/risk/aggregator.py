from typing import Dict

class RiskAggregator:
    def aggregate(self, scores: Dict[str, float]) -> str:
        total = sum(scores.values())
        avg = total / max(1, len(scores))
        
        if avg > 0.8: return "CRITICAL"
        if avg > 0.5: return "HIGH"
        if avg > 0.2: return "MEDIUM"
        return "LOW"
