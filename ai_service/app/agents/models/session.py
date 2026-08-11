from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import uuid
from app.planning.models.plan import ExecutionPlan
from app.agents.models.agent_models import AgentState, StepExecution
from app.agents.models.cursor import ExecutionCursor
from app.agents.models.journal import ExecutionJournal

class AgentMemory(BaseModel):
    """Short-lived memory specific to this execution session."""
    variables: Dict[str, Any] = Field(default_factory=dict)
    step_outputs: Dict[str, Any] = Field(default_factory=dict)

class AgentSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    state: AgentState = AgentState.IDLE
    plan: ExecutionPlan
    cursor: ExecutionCursor
    memory: AgentMemory = Field(default_factory=AgentMemory)
    history: List[StepExecution] = Field(default_factory=list)
    journal: ExecutionJournal = Field(default_factory=ExecutionJournal)
    runtime_context: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def create(cls, plan: ExecutionPlan, runtime_context: Dict[str, Any] = None) -> "AgentSession":
        return cls(
            plan=plan,
            cursor=ExecutionCursor.initialize(plan),
            runtime_context=runtime_context or {}
        )
