from abc import ABC, abstractmethod
from typing import Any
from app.platform.models.contexts import WorkflowContext

class IExecutionScheduler(ABC):
    """
    Interface for queuing and scheduling workflow executions.
    """
    
    @abstractmethod
    async def submit(self, workflow_invocation: Any, context: WorkflowContext) -> Any:
        """
        Submit a workflow for execution. Returns a future/task representing the execution.
        """
        pass
    
    @abstractmethod
    async def cancel(self, execution_id: str) -> bool:
        """
        Cancel a running or queued execution.
        """
        pass
    
    @abstractmethod
    async def status(self, execution_id: str) -> str:
        """
        Get the current state of an execution.
        """
        pass
