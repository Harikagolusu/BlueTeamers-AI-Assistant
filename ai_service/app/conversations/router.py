"""REST API router for Recent Conversations & Favorites.

All endpoints require a Bearer JWT and are scoped to the authenticated user.
"""
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_optional_raw_token
from app.conversations.dependencies import get_conversation_service
from app.conversations.models import (
    ConversationCreateRequest,
    ConversationListPage,
    ConversationUpdateRequest,
)
from app.conversations.service import ConversationService
from app.security.auth import resolve_user_identity

logger = logging.getLogger("app.api.conversations")

router = APIRouter()


def _resolve_user(token: Optional[str]) -> str:
    """Resolve the authenticated user id from the JWT. Raises 401 on failure.

    Uses the stable ``user_id`` claim so conversation records match those
    written by the chat pipeline (which keys by the same identity) even after
    the access token is refreshed and the ``email`` claim disappears.
    """
    user_id, _email = resolve_user_identity(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id


@router.get("", response_model=ConversationListPage)
async def list_conversations(
    token: Optional[str] = Depends(get_optional_raw_token),
    service: ConversationService = Depends(get_conversation_service),
    filter: str = Query("recent", description="all | favorites | recent | assessment | learning | chat | ..."),
    search: Optional[str] = Query(None, description="Full-text search across title, messages, course, tags"),
    days: Optional[int] = Query(None, ge=1, le=365, description="Only conversations updated within the last N days (e.g. 7 for the sidebar)"),
    page: int = Query(1, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    """List conversations (paginated, filterable, searchable). Most recent first."""
    user_id = _resolve_user(token)
    return await service.list(user_id, filter=filter, search=search, days=days, page=page, page_size=page_size)


@router.get("/search", response_model=ConversationListPage)
async def search_conversations(
    token: Optional[str] = Depends(get_optional_raw_token),
    service: ConversationService = Depends(get_conversation_service),
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    """Search conversations by title, message content, course, tags."""
    user_id = _resolve_user(token)
    return await service.search(user_id, q, page=page, page_size=page_size)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_conversation(
    request: ConversationCreateRequest,
    token: Optional[str] = Depends(get_optional_raw_token),
    service: ConversationService = Depends(get_conversation_service),
):
    """Create a new conversation record."""
    user_id = _resolve_user(token)
    convo = await service.create(user_id, request)
    return convo.model_dump()


@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    token: Optional[str] = Depends(get_optional_raw_token),
    service: ConversationService = Depends(get_conversation_service),
):
    """Load the complete chat history for an existing conversation (resume)."""
    user_id = _resolve_user(token)
    convo = await service.open(user_id, conversation_id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return convo.model_dump()


@router.patch("/{conversation_id}")
async def update_conversation(
    conversation_id: str,
    request: ConversationUpdateRequest,
    token: Optional[str] = Depends(get_optional_raw_token),
    service: ConversationService = Depends(get_conversation_service),
):
    """Update conversation metadata (rename, favorite, pin, archive, course, ...)."""
    user_id = _resolve_user(token)
    try:
        convo = await service.update(user_id, conversation_id, request)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return convo.summarize().model_dump()


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    token: Optional[str] = Depends(get_optional_raw_token),
    service: ConversationService = Depends(get_conversation_service),
):
    """Delete a conversation and all its messages."""
    user_id = _resolve_user(token)
    ok = await service.delete(user_id, conversation_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return None


@router.post("/{conversation_id}/favorite")
async def favorite_conversation(
    conversation_id: str,
    token: Optional[str] = Depends(get_optional_raw_token),
    service: ConversationService = Depends(get_conversation_service),
):
    """Mark a conversation as a favorite."""
    user_id = _resolve_user(token)
    convo = await service.set_favorite(user_id, conversation_id, True)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return convo.summarize().model_dump()


@router.post("/{conversation_id}/unfavorite")
async def unfavorite_conversation(
    conversation_id: str,
    token: Optional[str] = Depends(get_optional_raw_token),
    service: ConversationService = Depends(get_conversation_service),
):
    """Remove a conversation from favorites."""
    user_id = _resolve_user(token)
    convo = await service.set_favorite(user_id, conversation_id, False)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return convo.summarize().model_dump()
