from enum import Enum
from app.planning.models.plan import ExecutionStep
from app.agents.models.session import AgentSession
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import RecoveryTriggeredEvent

class RecoveryAction(str, Enum):
    RETRY_STEP = "RETRY_STEP"
    SKIP_STEP = "SKIP_STEP"
    ABORT_PLAN = "ABORT_PLAN"

class RecoveryPolicy:
    """Decides what action to take when a step fails by resolving strategies."""
    
    @staticmethod
    def determine_action(session: AgentSession, step: ExecutionStep, current_retries: int) -> RecoveryAction:
        from app.agents.recovery.strategies import RetryStrategy, SkipStrategy, FallbackStrategy
        
        # Build default fallback chain: Retry -> Skip (if optional) -> Abort
        strategy = FallbackStrategy(RetryStrategy(), SkipStrategy())
        action = strategy.determine_action(session, step, current_retries)
            
        agent_event_bus.publish(RecoveryTriggeredEvent(
            session_id=session.session_id,
            step_id=step.step_id,
            action=action.value
        ))
        
        return action
