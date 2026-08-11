from typing import Dict, Type
from app.tools.infrastructure.mitre.interfaces.i_mitre_provider import IMitreProvider

class MitreProviderFactory:
    _registry: Dict[str, Type[IMitreProvider]] = {}
    
    @classmethod
    def register(cls, name: str, provider_cls: Type[IMitreProvider]) -> None:
        cls._registry[name] = provider_cls
        
    @classmethod
    def create(cls, name: str, **kwargs) -> IMitreProvider:
        if name not in cls._registry:
            raise ValueError(f"MitreProvider '{name}' not registered.")
        return cls._registry[name](**kwargs)
