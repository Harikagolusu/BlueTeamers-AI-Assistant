from app.tools.application.interfaces.i_mitre_service import IMitreService
from app.tools.infrastructure.base.base_service import BaseService
from app.tools.infrastructure.mitre.factory.mitre_provider_factory import MitreProviderFactory
from app.tools.domain.schemas.mitre_schemas import TechniqueLookupSchema, TacticLookupSchema, GroupLookupSchema, SoftwareLookupSchema
from app.tools.domain.results.mitre_results import TechniqueLookupResult, TacticLookupResult, GroupLookupResult, SoftwareLookupResult
from app.tools.infrastructure.mitre.providers.mock_mitre_provider import MockMitreProvider

# Register mock provider explicitly
MitreProviderFactory.register("mock", MockMitreProvider)

class MitreApplicationService(BaseService, IMitreService):
    def __init__(self, provider_name: str = "mock"):
        super().__init__()
        self.provider_name = provider_name
        self.provider = None
        
    async def _on_initialize(self) -> None:
        self.provider = MitreProviderFactory.create(self.provider_name)
        self._logger.info(f"Initialized MitreApplicationService with {self.provider_name}")

    async def lookup_technique(self, schema: TechniqueLookupSchema) -> TechniqueLookupResult:
        technique = await self.provider.get_technique(schema.technique_id)
        return TechniqueLookupResult(technique=technique, found=technique is not None)

    async def lookup_tactic(self, schema: TacticLookupSchema) -> TacticLookupResult:
        tactic = await self.provider.get_tactic(schema.tactic_id)
        return TacticLookupResult(tactic=tactic, found=tactic is not None)

    async def lookup_group(self, schema: GroupLookupSchema) -> GroupLookupResult:
        group = await self.provider.get_group(schema.group_name)
        return GroupLookupResult(group=group, found=group is not None)

    async def lookup_software(self, schema: SoftwareLookupSchema) -> SoftwareLookupResult:
        software = await self.provider.get_software(schema.software_name)
        return SoftwareLookupResult(software=software, found=software is not None)
