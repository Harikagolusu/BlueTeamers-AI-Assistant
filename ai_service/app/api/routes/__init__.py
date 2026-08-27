from fastapi import APIRouter
from .chat import router as chat_router
from .health import router as health_router
from .protected import router as protected_router
from .token_usage import router as token_usage_router

router = APIRouter()
router.include_router(chat_router, prefix="/chat")
router.include_router(health_router)
router.include_router(protected_router)
router.include_router(token_usage_router)
