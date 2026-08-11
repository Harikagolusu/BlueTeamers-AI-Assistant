from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple

class IPromptBuilder(ABC):
    @abstractmethod
    def build_prompt(self, query: str, context: Dict[str, Any]) -> Tuple[str, str]:
        """Constructs a formalized prompt string. Returns (prompt, system_prompt)."""
        pass
