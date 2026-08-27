"""Lazy, side-effect-safe token usage recorder for the chat pipeline.

The RuntimeMiddleware (a BaseHTTPMiddleware) cannot see the LLM token usage
recorded deeper in the request: Starlette runs the inner app in a separate
task, and contextvars set there do not propagate back to the middleware. The
correct place to persist usage is therefore the request-handling task itself —
``ChatService.process_request`` — where the session scope is known and the
runtime context still carries the tokens the LLM provider recorded.

This module exposes a tiny async helper so ``ChatService`` can record usage
without importing the runtime dependencies graph (which would be circular).
"""

import logging

logger = logging.getLogger("app.runtime.token_usage_recorder")

_manager = None


async def record_tokens(scope: str, tokens: int, display_name: str = None, email: str = None) -> None:
    """Persist ``tokens`` consumed by ``scope`` (daily + monthly windows).

    No-op when tracking is disabled or when there is nothing to bill. The call
    is best-effort: accounting failures must never break the user's answer.
    When ``display_name``/``email`` is supplied (authenticated users) it is
    stored so ``overview`` can render human-readable names.
    """
    global _manager
    if not scope or not tokens or int(tokens) <= 0:
        return
    try:
        from app.core.config import settings

        if not settings.TOKEN_QUOTA_ENABLED:
            return
        if _manager is None:
            from app.runtime.services.token_usage_store import TokenUsageStore
            from app.runtime.services.token_quota_manager import PersistentTokenQuotaManager

            store = TokenUsageStore(db_path=settings.TOKEN_QUOTA_DB_PATH)
            _manager = PersistentTokenQuotaManager(
                store=store,
                daily_limit=settings.TOKEN_DAILY_LIMIT,
                monthly_limit=settings.TOKEN_MONTHLY_LIMIT,
                enforce=settings.TOKEN_QUOTA_ENFORCE,
            )
        await _manager.increment_usage(scope, int(tokens), display_name=display_name, email=email)
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("Failed to record token usage for %s: %s", scope, exc)