from typing import List
from abc import ABC, abstractmethod
from app.models.chat.chat_models import ExecutionResult

class IAggregator(ABC):
    @abstractmethod
    def aggregate(self, results: List[ExecutionResult]) -> ExecutionResult:
        """
        Merges outputs, removes duplicates, and preserves execution metadata.
        """
        pass
