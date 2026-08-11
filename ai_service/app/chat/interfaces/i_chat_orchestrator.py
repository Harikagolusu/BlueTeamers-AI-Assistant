from abc import ABC, abstractmethod
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult

class IChatOrchestrator(ABC):
    """
    The workflow manager. Executes the stages of the Execution Pipeline sequentially.
    """
    @abstractmethod
    async def execute_pipeline(self, context: ExecutionContext) -> ExecutionResult:
        """Executes the pluggable pipeline and returns the final ExecutionResult."""
        pass
