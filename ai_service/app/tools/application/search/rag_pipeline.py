from typing import List
from app.tools.domain.models.search_models import SearchDocument
from app.tools.infrastructure.search.interfaces.i_search_provider import ISearchProvider

class Retriever:
    def __init__(self, provider: ISearchProvider):
        self.provider = provider
        
    async def retrieve(self, query: str, limit: int) -> List[SearchDocument]:
        raw_results = await self.provider.search(query=query, limit=limit)
        return [SearchDocument(**raw) for raw in raw_results]

class Ranker:
    def rank(self, documents: List[SearchDocument]) -> List[SearchDocument]:
        # Simple sorting by score for now
        return sorted(documents, key=lambda x: x.score, reverse=True)

class ContextAssembler:
    def assemble(self, documents: List[SearchDocument]) -> str:
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"[{i}] {doc.title}\n{doc.content}")
        return "\n\n".join(context_parts)

class RAGPipeline:
    def __init__(self, retriever: Retriever, ranker: Ranker, assembler: ContextAssembler):
        self.retriever = retriever
        self.ranker = ranker
        self.assembler = assembler
        
    async def execute(self, query: str, limit: int = 5) -> str:
        docs = await self.retriever.retrieve(query, limit)
        ranked_docs = self.ranker.rank(docs)
        context = self.assembler.assemble(ranked_docs)
        return context
