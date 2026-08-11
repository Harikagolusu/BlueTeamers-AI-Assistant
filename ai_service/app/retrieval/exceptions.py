class RetrievalException(Exception):
    """Base exception for retrieval layer errors."""
    pass

class EmbeddingFailure(RetrievalException):
    pass

class SearchFailure(RetrievalException):
    pass

class MetadataFailure(RetrievalException):
    pass
