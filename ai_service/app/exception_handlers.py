from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.rag.exceptions import BaseRAGException
from app.core.logging import log_http_exception, log_validation_error, log_unhandled_exception
import logging

logger = logging.getLogger("app.exceptions")

from fastapi.encoders import jsonable_encoder

def setup_exception_handlers(app: FastAPI):
    """
    Registers global exception handlers for the application.
    """
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        log_http_exception(exc)
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        log_validation_error(exc)
        return JSONResponse(
            status_code=422,
            content={"detail": jsonable_encoder(exc.errors())},
        )

    @app.exception_handler(BaseRAGException)
    async def rag_domain_exception_handler(request: Request, exc: BaseRAGException):
        # We catch any unhandled BaseRAGException escaping the routers
        logger.error(f"Unhandled Domain Exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal domain fault occurred."},
        )

    from app.memory.exceptions import MemoryException
    @app.exception_handler(MemoryException)
    async def memory_exception_handler(request: Request, exc: MemoryException):
        logger.error(f"Memory Exception: {str(exc)}")
        # Memory exceptions are usually domain errors that shouldn't crash the request
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal memory fault occurred."},
        )

    from app.llm.exceptions import LLMException, ProviderConfigurationException
    @app.exception_handler(LLMException)
    async def llm_exception_handler(request: Request, exc: LLMException):
        """Structured, provider-agnostic error for any LLM provider failure."""
        logger.error(f"LLM Provider Exception: {str(exc)}", exc_info=True)
        # Configuration faults are server-side misconfigurations; provider faults are
        # transient/unavailable states. Both are surfaced as structured errors so the
        # frontend can distinguish them from a generic 500.
        if isinstance(exc, ProviderConfigurationException):
            return JSONResponse(
                status_code=500,
                content={"detail": str(exc), "code": exc.__class__.__name__},
            )
        return JSONResponse(
            status_code=503,
            content={"detail": str(exc), "code": exc.__class__.__name__},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        log_unhandled_exception(exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )
