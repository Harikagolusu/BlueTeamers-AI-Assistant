from typing import Dict, Any
from app.security.interfaces.i_trust import ITrustManager

class TrustManager(ITrustManager):
    def __init__(self):
        self._trusted_entities: Dict[str, bool] = {}

    def set_trust(self, entity_id: str, is_trusted: bool) -> None:
        self._trusted_entities[entity_id] = is_trusted

    def is_trusted(self, entity_id: str) -> bool:
        # Default deny
        return self._trusted_entities.get(entity_id, False)
