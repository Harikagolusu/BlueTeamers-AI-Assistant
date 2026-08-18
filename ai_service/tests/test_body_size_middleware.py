"""Regression tests for the request-body size limit (16 MiB ceiling).

The historic flaw: MaxBodySizeMiddleware only enforced the cap via the
``Content-Length`` header, so ``Transfer-Encoding: chunked`` requests (which
carry no Content-Length) sailed straight past the limit and reached the
chat endpoints (potentially multi-GB bodies -> memory/CPU DoS). The
middleware now consumes and counts the *actual* received bytes.
"""
import asyncio
import json

import pytest
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.middleware import MaxBodySizeMiddleware

MAX = 16 * 1024 * 1024


class _Body(BaseModel):
    query: str
    pad: str | None = None


class _Inner(BaseHTTPMiddleware):
    """Mirror the real stack: streamed responses flow through BaseHTTP layers."""

    async def dispatch(self, request, call_next):
        return await call_next(request)


def _make_app() -> FastAPI:
    app = FastAPI()

    @app.post("/chat")
    async def chat(r: _Body):
        return JSONResponse({"len": len(r.pad or "")})

    app.add_middleware(_Inner)
    app.add_middleware(MaxBodySizeMiddleware, max_bytes=MAX)
    return app


def _run(scope, receive, send):
    app = _make_app()
    return asyncio.run(MaxBodySizeMiddleware(app, max_bytes=MAX)(scope, receive, send))


def _chunked_scope(method="POST"):
    return {
        "type": "http",
        "method": method,
        "scheme": "http",
        "path": "/chat",
        "raw_path": "/chat",
        "query_string": b"",
        "root_path": "",
        "headers": [
            (b"host", b"testserver"),
            (b"content-type", b"application/json"),
        ],  # NO content-length -> chunked framing
        "client": ("127.0.0.1", 12345),
        "server": ("testserver", 80),
        "http_version": "1.1",
    }


def _content_length_scope(length: int):
    scope = _chunked_scope()
    scope["headers"] = scope["headers"] + [
        (b"content-length", str(length).encode()),
    ]
    return scope


class _Receiver:
    """Simulates an ASGI server feeding the body in chunks."""

    def __init__(self, body: bytes, chunk_size: int = 65536):
        self.body = body
        self.chunk_size = chunk_size or len(body)
        self.offset = 0

    async def __call__(self):
        if self.offset < len(self.body):
            chunk = self.body[self.offset : self.offset + self.chunk_size]
            self.offset += len(chunk)
            return {
                "type": "http.request",
                "body": chunk,
                "more_body": self.offset < len(self.body),
            }
        return {"type": "http.request", "body": b"", "more_body": False}


class _Collector:
    def __init__(self):
        self.messages = []

    async def __call__(self, message):
        self.messages.append(message)


def _status(collector):
    for m in collector.messages:
        if m["type"] == "http.response.start":
            return m["status"]
    return None


def _response_body(collector):
    return b"".join(
        m.get("body", b"")
        for m in collector.messages
        if m["type"] == "http.response.body"
    )


def test_content_length_over_cap_is_413():
    collector = _Collector()
    _run(_content_length_scope(MAX + 1), _Receiver(b"{}"), collector)
    assert _status(collector) == 413
    assert b"Request body too large" in _response_body(collector)


def test_chunked_over_cap_is_413():
    """The reported bug: chunked encoding must not bypass the 16 MiB cap."""
    big = json.dumps({"query": "x", "pad": "z" * (MAX + 1)}).encode()
    collector = _Collector()
    _run(_chunked_scope(), _Receiver(big), collector)
    assert _status(collector) == 413
    assert b"Request body too large" in _response_body(collector)


def test_chunked_exactly_at_cap_is_allowed():
    pad = "z" * (MAX - 32)
    body = json.dumps({"query": "x", "pad": pad}).encode()
    assert len(body) <= MAX
    collector = _Collector()
    _run(_chunked_scope(), _Receiver(body, chunk_size=1_000_000), collector)
    assert _status(collector) == 200
    assert json.loads(_response_body(collector)) == {"len": len(pad)}


def test_chunked_small_body_is_replayed_intact():
    body = json.dumps({"query": "hello", "pad": None}).encode()
    collector = _Collector()
    _run(_chunked_scope(), _Receiver(body, chunk_size=3), collector)
    assert _status(collector) == 200
    assert json.loads(_response_body(collector)) == {"len": 0}


def test_get_with_body_not_size_checked():
    collector = _Collector()
    _run(_chunked_scope(method="GET"), _Receiver(b"x" * (MAX + 10)), collector)
    # GET has no route -> FastAPI 405, but crucially not a 413 abort.
    assert _status(collector) in (405, 404)