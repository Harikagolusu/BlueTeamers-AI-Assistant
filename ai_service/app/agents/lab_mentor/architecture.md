# Lab Mentor Architecture

The Lab Mentor has been refactored into a thin orchestrator that delegates core educational tracking and validations to shared services (`app/services/lab`).

## Key Components

1. **LabSession**: Centralized session context, managed in `app/services/lab/models.py`. The agent persists and passes this context between tool executions.
2. **LabStateMachine**: A robust FSM enforcing allowed state transitions and protecting terminal states.
3. **Tools**: Modular capabilities (Lab Analysis, Mistake Detection, Hint Generation, etc.) that leverage the shared models to generate telemetry and adapt interactions.
4. **Execution Timeline**: Observability traces are emitted for every significant transition, hint request, and mistake classification.
