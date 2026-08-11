from pydantic import BaseModel, Field
from typing import List

class Role(BaseModel):
    role_id: str
    name: str
    description: str = ""
    permissions: List[str] = Field(default_factory=list)
