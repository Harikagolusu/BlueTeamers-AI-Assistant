"""REST API for the user's language preference (Feature 2 & 3).

- ``GET  /api/language/preference`` — the user's stored language mode
  (``auto`` when none was ever set).
- ``PUT  /api/language/preference`` — set the preference (a concrete language
  code or ``auto``).
- ``DELETE /api/language/preference`` — reset to Auto Detect.

All endpoints require a Bearer JWT and are scoped to the authenticated user.
Guests (no JWT) fall back to client-side localStorage, so no guest handling is
required here.
"""
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.api.dependencies import get_optional_raw_token
from app.multilingual.dependencies import get_language_preference_store
from app.multilingual.languages import is_supported_code
from app.multilingual.preferences import LanguagePreferenceStore
from app.security.auth import resolve_user_identity

logger = logging.getLogger("app.api.language")

router = APIRouter()

DEFAULT_LANGUAGE = "auto"


class LanguagePreferenceRequest(BaseModel):
    language: str


def _require_user(token: Optional[str]) -> str:
    """Resolve the authenticated user id; raise 401 when anonymous."""
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id, _email = resolve_user_identity(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id


@router.get("/preference")
async def get_language_preference(
    raw_token: Optional[str] = Depends(get_optional_raw_token),
    store: LanguagePreferenceStore = Depends(get_language_preference_store),
):
    """Return the stored language preference for the authenticated user."""
    user_id = _require_user(raw_token)
    language = await store.get(user_id)
    return {"language": language or DEFAULT_LANGUAGE}


@router.put("/preference")
async def set_language_preference(
    request: LanguagePreferenceRequest,
    raw_token: Optional[str] = Depends(get_optional_raw_token),
    store: LanguagePreferenceStore = Depends(get_language_preference_store),
):
    """Persist the authenticated user's preferred language mode."""
    user_id = _require_user(raw_token)
    language = (request.language or "").strip()
    if not is_supported_code(language):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported language code: {language!r}",
        )
    if language == DEFAULT_LANGUAGE:
        await store.clear(user_id)
        return {"language": DEFAULT_LANGUAGE}
    await store.set(user_id, language)
    return {"language": language}


@router.delete("/preference", status_code=status.HTTP_200_OK)
async def delete_language_preference(
    raw_token: Optional[str] = Depends(get_optional_raw_token),
    store: LanguagePreferenceStore = Depends(get_language_preference_store),
):
    """Reset the preference to Auto Detect."""
    user_id = _require_user(raw_token)
    await store.clear(user_id)
    return {"language": DEFAULT_LANGUAGE}