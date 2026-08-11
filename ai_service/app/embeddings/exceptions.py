class EmbeddingException(Exception):
    """Base exception for all embedding-related errors."""
    pass

class ModelLoadException(EmbeddingException):
    """Raised when the SentenceTransformer model fails to load."""
    pass

class EmbeddingGenerationException(EmbeddingException):
    """Raised when the model fails to generate vectors."""
    pass

class InvalidInputException(EmbeddingException):
    """Raised when input text is empty or improperly formatted."""
    pass
