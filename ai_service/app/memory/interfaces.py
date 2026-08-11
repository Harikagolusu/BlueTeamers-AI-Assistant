from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.memory.models import ConversationSession, MemoryMessage

class BaseMemoryStore(ABC):
    """
    Abstract storage interface for Conversation Sessions.
    Follows Dependency Inversion Principle allowing swapping of
    InMemory for Redis, Postgres, etc.
    """
    
    @abstractmethod
    async def create_session(self, session_id: str) -> ConversationSession:
        pass
        
    @abstractmethod
    async def get_session(self, session_id: str) -> Optional[ConversationSession]:
        pass
        
    @abstractmethod
    async def update_session(self, session: ConversationSession) -> None:
        pass
        
    @abstractmethod
    async def delete_session(self, session_id: str) -> bool:
        pass
        
    @abstractmethod
    async def health_check(self) -> dict:
        pass

class IMemoryManager(ABC):
    @abstractmethod
    async def load_history(self, session_user: str, tenant_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def save_turn(self, session_user: str, tenant_id: str, turn_data: Dict[str, Any]) -> None:
        pass
