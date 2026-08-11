from typing import Optional
from app.services.lab.models import LabState, LabSession
from app.services.lab.transition_rules import TRANSITION_RULES
from app.services.lab.exceptions import InvalidStateTransitionError, TerminalStateError

class LabStateMachine:
    """
    Shared service for managing and validating lab state transitions.
    """
    def __init__(self, session: Optional[LabSession] = None):
        self.session = session
        self.current_state = session.current_state if session else LabState.NOT_STARTED

    def can_transition(self, next_state: LabState) -> bool:
        """Check if a transition is valid without throwing an error."""
        if self.is_terminal_state(self.current_state):
            return False
        if next_state == self.current_state:
            return True # Trivial transition
        allowed_states = TRANSITION_RULES.get(self.current_state, [])
        return next_state in allowed_states

    def transition(self, next_state: LabState) -> LabState:
        """
        Transition to the next state, updating the session if attached.
        Throws InvalidStateTransitionError or TerminalStateError if invalid.
        """
        if self.current_state == next_state:
            return self.current_state

        if self.is_terminal_state(self.current_state):
            raise TerminalStateError(self.current_state.value)
            
        if not self.can_transition(next_state):
            raise InvalidStateTransitionError(self.current_state.value, next_state.value)

        self.current_state = next_state
        if self.session:
            self.session.current_state = next_state
            
        return self.current_state

    def is_terminal_state(self, state: Optional[LabState] = None) -> bool:
        """Check if a state is terminal."""
        s = state if state else self.current_state
        return len(TRANSITION_RULES.get(s, [])) == 0

    def reset(self) -> None:
        """Reset the state machine back to NOT_STARTED."""
        self.current_state = LabState.NOT_STARTED
        if self.session:
            self.session.current_state = LabState.NOT_STARTED
