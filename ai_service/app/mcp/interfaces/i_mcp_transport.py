from abc import ABC, abstractmethod
from typing import Optional

class IMCPTransport(ABC):
    @abstractmethod
    async def connect(self) -> None:
        """Establish connection."""
        pass
        
    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection."""
        pass
        
    @abstractmethod
    async def send(self, message: str) -> None:
        """Send a message."""
        pass
        
    @abstractmethod
    async def receive(self) -> Optional[str]:
        """Receive a message."""
        pass
