import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from app.services.workflow.workflow_context import WorkflowContext
from app.services.workflow.workflow_state import WorkflowState

logger = logging.getLogger(__name__)

class WorkflowStep(ABC):
    """
    A single unit of execution within a workflow.
    """
    def __init__(self, name: str, depends_on: List[str] = None, timeout: int = 0, retries: int = 0):
        self.name = name
        self.depends_on = depends_on or []
        self.timeout = timeout
        self.retries = retries
        self.state: WorkflowState = WorkflowState.CREATED
        self.error: Optional[Exception] = None

    @abstractmethod
    async def execute(self, context: WorkflowContext) -> Any:
        """
        The core logic of the step. Must be implemented by subclasses.
        """
        pass
        
    async def run_with_retry(self, context: WorkflowContext) -> Any:
        self.state = WorkflowState.RUNNING
        for attempt in range(self.retries + 1):
            try:
                if self.timeout > 0:
                    result = await asyncio.wait_for(self.execute(context), timeout=self.timeout)
                else:
                    result = await self.execute(context)
                self.state = WorkflowState.COMPLETED
                return result
            except asyncio.TimeoutError as e:
                self.error = e
                logger.warning(f"Step '{self.name}' timed out on attempt {attempt + 1}")
            except Exception as e:
                self.error = e
                logger.warning(f"Step '{self.name}' failed on attempt {attempt + 1}: {e}")
                
            if attempt < self.retries:
                self.state = WorkflowState.RETRYING
                await asyncio.sleep(1) # simple backoff
                
        self.state = WorkflowState.FAILED
        raise self.error or Exception(f"Step '{self.name}' failed.")
