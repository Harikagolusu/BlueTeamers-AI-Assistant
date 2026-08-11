class LabMentorError(Exception):
    """Base exception for Lab Mentor module."""
    pass

class InvalidStateTransitionError(LabMentorError):
    """Raised when an invalid state transition is attempted."""
    def __init__(self, current_state: str, next_state: str):
        self.current_state = current_state
        self.next_state = next_state
        super().__init__(f"Invalid state transition from {current_state} to {next_state}")

class TerminalStateError(LabMentorError):
    """Raised when a transition is attempted from a terminal state."""
    def __init__(self, state: str):
        self.state = state
        super().__init__(f"Cannot transition from terminal state {state}")
