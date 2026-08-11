from typing import Dict, List
from app.services.lab.models import LabState

# Declarative transition rules mapping a state to its allowed subsequent states.
# An empty list indicates a terminal state.
TRANSITION_RULES: Dict[LabState, List[LabState]] = {
    LabState.NOT_STARTED: [LabState.INITIALIZING, LabState.ABANDONED],
    LabState.INITIALIZING: [LabState.IN_PROGRESS, LabState.ABANDONED],
    LabState.IN_PROGRESS: [
        LabState.BLOCKED,
        LabState.AWAITING_HINT,
        LabState.AWAITING_REFLECTION,
        LabState.COMPLETED,
        LabState.ABANDONED
    ],
    LabState.BLOCKED: [
        LabState.AWAITING_HINT,
        LabState.IN_PROGRESS,
        LabState.ABANDONED
    ],
    LabState.AWAITING_HINT: [
        LabState.IN_PROGRESS,
        LabState.ABANDONED
    ],
    LabState.AWAITING_REFLECTION: [
        LabState.IN_PROGRESS,
        LabState.ABANDONED
    ],
    LabState.COMPLETED: [],  # Terminal state (RESET_ONLY)
    LabState.ABANDONED: []   # Terminal state (RESET_ONLY)
}
