from abc import ABC, abstractmethod
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult

class IExecutionEngine(ABC):
    """
    Generic interface for RAG, Tool, and General LLM execution engines.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the engine."""
        pass

    @abstractmethod
    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        """Executes the core engine logic based on the provided context."""
        pass
