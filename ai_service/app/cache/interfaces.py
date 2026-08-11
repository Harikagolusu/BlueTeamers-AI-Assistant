from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
from app.rag.schemas import RAGResponse

class BaseCacheStore(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[RAGResponse]:
        pass

    @abstractmethod
    async def set(self, key: str, value: RAGResponse, ttl: int) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    async def clear(self) -> None:
        pass

    @abstractmethod
    async def get_metrics(self) -> Dict[str, Any]:
        pass

class ICacheService(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    async def set(self, key: str, value: str, ttl: int = 3600) -> None:
        pass
