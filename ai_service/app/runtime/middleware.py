from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.runtime.services.runtime_manager import RuntimeManager
from app.runtime.context_manager import RuntimeContextManager
import uuid
import time

def _trusted_user_id(request: Request) -> str:
    """Derive a caller identity that the client cannot spoof.

    Prefer the validated JWT (``user_id`` claim) from the Authorization header;
    fall back to the client IP otherwise. The ``x-user-id`` header is NOT
    trusted because any caller can set it to a fresh value per request and
    bypass per-user rate limits / quotas.
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


class RuntimeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, runtime_manager: RuntimeManager):
        super().__init__(app)
        self.manager = runtime_manager

    async def dispatch(self, request: Request, call_next) -> Response:
        trace_id = request.headers.get("x-trace-id", str(uuid.uuid4()))
        user_id = _trusted_user_id(request)
        session_id = request.headers.get("x-session-id", str(uuid.uuid4()))
        
        # 1. Initialize RuntimeContext lifecycle
        with RuntimeContextManager.lifecycle(trace_id=trace_id, session_id=session_id, user_id=user_id):
            start_time = time.time()
            
            # 2. Check Governance (Rate Limits, Quotas)
            # Normally we'd extract endpoint, we use path here
            allowed = await self.manager.governance.rate_limiter.check_limit(user_id, request.url.path)
            if not allowed:
                return Response(content="Rate limit exceeded", status_code=429)
                
            has_quota = await self.manager.governance.quota_manager.check_quota(user_id)
            if not has_quota:
                return Response(content="Quota exhausted", status_code=403)
                
            try:
                # 3. Execution
                response = await call_next(request)
                return response
            finally:
                # 4. Finalize Accounting & Telemetry
                duration = (time.time() - start_time) * 1000
                ctx = RuntimeContextManager.get()
                
                # Accounting Update
                total_tokens = ctx.token_usage.total_tokens
                if total_tokens > 0:
                    # In real async context, we'd need a task group or ensure this completes. 
                    # For demonstration we await it.
                    await self.manager.governance.quota_manager.increment_usage(user_id, total_tokens)
                    
                # Audit Logging
                await self.manager.governance.audit_logger.log_event("REQUEST_COMPLETED", user_id, {
                    "trace_id": trace_id,
                    "tokens": total_tokens,
                    "cost": ctx.cost.total_cost,
                    "latency_ms": duration,
                    "path": request.url.path
                })
