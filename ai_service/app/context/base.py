from abc import ABC, abstractmethod
from app.context.schemas import ContextRequest, ContextResponse

class BaseContextBuilder(ABC):
    @abstractmethod
    def build_context(self, request: ContextRequest) -> ContextResponse:
        pass
        
    @abstractmethod
    def health_check(self) -> dict:
        pass
