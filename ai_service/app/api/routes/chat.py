from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException

from app.models.chat.chat_models import ChatRequest, ChatResponse
from app.chat.interfaces.i_chat_service import IChatService
from app.api.dependencies import get_optional_raw_token
from app.freemium.dependencies import get_freemium_service_singleton
from app.freemium.models import AccessStatus, FreemiumLimitExceeded
from app.freemium.service import FreemiumService
from app.security.auth import resolve_user_identity

# In a real app we'd import get_chat_service from app.chat.dependencies
# from app.chat.dependencies import get_chat_service

router = APIRouter()

from app.chat.bootstrap import get_chat_service

# Guest identities (no login) are tracked under a namespaced key derived from
# the persistent browser client id, so anonymous users also get the daily
# allowance. Authenticated users are resolved from the JWT and can be premium.
GUEST_ID_PREFIX = "guest:"


def _resolve_identity(
    raw_token: Optional[str], client_id: Optional[str] = None
) -> tuple:
    """Resolve (tracking_identity, token) for freemium.

    - Valid JWT  -> (user_id from token, token) so premium status applies.
    - No token but a client id (guest) -> (guest:<client_id>, None); guests are
      always free and are rate-limited like registered free users.
    - Neither -> (None, None); fully anonymous callers stay unlimited/untracked.
    """
    if raw_token:
        user_id, _email = resolve_user_identity(raw_token)
        return user_id, raw_token
    if client_id:
        return f"{GUEST_ID_PREFIX}{client_id}", None
    return None, None


def _request_user_id(raw_token: Optional[str]) -> Optional[str]:
    """Resolve the authenticated user_id from the JWT (None when anonymous)."""
    if not raw_token:
        return None
    user_id, _email = resolve_user_identity(raw_token)
    return user_id


def _limit_exceeded_detail(e: FreemiumLimitExceeded, identity: Optional[str]) -> dict:
    """Build the 429 payload. Guests are told to login+join; signed-in free
    users are told to purchase a course."""
    if identity and identity.startswith(GUEST_ID_PREFIX):
        message = (
            "You've reached today's free AI limit. Login and join a BlueTeamers "
            "course to unlock unlimited AI assistance and the full AI Workspace."
        )
    else:
        message = (
            "You've reached today's free AI limit. Purchase any BlueTeamers "
            "course to unlock unlimited AI assistance and the full AI Workspace."
        )
    return {
        "message": message,
        "code": "free_ai_limit_reached",
        "access": e.status.to_dict(),
    }


@router.get("/access", response_model=AccessStatus)
async def chat_access_endpoint(
    raw_token: Optional[str] = Depends(get_optional_raw_token),
    client_id: Optional[str] = None,
    freemium_service: FreemiumService = Depends(get_freemium_service_singleton),
):
    """
    Report the caller's AI access status for the freemium model.

    Free users (registered or guests identified by ``client_id``) see their
    daily allowance ("X / Y AI messages remaining today"); premium users see an
    unlimited (is_premium) status. The frontend uses this to render the usage
    indicator and the /chat workspace gate.
    """
    identity, token = _resolve_identity(raw_token, client_id)
    status = await freemium_service.get_access_status(identity, token, client_id=client_id)
    return status


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    raw_token: Optional[str] = Depends(get_optional_raw_token),
    chat_service: IChatService = Depends(get_chat_service),
    freemium_service: FreemiumService = Depends(get_freemium_service_singleton),
):
    """
    Main entry point for Chat integration.

    The JWT may arrive either in the request body (``request.token``) or, as
    the web client sends it, in the Authorization header. When the header is
    present and the body carries no token, the header wins so authenticated
    features (conversation persistence, memory, adaptive learning, platform
    context) work end-to-end.

    Freemium: free users (registered or guests carrying a persistent
    ``client_id``) may send up to ``FREEMIUM_FREE_MESSAGE_LIMIT`` messages per
    reset window. Requests beyond the limit are rejected with 429 and an
    upgrade payload; premium users are never limited.
    """
    if not request.token and raw_token:
        request.token = raw_token

    identity, token = _resolve_identity(raw_token, request.client_id)
    try:
        await freemium_service.check_and_consume(identity, token, client_id=request.client_id)
    except FreemiumLimitExceeded as e:
        raise HTTPException(
            status_code=429,
            detail=_limit_exceeded_detail(e, identity),
        )

    result = await chat_service.process_request(request)

    if request.stream:
        return StreamingResponse(result, media_type="text/event-stream")

    return result
