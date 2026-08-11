# SOC Analyst Agent Reference

## Overview
The SOC Analyst Agent acts as a Tier-1/Tier-2 Security Analyst within the BlueTeamers AI Assistant platform. It serves as the primary intelligence ("Brain") that orchestrates underlying cybersecurity tools ("Hands") to analyze alerts, extract IOCs, map activities to the MITRE ATT&CK framework, and generate structured response JSONs.

## Architecture

```mermaid
graph TD
    User([Platform / User Input]) --> |Event Data| EventBus
    EventBus --> |Triggers| AgentRuntime
    AgentRuntime --> |Instantiates| SOCAgent[SOC Analyst Agent]
    
    subgraph Agent Core (The Brain)
        SOCAgent --> Planner[Execution Planner]
        SOCAgent --> RAG[RAG Engine]
        SOCAgent --> LLM[LLM Provider]
        SOCAgent --> Memory[Memory Service]
    end
    
    subgraph Tools (The Hands)
        SOCAgent --> MITRETool
        SOCAgent --> IOCExtractor
        SOCAgent --> LogParser
        SOCAgent --> TimelineTool
        SOCAgent --> IndicatorFetcher
    end
    
    LLM --> |Structured JSON| SOCAgent
    SOCAgent --> |AgentResult| EventBus
```

## Lifecycle Execution Flow
The SOC Analyst Agent follows the standard 13-step lifecycle enforced by the `BaseAgent` class:
1. **Initialize**: Sets up tracing and internal logging.
2. **Validate**: Ensures session IDs and valid context exist.
3. **Prepare Context**: Loads historical Investigation context from MemoryService.
4. **Plan**: Decomposes the alert into logical analysis phases.
5. **Retrieve**: Queries the KnowledgeSearchTool.
6. **Select Tools**: Evaluates which tools are necessary (e.g. LogParser vs IOCExtractor).
7. **Execute Tools**: Calls underlying functional tools.
8. **Reason**: Synthesizes output via `gpt-4-turbo`.
9. **Post Process**: Converts JSON back into strict `AgentResult`.
10. **Update Memory**: Pushes conclusion to Session history.
11. **Publish Events**: Emits `SOCAnalysisCompleteEvent`.
12. **Cleanup**: Frees buffers.

## Testing Procedures
- Unit tests: `pytest tests/agents/soc/test_soc_unit.py` (Tests lifecycle, memory, and LLM fallbacks).
- Integration tests: `pytest tests/agents/soc/test_soc_integration.py` (Tests Tool bindings).
- E2E tests: `pytest tests/agents/soc/test_soc_e2e.py` (Validates full scenarios using the actual Platform).
