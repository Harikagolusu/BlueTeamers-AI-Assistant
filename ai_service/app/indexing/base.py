from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.indexing.schemas import (
    IndexDocumentRequest, BatchIndexRequest, 
    IndexingResult, BatchIndexResult, DeleteIndexRequest, HealthResponse
)

class BaseIndexingPipeline(ABC):
    @abstractmethod
    def index_document(self, request: IndexDocumentRequest) -> IndexingResult:
        pass
        
    @abstractmethod
    def index_documents(self, request: BatchIndexRequest) -> BatchIndexResult:
        pass
        
    @abstractmethod
    def update_document(self, request: IndexDocumentRequest) -> IndexingResult:
        pass
        
    @abstractmethod
    def delete_document(self, request: DeleteIndexRequest) -> bool:
        pass
        
    @abstractmethod
    def reindex(self, request: BatchIndexRequest) -> BatchIndexResult:
        pass
        
    @abstractmethod
    def health_check(self) -> HealthResponse:
        pass
