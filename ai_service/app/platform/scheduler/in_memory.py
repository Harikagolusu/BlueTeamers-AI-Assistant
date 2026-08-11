import asyncio
import logging
from typing import Any, Dict
from app.platform.scheduler.interface import IExecutionScheduler
from app.platform.models.contexts import WorkflowContext

logger = logging.getLogger(__name__)

class InMemoryExecutionScheduler(IExecutionScheduler):
    """
    In-memory scheduler using asyncio queues.
    """
    def __init__(self, max_concurrent: int = 10):
        self.queue = asyncio.PriorityQueue()
        self.tasks: Dict[str, asyncio.Task] = {}
        self._max_concurrent = max_concurrent
        
    async def submit(self, workflow_coro: Any, context: WorkflowContext) -> asyncio.Task:
        """
        Submits a workflow coroutine to the event loop.
        In a real queue, this would push a serializable object to RabbitMQ/Redis.
        Since we are in-memory, we create a task immediately.
        """
        task_id = context.correlation_id
        
        # Priority mapping (lower number = higher priority)
        priority = 10
        if context.execution_strategy == "PARALLEL":
            priority = 5
            
        # We push to the PriorityQueue (we're simulating a worker pulling this)
        # But for direct async execution, we can also just create a task.
        task = asyncio.create_task(self._wrap_execution(workflow_coro, context))
        self.tasks[task_id] = task
        return task

    async def _wrap_execution(self, workflow_coro, context: WorkflowContext):
        try:
            return await workflow_coro
        except asyncio.CancelledError:
            logger.warning(f"Workflow {context.workflow_id} cancelled.")
            raise
        except Exception as e:
            logger.error(f"Workflow {context.workflow_id} failed: {e}")
            raise
            
    async def cancel(self, execution_id: str) -> bool:
        if execution_id in self.tasks:
            task = self.tasks[execution_id]
            if not task.done():
                task.cancel()
                return True
        return False
        
    async def status(self, execution_id: str) -> str:
        if execution_id not in self.tasks:
            return "UNKNOWN"
        task = self.tasks[execution_id]
        if task.cancelled():
            return "CANCELLED"
        if task.done():
            if task.exception():
                return "FAILED"
            return "COMPLETED"
        return "RUNNING"
