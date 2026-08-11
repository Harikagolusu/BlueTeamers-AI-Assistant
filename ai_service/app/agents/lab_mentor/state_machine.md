# Lab State Machine

The state machine is defined in `app/services/lab/state_machine.py`.

## Core States
- `NOT_STARTED`
- `INITIALIZING`
- `IN_PROGRESS`
- `BLOCKED`
- `AWAITING_HINT`
- `AWAITING_REFLECTION`
- `COMPLETED`
- `ABANDONED`

## Principles
1. **No direct mutations**: Transitions must flow through `machine.transition(next_state)`.
2. **Terminal Protection**: `COMPLETED` and `ABANDONED` cannot transition to other states without a hard reset.
3. **Invalid Transitions**: Attempting an unauthorized transition throws `InvalidStateTransitionError`.
