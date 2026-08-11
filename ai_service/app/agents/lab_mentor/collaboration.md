# Collaboration Model

The Lab Mentor Agent is strictly prohibited from instantiating or depending directly on other agents (like the Knowledge Assistant or Investigation Agent).

Instead, it orchestrates requests through the `CapabilityRegistry` and `AgentOrchestrationService`.

## Use Cases
1. **Concept Explanations**: Uses Capability `EDUCATION` to dispatch fundamental knowledge requests to the Knowledge Assistant.
2. **Technical Analysis**: Uses Capability `TECHNICAL_ANALYSIS` to request deep-dive forensic reasoning from the Investigation Agent.
