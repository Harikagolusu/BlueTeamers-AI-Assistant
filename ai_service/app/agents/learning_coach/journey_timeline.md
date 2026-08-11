# Journey Timeline

The `LearnerProfile` maintains a chronologically ordered `journey_timeline` composed of `JourneyTransition` events. 

## Tracking Transitions
The timeline records every shift in a learner's status through the core state machine (`ONBOARDING`, `LEARNING`, `PRACTICING`, `ASSESSING`, `REMEDIATION`, `CERTIFICATION_READY`, `COMPLETED`, `PAUSED`).

## Event Structure
Each transition holds:
- `timestamp`: UTC time of state change.
- `previous_state`: The state being exited.
- `new_state`: The state being entered.
- `trigger`: The event generating the transition (e.g., "Roadmap execution active").
- `reason`: Explainable text for the timeline history.

This chronological history allows the coach to identify stalled states and pattern metrics.
