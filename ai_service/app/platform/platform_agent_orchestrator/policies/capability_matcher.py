from typing import Protocol, List
from pydantic import BaseModel

class CapabilityMatch(BaseModel):
    capability: str
    agent_id: str
    match_type: str # EXACT, METADATA, FALLBACK
    score: float
    metadata: dict = {}

class CapabilityMatcher(Protocol):
    def match(self, capability: str, registry) -> List[CapabilityMatch]:
        ...

class MetadataCapabilityMatcher:
    def match(self, capability: str, registry) -> List[CapabilityMatch]:
        # MVP Implementation: exact match, then metadata tags, then fallback
        # In a real environment, registry would be queried.
        return [
            CapabilityMatch(
                capability=capability,
                agent_id="InvestigationAgent", # Mock fallback
                match_type="EXACT",
                score=1.0
            )
        ]
