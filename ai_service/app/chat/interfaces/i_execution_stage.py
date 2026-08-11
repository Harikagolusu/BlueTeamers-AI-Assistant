from abc import ABC, abstractmethod
from app.chat.context.execution_context import ExecutionContext

class IExecutionStage(ABC):
    """
    Interface for a pluggable stage in the ChatOrchestrator's execution pipeline.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the name of the stage."""
        pass

    @abstractmethod
    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        """
        Executes the stage logic and returns the (potentially updated) context.
        Note: ExecutionContext is frozen, so updates must return a new derived context.
        """
        pass
