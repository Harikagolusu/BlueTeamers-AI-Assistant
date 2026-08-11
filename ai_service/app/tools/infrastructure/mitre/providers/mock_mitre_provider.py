from datetime import datetime, timezone
from typing import Optional
from app.tools.infrastructure.mitre.interfaces.i_mitre_provider import IMitreProvider
from app.tools.infrastructure.providers.models import ProviderHealth, ProviderStatus
from app.tools.domain.models.mitre_models import MitreTechnique, MitreTactic, MitreGroup, MitreSoftware

class MockMitreProvider(IMitreProvider):
    async def get_technique(self, technique_id: str) -> Optional[MitreTechnique]:
        if "T" in technique_id:
            return MitreTechnique(id=technique_id, name="Mock Technique", description="A mock STIX mapped technique", platforms=["Windows"])
        return None

    async def get_tactic(self, tactic_id: str) -> Optional[MitreTactic]:
        if "TA" in tactic_id:
            return MitreTactic(id=tactic_id, name="Mock Tactic", description="A mock tactic")
        return None

    async def get_group(self, group_name: str) -> Optional[MitreGroup]:
        return MitreGroup(id="G0001", name=group_name, aliases=[])

    async def get_software(self, software_name: str) -> Optional[MitreSoftware]:
        return MitreSoftware(id="S0001", name=software_name, type="malware")
        
    async def health_check(self) -> ProviderHealth:
        return ProviderHealth(
            status=ProviderStatus.CONNECTED,
            latency_ms=12.5,
            version="1.0-mock",
            provider_name="MockMitreProvider",
            last_checked=datetime.now(timezone.utc)
        )
