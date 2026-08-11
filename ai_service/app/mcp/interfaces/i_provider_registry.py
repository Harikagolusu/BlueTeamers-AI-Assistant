from abc import ABC, abstractmethod
from typing import List, Optional
from app.mcp.interfaces.i_tool_provider import IToolProvider

class IProviderRegistry(ABC):
    @abstractmethod
    def register(self, provider: IToolProvider) -> None:
        pass
        
    @abstractmethod
    def resolve(self, provider_id: str) -> Optional[IToolProvider]:
        pass
        
    @abstractmethod
    def remove(self, provider_id: str) -> None:
        pass
        
    @abstractmethod
    def list_providers(self) -> List[IToolProvider]:
        pass
