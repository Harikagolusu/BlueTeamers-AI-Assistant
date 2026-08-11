from typing import Dict, Type
from app.tools.infrastructure.search.interfaces.i_search_provider import ISearchProvider

class SearchProviderFactory:
    _registry: Dict[str, Type[ISearchProvider]] = {}
    
    @classmethod
    def register(cls, name: str, provider_cls: Type[ISearchProvider]) -> None:
        cls._registry[name] = provider_cls
        
    @classmethod
    def create(cls, name: str, **kwargs) -> ISearchProvider:
        if name not in cls._registry:
            raise ValueError(f"SearchProvider '{name}' not registered.")
        return cls._registry[name](**kwargs)
