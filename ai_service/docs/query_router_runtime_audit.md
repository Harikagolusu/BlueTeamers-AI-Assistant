# Query Router Runtime Audit

This document summarizes the audit and implementation of the query routing mechanism in the BlueTeamers AI Assistant.

## Intent Analysis & Routing Architecture

When a request hits the chat API endpoint, it enters the `ChatService` which initiates the `ChatOrchestrator` execution pipeline. The pipeline processes the request through the following stages:

```
User Query
      │
      ▼
ChatService
      │
      ▼
ChatOrchestrator
      │
      ├─► CacheStage: Check semantic cache
      ├─► MemoryLoadStage: Load conversation history
      ├─► IntentAnalysisStage: Analyze intent via RuleIntentClassifier
      ├─► RoutePlanningStage: Resolve recommended engine
      ├─► EngineExecutionStage: Run General/RAG/Tool/Agent Engine
      ├─► CompositionStage: Formulate ChatResponse
      └─► PersistenceStage: Save conversation turns
```

### 1. Intent Analysis Stage
Runs the `IntentIntelligenceService` which triggers the intent analysis pipeline:
- **Entity Extraction**: Uses regex to extract entities (e.g. CVE codes, IP addresses, MITRE ATT&CK IDs).
- **Intent Classification**: Evaluates rules to classify user query into intents (e.g., `GREETING`, `RAG_QUERY`, `TOOL_REQUEST`, `GENERAL_CHAT`).
- **Confidence Evaluation**: Evaluates confidence levels based on matched features and syntax rules.
- **Policy Evaluation**: Assesses fallback and ambiguity thresholds.
- **Execution Planning**: Maps the primary intent type to recommended execution engines:
  - `IntentType.GENERAL_CHAT` / `GREETING` / `SMALL_TALK` -> `GENERAL` (GeneralExecutionEngine)
  - `IntentType.RAG_QUERY` -> `RAG` (RagExecutionEngine)
  - `IntentType.TOOL_REQUEST` -> `TOOL` (ToolExecutionEngine)

### 2. Route Planning Stage
Extracts `route_recommendation` from the intent analysis result.
If a recommended engine (e.g., `"GENERAL"`, `"RAG"`, `"TOOL"`) is present, it directly selects it. Otherwise, it defaults to `"AGENT"` (AgentExecutor) for multi-step agent plan execution.

## Routing Test Matrices

We validated the query router classifications against standard user inputs:

| Query | Classified Intent | Recommended Route | Actual Engine Triggered | Bypasses Retriever? |
|-------|-------------------|-------------------|------------------------|---------------------|
| "Hello" | `GREETING` | `GENERAL` | `GeneralExecutionEngine` | **Yes** (No retrieval) |
| "Who are you?" | `GENERAL_CHAT` | `GENERAL` | `GeneralExecutionEngine` | **Yes** (No retrieval) |
| "Explain recursion" | `GENERAL_CHAT` | `GENERAL` | `GeneralExecutionEngine` | **Yes** (No retrieval) |
| "What is MITRE ATT&CK?" | `RAG_QUERY` | `RAG` | `RagExecutionEngine` | **No** (Performs RAG) |
| "Explain T1059" | `RAG_QUERY` | `RAG` | `RagExecutionEngine` | **No** (Performs RAG) |
| "Search CVE-2024-12345" | `TOOL_REQUEST` | `TOOL` | `ToolExecutionEngine` | **Yes** (Bypasses RAG to execute tools) |

This audit confirms that the query router classifications align exactly with the intended architecture.
