class VectorStoreException(Exception):
    """Base exception for all vector store errors."""
    pass

class IndexNotInitializedException(VectorStoreException):
    """Raised when attempting an operation on an uninitialized FAISS index."""
    pass

class MetadataSyncException(VectorStoreException):
    """Raised when metadata and vectors are out of sync."""
    pass
