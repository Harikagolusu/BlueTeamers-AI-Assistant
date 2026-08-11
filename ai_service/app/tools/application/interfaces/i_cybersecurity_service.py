from abc import ABC, abstractmethod
from app.tools.domain.schemas.cybersecurity_schemas import (
    ThreatSchema, IocSchema, HashReputationSchema, UrlValidationSchema, IpUtilitySchema
)
from app.tools.domain.results.cybersecurity_results import (
    ThreatResult, IocResult, HashReputationResult, UrlValidationResult, IpUtilityResult
)

class ICybersecurityService(ABC):
    """
    Application interface for cybersecurity utilities.
    """
    @abstractmethod
    async def lookup_threat(self, schema: ThreatSchema) -> ThreatResult:
        pass

    @abstractmethod
    async def lookup_ioc(self, schema: IocSchema) -> IocResult:
        pass

    @abstractmethod
    async def check_hash_reputation(self, schema: HashReputationSchema) -> HashReputationResult:
        pass

    @abstractmethod
    async def validate_url(self, schema: UrlValidationSchema) -> UrlValidationResult:
        pass

    @abstractmethod
    async def get_ip_utility(self, schema: IpUtilitySchema) -> IpUtilityResult:
        pass
