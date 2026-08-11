from abc import ABC, abstractmethod
from typing import AsyncGenerator, Union, Dict, Any, List

class ILLMService(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    async def stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        pass
