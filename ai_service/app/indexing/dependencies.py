from fastapi import Depends

from app.chunking.base import BaseChunker
from app.chunking.dependencies import get_chunker
from app.embeddings.service import EmbeddingService
from app.embeddings.dependencies import get_embedding_service
from app.vector_store.service import VectorStoreService
from app.vector_store.dependencies import get_vector_store_service
from app.indexing.service import IndexingService
from app.indexing.base import BaseIndexingPipeline

def get_indexing_service(
    chunker: BaseChunker = Depends(get_chunker),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_store: VectorStoreService = Depends(get_vector_store_service)
) -> BaseIndexingPipeline:
    """
    Wires up the entire pipeline dependency tree.
    FastAPI will automatically resolve Chunker -> Embeddings -> VectorStore.
    """
    return IndexingService(chunker, embedding_service, vector_store)
