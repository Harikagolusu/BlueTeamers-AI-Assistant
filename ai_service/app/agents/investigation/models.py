from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from app.shared.models.investigation import (
    Evidence,
    EvidenceCollection,
    EvidenceCorrelation,
    TimelineEvent,
    Timeline,
    InvestigationFinding,
    InvestigationRecommendation,
    InvestigationSummary
)

class InvestigationRequest(BaseModel):
    evidence_items: List[Dict[str, Any]] = Field(..., description="Raw uploaded evidence like Windows/Linux logs, alerts, etc.")
    investigation_goal: Optional[str] = Field(None, description="Optional specific goal for the investigation.")

class InvestigationContext(BaseModel):
    raw_request: Optional[InvestigationRequest] = None
    collection: Optional[EvidenceCollection] = None
    correlation: Optional[EvidenceCorrelation] = None
    timeline: Optional[Timeline] = None
    soc_findings: List[Any] = Field(default_factory=list, description="Findings from SOC Analyst Agent")
    ti_findings: List[Any] = Field(default_factory=list, description="Findings from Threat Intelligence Agent")
    plan: Optional[Dict[str, Any]] = None

class InvestigationResponse(BaseModel):
    executive_summary: str = Field(..., description="Executive Summary")
    evidence_collected: EvidenceCollection = Field(..., description="Evidence Collected")
    evidence_correlation: EvidenceCorrelation = Field(..., description="Evidence Correlation")
    soc_findings: List[Dict[str, Any]] = Field(default_factory=list, description="SOC Findings")
    threat_intelligence_findings: List[Dict[str, Any]] = Field(default_factory=list, description="Threat Intelligence Findings")
    mitre_mapping: List[Dict[str, Any]] = Field(default_factory=list, description="MITRE Mapping")
    incident_timeline: Timeline = Field(..., description="Incident Timeline")
    affected_assets: List[str] = Field(default_factory=list, description="Affected Assets")
    risk_assessment: str = Field(..., description="Risk Assessment")
    confidence: int = Field(..., description="Confidence score 0-100")
    recommendations: List[InvestigationRecommendation] = Field(default_factory=list, description="Recommendations")
    next_investigation_steps: List[str] = Field(default_factory=list, description="Next Investigation Steps")
    learning_guidance: str = Field(..., description="Learning Guidance for junior analysts")
