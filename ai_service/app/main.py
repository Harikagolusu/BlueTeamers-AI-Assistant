from fastapi import FastAPI

from app.core.config import settings
from app.lifecycle import lifespan
from app.middleware import setup_middlewares
from app.exception_handlers import setup_exception_handlers

# Routers
from app.health import router as health_router
from app.api.routes import router as api_router          # ChatOrchestrator path (correct)
from app.chat.router import router as legacy_chat_router  # RAGService path (kept for /api/v1/chat/* legacy endpoints)
from app.observability.router import router as obs_router
from app.knowledge.router import router as knowledge_router
from app.conversations.router import router as conversations_router
from app.multilingual.router import router as language_router

# ========================================================
# Application Configuration
# ========================================================
app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise API integration layer for BlueTeamers AI Assistant.",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    # Security (audit B-04): interactive API documentation and the OpenAPI
    # schema are disabled outside development so production never exposes
    # route/parameter details to unauthenticated callers.
    docs_url="/docs" if settings.DEVELOPMENT_MODE else None,
    redoc_url="/redoc" if settings.DEVELOPMENT_MODE else None,
    openapi_url="/openapi.json" if settings.DEVELOPMENT_MODE else None,
    contact={
        "name": "InfoSec Dairies AI Team",
        "email": "ai-support@infosecdairies.io",
    },
    license_info={
        "name": "Proprietary",
    },
    openapi_tags=[
        {"name": "Health", "description": "System health and status checks."},
        {"name": "Chat", "description": "Conversational AI endpoints powered by the RAG Engine."},
    ]
)

# ========================================================
# Wiring (Middlewares, Exception Handlers)
# ========================================================
setup_middlewares(app)
setup_exception_handlers(app)

# ========================================================
# Router Registration
# ========================================================
# Primary chat path: ChatOrchestrator -> IntentAnalysis -> QueryRouter -> Engine
# Endpoint: POST /api/chat/
app.include_router(api_router, prefix="/api")

# Legacy chat path: RAGService direct (kept for backwards compatibility with /api/v1/chat/*)
app.include_router(legacy_chat_router)

app.include_router(obs_router)
app.include_router(health_router)
app.include_router(knowledge_router)
app.include_router(conversations_router, prefix="/api/conversations")
app.include_router(language_router, prefix="/api/language")
