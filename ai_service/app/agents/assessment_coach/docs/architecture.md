# Assessment Coach Architecture

## Overview

The Assessment Coach Agent relies on the standard platform `BaseAgent` and acts as a thin orchestrator over a suite of specialized tools. It implements v2.0 hardening principles including full lifecycle state management and append-only versioned memory.

## State Machine

```mermaid
stateDiagram-v2
    [*] --> CREATED
    CREATED --> PREPARING
    PREPARING --> RUNNING
    RUNNING --> PAUSED
    PAUSED --> RUNNING
    RUNNING --> SCORING
    SCORING --> GENERATING_FEEDBACK
    GENERATING_FEEDBACK --> COMPLETED
    RUNNING --> FAILED
    RUNNING --> CANCELLED
    COMPLETED --> [*]
    FAILED --> [*]
    CANCELLED --> [*]
```

## Parallel Execution DAG

```mermaid
graph TD
    A[Assessment Request] --> B(AssessmentCoachAgent)
    B --> C[WorkflowBuilder DAG]
    
    C --> D[Retrieve Historical Context]
    D --> E[Evaluate Knowledge]
    D --> F[Evaluate Practical Skills]
    D --> X[Evaluate Scenario]
    
    E --> G[Compute Competencies]
    F --> G
    X --> G
    
    G --> H[Detect Gaps]
    G --> I[Compute Readiness]
    
    H --> J[Generate Adaptive Questions]
    H --> K[Generate Feedback]
    
    I --> L[Update Analytics]
    L --> M[Return Response]
```

## Tools
The agent uses 10 isolated tools representing distinct domains of evaluation, supporting dependency injection for future expansions. All outputs guarantee deterministic explainability.
