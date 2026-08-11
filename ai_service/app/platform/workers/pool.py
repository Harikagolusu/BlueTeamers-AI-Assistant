import asyncio
import logging
from typing import Any, List
from app.platform.models.contexts import AgentContext
from app.shared.models.communication import AgentRequest

logger = logging.getLogger(__name__)

class Worker:
    def __init__(self, worker_id: str, orchestration_service: Any):
        self.worker_id = worker_id
        self.orchestration_service = orchestration_service
        self.is_busy = False

    async def execute(self, capability: str, request: AgentRequest, context: AgentContext) -> Any:
        """
        Executes a capability strictly through the orchestration service.
        No direct agent instantiation.
        """
        self.is_busy = True
        logger.info(f"Worker {self.worker_id} executing capability {capability}")
        try:
            # Route to orchestration service
            result = await self.orchestration_service.handle_request(request, context)
            return result
        finally:
            self.is_busy = False

class AgentWorkerPool:
    """
    Manages a pool of isolated workers.
    """
    def __init__(self, pool_size: int, orchestration_service: Any):
        self.pool_size = pool_size
        self.workers = [Worker(f"worker-{i}", orchestration_service) for i in range(pool_size)]
        
    def get_available_worker(self) -> Worker:
        for w in self.workers:
            if not w.is_busy:
                return w
        # If all busy, we could implement blocking/queueing here.
        # For simplicity, returning the first one. In reality the scheduler handles queuing.
        return self.workers[0]
