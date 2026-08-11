import uuid
import time
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from app.core.logging import request_id_var
from app.chat.schemas import ChatRequest, ChatResponse
from app.chat.exceptions.handlers import handle_chat_exception
from app.chat.dependencies import get_chat_health_service
from app.chat.health import ChatHealthService
from app.chat.bootstrap import get_chat_service
from app.chat.interfaces.i_chat_service import IChatService
from app.models.chat.chat_models import ChatRequest as DomainChatRequest
from app.rag.schemas import PipelineMetrics

logger = logging.getLogger("app.chat.router")

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    request: ChatRequest,
    chat_service: IChatService = Depends(get_chat_service)
):
    """
    Orchestrated Chat Endpoint routing via ChatService.
    """
    req_id = request.request_id or uuid.uuid4()
    request_id_var.set(str(req_id))
    
    start_time = time.time()
    logger.info(f"Chat API Request Started - RequestID: {req_id}")

    domain_request = DomainChatRequest(
        conversation_id=request.conversation_id,
        message=request.query,
        stream=False,
        images=request.images,
        files=request.files
    )

    try:
        result = await chat_service.process_request(domain_request)
        
        latency = (time.time() - start_time) * 1000
        logger.info(f"Chat API Request Completed - RequestID: {req_id} - Latency: {latency:.2f}ms")
        
        citations = result.metadata.get("citations", [])
        metrics = result.metadata.get("metrics") or PipelineMetrics()
        
        return ChatResponse(
            answer=result.message,
            citations=citations,
            request_id=req_id,
            metrics=metrics
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise handle_chat_exception(e)

@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    chat_service: IChatService = Depends(get_chat_service)
):
    """
    Streaming Chat Endpoint routing via ChatService.
    """
    req_id = request.request_id or uuid.uuid4()
    request_id_var.set(str(req_id))
    
    logger.info(f"Chat API Stream Request Started - RequestID: {req_id}")

    domain_request = DomainChatRequest(
        conversation_id=request.conversation_id,
        message=request.query,
        stream=True,
        images=request.images,
        files=request.files
    )
    
    try:
        generator = await chat_service.process_request(domain_request)
        return StreamingResponse(generator, media_type="text/event-stream")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise handle_chat_exception(e)

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(
    health_service: ChatHealthService = Depends(get_chat_health_service)
):
    """
    Chat API Health Endpoint.
    """
    return health_service.check_health()
