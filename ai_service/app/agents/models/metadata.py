from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PackageMetadata(BaseModel):
    author: str
    organization: Optional[str] = None
    license: str = "MIT"
    homepage: Optional[str] = None
    repository: Optional[str] = None
    documentation_url: Optional[str] = None
    created_date: datetime = Field(default_factory=datetime.utcnow)
    updated_date: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = Field(default_factory=list)
    category: str = "general"
    platform_compatibility: str = ">=1.0.0"
