from abc import ABC, abstractmethod
from typing import Dict, Any

class ILogFormatter(ABC):
    @abstractmethod
    def format(self, level: str, message: str, context: Dict[str, Any]) -> str: pass

class ILogSink(ABC):
    @abstractmethod
    async def write(self, formatted_log: str) -> None: pass

class ILogger(ABC):
    @abstractmethod
    def trace(self, message: str, **kwargs) -> None: pass
    @abstractmethod
    def debug(self, message: str, **kwargs) -> None: pass
    @abstractmethod
    def info(self, message: str, **kwargs) -> None: pass
    @abstractmethod
    def warning(self, message: str, **kwargs) -> None: pass
    @abstractmethod
    def error(self, message: str, **kwargs) -> None: pass
    @abstractmethod
    def critical(self, message: str, **kwargs) -> None: pass
