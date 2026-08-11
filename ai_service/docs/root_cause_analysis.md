# Root Cause Analysis

This report explains the critical bugs identified during the Phase 7.3 runtime debugging sprint and how they were resolved.

## Identified Issues & Root Causes

### 1. Legacy Chat Router Bypassed Orchestration (`app/chat/router.py`)
- **Symptoms**: Every request sent to the chatbot was routed to the retriever, resulting in `No relevant context found` (404) even for simple greetings like `"Hello"`.
- **Root Cause**: The FastAPI app registered both `api_router` (under `/api`) and `legacy_chat_router` (under `/api/v1/chat`). The frontend and standard test scripts were configured to hit `/api/v1/chat`. `legacy_chat_router` directly invoked `RAGService.generate_answer()`, entirely bypassing `ChatOrchestrator` and `PlatformAgentOrchestrator`.
- **Resolution**: Rewrote `app/chat/router.py` to route both synchronous and streaming requests through the composition root (`ChatService`), ensuring `/api/v1/chat` participates in the unified orchestration pipeline.

### 2. Request Schema Incompatibility
- **Symptoms**: Request validation error (HTTP 422) occurred on endpoints.
- **Root Cause**: The orchestrator endpoint `/api/chat/` expected `ChatRequest` from `app.models.chat.chat_models` which required a `message` field. However, the frontend and standard scripts sent `query`.
- **Resolution**: Extended the Pydantic schemas in `app/models/chat/chat_models.py` by adding `query` and `answer` fields, along with `model_validator(mode="before")` helpers to map incoming `query` payloads to `message` (and outgoing `message` to `answer`). This maintains absolute backward compatibility while restoring seamless frontend integration.

### 3. Missing Concrete Dependency Implementations in Composition Root
- **Symptoms**: `ModuleNotFoundError` during startup.
- **Root Cause**: The composition root (`bootstrap.py`) attempted to import:
  - `RedisMemoryManager` (from `app.memory.redis_manager`)
  - `RedisCache` (from `app.cache.redis_cache`)
  - `FAISSRetriever` (from `app.retrieval.faiss_retriever`)
  None of these classes existed in the repository, crashing the backend service during initialization.
- **Resolution**: 
  - Implemented `DefaultMemoryManager` adapter wrapping `MemoryService` to implement `IMemoryManager`.
  - Implemented `DefaultCacheManager` adapter wrapping `BaseCacheStore` to implement `ICacheService`.
  - Replaced the FAISSRetriever import with `RetrievalService` manually wired through `get_embedding_service()`, `get_vector_store_service()`, and `get_reranker()`.
  - Implemented `LocalToolExecutor` adapter to bridge legacy MCP providers to the modern `ToolService`.

### 4. FastAPI Dependency Injection Leaks in Bootstrap Code
- **Symptoms**: `AttributeError: 'Depends' object has no attribute 'load'` during engine execution.
- **Root Cause**: Calling FastAPI dependency helper functions (e.g. `get_vector_store_service()`, `get_cache_service()`) from plain Python code inside `bootstrap.py` returned raw `Depends` wrapper objects, rather than resolving the actual dependencies.
- **Resolution**: Manually resolved all Depends parameters inside `bootstrap.py` and passed them explicitly to the dependency factory functions.

### 5. Ollama Model Name Mismatch
- **Symptoms**: `ModelNotFoundException: Ollama model 'qwen2.5:3b' not found`.
- **Root Cause**: The `.env` config file mandated the model `qwen2.5:3b`, but the local Ollama server only had the `qwen2.5:7b` model pulled.
- **Resolution**: Updated `OLLAMA_MODEL` in `.env` to `qwen2.5:7b`.
