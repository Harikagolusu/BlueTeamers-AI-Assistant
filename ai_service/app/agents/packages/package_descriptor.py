from pydantic import BaseModel
from typing import List
from app.agents.models.agent_package import AgentPackage

class PackageDescriptor(BaseModel):
    package_id: str
    name: str
    version: str
    description: str
    is_installed: bool = False
    is_enabled: bool = False
