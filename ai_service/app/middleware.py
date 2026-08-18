from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
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

_JSON_413_BODY = b'{"detail":"Request body too large."}'


class MaxBodySizeMiddleware:
    """Pure-ASGI middleware enforcing the body cap on the **actual bytes
    received**, not the ``Content-Length`` header.

    A client that sends ``Transfer-Encoding: chunked`` supplies no
    ``Content-Length``, so a header-only check never fired for those requests,
    allowing oversized bodies past the limit (potential memory/CPU DoS). This
    middleware consumes the request body itself for POST/PUT/PATCH requests and
    counts the bytes: the moment the running total crosses the cap it stops
    reading and answers 413, so the downstream parse never sees more than the
    cap. Bodies within the cap are replayed transparently to the rest of the
    stack (bounded by the cap, so at most ~2x the cap is ever buffered).

    Being pure ASGI (no BaseHTTPMiddleware request buffering / StreamingResponse
    re-entrancy), it composes cleanly with the chat endpoints, including the
    SSE ``/api/v1/chat/stream`` route that the previous body-reading variant had
    to exclude.
    """

    def __init__(self, app: ASGIApp, max_bytes: int = MAX_BODY_BYTES):
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Fast path: a declared Content-Length over the cap is rejected without
        # reading anything.
        for name, value in (scope.get("headers") or []):
            if name == b"content-length":
                try:
                    content_length = int(value)
                except ValueError:
                    content_length = None
                if content_length is not None and content_length > self.max_bytes:
                    return await self._reject(send)
                break

        if (scope.get("method") or "").upper() in ("POST", "PUT", "PATCH"):
            buffered, over, disconnected = await self._drain(receive)
            if disconnected:
                return  # client hung up mid-body; nothing to answer
            if over:
                return await self._reject(send)
            if buffered is not None:
                receive = self._serve_body(buffered, receive)

        await self.app(scope, receive, send)

    async def _drain(self, receive: Receive) -> tuple[bytes | None, bool, bool]:
        """Consume the request body once, enforcing the cap on actual bytes.

        Returns ``(buffered, over, disconnected)``: the body bytes when it fit
        within the cap, whether it exceeded the cap (read is stopped early), and
        whether the client disconnected before the body was complete.
        """
        buffered = bytearray()
        while True:
            message = await receive()
            mtype = message.get("type")
            if mtype == "http.request":
                body = message.get("body") or b""
                if body:
                    buffered.extend(body)
                    if len(buffered) > self.max_bytes:
                        return None, True, False
                if not message.get("more_body", False):
                    break
            elif mtype == "http.disconnect":
                return None, False, True
        return bytes(buffered), False, False

    @staticmethod
    def _serve_body(body: bytes, receive: Receive) -> Receive:
        served = False

        async def wrapped_receive():
            nonlocal served
            if not served:
                served = True
                return {
                    "type": "http.request",
                    "body": body,
                    "more_body": False,
                }
            return await receive()

        return wrapped_receive

    @staticmethod
    async def _reject(send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": 413,
                "headers": [
                    (b"content-type", b"application/json"),
                    (b"content-length", str(len(_JSON_413_BODY)).encode()),
                ],
            }
        )
        await send(
            {"type": "http.response.body", "body": _JSON_413_BODY, "more_body": False}
        )


def setup_middlewares(app: FastAPI):
    """
    Registers all production-ready middlewares.
    Includes:
    - Request Body Size Limit
    - CORS Middleware
    - Request ID, Timing, and Structured Logging Middleware
    """

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

    # MaxBodySize registered LAST so Starlette wraps it outermost: oversized
    # bodies are rejected (413) before CORS/logging/observability run.
    app.add_middleware(MaxBodySizeMiddleware)