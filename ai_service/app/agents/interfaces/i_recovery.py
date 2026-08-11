from abc import ABC, abstractmethod
from typing import Optional
from app.agents.models.session import AgentSession
from app.planning.models.plan import ExecutionStep
from app.agents.recovery.recovery_policy import RecoveryAction

class IRecoveryStrategy(ABC):
    """Base interface for all recovery strategies."""
    
    @abstractmethod
    def determine_action(self, session: AgentSession, step: ExecutionStep, current_retries: int) -> RecoveryAction:
        pass
