from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time

class TraceNodeType(str, Enum):
    WORKFLOW = "WORKFLOW"
    AGENT = "AGENT"
    TOOL = "TOOL"
    LLM = "LLM"
    MEMORY = "MEMORY"
    OUTPUT = "OUTPUT"

class TraceNode(BaseModel):
    node_id: str
    node_type: TraceNodeType
    name: str
    start_time: float
    end_time: Optional[float] = None
    success: Optional[bool] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    children: List['TraceNode'] = Field(default_factory=list)
    
    def complete(self, success: bool, **kwargs):
        self.end_time = time.time()
        self.success = success
        self.attributes.update(kwargs)
        
    def add_child(self, child: 'TraceNode'):
        self.children.append(child)

class TraceGraph(BaseModel):
    trace_id: str
    root: TraceNode
