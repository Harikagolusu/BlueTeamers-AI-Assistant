import uuid
import time
import logging
from typing import Optional
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
from app.api.dependencies import get_optional_raw_token
from app.security.auth import resolve_user_identity
from app.security.rate_limit import enforce_chat_rate_limit
from app.freemium.dependencies import get_freemium_service_singleton
from app.freemium.models import FreemiumLimitExceeded
from app.freemium.service import FreemiumService

logger = logging.getLogger("app.chat.router")

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])

GUEST_ID_PREFIX = "guest:"


def _require_identity(raw_token: Optional[str], client_id: Optional[str]) -> None:
    """Fail closed when a caller carries neither a valid JWT nor a guest id.

    Mirrors the identity policy of the main /api/chat/ endpoint: anonymous
    callers must never drive the LLM at unlimited cost.
    """
    if raw_token:
        user_id, _email = resolve_user_identity(raw_token)
        if user_id:
            return
    if client_id:
        return
    raise HTTPException(
        status_code=401,
        detail="Authentication required: provide a bearer token or a client_id.",
    )


def _resolve_identity_for_freemium(
    raw_token: Optional[str], client_id: Optional[str]
) -> tuple:
    """Resolve (tracking_identity, token) for freemium, matching /api/chat/."""
    if raw_token:
        user_id, _email = resolve_user_identity(raw_token)
        if user_id:
            return user_id, raw_token
    if client_id:
        return f"{GUEST_ID_PREFIX}{client_id}", None
    raise HTTPException(
        status_code=401,
        detail="Authentication required: provide a bearer token or a client_id.",
    )


@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    request: ChatRequest,
    raw_token: Optional[str] = Depends(get_optional_raw_token),
    _rate_limited: None = Depends(enforce_chat_rate_limit),
    chat_service: IChatService = Depends(get_chat_service),
    freemium_service: FreemiumService = Depends(get_freemium_service_singleton),
):
    """
    Orchestrated Chat Endpoint routing via ChatService.
    """
    _require_identity(raw_token, request.client_id)
    identity, _token = _resolve_identity_for_freemium(raw_token, request.client_id)
    try:
        await freemium_service.check_and_consume(identity, _token, client_id=request.client_id)
    except FreemiumLimitExceeded as e:
        raise HTTPException(status_code=429, detail=e.status.to_dict())

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
    raw_token: Optional[str] = Depends(get_optional_raw_token),
    _rate_limited: None = Depends(enforce_chat_rate_limit),
    chat_service: IChatService = Depends(get_chat_service),
    freemium_service: FreemiumService = Depends(get_freemium_service_singleton),
):
    """
    Streaming Chat Endpoint routing via ChatService.
    """
    _require_identity(raw_token, request.client_id)
    identity, _token = _resolve_identity_for_freemium(raw_token, request.client_id)
    try:
        await freemium_service.check_and_consume(identity, _token, client_id=request.client_id)
    except FreemiumLimitExceeded as e:
        raise HTTPException(status_code=429, detail=e.status.to_dict())

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
