from abc import ABC, abstractmethod
from typing import Dict, Any, List

class ThreatIntelligenceProvider(ABC):
    """
    Shared Platform Interface for integrating external Threat Intelligence feeds (e.g., MISP, OpenCTI, VirusTotal).
    """

    @abstractmethod
    async def lookup_ioc(self, indicator: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_reputation(self, indicator: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_threat_actor(self, actor_name: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_campaign(self, campaign_name: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def correlate_indicators(self, indicators: List[str]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def map_to_mitre(self, entity: str) -> List[Dict[str, Any]]:
        pass
