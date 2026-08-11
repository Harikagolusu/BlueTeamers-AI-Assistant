"""Dependency injection for the freemium subsystem (Sprint 5)."""
import logging

from app.core.config import settings
from app.freemium.service import FreemiumService
from app.freemium.store import FreemiumStore

logger = logging.getLogger("app.freemium.dependencies")

# Singleton store + service (durable SQLite-backed, restart-safe).
_store_instance = FreemiumStore(db_path=settings.FREEMIUM_DB_PATH)


def get_freemium_store() -> FreemiumStore:
    return _store_instance


def get_freemium_service() -> FreemiumService:
    """Composition root for the freemium service.

    The platform repository (Django purchases) is wired lazily so import time
    stays cheap and tests can override the dependency.
    """
    from app.platform.repositories.django_repository import DjangoPlatformRepository
    from app.platform.services.platform_client import platform_client

    try:
        platform_repo = DjangoPlatformRepository(platform_client)
    except Exception as e:  # pragma: no cover - platform client is static
        logger.warning(f"Failed to build platform repository for freemium: {e}")
        platform_repo = None
    return FreemiumService(store=_store_instance, platform_repo=platform_repo)


# Cached instance so the platform repo is built once per process.
_service_instance: FreemiumService | None = None


def get_freemium_service_singleton() -> FreemiumService:
    global _service_instance
    if _service_instance is None:
        _service_instance = get_freemium_service()
    return _service_instance
