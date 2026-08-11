from typing import List, Any
from app.security.interfaces.i_risk import IRiskEvaluator
from app.security.risk.analyzers import IRiskAnalyzer
from app.security.risk.aggregator import RiskAggregator

class RiskPipeline(IRiskEvaluator):
    def __init__(self, analyzers: List[IRiskAnalyzer], aggregator: RiskAggregator):
        self._analyzers = analyzers
        self._aggregator = aggregator

    def evaluate(self, package: Any) -> str:
        scores = {}
        for analyzer in self._analyzers:
            scores.update(analyzer.analyze(package))
            
        return self._aggregator.aggregate(scores)
