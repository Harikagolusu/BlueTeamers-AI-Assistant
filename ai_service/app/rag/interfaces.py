from abc import ABC, abstractmethod
from typing import List, Dict, Any

class Document:
    def __init__(self, content: str, metadata: Dict[str, Any] = None, score: float = 0.0):
        self.content = content
        self.metadata = metadata or {}
        self.score = score

class IRetriever(ABC):
    @abstractmethod
    async def search(self, query: str, top_k: int = 5, metadata_filters: Dict[str, Any] = None) -> List[Document]:
        pass
