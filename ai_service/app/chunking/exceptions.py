class ChunkingException(Exception):
    """Base exception for all chunking errors."""
    pass

class EmptyContentException(ChunkingException):
    """Raised when the lesson content is empty or null."""
    pass

class InvalidMarkdownException(ChunkingException):
    """Raised when the markdown is structurally invalid."""
    pass

class OversizedContentException(ChunkingException):
    """Raised when the content exceeds the maximum allowed length."""
    pass
