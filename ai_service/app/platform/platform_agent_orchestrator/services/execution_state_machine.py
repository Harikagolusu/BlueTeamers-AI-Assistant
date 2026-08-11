from app.platform.platform_agent_orchestrator.models import ExecutionState, ExecutionStep

class InvalidStateTransitionError(Exception):
    pass

class ExecutionStateMachine:
    # Valid transitions
    TRANSITIONS = {
        ExecutionState.PENDING: [ExecutionState.READY, ExecutionState.CANCELLED, ExecutionState.SKIPPED],
        ExecutionState.READY: [ExecutionState.RUNNING, ExecutionState.CANCELLED],
        ExecutionState.RUNNING: [ExecutionState.WAITING, ExecutionState.COMPLETED, ExecutionState.FAILED, ExecutionState.CANCELLED],
        ExecutionState.WAITING: [ExecutionState.READY, ExecutionState.CANCELLED],
        ExecutionState.RETRYING: [ExecutionState.READY, ExecutionState.CANCELLED, ExecutionState.FAILED],
        ExecutionState.COMPLETED: [],
        ExecutionState.FAILED: [ExecutionState.RETRYING],
        ExecutionState.SKIPPED: [],
        ExecutionState.CANCELLED: []
    }

    @classmethod
    def transition(cls, step: ExecutionStep, new_state: ExecutionState) -> ExecutionStep:
        current_state = step.state
        if new_state not in cls.TRANSITIONS[current_state]:
            raise InvalidStateTransitionError(f"Cannot transition from {current_state} to {new_state}")
        
        step.state = new_state
        return step
