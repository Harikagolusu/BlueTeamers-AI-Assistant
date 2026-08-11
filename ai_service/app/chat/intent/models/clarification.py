from typing import List, Optional
from pydantic import BaseModel, Field

class ClarificationRequest(BaseModel):
    reason: str
    suggested_prompt: str
    missing_information: List[str] = Field(default_factory=list)
