# RAG Runtime Validation

This document outlines the validation of the Retrieval-Augmented Generation (RAG) execution path.

## RAG Intent Routing Verification

When a cybersecurity-specific query is analyzed, the pipeline correctly routes it through `RagExecutionEngine`.

### RAG Execution Pipeline

```
Cybersecurity Query
      │
      ▼
IntentAnalysisStage (Classifies: RAG_QUERY)
      │
      ▼
RoutePlanningStage (Route recommendation: RAG)
      │
      ▼
EngineExecutionStage (Triggers: RagExecutionEngine)
      │
      ├─► RetrievalService: Generate embeddings -> search FAISS index
      ├─► PromptBuilder: Build system prompt + context documents
      └─► OllamaProvider: Generate response using qwen2.5:7b
```

## Validation Tests

### Test 1: Cybersecurity Inquiry (RAG Path)
- **Input Query**: `"What is MITRE ATT&CK?"`
- **Observed Behavior**:
  - Classifies as `IntentType.RAG_QUERY` (Confidence: 0.95).
  - Routes to `RAG` engine.
  - Triggers `RetrievalService`.
  - Searches FAISS index. (Since the index is currently empty in local dev, it logs `Retrieved: 0` and proceeds gracefully without raising a 404 error).
  - Prompts Ollama with the query context.
  - **Ollama Response**: Returns a correct threat intelligence explanation of MITRE ATT&CK.

### Test 2: General Conversation (Non-RAG Path)
- **Input Query**: `"Hello"`
- **Observed Behavior**:
  - Classifies as `IntentType.GREETING`.
  - Routes to `GENERAL` engine.
  - Bypasses retrieval entirely (no FAISS search or embedding generation is executed, latency is minimized).
  - Generates conversational response.

## RAG Subsystem Audit

We validated that the retrieval subsystem initializes cleanly:
- **Embedding Model**: `BAAI/bge-small-en-v1.5` loads successfully on CPU.
- **FAISS Vector Store**: Initializes successfully as `IndexFlatIP` with dimension 384.
- **Similarity Search**: Integrates correctly with `RetrievalService`.
- **RAG Graceful Degradation**: If retrieval yields 0 documents, the `RagExecutionEngine` is resilient and falls back to prompting the LLM with the raw query without throwing empty context/404 exceptions, preserving end-to-end reliability.
