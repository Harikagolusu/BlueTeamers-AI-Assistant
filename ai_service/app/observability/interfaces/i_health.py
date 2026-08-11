from abc import ABC, abstractmethod
from typing import Dict, Any

class IHealthCheck(ABC):
    @abstractmethod
    async def check_health(self) -> Dict[str, Any]: pass

class IHealthRegistry(ABC):
    @abstractmethod
    def register_check(self, name: str, check: IHealthCheck) -> None: pass
    @abstractmethod
    def get_checks(self) -> Dict[str, IHealthCheck]: pass

class IHealthMonitor(ABC):
    @abstractmethod
    def get_status(self) -> Dict[str, Any]: pass

class IHealthScheduler(ABC):
    @abstractmethod
    def start(self) -> None: pass
    @abstractmethod
    def stop(self) -> None: pass
