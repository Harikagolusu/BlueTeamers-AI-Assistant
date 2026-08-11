from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid
import json
from app.agents.models.session import AgentSession
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import CheckpointCreatedEvent

class AgentCheckpoint(BaseModel):
    checkpoint_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    state_snapshot: str # Serialized session state
    reason: str

class CheckpointManager:
    """Manages creation and retrieval of session checkpoints."""
    
    @staticmethod
    def create_checkpoint(session: AgentSession, reason: str) -> AgentCheckpoint:
        # In a real system, we'd serialize to a DB. For now, in-memory serialization.
        snapshot = session.model_dump_json()
        checkpoint = AgentCheckpoint(
            session_id=session.session_id,
            state_snapshot=snapshot,
            reason=reason
        )
        
        agent_event_bus.publish(CheckpointCreatedEvent(
            session_id=session.session_id,
            checkpoint_id=checkpoint.checkpoint_id
        ))
        return checkpoint

    @staticmethod
    def restore_checkpoint(checkpoint: AgentCheckpoint) -> AgentSession:
        return AgentSession.model_validate_json(checkpoint.state_snapshot)
