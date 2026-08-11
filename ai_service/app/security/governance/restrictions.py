from typing import Dict, List
from app.security.interfaces.i_governance import IRestrictionManager

class RestrictionManager(IRestrictionManager):
    def __init__(self):
        self._allowed: Dict[str, Dict[str, List[str]]] = {} # tenant_id -> entity_type -> allowed_ids

    def set_allowed(self, tenant_id: str, entity_type: str, allowed_ids: List[str]) -> None:
        if tenant_id not in self._allowed:
            self._allowed[tenant_id] = {}
        self._allowed[tenant_id][entity_type] = allowed_ids

    def is_allowed(self, tenant_id: str, entity_type: str, entity_id: str) -> bool:
        allowed = self._allowed.get(tenant_id, {}).get(entity_type, [])
        if not allowed or "*" in allowed:
            return True # No restrictions set
        return entity_id in allowed
