# Course-Aware Assessment Agent

## Feature
Implemented a dedicated Course-Aware Assessment Agent that only offers interactive
in-chat quizzes when the learner is **enrolled** in a course whose topic the current
question maps to (and they have not recently been assessed on that topic). When the
learner is not enrolled in a matching course, NO quiz is offered; the pipeline
delegates to the Course Recommendation service and surfaces related courses
(Enroll / Go to course / Course info / skip) instead.

## Design
- Assessment Agent (`app/agents/assessment`) now owns only quiz generation,
  evaluation, explanation, scoring and progress tracking.
- New `CourseContextService` (`app/agents/assessment/course_context.py`) decides
  *quiz eligibility* from live enrolment state — it does NOT recommend courses.
  Course recommendations are delegated to the existing `RecommendationService`
  from the `AssessmentStage`.
- Trigger rules enforced: enrolled ✓ + topic belongs to course ✓ + learning
  question ✓ + not recently assessed ✓ + explicit user confirmation ✓.
- Learning progress now tracked per course (assessments, scores, weak/strong
  topics, completion %, last assessment date, revision topics).

## Files
- Added: `app/agents/assessment/course_context.py`
- Modified: `app/agents/assessment/agent.py`, `models.py`, `profile_store.py`,
  `app/chat/pipeline/assessment_stage.py`, `app/chat/bootstrap.py`,
  `app/core/config.py`
- Tests: added `tests/agents/assessment/test_course_context.py`,
  `tests/chat/test_assessment_stage_course.py`; updated
  `tests/chat/pipeline/test_assessment_stage.py` (legacy-mode stage mechanics).

## Validation
- `tests/agents/assessment` (26 passed)
- `tests/chat` (81 passed)
- Full `get_chat_service()` bootstrap builds successfully.

---

# Phase 5 â€” Production Stabilization

## Baseline Audit

### Objective
Establish the current health of the codebase before beginning production stabilization, ensuring all future changes are driven by existing failures or warnings.

### Problem
The initial `pytest` run revealed existing test failures and a large number of deprecation warnings related to Pydantic v2 and `datetime.utcnow()`.

### Root Cause
- Pydantic V1 `class Config` and `.copy()` are heavily used.
- `datetime.utcnow()` is used across security and observability modules.
- Unawaited coroutine warnings in test mocks.

### Solution
Ran the full test suite with `$env:PYTHONPATH = "."` to correctly resolve local imports, capturing the baseline state.

### Files Modified
- None (Audit Only)

### Validation
- `pytest` executed.
- Baseline Results:
  - 340 tests collected.
  - 335 passed.
  - 5 failed (`test_tool_engine_execution`, `test_general_chat_non_streaming`, `test_rag_chat_non_streaming`, `test_tool_chat_non_streaming`, `test_cache_hit_bypasses_execution`).
  - 275 warnings (predominantly `PydanticDeprecatedSince20` and `DeprecationWarning` for `datetime`).

### Design Decision
Following the stabilization strategy, all changes going forward will specifically target fixing these 5 failures and resolving the 275 warnings in isolated, verifiable chunks.

### Impact
Provides a clear, deterministic starting point to measure regression-free progress.

### Lessons Learned
`PYTHONPATH` must be explicitly set for test discovery when executing from the project root on Windows to avoid `ModuleNotFoundError` during test collection.
## Phase 2 — Interface Compatibility

### Objective
Ensure Event models and Tool mock implementations are compatible with the latest execution architectures.

### Problem
ExecutionResult.failed() was missing the required errors positional argument. The async mock for provider.execute in 	est_tool_engine_execution was returning an unawaited coroutine due to mocking the wrong method (execute_tool instead of execute). BaseTool lacked initialize and shutdown implementations, breaking abstract class instantiations.

### Root Cause
Changes in the ITool interface required all tools (including BaseTool) to implement lifecycle hooks. The ToolExecutionEngine updated its provider invocation but tests were not updated to mock the new execute method signature.

### Solution
- Implemented default initialize() and shutdown() methods in pp/tools/base.py.
- Fixed the mock setup in 	ests/chat/engines/test_engines.py to mock provider.execute.
- Fixed ExecutionResult.failed() argument signature in pp/chat/engines/tool_engine.py.

### Files Modified
- app/tools/base.py
- app/chat/engines/tool_engine.py
- tests/chat/engines/test_engines.py

### Validation
- pytest tests/chat/engines/test_engines.py
- PASS (3 passed)

### Design Decision
Adding empty implementations for initialize and shutdown directly on BaseTool correctly satisfies the ITool contract without forcing every simple mock tool to define them manually.

### Lessons Learned
Async mock assignments must exactly match the method signature invoked by the code, otherwise the mock returns a raw coroutine object which causes cryptic type validation failures downstream (e.g. Pydantic rejecting coroutines when expecting strings).

### Phase 6 - Dependency Modernization & Full Validation
- Fixed SentenceTransformers deprecation for get_embedding_dimension() method.
- Resolved Python 3.16 syncio.iscoroutinefunction deprecation by shifting to inspect.iscoroutinefunction().
- Suppressed StarletteDeprecationWarning regarding httpx by installing httpx2.
- Executed full test suite validating all phases.
- **Result**: 340 tests passed successfully. Warning count dropped significantly.



## Phase 6 - Frontend Integration & Local Deployment

### Objective
Integrate the backend with the React frontend and prepare the suite for local demonstration using Ollama.

### Problem
Frontend lacked a Chat UI and SSE streaming support. Backend chat endpoint was coupled to dummy implementations.

### Root Cause
Phase 5 focused solely on backend stabilization. Frontend chat components had not been implemented.

### Solution
- Created a dependency injection bootstrap layer (\pp/chat/bootstrap.py\) to wire up real Ollama and FAISS dependencies.
- Updated \pp/api/routes/chat.py\ to use the bootstrap layer, preserving the API contract.
- Implemented \useChat.ts\ for SSE processing in the React frontend.
- Built \Chat.tsx\ with Markdown support and integrated it into a new \/chat\ route.
- Generated deployment batch scripts and demonstration documentation.

### Files Modified
- \pp/chat/bootstrap.py\ (NEW)
- \pp/api/routes/chat.py\`n- \infosecdairies/src/hooks/useChat.ts\ (NEW)
- \infosecdairies/src/components/ui/Chat.tsx\ (NEW)
- \infosecdairies/src/pages/ChatPage.tsx\ (NEW)
- \infosecdairies/src/App.tsx\`n- Various markdown and batch script files for deployment.

### Validation
- Verified frontend build.
- Batch scripts correctly launch all dependencies.

### Design Decision
Kept \chat.py\ unmodified in its signature, moving all orchestration logic to \ootstrap.py\. Used Qwen2.5:7b as the standard demo model for speed and capability.

### Lessons Learned
SSE parsing in React requires robust chunk handling since text streams may be split arbitrarily over network packets.


## Phase 7.1 - Ollama Integration Architecture Audit

### Objective
Perform a comprehensive audit of the AI execution pipeline to identify the safest integration point for Ollama as a first-class LLM provider without modifying existing logic.

### Problem
Ollama integration requires careful alignment with the existing enterprise architecture (Dependency Injection, Thin Orchestrator).

### Solution
Conducted a static analysis of the LLM Factory layer, Chat Engines, Tool Calling pipelines, and RAG execution paths. 
Generated complete architectural documentation mapping the execution flow from the React frontend down to the LLM generation.

### Files Modified
- docs/ollama_architecture_audit.md (NEW)
- docs/llm_execution_flow.md (NEW)
- docs/provider_inventory.md (NEW)
- docs/ollama_integration_plan.md (NEW)
- docs/risk_assessment.md (NEW)

### Validation
- Verified that \LLMFactory\ and \OllamaProvider\ already exist natively in the architecture.

### Design Decision
The optimal integration strategy is to simply update \pp/chat/bootstrap.py\ to dynamically fetch the provider from \LLMFactory.get_provider()\, rather than writing net-new classes.

### Lessons Learned
The underlying abstractions (e.g., \ILLMService\) provided a highly decoupled foundation, allowing the factory pattern to hot-swap models without touching the orchestrator logic.


## Phase 7.2 - Ollama Runtime Integration

### Objective
Integrate the local Ollama runtime smoothly by enforcing Dependency Injection routing without manipulating API logic.

### Changes Implemented
- **Environment Config**: Updated \.env\ and \pp/core/config.py\ to mandate \LLM_PROVIDER=ollama\ and \OLLAMA_MODEL=qwen2.5:3b\.
- **Composition Root**: Modified \pp/chat/bootstrap.py\ to construct the main pipeline using \LLMFactory.get_provider()\, entirely decoupling it from explicit Ollama dependencies.
- **Deprecation Governance**: Left \ollama_client.py\ untouched per user instructions to avoid potentially disrupting hidden dependencies until a proper cleanup phase.

### Documentation
- **ollama_runtime_validation.md**: Outlines backend functionality tests and RAG routing validation.
- **ollama_integration_summary.md**: Overall summary of the integration phase.

## Phase 7.3 - Critical Runtime Debugging & End-to-End Chat Routing

### Objective
Restore the intended query routing path and ensure end-to-end chat execution works for GREETING, GENERAL, RAG, and TOOL flows without bypassing orchestration.

### Changes Implemented
- **Legacy Endpoint Routing**: Refactored `app/chat/router.py` to delegate `/api/v1/chat` and `/api/v1/chat/stream` requests directly to `ChatService` instead of directly calling `RAGService`.
- **Composition Root Hardening**: Modified `app/chat/bootstrap.py` to fix missing/broken imports (`RedisMemoryManager`, `RedisCache`), manually resolve FastAPI `Depends` variables, and configure MCP adapters.
- **RAG Subsystem Wiring**: Created `app/retrieval/faiss_retriever.py` adapter to map `RetrievalService` results into the `IRetriever` interface used by `RagExecutionEngine`.
- **Schema Mapping**: Extended `ChatRequest` and `ChatResponse` models in `app/models/chat/chat_models.py` with `query`/`answer` fields and model validators to ensure backward compatibility with frontend payloads.
- **Streaming Fix**: Corrected streaming generator lookup in `app/chat/service.py` to extract from the final `ExecutionResult` object.
- **Ollama Configuration**: Updated `OLLAMA_MODEL` to `qwen2.5:7b` in `.env` to match the model installed on the host.

### Documentation
- **query_router_runtime_audit.md**: Outlines the routing logic and test matrix.
- **runtime_execution_trace.md**: Synchronous and streaming request traces.
- **root_cause_analysis.md**: Exhaustive summary of runtime issues and fixes.
- **rag_runtime_validation.md**: RAG path validation and search verification.
- **phase73_completion_report.md**: Final sprint completion summary.

### Validation
- Successfully ran and passed all tests: `tests/test_chat.py`, `tests/chat/test_orchestrator.py`, `tests/chat/test_service.py`, and `tests/chat/test_api_integration.py`.
- Verified end-to-end local streaming and non-streaming requests using `test_stream.py` and `test_api.py`.

## Phase 7.4 - Response Formatting & Rendering Stabilization

### Objective
Ensure LLM response markdown formatting (headings, code blocks, bullet points, spacing) is fully preserved across the streaming pipeline and rendered styled inside the React interface.

### Changes Implemented
- **JSON Streaming Serialization**: Refactored `_stream_response` in `app/chat/service.py` to serialize streaming tokens into structured JSON payloads (`data: {"token": "..."}\n\n`) and yield `[DONE]`. This prevents newlines/whitespace character loss over the HTTP event-stream connection.
- **Frontend Typography Activation**: Registered the `@tailwindcss/typography` plugin in `infosecdairies/tailwind.config.ts` to activate CSS rendering rules for the Tailwind prose classes (`prose prose-sm dark:prose-invert`) wrapped around `<ReactMarkdown>`.
- **Test Suite Updates**: Adjusted stream checks and assertions in `tests/chat/test_api_integration.py`, `tests/chat/test_service.py`, and `tests/chat/test_stress_validation.py` to match the JSON event stream structure.

### Documentation
- **response_formatting_audit.md**: Documents pipeline segment status and causes of formatting failure.
- **markdown_rendering_validation.md**: Verifies headings, lists, tables, code blocks, bold/italic, and blockquotes rendering.
- **phase74_completion_report.md**: Summarizes sprint metrics and validations.

### Validation
- All 340 tests passed cleanly.
- Verified output stream structure via `test_stream.py`.



## Feature 1 - Intelligent Query Router

### Objective
Restore intended routing architecture and accurately classify requests into 7 distinct intents.

### Changes Implemented
- Updated `IntentType` enum in `intent_types.py`.
- Updated `RuleIntentClassifier` to support keyword and file-based intent matching for IMAGE_CHAT, DOCUMENT_CHAT, LAB_ASSISTANT, and INVESTIGATION.
- Updated `RuleRoutePlanner` to correctly route these intents to the appropriate engine (AGENT, RAG, TOOL, GENERAL).

### Validation
- Verified via pytest tests in `tests/chat/`.

## Feature 2 - Platform Knowledge Repository

### Objective
Ensure that platform-specific questions (courses, labs, learning paths, assessments, badges, progress, certifications, platform documentation) are answered exclusively from BlueTeamers data sources. Prevent the LLM from inventing or recommending external courses.

### Changes Implemented
- **Intent Routing**: Added `PLATFORM_INFO` to `IntentType` enum and configured `RuleIntentClassifier` to route platform-related queries (e.g., "suggest a course", "what certifications do you have") to this intent. Boosted confidence in `RuleConfidenceEvaluator`.
- **Engine Mapping**: Updated `RuleRoutePlanner` to map `PLATFORM_INFO` to the `"PLATFORM"` execution engine.
- **Repository Integration**: Created `IPlatformKnowledgeRepository` interface and `PlatformKnowledgeRepository` implementation, reusing existing `CoursesAPI` and Django integrations for accurate, live catalog querying. Added mock fallback for missing endpoints like `labs` and `badges`.
- **Platform Execution Engine**: Created `PlatformExecutionEngine` to inject platform context into the LLM system prompt, instructing it strictly to only use the provided platform data and not hallucinate external materials.

### Validation
- Validated intent classification via `test_classifiers.py`.
- Validated engine execution and mock LLM prompting via `test_platform_engine.py`.

## Feature 3 - Live Platform Data End-to-End (Django + Demo Auth)

### Objective
Make platform-specific responses (progress, enrolled courses, certificates) show real BlueTeamers account data instead of "no access" fallbacks.

### Root Cause
- Django backend (port 8000) was not running in this environment, so demo auth and platform API calls always failed.
- `planning_stage.py:38` called `context.memory.get_recent_context(3)` on a plain dict — crashed with `AttributeError` once `PlatformContextLoadStage` populated `context.memory` with `platform_context`.
- `DjangoPlatformRepository._map_courses` constructed `Course(id=...)` but pydantic v2 alias `slug` requires the alias keyword, silently dropping the id (courses had empty ids, so `get_enrolled_courses` returned nothing).

### Changes Implemented
- Bootstrapped a Django venv at `infosecdairies/infosec-backend/backend/.venv` (`python3 -m venv --without-pip` + `get-pip.py`, since ensurepip is absent on this host) and installed requirements (Django 6.0.7, DRF 3.17.1, allauth 65.18, dj-rest-auth 7.2, simplejwt 5.5.1).
- Generated+applied the pending `certificates` migration (`0004_alter_certificate_course_slug_and_more`).
- Seeded demo data via `infosecdairies/infosec-backend/backend/seed_demo_user.py`: user `harika@example.com` / `password123`, paid `CoursePurchase` + `Enrollment` for blue-team-soc-fundamentals, log-analysis-for-beginners, siem-fundamentals; `LessonProgress` for a subset of lessons; `QuizScore` records.
- Started Django on `0.0.0.0:8000` (HS256 JWT fallback — no private key locally), log at `~/ailogs/django.log`.
- Fixed `app/chat/pipeline/planning_stage.py`: pass `context.memory or {}` directly to `create_plan` (memory is a `Dict[str, Any]`, not a manager object).
- Fixed `app/platform/repositories/django_repository.py` `_map_courses`: use `slug=` instead of `id=` to satisfy the pydantic alias.

### Validation
- `POST /api/chat/` "what is my progress in blue team soc fundamentals?" -> "you have completed 6 lessons and are 11% through the course" (real data, `context_used=[enrolled-courses, progress]`).
- "which courses am I enrolled in?" -> lists the 3 seeded courses.
- "do I have any certificates?" -> reports none + lists enrollments.
- RAG still returns citations ("what is SIEM" -> Blue Team & SOC Fundamentals / What is a SIEM?) and GENERAL chat still works.
- Demo JWT is cached by `DemoAuthenticationService` (no login on every request).

## Feature 4 - Interactive Course Cards with Actions

### Objective
Make platform responses redirect users directly to their courses: render course cards in chat with "Enroll course", "Go to course", and "Course info" actions.

### Root Cause
- `PlatformExecutionEngine._build_platform_ui` produced cards with a single `action` (label/action_type/payload), but `Chat.tsx` only rendered card types `course_recommendation` and `progress_snapshot` — neither of which the backend ever emits, so platform cards never displayed.

### Changes Implemented
- `ai_service/app/chat/engines/platform_engine.py` `_build_platform_ui`:
  - Enrolled-course cards now include title, difficulty, duration, description, live `progress` % (from progress data), and `actions` = ["Go to course" -> open_course /courses/:slug, "Course info" -> course_info].
  - Recommended-but-not-enrolled course cards add "Enroll course" -> enroll_course /courses/:slug/checkout (skip already-enrolled slugs).
  - Certificate actions now carry a `url` to `/verify/:id`.
  - Kept single `action` field = first action for backward compatibility.
- `infosecdairies/src/components/ui/chat/PlatformCards.tsx`: added `CourseCard` — renders title, level/duration, progress bar, expandable description ("Course info" toggles inline), and action buttons; opens payload `url` in a new tab for navigation actions.
- `infosecdairies/src/components/ui/Chat.tsx`: renders `CourseCard` for cards of type `course` (or any card with a non-empty `actions` array).

### Validation
- `POST /api/chat/` "which courses am I enrolled in?" -> 3 cards, each with ["Go to course", "Course info"] and url `/courses/<slug>`.
- "what is my progress in blue team soc fundamentals?" -> cards show live progress (11% / 12% / 6%).
- "suggest a course" -> cards for unenrolled courses include ["Enroll course", "Go to course", "Course info"] (verified via `_build_platform_ui` unit call; enrolled slugs are de-duplicated).
- `node node_modules/typescript/bin/tsc --noEmit` passes. ESLint: only pre-existing `no-explicit-any` errors (file-wide convention).
