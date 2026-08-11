from abc import ABC, abstractmethod
from typing import Any

class ISecurityContextProvider(ABC):
    @abstractmethod
    def get_context(self) -> Any: pass
    @abstractmethod
    def set_context(self, context: Any) -> None: pass
    @abstractmethod
    def clear_context(self) -> None: pass
