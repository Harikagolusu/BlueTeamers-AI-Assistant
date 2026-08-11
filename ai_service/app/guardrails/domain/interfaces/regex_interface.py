from abc import ABC, abstractmethod

class IRegexEngine(ABC):
    """Domain interface for regex evaluation."""
    
    @abstractmethod
    def contains_match(self, text: str) -> bool:
        """Returns True if the text matches any blocked pattern."""
        pass
