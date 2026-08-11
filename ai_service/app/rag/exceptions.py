class BaseRAGException(Exception):
    """Root exception for RAG module."""
    pass

class RetrievalFailure(BaseRAGException):
    pass

class ContextFailure(BaseRAGException):
    pass

class PromptFailure(BaseRAGException):
    pass

class GenerationFailure(BaseRAGException):
    pass

class ValidationFailure(BaseRAGException):
    pass

class OrchestrationFailure(BaseRAGException):
    pass

class EmptyContextException(BaseRAGException):
    pass
