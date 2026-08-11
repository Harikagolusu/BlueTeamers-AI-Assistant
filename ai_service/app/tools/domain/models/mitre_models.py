from pydantic import BaseModel, Field
from typing import List

class MitreTechnique(BaseModel):
    id: str = Field(..., description="MITRE ATT&CK ID (e.g. T1110)")
    name: str = Field(..., description="Technique name")
    description: str = Field(..., description="Technique description")
    platforms: List[str] = Field(default_factory=list)

class MitreTactic(BaseModel):
    id: str = Field(..., description="MITRE ATT&CK ID (e.g. TA0001)")
    name: str = Field(..., description="Tactic name")
    description: str = Field(..., description="Tactic description")

class MitreGroup(BaseModel):
    id: str = Field(..., description="Group ID")
    name: str = Field(..., description="Group name")
    aliases: List[str] = Field(default_factory=list)

class MitreSoftware(BaseModel):
    id: str = Field(..., description="Software ID")
    name: str = Field(..., description="Software name")
    type: str = Field(..., description="Software type (malware, tool)")

class MitreMitigation(BaseModel):
    id: str = Field(..., description="Mitigation ID")
    name: str = Field(..., description="Mitigation name")

class MitreCampaign(BaseModel):
    id: str = Field(..., description="Campaign ID")
    name: str = Field(..., description="Campaign name")

class MitreDataSource(BaseModel):
    id: str = Field(..., description="Data Source ID")
    name: str = Field(..., description="Data Source name")

class MitreDataComponent(BaseModel):
    id: str = Field(..., description="Data Component ID")
    name: str = Field(..., description="Data Component name")
