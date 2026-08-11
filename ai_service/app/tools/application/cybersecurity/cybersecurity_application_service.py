import ipaddress
import urllib.parse
from app.tools.application.interfaces.i_cybersecurity_service import ICybersecurityService
from app.tools.infrastructure.base.base_service import BaseService
from app.tools.domain.schemas.cybersecurity_schemas import (
    ThreatSchema, IocSchema, HashReputationSchema, UrlValidationSchema, IpUtilitySchema
)
from app.tools.domain.results.cybersecurity_results import (
    ThreatResult, IocResult, HashReputationResult, UrlValidationResult, IpUtilityResult
)

class CybersecurityApplicationService(BaseService, ICybersecurityService):
    async def _on_initialize(self) -> None:
        self._logger.info("Initializing CybersecurityApplicationService")

    async def lookup_threat(self, schema: ThreatSchema) -> ThreatResult:
        # Mock threat intelligence
        is_malicious = "bad" in schema.indicator.lower()
        return ThreatResult(
            is_malicious=is_malicious,
            confidence=0.9 if is_malicious else 0.1,
            details={"source": "mock_threat_intel"}
        )

    async def lookup_ioc(self, schema: IocSchema) -> IocResult:
        return IocResult(
            known_ioc=schema.ioc == "1.2.3.4",
            campaign="apt29" if schema.ioc == "1.2.3.4" else "unknown"
        )

    async def check_hash_reputation(self, schema: HashReputationSchema) -> HashReputationResult:
        score = 100 if "a" in schema.file_hash else 10
        return HashReputationResult(
            score=score,
            malware_family="ransomware" if score > 80 else "none"
        )

    async def validate_url(self, schema: UrlValidationSchema) -> UrlValidationResult:
        try:
            result = urllib.parse.urlparse(schema.url)
            is_valid = all([result.scheme, result.netloc])
        except Exception:
            is_valid = False
            
        return UrlValidationResult(
            is_valid=is_valid,
            domain_age_days=365 if is_valid else -1
        )

    async def get_ip_utility(self, schema: IpUtilitySchema) -> IpUtilityResult:
        try:
            ipaddress.ip_address(schema.ip_address)
        except ValueError:
            raise ValueError(f"Invalid IP address: {schema.ip_address}")
            
        data = {"country": "US"} if schema.action == "geolocation" else {"asn": "AS12345"}
        return IpUtilityResult(ip=schema.ip_address, result_data=data)
