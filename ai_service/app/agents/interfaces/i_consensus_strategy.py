from typing import List, Any
from abc import ABC, abstractmethod
from app.models.chat.chat_models import ExecutionResult

class IConsensusStrategy(ABC):
    @abstractmethod
    def achieve_consensus(self, results: List[ExecutionResult]) -> ExecutionResult:
        """
        Evaluates multiple agent results and returns a single consensus result.
        """
        pass
