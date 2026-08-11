from abc import ABC, abstractmethod
from typing import Any

class IProfiler(ABC):
    @abstractmethod
    def start(self) -> None: pass
    @abstractmethod
    def stop(self) -> Any: pass
