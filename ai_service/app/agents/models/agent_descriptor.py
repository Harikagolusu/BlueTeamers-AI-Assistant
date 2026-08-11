import uuid
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.agents.models.capability import CapabilityModel

class AgentStatus(str, Enum):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)
    AVAILABLE = "AVAILABLE"
    BUSY = "BUSY"
    OFFLINE = "OFFLINE"
    ERROR = "ERROR"

class AgentDescriptor(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)
    """
    Describes an agent registered in the system, its capabilities, and routing priority.
    """
    agent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""
    version: str = "1.0.0"
    priority: int = 1
    capabilities: List[CapabilityModel] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    status: AgentStatus = AgentStatus.AVAILABLE
    
    # Cost per token or step (used for ranking)
    cost_weight: float = 1.0
