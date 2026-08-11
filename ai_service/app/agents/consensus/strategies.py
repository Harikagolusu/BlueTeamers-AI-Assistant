from typing import List, Dict
from app.agents.interfaces.i_consensus_strategy import IConsensusStrategy
from app.models.chat.chat_models import ExecutionResult, ExecutionStatus

class MajorityVoteStrategy(IConsensusStrategy):
    """
    Groups results by their message content. 
    The response with the most identical/similar results wins.
    """
    def achieve_consensus(self, results: List[ExecutionResult]) -> ExecutionResult:
        if not results:
            return ExecutionResult.failed("CONSENSUS", [{"error": "No results."}])
            
        votes: Dict[str, List[ExecutionResult]] = {}
        for r in results:
            msg = r.message.strip()
            if msg not in votes:
                votes[msg] = []
            votes[msg].append(r)
            
        # Find the majority string
        majority_msg = max(votes.keys(), key=lambda k: len(votes[k]))
        majority_group = votes[majority_msg]
        
        # Return the best representative from the majority group (e.g. highest confidence)
        best_result = sorted(
            majority_group, 
            key=lambda r: r.metadata.get("confidence", 0.0), 
            reverse=True
        )[0]
        
        best_result.metadata["consensus_strategy"] = "MAJORITY_VOTE"
        best_result.metadata["vote_count"] = len(majority_group)
        return best_result

class HighestConfidenceStrategy(IConsensusStrategy):
    """
    Picks the result with the highest confidence score in its metadata.
    """
    def achieve_consensus(self, results: List[ExecutionResult]) -> ExecutionResult:
        if not results:
            return ExecutionResult.failed("CONSENSUS", [{"error": "No results."}])
            
        best = max(results, key=lambda r: r.metadata.get("confidence", 0.0))
        best.metadata["consensus_strategy"] = "HIGHEST_CONFIDENCE"
        return best
