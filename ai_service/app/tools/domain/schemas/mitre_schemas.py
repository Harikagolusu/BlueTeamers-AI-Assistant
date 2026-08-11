from pydantic import Field
from app.tools.domain.schemas.base_schema import BaseSchema

class TechniqueLookupSchema(BaseSchema):
    technique_id: str = Field(..., description="MITRE ATT&CK Technique ID (e.g., T1110)")

class TacticLookupSchema(BaseSchema):
    tactic_id: str = Field(..., description="MITRE ATT&CK Tactic ID (e.g., TA0006)")

class GroupLookupSchema(BaseSchema):
    group_name: str = Field(..., description="Threat group name or alias")

class SoftwareLookupSchema(BaseSchema):
    software_name: str = Field(..., description="Malware or tool name")
