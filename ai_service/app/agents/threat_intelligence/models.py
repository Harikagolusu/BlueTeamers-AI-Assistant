from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class IndicatorDetail(BaseModel):
    value: str
    type: str
    description: str
    confidence: int

class ThreatAssessment(BaseModel):
    risk_level: str
    summary: str
    affected_assets: List[str] = Field(default_factory=list)

class ThreatIntelligence(BaseModel):
    threat_actors: List[str] = Field(default_factory=list)
    campaigns: List[str] = Field(default_factory=list)
    related_malware: List[str] = Field(default_factory=list)

class MitreMapping(BaseModel):
    tactic: str
    technique_id: str
    technique_name: str
    description: str

class ThreatIntelligenceResponse(BaseModel):
    executive_summary: str = Field(..., description="High-level summary of the findings.")
    indicator_details: List[IndicatorDetail] = Field(default_factory=list, description="Details of the analyzed indicators.")
    threat_assessment: ThreatAssessment = Field(..., description="Overall risk assessment.")
    threat_intelligence: ThreatIntelligence = Field(default_factory=ThreatIntelligence, description="Information on actors, campaigns, and malware.")
    mitre_attack_mapping: List[MitreMapping] = Field(default_factory=list, description="Relevant MITRE ATT&CK mappings.")
    evidence: List[str] = Field(default_factory=list, description="Factual evidence supporting the assessment.")
    confidence_score: int = Field(..., description="Confidence score from 0 to 100.")
    recommended_next_steps: List[str] = Field(default_factory=list, description="Actionable recommendations for next steps.")
    references: Optional[List[str]] = Field(default_factory=list, description="Optional links or references for further context.")
