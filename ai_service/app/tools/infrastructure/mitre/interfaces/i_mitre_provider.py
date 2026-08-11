from abc import ABC, abstractmethod
from typing import Optional
from app.tools.domain.models.mitre_models import MitreTechnique, MitreTactic, MitreGroup, MitreSoftware
from app.tools.infrastructure.providers.models import ProviderHealth

class IMitreProvider(ABC):
    @abstractmethod
    async def get_technique(self, technique_id: str) -> Optional[MitreTechnique]:
        pass

    @abstractmethod
    async def get_tactic(self, tactic_id: str) -> Optional[MitreTactic]:
        pass

    @abstractmethod
    async def get_group(self, group_name: str) -> Optional[MitreGroup]:
        pass

    @abstractmethod
    async def get_software(self, software_name: str) -> Optional[MitreSoftware]:
        pass
        
    @abstractmethod
    async def health_check(self) -> ProviderHealth:
        pass
