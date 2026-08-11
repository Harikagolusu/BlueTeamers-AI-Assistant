from app.tools.application.interfaces.i_search_service import ISearchService
from app.tools.infrastructure.base.base_service import BaseService
from app.tools.infrastructure.search.factory.search_provider_factory import SearchProviderFactory
from app.tools.domain.schemas.search_schemas import VectorSearchSchema, DocumentSearchSchema, SemanticSearchSchema
from app.tools.domain.results.search_results import VectorSearchResult, DocumentSearchResult, SemanticSearchResult
from app.tools.domain.models.search_models import SearchDocument
from app.tools.infrastructure.search.providers.mock_search_provider import MockSearchProvider

# Register mock provider explicitly
SearchProviderFactory.register("mock", MockSearchProvider)

class SearchApplicationService(BaseService, ISearchService):
    def __init__(self, provider_name: str = "mock"):
        super().__init__()
        self.provider_name = provider_name
        self.provider = None
        
    async def _on_initialize(self) -> None:
        self.provider = SearchProviderFactory.create(self.provider_name)
        self._logger.info(f"Initialized SearchApplicationService with {self.provider_name}")

    async def _perform_search(self, query: str, limit: int) -> list[SearchDocument]:
        raw_results = await self.provider.search(query=query, limit=limit)
        documents = []
        for raw in raw_results:
            documents.append(SearchDocument(**raw))
        return documents

    async def vector_search(self, schema: VectorSearchSchema) -> VectorSearchResult:
        docs = await self._perform_search(schema.query, schema.limit)
        return VectorSearchResult(documents=docs)

    async def document_search(self, schema: DocumentSearchSchema) -> DocumentSearchResult:
        docs = await self._perform_search(schema.keyword, schema.limit)
        return DocumentSearchResult(documents=docs)

    async def semantic_search(self, schema: SemanticSearchSchema) -> SemanticSearchResult:
        docs = await self._perform_search(schema.query, schema.limit)
        return SemanticSearchResult(documents=docs)
