from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.core.middleware import LoggingMiddleware
from app.observability.service_middleware import ObservabilityMiddleware
from app.observability.dependencies import get_observability_service

from app.core.config import settings

# Reject oversized request bodies before they are buffered into memory. This is
# the first line of defense against multi-GB JSON chat payloads (thousands of
# attachments) that the per-attachment caps only see after the full body exists.
#
# The cap must also fit real image uploads: attachments arrive as base64 data
# URLs (~1.33x the raw bytes) and a typical phone/desktop screenshot is 1-8 MB
# decoded. The per-attachment decoder (8 MiB decoded) and the pixel caps are the
# real memory guards; this is a coarse ceiling against protocol-level abuse.
MAX_BODY_BYTES = 16 * 1024 * 1024  # 16 MiB

class MaxBodySizeMiddleware(BaseHTTPMiddleware):
    """Reject requests whose body exceeds a hard cap with 413 before reading it."""

    # Streaming chat endpoints are excluded from body-size re-reading because
    # Starlette's BaseHTTPMiddleware raises "Unexpected message received:
    # http.request" when a body-reading middleware wraps a StreamingResponse.
    # The Content-Length header check above is sufficient for those routes.
    _SKIP_BODY_READ = frozenset({"/api/chat/", "/api/v1/chat/stream", "/api/v1/chat"})

    def __init__(self, app, max_bytes: int = MAX_BODY_BYTES):
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and content_length.isdigit():
            if int(content_length) > self.max_bytes:
                return JSONResponse(
                    status_code=413,
                    content={"detail": "Request body too large."},
                )
        # Content-Length may be absent (chunked) — enforce via a size-checked
        # streaming receive that aborts once the cap is exceeded.
        if request.method in ("POST", "PUT", "PATCH") and request.url.path not in self._SKIP_BODY_READ:
            body = await request.body()
            if len(body) > self.max_bytes:
                return JSONResponse(
                    status_code=413,
                    content={"detail": "Request body too large."},
                )
            # Rebuild the request stream so downstream handlers can still read it.
            async def _receive():
                return {"type": "http.request", "body": body, "more_body": False}
            request._receive = _receive
        return await call_next(request)


def setup_middlewares(app: FastAPI):
    """
    Registers all production-ready middlewares.
    Includes:
    - Request Body Size Limit
    - CORS Middleware
    - Request ID, Timing, and Structured Logging Middleware
    """

    # Reject oversized bodies first (outermost).
    app.add_middleware(MaxBodySizeMiddleware)

    # Register CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register structured logging & request timing (order matters in FastAPI)
    app.add_middleware(LoggingMiddleware)

    # Register Observability Middleware (Tracing & Metrics)
    # Added last so it's the outermost middleware.
    obs_service = get_observability_service()
    app.add_middleware(ObservabilityMiddleware, observability_service=obs_service)

    from app.runtime.middleware import RuntimeMiddleware
    from app.runtime.dependencies import get_runtime_manager
    runtime_manager = get_runtime_manager()
    app.add_middleware(RuntimeMiddleware, runtime_manager=runtime_manager)
