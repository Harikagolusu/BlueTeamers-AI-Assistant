from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any

class BaseVectorStore(ABC):
    """
    Abstract interface defining the contract for any vector store implementation.
    Adheres strictly to the Open/Closed Principle.
    """
    @abstractmethod
    def initialize(self, dimension: int) -> None:
        pass
        
    @abstractmethod
    def load(self) -> None:
        pass
        
    @abstractmethod
    def save(self) -> None:
        pass
        
    @abstractmethod
    def add(self, id: str, vector: List[float]) -> None:
        pass
        
    @abstractmethod
    def add_batch(self, ids: List[str], vectors: List[List[float]]) -> None:
        pass
        
    @abstractmethod
    def update(self, id: str, vector: List[float]) -> None:
        pass
        
    @abstractmethod
    def delete(self, id: str) -> None:
        pass
        
    @abstractmethod
    def search(self, query_vector: List[float], top_k: int) -> Tuple[List[str], List[float]]:
        pass
        
    @abstractmethod
    def count(self) -> int:
        pass
        
    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        pass
