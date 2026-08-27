"""Report the caller's daily + monthly token usage.

Used while the team measures real consumption (colleagues testing the bot) and,
later, to let end users see how much of their daily/monthly allowance remains.
The identity matches the runtime token-quota scope (authenticated user id, or
source IP for anonymous callers).
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Optional

from app.security.auth import resolve_user_identity
from app.api.dependencies import get_optional_raw_token
from app.runtime.dependencies import get_runtime_manager
from app.runtime.services.runtime_manager import RuntimeManager

router = APIRouter()


def _scope(raw_token: Optional[str], request: Request, client_id: Optional[str] = None) -> str:
    """Derive the same scope the chat pipeline bills for this caller.

    Authenticated user -> ``user:<id>``; guest with a persistent browser id ->
    ``guest:<client_id>``; otherwise the source IP (matching the runtime
    middleware's anonymous fallback).
    """
    if raw_token:
        try:
            user_id, _email = resolve_user_identity(raw_token)
            if user_id:
                return f"user:{user_id}"
        except Exception:
            pass
    if client_id:
        return f"guest:{client_id}"
    host = request.client.host if request.client else "unknown"
    return f"ip:{host}"


def _resolve_django_display(scope: str) -> tuple:
    """Fetch (full_name, email) from Django ``accounts_user`` for ``user:<id>`` scopes.

    Best-effort: returns (None, None) for guests or on any failure. Mirrors the
    resolver in ``ChatService`` so the log shows names even before the first
    billed chat persists the meta row.
    """
    if not scope or not scope.startswith("user:"):
        return None, None
    raw_id = scope.split(":", 1)[-1]
    try:
        import pathlib, sqlite3

        candidates = [
            pathlib.Path("infosecdairies/infosec-backend/backend/db.sqlite3"),
            pathlib.Path("../infosecdairies/infosec-backend/backend/db.sqlite3"),
            pathlib.Path("/home/harika/BlueTeamers-AI-Assistant/infosecdairies/infosec-backend/backend/db.sqlite3"),
        ]
        db_path = next((p for p in candidates if p.exists()), None)
        if not db_path:
            return None, None
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT full_name, email FROM accounts_user WHERE id = ?", (raw_id,)).fetchone()
        conn.close()
        if row:
            return row["full_name"], row["email"]
    except Exception:
        pass
    return None, None


@router.get("/token-usage")
async def token_usage_endpoint(
    request: Request,
    client_id: Optional[str] = None,
    raw_token: str = Depends(get_optional_raw_token),
    runtime_manager: RuntimeManager = Depends(get_runtime_manager),
):
    quota = getattr(runtime_manager.governance, "quota_manager", None)
    if quota is None or not hasattr(quota, "get_status"):
        raise HTTPException(status_code=503, detail="Token quota unavailable")

    scope = _scope(raw_token, request, client_id)
    status = await quota.get_status(scope)
    # Enrich with human-readable name: prefer persisted meta, fall back to Django DB
    display_name = status.get("display_name")
    email = status.get("email")
    if scope.startswith("user:") and not display_name:
        dn, em = _resolve_django_display(scope)
        display_name = display_name or dn
        email = email or em
        # Also try JWT email hint if still missing
        if not email and raw_token:
            try:
                _uid, _em = resolve_user_identity(raw_token)
                email = email or _em
            except Exception:
                pass
    return {
        "scope": status["scope"],
        "display_name": display_name,
        "email": email,
        "daily": {
            "used": status["daily_used"],
            "limit": status["daily_limit"],
            "remaining": status["daily_remaining"],
            "reset": "daily (UTC midnight)",
        },
        "monthly": {
            "used": status["monthly_used"],
            "limit": status["monthly_limit"],
            "remaining": status["monthly_remaining"],
            "reset": "monthly (1st of month)",
        },
        "enforcement": ("active" if status.get("enforce") else "audit-only (recording, not blocking)"),
    }


@router.get("/token-usage/overview")
async def token_usage_overview(
    runtime_manager: RuntimeManager = Depends(get_runtime_manager),
):
    """Live consumption across every user/device (team monitor).

    Aggregates today's and this month's LLM token usage for all scopes and
    returns it sorted by daily usage (highest first). Poll this endpoint to
    watch teammates' consumption in near-real time. Missing display names for
    ``user:<id>`` scopes are backfilled from Django ``accounts_user`` so the
    log shows names even for usage recorded before name tracking was added.
    """
    quota = getattr(runtime_manager.governance, "quota_manager", None)
    if quota is None or not hasattr(quota, "overview"):
        raise HTTPException(status_code=503, detail="Token quota unavailable")

    data = await quota.overview()
    for entry in data.get("users", []):
        if entry.get("scope", "").startswith("user:") and not entry.get("display_name"):
            dn, em = _resolve_django_display(entry["scope"])
            if dn:
                entry["display_name"] = dn
            if em and not entry.get("email"):
                entry["email"] = em
    return data