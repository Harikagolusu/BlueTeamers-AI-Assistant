# LLM Execution Flow

## High-Level Sequence

1. **Frontend Request** -> POST /api/chat/
2. **FastAPI Endpoint** -> chat.py
3. **Orchestrator Stages**:
   - CacheStage
   - MemoryLoadStage (Fetches prior conversation turns)
   - IntentAnalysisStage (Selects GENERAL, RAG, TOOL, or AGENT)
   - RoutePlanningStage
   - EngineExecutionStage (Invokes the relevant engine)
4. **Engine Execution** (e.g. RagExecutionEngine):
   - Retrieves documents via FAISSRetriever.
   - Builds prompt via PromptBuilder.
   - Invokes LLMFactory.get_provider().generate() or stream_generate().
5. **Response Generation**:
   - Engine result wrapped in ExecutionResult.
   - Passes through CompositionStage and PersistenceStage.
   - Returned as JSON or StreamingResponse (Server-Sent Events).
