# Threat Intelligence Agent Architecture

The Threat Intelligence Agent is built strictly on top of the existing BlueTeamers AI Assistant SDK.

## Core Components

- **Agent Manifest (`manifest.yaml`)**: Defines the capabilities, required permissions, dynamic model assignment, and required tools for the agent.
- **Provider Interface (`provider.py`)**: (Migrated) See shared platform capabilities under `app/providers/threat_intelligence/`.
- **Tools (`tools/`)**: Extend the `BaseTool` class. Each handles a specific CTI responsibility. Now utilizes full Dependency Injection (DI) and `pydantic` schemas for robust validation.
- **Models (`models.py`)**: Defines Pydantic data models used to enforce structured LLM output (e.g., `ThreatIntelligenceResponse`).
- **Prompts (`prompts.py`)**: Registers the `THREAT_INTELLIGENCE_SYSTEM` prompt.
- **Agent (`agent.py`)**: The `ThreatIntelligenceAgent` class orchestrates the standard 13-step lifecycle exactly as defined in `BaseAgent`.
- **Registry (`registry.py`)**: Handles decoupling the component registration logic from the agent, wiring the agent and tools into `AgentFactory` and `ToolRegistry` respectively.

## Data Flow

1. **Input**: Context containing indicators or text.
2. **Tool Execution**: Tools query the `ThreatIntelligenceProvider`.
3. **Context Aggregation**: Tool responses are serialized into the `investigation_context`.
4. **Reasoning**: The aggregated context is sent alongside the system prompt to the LLM.
5. **Output**: Structured JSON is validated and returned.
