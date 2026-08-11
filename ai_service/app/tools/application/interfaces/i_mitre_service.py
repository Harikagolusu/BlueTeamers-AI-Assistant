from abc import ABC, abstractmethod
from app.tools.domain.schemas.mitre_schemas import TechniqueLookupSchema, TacticLookupSchema, GroupLookupSchema, SoftwareLookupSchema
from app.tools.domain.results.mitre_results import TechniqueLookupResult, TacticLookupResult, GroupLookupResult, SoftwareLookupResult

class IMitreService(ABC):
    @abstractmethod
    async def lookup_technique(self, schema: TechniqueLookupSchema) -> TechniqueLookupResult:
        pass

    @abstractmethod
    async def lookup_tactic(self, schema: TacticLookupSchema) -> TacticLookupResult:
        pass

    @abstractmethod
    async def lookup_group(self, schema: GroupLookupSchema) -> GroupLookupResult:
        pass

    @abstractmethod
    async def lookup_software(self, schema: SoftwareLookupSchema) -> SoftwareLookupResult:
        pass
