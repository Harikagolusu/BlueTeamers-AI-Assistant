from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware import LoggingMiddleware
from app.observability.service_middleware import ObservabilityMiddleware
from app.observability.dependencies import get_observability_service

from app.core.config import settings

def setup_middlewares(app: FastAPI):
    """
    Registers all production-ready middlewares.
    Includes:
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
