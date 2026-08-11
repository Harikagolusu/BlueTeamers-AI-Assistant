from typing import Any
import logging

logger = logging.getLogger(__name__)

class ExecutionReplayManager:
    """
    Manages the replay of a workflow by routing the historical payload 
    back through the PlatformAgentOrchestrator to ensure exact reproduction.
    """
    def __init__(self, orchestrator: Any, history_repo: Any):
        self.orchestrator = orchestrator
        self.history_repo = history_repo
        
    async def replay_workflow(self, execution_id: str) -> Any:
        history = self.history_repo.get_history(execution_id)
        if not history:
            raise ValueError(f"No history found for execution {execution_id}")
            
        # Reconstruct original request from the first CREATE event
        # Assuming metadata contains the request string for simplicity
        original_request = history[0].get("metadata", {}).get("request", "")
        
        logger.info(f"Replaying execution {execution_id}")
        
        # Route through the exact production path
        return await self.orchestrator.process_request(original_request)
