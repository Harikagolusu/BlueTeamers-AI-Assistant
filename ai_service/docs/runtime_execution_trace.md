# Runtime Execution Trace

This trace documents the end-to-end execution path for requests sent to `/api/v1/chat`.

## Synchronous Trace: GREETING Flow (`"Hello"`)

1. **Inbound HTTP Request**:
   `POST /api/v1/chat` with body `{"query": "Hello", "stream": false}` received by `app/chat/router.py`.

2. **Domain Mapping**:
   Mapped to `DomainChatRequest(message="Hello", stream=False)` and sent to `ChatService.process_request()`.

3. **Orchestrator Initiation**:
   `ChatService` creates `ExecutionContext` and triggers `ChatOrchestrator.execute_pipeline()`.

4. **Cache Stage (`CacheStage`)**:
   Checks `DefaultCacheManager`. Cache miss.

5. **Memory Load Stage (`MemoryLoadStage`)**:
   Loads history from `DefaultMemoryManager` wrapping `MemoryService`. No previous history found.

6. **Intent Analysis Stage (`IntentAnalysisStage`)**:
   - `RuleIntentClassifier` matches query `"Hello"` against `greeting_keywords`.
   - Classifies query as `IntentType.GREETING` (Confidence: 0.99).
   - `RuleRoutePlanner` assigns recommended route: `engine="GENERAL"`.

7. **Route Planning Stage (`RoutePlanningStage`)**:
   Reads `route_recommendation` from metadata and selects `"GENERAL"` engine.

8. **Engine Execution Stage (`EngineExecutionStage`)**:
   - Spawns `GeneralExecutionEngine` from engine factory.
   - Wraps the engine with `RuntimePolicyProxy` (enforcing resilience policies: retry, timeout, circuit breaker).
   - Builds prompt: `"[System] ... [User] Hello"`.
   - Calls `LLMProviderAdapter.generate()`.
   - Adapter maps prompt to `LLMRequest` and calls `OllamaProvider.generate()`.
   - `OllamaProvider` posts request to local Ollama API endpoint `/api/generate` on model `qwen2.5:7b`.
   - Receives JSON response containing output text and wraps it in `LLMResponse`.
   - Engine returns `ExecutionResult(status=SUCCESS, engine_name="GENERAL", message="...")`.

9. **Composition Stage (`CompositionStage`)**:
   Transforms `ExecutionResult` into `ChatResponse` DTO and stores it in context metadata.

10. **Persistence Stage (`PersistenceStage`)**:
    Saves the user message `"Hello"` and assistant response using `DefaultMemoryManager.save_turn()`.

11. **HTTP Response**:
    `ChatService` returns mapped legacy `ChatResponse` back to the HTTP client (HTTP Status 200).

---

## Streaming Trace: GENERAL_CHAT Flow (`"Hi"`)

1. **Inbound HTTP Request**:
   `POST /api/v1/chat/stream` with body `{"query": "Hi", "stream": true}` received by `app/chat/router.py`.

2. **Domain Mapping**:
   Mapped to `DomainChatRequest(message="Hi", stream=True)` and sent to `ChatService.process_request()`.

3. **Orchestrator Initiation**:
   Creates `ExecutionContext(streaming_mode=True)` and executes stages.

4. **Engine Execution Stage (`EngineExecutionStage`)**:
   - `GeneralExecutionEngine` detects `context.streaming_mode = True`.
   - Instead of calling generate synchronously, it calls `self._llm.stream(prompt)` which resolves to `LLMProviderAdapter.stream()`.
   - Adapter returns an async token generator from `OllamaProvider.stream_generate()`.
   - Engine returns `ExecutionResult(status=SUCCESS, engine_name="GENERAL", message="[Streaming Generator]", metadata={"generator": generator})`.

5. **Composition Stage**:
   Bridges the generator into `chat_response` metadata.

6. **Chat Service Resolution**:
   `ChatService` detects `context.streaming_mode = True`, extracts the generator from the result metadata, and wraps it in `_stream_response()`.

7. **SSE Delivery**:
   HTTP client receives `StreamingResponse` (media type `text/event-stream`).
   As Ollama returns tokens, they are immediately flushed to the client formatted as `data: {token}\n\n`.
