import uuid
import logging

from app.core.logging import request_id_var
from app.rag.base import BaseRAGEngine
from app.rag.schemas import RAGRequest, RAGResponse
from app.rag.exceptions import (
    BaseRAGException, OrchestrationFailure
)

logger = logging.getLogger("app.rag.service")

class RAGService:
    """
    API Facade.
    Receives requests, handles UUID generation, and acts as an exception barrier.
    No orchestration logic.
    """
    def __init__(self, engine: BaseRAGEngine):
        self.engine = engine

    def generate_answer(self, request: RAGRequest) -> RAGResponse:
        # 1. UUID assignment if absent
        if not request.request_id:
            request.request_id = uuid.uuid4()
            
        # Bind the UUID to the context var so logs track it automatically
        request_id_var.set(str(request.request_id))
        
        logger.info(f"RAGService received request, ID: {request.request_id}")
        
        # 2. Invoke Engine and handle exceptions
        try:
            response = self.engine.generate_answer(request)
            return response
        except BaseRAGException as e:
            # Re-raise domain exceptions so FastAPI exception handlers can intercept and format to 4xx/5xx
            logger.error(f"Domain Failure in RAG Pipeline: {str(e)}")
            raise e
        except Exception as e:
            # Catch unexpected system faults
            logger.critical(f"Unexpected Pipeline Collapse: {str(e)}")
            raise OrchestrationFailure(f"An unexpected error occurred in the RAG orchestrator: {str(e)}")

    async def stream_answer(self, request: RAGRequest):
        # 1. UUID assignment if absent
        if not request.request_id:
            request.request_id = uuid.uuid4()
            
        # Bind the UUID to the context var so logs track it automatically
        request_id_var.set(str(request.request_id))
        
        logger.info(f"RAGService received stream request, ID: {request.request_id}")
        
        # 2. Invoke Engine and handle exceptions
        try:
            async for chunk in self.engine.stream_answer(request):
                yield chunk
        except BaseRAGException as e:
            logger.error(f"Domain Failure in RAG Pipeline: {str(e)}")
            raise e
        except Exception as e:
            logger.critical(f"Unexpected Pipeline Collapse: {str(e)}")
            raise OrchestrationFailure(f"An unexpected error occurred in the RAG orchestrator: {str(e)}")
