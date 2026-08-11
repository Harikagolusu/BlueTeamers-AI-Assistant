from app.agents.interfaces.i_recovery import IRecoveryStrategy
from app.agents.recovery.recovery_policy import RecoveryAction
from app.agents.models.session import AgentSession
from app.planning.models.plan import ExecutionStep

class RetryStrategy(IRecoveryStrategy):
    def determine_action(self, session: AgentSession, step: ExecutionStep, current_retries: int) -> RecoveryAction:
        max_retries = step.retry_policy.get("max_attempts", 3)
        if current_retries < max_retries:
            return RecoveryAction.RETRY_STEP
        return RecoveryAction.ABORT_PLAN

class SkipStrategy(IRecoveryStrategy):
    def determine_action(self, session: AgentSession, step: ExecutionStep, current_retries: int) -> RecoveryAction:
        if step.optional:
            return RecoveryAction.SKIP_STEP
        return RecoveryAction.ABORT_PLAN

class AbortStrategy(IRecoveryStrategy):
    def determine_action(self, session: AgentSession, step: ExecutionStep, current_retries: int) -> RecoveryAction:
        return RecoveryAction.ABORT_PLAN

class FallbackStrategy(IRecoveryStrategy):
    def __init__(self, primary: IRecoveryStrategy, secondary: IRecoveryStrategy):
        self.primary = primary
        self.secondary = secondary

    def determine_action(self, session: AgentSession, step: ExecutionStep, current_retries: int) -> RecoveryAction:
        action = self.primary.determine_action(session, step, current_retries)
        if action == RecoveryAction.ABORT_PLAN:
            return self.secondary.determine_action(session, step, current_retries)
        return action
