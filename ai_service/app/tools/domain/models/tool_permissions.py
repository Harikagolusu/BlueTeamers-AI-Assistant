from typing import List
from pydantic import BaseModel, Field

class ToolPermissions(BaseModel):
    required_permissions: List[str] = Field(default_factory=list, description="Specific action permissions required")
    required_roles: List[str] = Field(default_factory=list, description="User roles required to execute")
    scopes: List[str] = Field(default_factory=list, description="OAuth or access scopes required")
    supported_operations: List[str] = Field(default_factory=list, description="CRUD operations supported if applicable")

    model_config = {"frozen": True}
