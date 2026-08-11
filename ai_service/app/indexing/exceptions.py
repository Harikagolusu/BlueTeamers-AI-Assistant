class IndexingException(Exception):
    """Base exception for indexing pipeline errors."""
    pass

class ChunkingFailure(IndexingException):
    pass

class EmbeddingFailure(IndexingException):
    pass

class VectorStoreFailure(IndexingException):
    pass

class PipelineFailure(IndexingException):
    pass
