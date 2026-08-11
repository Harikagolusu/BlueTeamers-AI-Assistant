from abc import ABC, abstractmethod
from app.planning.models.plan import Capability

class IExecutionEngineResolver(ABC):
    @abstractmethod
    def resolve(self, capability: Capability) -> str:
        """
        Maps a logical planning capability to a concrete Engine name in the registry.
        """
        pass
