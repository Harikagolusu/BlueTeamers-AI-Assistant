import re
from typing import Dict, Any
from app.chat.intent.interfaces import IEntityExtractor
from app.chat.intent.models.entities import EntityCollection, ExtractedEntity

class RegexEntityExtractor(IEntityExtractor):
    def __init__(self):
        # Basic patterns for cybersecurity entities
        self.patterns = {
            "CVE": r"CVE-\d{4}-\d{4,7}",
            "MITRE_TID": r"T\d{4}(?:\.\d{3})?",
            "IP_ADDRESS": r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
            "DOMAIN": r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" # Simplistic domain regex for demo purposes
        }

    async def extract(self, query: str, context: Dict[str, Any]) -> EntityCollection:
        entities = EntityCollection()
        
        for entity_type, pattern in self.patterns.items():
            matches = set(re.findall(pattern, query, re.IGNORECASE))
            for match in matches:
                entities.add(ExtractedEntity(
                    type=entity_type,
                    value=match.upper() if entity_type in ["CVE", "MITRE_TID"] else match.lower()
                ))
                
        return entities
