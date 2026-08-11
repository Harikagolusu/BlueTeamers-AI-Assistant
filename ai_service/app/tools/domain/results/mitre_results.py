from pydantic import Field
from typing import Optional
from app.tools.domain.results.base_result import BaseResult
from app.tools.domain.models.mitre_models import MitreTechnique, MitreTactic, MitreGroup, MitreSoftware

class TechniqueLookupResult(BaseResult):
    technique: Optional[MitreTechnique] = Field(None, description="The matched technique")
    found: bool = Field(..., description="True if technique was found")

class TacticLookupResult(BaseResult):
    tactic: Optional[MitreTactic] = Field(None, description="The matched tactic")
    found: bool = Field(..., description="True if tactic was found")

class GroupLookupResult(BaseResult):
    group: Optional[MitreGroup] = Field(None, description="The matched group")
    found: bool = Field(..., description="True if group was found")

class SoftwareLookupResult(BaseResult):
    software: Optional[MitreSoftware] = Field(None, description="The matched software")
    found: bool = Field(..., description="True if software was found")
