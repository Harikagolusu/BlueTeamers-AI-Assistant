from typing import List, Dict, Any
from app.rag.interfaces import IRetriever, Document
from app.retrieval.service import RetrievalService
from app.retrieval.schemas import RetrievalRequest

class FAISSRetriever(IRetriever):
    """
    Adapter bridging RetrievalService to IRetriever interface required by RagExecutionEngine.
    """
    def __init__(self, retrieval_service: RetrievalService):
        self._retrieval_service = retrieval_service

    async def search(self, query: str, top_k: int = 5, metadata_filters: Dict[str, Any] = None) -> List[Document]:
        request = RetrievalRequest(
            query=query,
            top_k=top_k,
            metadata_filters=metadata_filters
        )
        
        # Execute retrieval (synchronous execution is fine for local similarity search)
        response = self._retrieval_service.retrieve(request)
        
        # Map RetrievalResponse to List[Document]
        documents = []
        for result in response.results:
            meta = dict(result.metadata)
            meta.setdefault("chunk_id", result.chunk_id)
            documents.append(Document(
                content=result.text,
                metadata=meta,
                score=result.score
            ))
        return documents
