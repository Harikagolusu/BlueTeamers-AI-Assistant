# Collaboration Framework

The Assessment Coach is heavily reliant on the **Agent Orchestration Service** for cross-agent collaboration.

## Interactions
- **Knowledge Assistant**: Can be used to verify specific concepts if required.
- **Lab Mentor**: Can provide previous lab performance data to aid in practical assessments.
- **Learning Coach**: Primary collaborator. Provides the overarching learning roadmap, goals, and competency history.

**Crucial Note**: The Assessment Coach MUST NOT directly import or instantiate these agents. It uses `self.orchestration_service.get_historical_metrics()` and fallback mechanisms to ensure independence.
