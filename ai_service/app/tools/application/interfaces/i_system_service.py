from abc import ABC, abstractmethod
from app.tools.domain.schemas.system_schemas import (
    EnvironmentSchema, ConfigSchema, PlatformSchema, VersionSchema
)
from app.tools.domain.results.system_results import (
    EnvironmentResult, ConfigResult, PlatformResult, VersionResult
)

class ISystemService(ABC):
    """
    Application interface for system utilities.
    """
    @abstractmethod
    async def get_environment(self, schema: EnvironmentSchema) -> EnvironmentResult:
        pass

    @abstractmethod
    async def get_config(self, schema: ConfigSchema) -> ConfigResult:
        pass

    @abstractmethod
    async def get_platform(self, schema: PlatformSchema) -> PlatformResult:
        pass

    @abstractmethod
    async def get_version(self, schema: VersionSchema) -> VersionResult:
        pass
