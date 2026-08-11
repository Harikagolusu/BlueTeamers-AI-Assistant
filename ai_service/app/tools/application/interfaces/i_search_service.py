from abc import ABC, abstractmethod
from app.tools.domain.schemas.search_schemas import VectorSearchSchema, DocumentSearchSchema, SemanticSearchSchema
from app.tools.domain.results.search_results import VectorSearchResult, DocumentSearchResult, SemanticSearchResult

class ISearchService(ABC):
    @abstractmethod
    async def vector_search(self, schema: VectorSearchSchema) -> VectorSearchResult:
        pass

    @abstractmethod
    async def document_search(self, schema: DocumentSearchSchema) -> DocumentSearchResult:
        pass

    @abstractmethod
    async def semantic_search(self, schema: SemanticSearchSchema) -> SemanticSearchResult:
        pass
