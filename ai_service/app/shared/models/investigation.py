from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class Evidence(BaseModel):
    id: str = Field(..., description="Unique identifier for the evidence")
    type: str = Field(..., description="Type of evidence (e.g., Windows Log, Sysmon, Authentication)")
    source: str = Field(..., description="Source system or file")
    content: Dict[str, Any] = Field(..., description="The parsed content of the evidence")
    timestamp: Optional[str] = Field(None, description="Primary timestamp associated with the evidence")

class EvidenceCollection(BaseModel):
    items: List[Evidence] = Field(default_factory=list, description="List of normalized evidence items")
    total_count: int = Field(0, description="Total count of evidence items")

class EvidenceCorrelation(BaseModel):
    correlated_entities: Dict[str, List[str]] = Field(default_factory=dict, description="Maps entity types (IPs, users, hashes) to evidence IDs")
    process_trees: List[Dict[str, Any]] = Field(default_factory=list, description="Reconstructed process parent-child trees")
    network_sessions: List[Dict[str, Any]] = Field(default_factory=list, description="Correlated network sessions")

class TimelineEvent(BaseModel):
    timestamp: str = Field(..., description="When the event occurred")
    event_type: str = Field(..., description="Type of event")
    description: str = Field(..., description="Description of the event")
    mitre_tactic: Optional[str] = Field(None, description="Associated MITRE ATT&CK tactic")
    mitre_technique: Optional[str] = Field(None, description="Associated MITRE ATT&CK technique")
    evidence_refs: List[str] = Field(default_factory=list, description="References to evidence IDs")

class Timeline(BaseModel):
    events: List[TimelineEvent] = Field(default_factory=list, description="Chronological list of events")

class InvestigationFinding(BaseModel):
    title: str = Field(..., description="Short title for the finding")
    description: str = Field(..., description="Detailed description")
    severity: str = Field(..., description="Severity of the finding (LOW, MEDIUM, HIGH, CRITICAL)")
    confidence: int = Field(..., description="Confidence score 0-100")

class InvestigationRecommendation(BaseModel):
    action: str = Field(..., description="Action to take")
    priority: str = Field(..., description="Priority (LOW, MEDIUM, HIGH, CRITICAL)")
    description: str = Field(..., description="Detailed description of the recommendation")

class InvestigationSummary(BaseModel):
    executive_summary: str = Field(..., description="High-level overview of the incident")
    risk_assessment: str = Field(..., description="Overall risk assessment")
    affected_assets: List[str] = Field(default_factory=list, description="List of affected hosts, users, or systems")
    confidence: int = Field(..., description="Overall confidence score 0-100")
