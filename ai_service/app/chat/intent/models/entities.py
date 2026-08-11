from typing import Dict, Any, List
from pydantic import BaseModel, Field

class ExtractedEntity(BaseModel):
    type: str  # e.g., "CVE", "IP_ADDRESS", "MITRE_TID"
    value: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class EntityCollection(BaseModel):
    """A richer collection for managing and querying extracted entities."""
    entities: List[ExtractedEntity] = Field(default_factory=list)

    def add(self, entity: ExtractedEntity):
        self.entities.append(entity)

    def get(self, entity_type: str) -> List[ExtractedEntity]:
        """Returns all entities of a specific type."""
        return [e for e in self.entities if e.type == entity_type]

    def has(self, entity_type: str) -> bool:
        """Returns True if an entity of the specific type exists."""
        return any(e.type == entity_type for e in self.entities)

    def all(self) -> List[ExtractedEntity]:
        """Returns all extracted entities."""
        return self.entities

    def to_list(self) -> List[dict]:
        """Serializes to a list of dicts for Pydantic/API boundaries."""
        return [e.model_dump() for e in self.entities]
        
    @classmethod
    def from_list(cls, entity_dicts: List[dict]):
        entities = [ExtractedEntity(**e) for e in entity_dicts]
        return cls(entities=entities)
