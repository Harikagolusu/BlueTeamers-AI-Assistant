from abc import ABC, abstractmethod

class IGuardrailsService(ABC):
    @abstractmethod
    async def validate(self, prompt: str) -> bool:
        """Returns True if prompt is safe, False if malicious/policy violation."""
        pass
