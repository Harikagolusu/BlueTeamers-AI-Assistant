from abc import ABC, abstractmethod
from typing import List
from app.retrieval.schemas import (
    RetrievalRequest, BatchRetrievalRequest, 
    RetrievalResponse, HealthResponse
)

class BaseRetriever(ABC):
    @abstractmethod
    def retrieve(self, request: RetrievalRequest) -> RetrievalResponse:
        pass
        
    @abstractmethod
    def retrieve_batch(self, request: BatchRetrievalRequest) -> List[RetrievalResponse]:
        pass
        
    @abstractmethod
    def health_check(self) -> HealthResponse:
        pass
