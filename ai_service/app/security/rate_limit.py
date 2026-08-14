"""In-process rate limiting for chat endpoints.

A simple fixed-window counter keyed by the authenticated user's stable
user_id (when a valid bearer token is present) or by client IP otherwise.
Suitable for a single-instance deployment; swap for Redis when scaling
horizontally.

The client IP is taken from the transport peer (request.client), NOT from
X-Forwarded-For, so a remote attacker can't rotate a spoofed header to reset
the limit. Deployments behind a trusted proxy must configure it via
`--forwarded-allow-ips` / proxy headers so the peer is the real client.
"""
import time
import threading
from typing import Dict, Tuple

from fastapi import Request, HTTPException

from app.core.config import settings

# Upper bound on tracked windows to avoid an unbounded dictionary when many
# distinct identities hit the limiter (post-auth clean-up on reset too).
_MAX_WINDOWS = 100_000


class FixedWindowLimiter:
    def __init__(self):
        self._lock = threading.Lock()
        self._windows: Dict[str, Tuple[float, int]] = {}

    def check(self, key: str, limit: int, window_seconds: int) -> bool:
        now = time.monotonic()
        with self._lock:
            if len(self._windows) >= _MAX_WINDOWS:
                # Evict the oldest-keyed entries (dict preserves insertion order).
                for stale_key in list(self._windows)[: _MAX_WINDOWS // 10]:
                    self._windows.pop(stale_key, None)
            start, count = self._windows.get(key, (now, 0))
            if now - start >= window_seconds:
                start, count = now, 0
            if count >= limit:
                self._windows[key] = (start, count)
                return False
            self._windows[key] = (start, count + 1)
            return True

    def reset(self, key: str) -> None:
        with self._lock:
            self._windows.pop(key, None)

    def clear(self) -> None:
        """Drop all windows. Used by tests to avoid cross-test interference."""
        with self._lock:
            self._windows.clear()


_limiter = FixedWindowLimiter()


def _client_ident(request: Request) -> str:
    """Identify the caller: authenticated user_id if possible, else client IP.

    The IP is the transport peer only — never the X-Forwarded-For header —
    so a client cannot rotate a spoofed header to evade the limit.
    """
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        token = auth[7:].strip()
        if token:
            try:
                from app.security.auth import resolve_user_identity
                user_id, _email = resolve_user_identity(token)
                if user_id:
                    return f"user:{user_id}"
            except Exception:
                pass
    host = request.client.host if request.client else "unknown"
    return f"ip:{host}"


def enforce_chat_rate_limit(request: Request) -> None:
    """FastAPI dependency: 429 when the caller exceeds the chat rate limit."""
    if not settings.CHAT_RATE_LIMIT_ENABLED:
        return

    key = _client_ident(request)
    if not _limiter.check(
        key,
        limit=settings.CHAT_RATE_LIMIT,
        window_seconds=settings.CHAT_RATE_WINDOW_SECONDS,
    ):
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Try again in {settings.CHAT_RATE_WINDOW_SECONDS}s.",
            headers={"Retry-After": str(settings.CHAT_RATE_WINDOW_SECONDS)},
        )
