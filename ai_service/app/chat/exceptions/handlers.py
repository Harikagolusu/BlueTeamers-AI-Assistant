from fastapi import HTTPException, status
import logging

from app.rag.exceptions import (
    BaseRAGException,
    RetrievalFailure,
    ContextFailure,
    PromptFailure,
    GenerationFailure,
    ValidationFailure,
    OrchestrationFailure,
    EmptyContextException
)

logger = logging.getLogger("app.chat.exceptions")

def handle_chat_exception(e: Exception) -> HTTPException:
    """
    Converts internal domain exceptions into appropriate FastAPI HTTPExceptions.
    Ensures internal architecture traces do not leak to the client.
    """
    if isinstance(e, EmptyContextException):
        logger.warning(f"Chat request failed: Empty Context - {str(e)}")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No relevant context found for the query.")
        
    elif isinstance(e, ValidationFailure):
        logger.warning(f"Chat request failed: Validation - {str(e)}")
        # If the LLM generated garbage, it's an internal error from the user's perspective,
        # but 400 or 500 can be debated. We'll use 500 as the system failed to produce a valid output.
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate a valid response.")
        
    elif isinstance(e, RetrievalFailure):
        logger.error(f"Chat request failed: Retrieval - {str(e)}")
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal search service failure.")
        
    elif isinstance(e, GenerationFailure):
        logger.error(f"Chat request failed: Generation - {str(e)}")
        return HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI generation service unavailable.")
        
    elif isinstance(e, BaseRAGException):
        logger.error(f"Chat request failed: RAG Domain - {str(e)}")
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal orchestration failure.")
        
    else:
        logger.critical(f"Chat request failed: Unexpected System Fault - {str(e)}")
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
