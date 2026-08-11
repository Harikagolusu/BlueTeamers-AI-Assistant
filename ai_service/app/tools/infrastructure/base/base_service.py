from abc import ABC
import logging
from enum import Enum
from typing import Optional

class ServiceState(Enum):
    UNINITIALIZED = "UNINITIALIZED"
    INITIALIZING = "INITIALIZING"
    INITIALIZED = "INITIALIZED"
    FAILED = "FAILED"
    STOPPED = "STOPPED"

class BaseService(ABC):
    """
    Abstract base service providing lifecycle hooks.
    """
    def __init__(self):
        self._state = ServiceState.UNINITIALIZED
        self._logger = logging.getLogger(self.__class__.__name__)

    async def initialize(self) -> None:
        """Called once during startup. Fails safely."""
        try:
            self._state = ServiceState.INITIALIZING
            await self._on_initialize()
            self._state = ServiceState.INITIALIZED
        except Exception as e:
            self._state = ServiceState.FAILED
            self._logger.error(f"Failed to initialize {self.__class__.__name__}: {e}")

    async def _on_initialize(self) -> None:
        """Override to implement specific initialization logic."""
        pass

    async def shutdown(self) -> None:
        """Called during graceful termination."""
        await self._on_shutdown()
        self._state = ServiceState.STOPPED

    async def _on_shutdown(self) -> None:
        """Override to implement specific shutdown logic."""
        pass

    def health_check(self) -> bool:
        """Returns True if the service is healthy."""
        return self._state == ServiceState.INITIALIZED

    async def reset(self) -> None:
        """Resets the service state."""
        await self.shutdown()
        await self.initialize()
