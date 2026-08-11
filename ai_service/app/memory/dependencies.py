from fastapi import Depends
from app.core.config import settings
from app.memory.interfaces import BaseMemoryStore
from app.memory.memory_store import SQLiteStore
from app.memory.memory_service import MemoryService
from app.memory.health import MemoryHealthService

# Singleton store instance backed by SQLite for durable, restart-safe memory.
_store_instance = SQLiteStore(db_path=settings.MEMORY_DB_PATH)

def get_memory_store() -> BaseMemoryStore:
    return _store_instance

from app.observability.service import ObservabilityService
from app.observability.dependencies import get_observability_service

def get_memory_service(
    store: BaseMemoryStore = Depends(get_memory_store),
    obs: ObservabilityService = Depends(get_observability_service)
) -> MemoryService:
    return MemoryService(
        store=store,
        enabled=settings.MEMORY_ENABLED,
        max_messages=settings.MEMORY_WINDOW,
        obs=obs
    )

def get_memory_health_service(
    store: BaseMemoryStore = Depends(get_memory_store)
) -> MemoryHealthService:
    return MemoryHealthService(
        store=store,
        enabled=settings.MEMORY_ENABLED
    )
