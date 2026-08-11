## [1.4.0] - 2026-08-07
### Removed
- **Cost Optimization Layer (Sprint 6) removed** — the LLM is used directly again.
  The rule-based request router, semantic response cache, rolling-memory context
  builder, token budget / response-length managers, RAG direct-answer interception
  and request analytics were all serving stale, intercepted or degenerate responses
  (e.g. a `"Mock Response"` the test suite cached into the production
  `data/semantic_cache.db`, which the live server then replayed to users on
  semantically similar queries). Removed:
  - `app/cost/` package (router, semantic_cache, budget, length, rolling_memory,
    context_builder, optimizer, analytics, models, stage, dependencies).
  - `app/api/routes/cost.py` and its `/api/cost` registration (now 404).
  - All `COST_*` settings from `app/core/config.py`.
  - `CostOptimizationLayer` LLM wrapper and the `CostOptimizationStage` /
    `ContextOptimizationStage` / `RAGDirectAnswerStage` pipeline stages in
    `app/chat/bootstrap.py` (pipeline now runs straight from `CacheStage` into
    memory / persona / platform context / intent / routing / engines).
  - `docs/cost_optimization_layer.md` and `tests/cost/`.
- The persona + platform-context wiring (`PlatformContextLoadStage`,
  `PersonaLoadStage`) and the persona-aware `GreetingResponseBuilder` greeting
  flow are **kept** — those are Sprint 5 features, not part of the cost layer.

### Changed
- `tests/conftest.py`: removed the cost-store isolation fixture.
- `tests/persona/test_pipeline_wiring.py`: mini pipeline no longer includes a
  `CostOptimizationStage`.
- `tests/chat/test_api_integration.py`: `"What is a SOC?"` / `"explain phishing"`
  no longer bypass the LLM; general questions are asserted to reach the (mocked)
  provider, and the removed cost-specific test was deleted.
- Rebuilt the FAISS index (`vector_store/`), which had been corrupted/truncated
  during repeated service restarts: `scratch/rebuild_index.py` re-ingested all
  10 course overviews + 3553 lesson chunks (3563 vectors).

### Validation
- 675 passed (full regression suite minus the removed cost tests), flake8 clean.
- Live probes on `/api/chat/`: `hello` → persona greeting; `what is siem` →
  streamed LLM answer; `what is soc` / `what is phishing` → routed to the LLM;
  `GET /api/cost/analytics` → 404. The dev OmniRoute gateway still returns
  single-token answers (`!` / `.`) for **non-stream** requests — the web client
  always streams, so this does not affect the user experience.

## [1.3.0] - 2026-08-07
### Added
- Cost Optimization Layer (Sprint 6): transparent token/cost reduction between the
  chat pipeline and the LLM provider. Rule-based request router (greetings, thanks,
  goodbyes, help, navigation, static FAQs answered locally), semantic response cache
  (SQLite + cosine similarity), rolling conversation memory with compact history,
  token budget manager (prompt never exceeds cap), response-length guidance
  (concise/detailed max_tokens), high-confidence RAG direct answers, and SQLite
  request analytics with an internal `GET /api/cost/analytics` endpoint.
- New package `app/cost/` (models, router, semantic_cache, context_builder,
  rolling_memory, budget, length, analytics, optimizer, stage, dependencies).
- Unit tests: `tests/cost/test_cost_layer.py` (13 tests).

### Changed- `app/chat/bootstrap.py`: wrapped the LLM with `CostOptimizationLayer` and inserted
  `CostOptimizationStage`, `ContextOptimizationStage`, `RAGDirectAnswerStage` into the
  stage pipeline.
- `app/chat/bootstrap.py`: wired the previously-orphaned `PlatformContextLoadStage`
  and `PersonaLoadStage` into the pipeline (after `MemoryLoadStage`, before intent
  analysis) so the BlueTeamers mentor persona + learner level actually reach the
  LLM system prompt — fixes responses that had reverted to a generic voice.
- `app/core/config.py`: added the `COST_*` settings block.
- `app/llm/adapter.py`: forwards `max_tokens` (backward compatible).
- `app/api/routes/__init__.py`: registered the `/cost` router.
- `app/cost/router.py` GREETING response: keeps markdown `\n\n` so streamed templated
  greetings preserve newlines (regression vs. existing greeting flow).
- `app/prompt_builder/simple_prompt_builder.py` + `app/persona/personas.py`: added a
  "cybersecurity-first" rule so ambiguous terms (`siem`, `soc`, `ids`, `ips`, ...) are
  ALWAYS answered in their cybersecurity sense — never disambiguated into languages,
  names, cities, fruits, etc., and never answered with "which context are you referring
  to?". 
- `app/cost/stage.py`: `RAGDirectAnswerStage` now recognizes a `SECURITY_TERMS`
  vocabulary (siem, soc, soar, edr, xdr, ids, ips, waf, dlp, pki, cve, owasp, mitre,
  phishing, ransomware, ...). A bare security term or a short factual query that
  mentions one (e.g. "what is siem") is answered deterministically from the user's
  RAG knowledge base at a lower confidence threshold (`term_threshold`, default
  0.60) instead of the general 0.86 — the local dev LLM ignored system-prompt
  disambiguation rules, so these queries never reach the LLM at all
  (`llm_used: false`). Query is ignored above 140 chars and non-term queries keep
  the existing length/"what is" guards.
- `app/core/config.py`: added `COST_RAG_DIRECT_ANSWER_TERM_THRESHOLD` (0.60).
- `app/cost/dependencies.py` + `app/chat/bootstrap.py`: pass `term_threshold` into
  `RAGDirectAnswerStage`.
- `app/cost/stage.py`: `RAGDirectAnswerStage` now cleans direct-RAG output.
  `_pick_best_document` scans top-5 results and skips junk chunks (ASCII-art /
  box-drawing diagrams, bare code-fence leftovers, fragments under 10 words)
  so retrieval noise like a stray "SOC Manager" diagram is never returned.
  `_clean_content` drops redundant leading headings (e.g. `# Welcome to the SOC`
  + `# Welcome to the Security Operations Center` → keep the latter) and
  duplicate consecutive headings (`# What is SIEM?` repeated), then collapses
  blank runs — giving structured, readable answers instead of raw lesson dumps.
- Tests: `tests/cost/test_cost_layer.py` now has 20 tests (added ASCII-art
  rejection and heading deduplication; made fixture docs realistic lengths).

### Validation
- 695 passed (20 cost tests + 2 persona pipeline-wiring tests + 2 ambiguity-rule
  tests + full regression suite), flake8 clean on cost files, bootstrap smoke OK.
- Live probes on `/api/chat/` confirm `"soc"`, `"what is soc"` and `"siem"` all
  stream clean, structured course content with `llm_used: false` — no ASCII
  diagrams, no duplicated headings, no disambiguation.
- Design + verification steps: `docs/cost_optimization_layer.md`.
- Persona end-to-end check: `scratch/persona_verify.py`.

## [1.2.0] - 2026-08-05
### Added
- Course-Aware Assessment Agent: quizzes are only offered when the user is enrolled
  in a course matching the asked topic and has not recently been assessed on it.
- `CourseContextService` for deterministic quiz-eligibility gating from enrolment state.
- Per-course learning progress tracking (scores, weak/strong topics, completion %,
  last assessment date, revision topics).
- When not enrolled, the AssessmentStage now delegates to the Course Recommendation
  service (no quiz) and surfaces Enroll / View Course / skip course cards.

### Changed
- `app/agents/assessment/agent.py`: added `resolve_offer()` course gate, course-aware
  `offer_message()`, `course_recommendation_message()`, and course_slug tracking.
- `app/chat/pipeline/assessment_stage.py`: course-aware `_maybe_offer()`,
  `_recommend_course()` and course-card builder.
- `app/chat/bootstrap.py`: wired `CourseContextService` (AssessmentAgent) and
  `RecommendationService` (AssessmentStage).
- `app/core/config.py`: added `ASSESSMENT_REQUIRE_ENROLLMENT`,
  `ASSESSMENT_RECENT_WINDOW_SECONDS`, `ASSESSMENT_COURSE_RECOMMENDATION_COUNT`.

### Validation
- 26 passed (agents/assessment), 81 passed (chat), bootstrap builds.

## 2026-08-03

### Modified Files
- None (Baseline Audit)

### Reason
Established the baseline state of the platform to guide Phase 5 Production Stabilization. All future changes will be driven by fixing these identified issues.

### Validation
- `pytest`
- Baseline Results: 340 collected, 335 PASS, 5 FAILED, 275 WARNINGS.

### Status
Completed

### Modified Files
- app/tools/base.py
- app/chat/engines/tool_engine.py
- tests/chat/engines/test_engines.py

### Reason
Fixed BaseTool interface missing initialize/shutdown. Fixed async mock returning unawaited coroutines in 	est_tool_engine_execution. Fixed ExecutionResult.failed() argument signature.

### Validation
- pytest tests/chat/engines/test_engines.py
- PASS

### Status
Completed

### Sprint Phase 6 - Dependency Modernization & Full Validation
- **app/embeddings/provider.py**: Updated SentenceTransformers method get_sentence_embedding_dimension to get_embedding_dimension.
- **app/agents/events/event_bus.py**: Migrated from syncio.iscoroutinefunction to inspect.iscoroutinefunction.
- **requirements.txt**: Added httpx2 to resolve StarletteDeprecationWarning.
- **app/agents/context.py**: Reverted erroneous rozen=True setting injected by batch scripts across sub-contexts, ensuring mutability of runtime properties during initialization while retaining AgentContext immutability.
- **app/guardrails/config/guardrails_config.py**: Adjusted ConfigDict to include extra='ignore' to support broader environment variables without validation failures.
- **Test Suite**: Fully green. 340 passing tests.



### Sprint Phase 6 - Frontend Integration & Local Deployment
- **app/chat/bootstrap.py**: Created dependency injection bootstrap layer to wire up Ollama and FAISS.
- **app/api/routes/chat.py**: Updated to use bootstrap dependency, removing inline Dummy classes.
- **infosecdairies/src/hooks/useChat.ts**: Implemented custom hook for handling Server-Sent Events (SSE) streaming.
- **infosecdairies/src/components/ui/Chat.tsx**: Built chat interface with Markdown and streaming token support.
- **infosecdairies/src/pages/ChatPage.tsx**: Added full page view for the Chat UI.
- **Batch Scripts**: Added start_ollama.bat, start_backend.bat, start_frontend.bat, and start_all.bat for localized deployment.
- **Status**: Completed.


### Sprint Phase 7.1 - Ollama Integration Architecture Audit
- **docs/ollama_architecture_audit.md**: Detailed audit of the Chat Pipeline, RAG, and Tool Engine integration points.
- **docs/llm_execution_flow.md**: High-level flow tracing user requests through the orchestrator to the LLM.
- **docs/provider_inventory.md**: Documented \LLMFactory\, \BaseLLMProvider\, and \OllamaProvider\.
- **docs/ollama_integration_plan.md**: Outlined plan to configure DI factory injection.
- **docs/risk_assessment.md**: Validated architectural risk as LOW.
- **Status**: Completed.


### Sprint Phase 7.2 - Ollama Runtime Integration
- **.env**: Set \OLLAMA_MODEL\ to \qwen2.5:3b\.
- **app/core/config.py**: Set default model to \qwen2.5:3b\.
- **app/chat/bootstrap.py**: Removed hardcoded \OllamaLLMService\ and injected generic \LLMFactory.get_provider()\.
- **docs/ollama_runtime_validation.md**: Generated testing summary for Ollama startup.
- **docs/ollama_integration_summary.md**: Generated overarching report.
- **Status**: Completed.


### Sprint Phase 7.3 - Critical Runtime Debugging & End-to-End Chat Routing
- **app/chat/router.py**: Rerouted legacy `/api/v1/chat` and `/api/v1/chat/stream` endpoints to pass through `ChatService`.
- **app/chat/bootstrap.py**: Wired up concrete adapters, manually resolved FastAPI Depends, and configured MCP `LocalToolExecutor` adapter.
- **app/retrieval/faiss_retriever.py**: Added retriever bridge adapter to implement `IRetriever` expected by `RagExecutionEngine`.
- **app/models/chat/chat_models.py**: Extended Pydantic request and response schemas to support both `query` and `message` payloads.
- **app/chat/service.py**: Fixed stream generator resolution from final context metadata.
- **app/memory/default_manager.py**: Added memory manager adapter for `MemoryService` integration.
- **app/cache/default_manager.py**: Added cache manager adapter for `BaseCacheStore` integration.
- **app/tools/executors/local_executor.py**: Added tool executor bridge adapter.
- **.env**: Updated `OLLAMA_MODEL` to `qwen2.5:7b` to match available models.
- **Status**: Completed.


### Sprint Phase 7.4 - Response Formatting & Rendering Stabilization
- **app/chat/service.py**: Modified `_stream_response` to serialize streaming tokens to standard JSON event-stream payloads.
- **infosecdairies/tailwind.config.ts**: Enabled `@tailwindcss/typography` plugin in React config to support Markdown elements rendering styled with the prose typography classes.
- **tests/chat/test_api_integration.py**: Adjusted streaming tests to match JSON event stream structure.
- **tests/chat/test_service.py**: Adjusted streaming count assertions.
- **tests/chat/test_stress_validation.py**: Updated stream checks.
- **Status**: Completed.



## [1.1.0] - 2026-08-03
### Added
- Feature 1: Intelligent Query Router supporting 7 new distinct intents (IMAGE_CHAT, DOCUMENT_CHAT, LAB_ASSISTANT, INVESTIGATION, RAG_CHAT, TOOL_CHAT, GENERAL_CHAT).

### Changed
- Refactored `RuleIntentClassifier` to detect files and keywords for the new intents.
- Updated `RuleRoutePlanner` to route IMAGE_CHAT, DOCUMENT_CHAT, LAB_ASSISTANT, and INVESTIGATION to the AGENT engine.
