from abc import ABC, abstractmethod
from typing import Dict, Any, Callable, Awaitable

class IMCPTransport(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass
        
    @abstractmethod
    async def disconnect(self) -> None:
        pass
        
    @abstractmethod
    async def send_message(self, message: Dict[str, Any]) -> None:
        pass
        
    @abstractmethod
    def on_message(self, callback: Callable[[Dict[str, Any]], Awaitable[None]]) -> None:
        pass
