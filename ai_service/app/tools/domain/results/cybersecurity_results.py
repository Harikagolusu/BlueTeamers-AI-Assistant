from pydantic import Field
from typing import Dict, Any
from app.tools.domain.results.base_result import BaseResult

class ThreatResult(BaseResult):
    is_malicious: bool = Field(..., description="True if indicator is malicious")
    confidence: float = Field(..., description="Confidence score 0.0 - 1.0")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional context")

class IocResult(BaseResult):
    known_ioc: bool = Field(..., description="True if found in IOC databases")
    campaign: str = Field(default="unknown", description="Associated threat campaign")

class HashReputationResult(BaseResult):
    score: int = Field(..., description="Reputation score 0-100")
    malware_family: str = Field(default="unknown", description="Associated malware family")

class UrlValidationResult(BaseResult):
    is_valid: bool = Field(..., description="URL is syntactically valid and reachable")
    domain_age_days: int = Field(default=-1, description="Domain age if known")

class IpUtilityResult(BaseResult):
    ip: str = Field(..., description="The IP address")
    result_data: Dict[str, Any] = Field(..., description="Requested data (geolocation, etc)")
