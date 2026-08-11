from abc import ABC, abstractmethod
from typing import Any

class IRiskEvaluator(ABC):
    @abstractmethod
    def evaluate(self, package: Any) -> str: pass
