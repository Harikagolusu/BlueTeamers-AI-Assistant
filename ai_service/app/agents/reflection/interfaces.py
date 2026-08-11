from abc import ABC, abstractmethod
from app.models.chat.chat_models import ExecutionResult

class IReflectionStage(ABC):
    """A single stage in the reflection pipeline."""
    
    @abstractmethod
    def validate(self, result: ExecutionResult) -> bool:
        """Return True if the execution result passes this validation stage, False otherwise."""
        pass
