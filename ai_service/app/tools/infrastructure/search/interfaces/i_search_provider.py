from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.tools.infrastructure.providers.models import ProviderHealth

class ISearchProvider(ABC):
    @abstractmethod
    async def search(self, query: str, limit: int = 10, **kwargs) -> List[Dict[str, Any]]:
        pass
        
    @abstractmethod
    async def health_check(self) -> ProviderHealth:
        pass
