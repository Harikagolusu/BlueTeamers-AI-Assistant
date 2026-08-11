# BlueTeamers AI Assistant — Technical Context

This document describes the **current, implemented** state of the AI Assistant
feature for the BlueTeamers cybersecurity e-learning platform. It covers the
FastAPI AI service (`ai_service/`), the React frontend surfaces
(`infosecdairies/src/`), and how they integrate with the Django backend. Only
wired, functioning code is described; scaffolding or placeholder code is called
out explicitly so it is not mistaken for implemented behaviour.

---

## 1. Project Overview

The AI Assistant is a chat-based cybersecurity learning copilot for BlueTeamers
(InfoSec Dairies). It consists of three cooperating processes:

| Process | Tech | Port | Notes |
|---|---|---|---|
| **Frontend** | React + Vite + TypeScript + Tailwind | `http://127.0.0.1:5173` (dev) | Vite proxy to Django and AI service; `src/services/api.ts` governs base URLs |
| **Django backend** | Django 6 + DRF + Simple JWT | `:8000` | Auth, courses, certificates, payments |
| **AI service** | FastAPI + Uvicorn | `:8001` | Chat pipeline, RAG, memory, conversations, freemium |

The AI service is the core of this feature. It exposes:

- `POST /api/chat/` — streaming/non-streaming chat (runtime chat path).
- `POST /api/v1/chat/` — legacy RAG chat (kept for backward compatibility).
- `GET /api/chat/access` — freemium access status for the frontend indicator.
- `/api/conversations` — Recent Conversations & Favorites CRUD.
- `/api/health`, `/api/me`, `/api/knowledge/*`, `/metrics` — ops endpoints.

Note: the frontend also calls `GET /api/chat/session` to initialise the
workspace with a personalised welcome message
(`app/chat/services/session_initializer.py::SessionInitializer`), but this
service is **not wired to any route** — the endpoint returns 404 and the
frontend silently falls back to a fresh conversation (see §10).

The working LLM path in development is **OmniRoute** (an OpenAI-compatible
gateway); the production provider contract is **Amazon Bedrock**. All providers
sit behind the `BaseLLMProvider` interface and are chosen by
`app/llm/factory.py`.

---

## 2. High-Level Architecture

```
┌──────────────────────┐   fetch() w/ Bearer JWT    ┌─────────────────────┐
│ React frontend       │ ──────────────────────────► │ FastAPI AI service  │
│ (Workspace, floating │   SSE text/event-stream     │ (127.0.0.1:8001)    │
│ assistant)           │ ◄────────────────────────── │                     │
└──────────────────────┘                             └──────┬───────┬──────┘
                                                             │       │
                                            HTTPS to Django   │       │ LLM over HTTP
                                                             ▼       ▼
                                              ┌────────────────┐  ┌──────────────┐
                                              │ Django :8000   │  │ OmniRoute    │
                                              │ auth/courses/  │  │ /v1/chat/    │
                                              │ payments/certs │  │ completions  │
                                              └────────────────┘  └──────────────┘
```

Key design decisions:

- **Composition root**: `app/chat/bootstrap.py::get_chat_service()` wires every
  dependency manually (no DI framework) and returns the same `ChatService`
  singleton used by both chat routers.
- **Pipeline pattern**: `ChatOrchestrator` runs 14 ordered, immutable-context
  stages. Each stage takes an `ExecutionContext` and returns a derived copy.
- **Engine registry**: routing resolves an Intent → engine name → engine class,
  then `RealEngineFactory` instantiates it (every engine wrapped in
  `RuntimePolicyProxy`).
- **Provider abstraction**: LLM providers, embedding providers, vector stores,
  rerankers, memory stores, caches all have interface + concrete layers so
  development (local/OmniRoute) and production (Bedrock) differ by config.
- **JWT trust**: the AI service verifies Django-issued RS256 access tokens using
  the Django public key; `user_id` (stable across refresh) is the canonical
  identity for memory/conversations/freemium.

---

## 3. Folder Structure (AI service)

```
ai_service/
├── app/
│   ├── main.py                  # FastAPI app, router registration
│   ├── lifecycle.py             # lifespan: logging + background knowledge ingest
│   ├── middleware.py            # CORS -> Logging -> Observability -> Runtime
│   ├── config.py                # Pydantic Settings (single source of config)
│   ├── chat/                    # Chat orchestration (the runtime path)
│   │   ├── bootstrap.py         # Composition root
│   │   ├── orchestrator.py      # Pipeline runner
│   │   ├── service.py           # ChatService (Application Layer boundary)
│   │   ├── router.py            # Legacy /api/v1/chat endpoints
│   │   ├── pipeline/            # 14 pipeline stages
│   │   ├── engines/             # 17 execution engines + factories
│   │   ├── intent/              # Intent Intelligence pipeline
│   │   ├── policies/            # RuntimePolicyProxy (rate-limit/quota/audit)
│   │   ├── context/             # ExecutionContext (immutable)
│   │   └── exceptions/, sanitize.py, schemas.py
│   ├── api/routes/              # /api/chat, /api/health, /api/me
│   ├── llm/                     # Providers: OmniRoute, Bedrock, Ollama; adapter/factory
│   ├── rag/                     # RAG engine + interfaces (RAGService facade)
│   ├── retrieval/               # RetrievalService, FAISSRetriever, reranker
│   ├── embeddings/              # SentenceTransformer provider (bge-small-en-v1.5)
│   ├── vector_store/            # FAISS provider + JSON metadata store
│   ├── chunking/                # MarkdownRecursiveChunker
│   ├── knowledge/               # Static-course ingestion pipeline + sources
│   ├── memory/                  # Short-term session memory (in-memory store)
│   ├── conversations/           # Recent Conversations & Favorites (SQLite)
│   ├── freemium/                # Free/premium AI access (SQLite)
│   ├── adaptive/                # Adaptive learning engine (SQLite)
│   ├── persona/                 # Persona prompt builder + level detector
│   ├── prompt_builder/          # SimplePromptBuilder (domain prompt builder)
│   ├── platform/                # Django API client, repository, context, recommend
│   ├── streaming/               # SSE StreamingService (legacy RAG streaming)
│   ├── cache/                   # In-memory semantic cache
│   ├── observability/           # Prometheus metrics + W3C tracing middleware
│   ├── security/                # JWTValidator, resolve_user_identity
│   ├── guardrails/              # Guardrails service (health-wired)
│   ├── mcp/                     # MCP config/catalog/provider registry (scaffold tools)
│   ├── tools/                   # Tool framework (some implementations real, unused at runtime)
│   ├── agents/                  # Agent platform scaffolding (AgentExecutor is the wired exception)
│   ├── planning/                # Planning layer for the AGENT engine
│   ├── context/                 # (platform context lives in platform/)
│   ├── recommendation/          # Course recommendation service
│   ├── runtime/                 # RuntimeManager middleware (rate-limit/audit)
│   ├── evaluation/, analytics/, graph/, indexing/, services/, shared/, providers/, utils/
│   └── models/                  # Pydantic DTOs (ChatRequest, ExecutionResult, ...)
├── data/
│   ├── conversations.db         # conversations + messages (SQLite)
│   ├── freemium.db              # daily_usage (SQLite)
│   ├── memory.db                # session memory (SQLite)
│   ├── adaptive.db              # learner profiles (SQLite) [default store]
│   └── vector_store/            # FAISS index + metadata.json
└── tests/                       # Backend test suite (conversations, retrieval, etc.)
```

The repository root also contains `infosecdairies/` (React frontend) and
`infosecdairies/infosec-backend/` (Django).

---

## 4. Modules

### 4.1 `app/chat` — chat orchestration

- **`bootstrap.py`** is the composition root. It builds: LLM provider (via
  `LLMFactory`) → `LLMProviderAdapter` → prompt builder → cache/memory/embedding/
  vector-store/retrieval services → intent service → tool executor/catalog →
  engine registry + `RealEngineFactory` → pipeline stages → `ChatOrchestrator` →
  `ChatService`.
- **`orchestrator.py`** iterates the stage list, passes the (immutable) context,
  stops on `cancellation_requested`, and extracts `execution_result` from
  context metadata.

### 4.2 `app/llm` — LLM provider abstraction

- `BaseLLMProvider` interface: `generate(LLMRequest) -> LLMResponse`,
  `stream_generate(LLMRequest) -> AsyncGenerator[str, ...]`,
  `health_check()`.
- Concrete providers: `OmniRouteProvider` (OpenAI-compatible `/chat/completions`
  + `/models`), `BedrockProvider` (AWS Bedrock runtime), `OllamaProvider`.
- `LLMFactory.get_provider()` is a singleton factory driven by
  `settings.LLM_PROVIDER` with mode-aware fallback (development → omniroute,
  production → bedrock).
- `LLMProviderAdapter` (implements `ILLMService`) bridges the provider transport
  interface to the domain prompt-string interface the engines use. Plain-string
  `generate(prompt, **kwargs)`/`stream(prompt, **kwargs)`.

### 4.3 `app/rag` — RAG engine (facade)

- `RAGService` is a facade over `BaseRAGEngine` (`generate_answer`,
  `stream_answer`). It handles request-id binding and exception translation.
- `app/rag/engine.py` orchestrates retrieve → prompt build → LLM → response.
  The **runtime** chat path no longer uses `RAGService` directly (the
  `ChatOrchestrator` path with engine `RAG` does), but `RAGService` remains the
  legacy `/api/v1/chat` engine.

### 4.4 `app/retrieval` — retrieval pipeline

- `RetrievalService.retrieve()` runs query → embed → vector search →
  metadata mapping + `MIN_SIMILARITY_SCORE` filtering → rerank.
- `FAISSRetriever` adapts `RetrievalService` to the `IRetriever` interface the
  RAG engine expects (`search(query, top_k, metadata_filters)`).

### 4.5 `app/embeddings` — embeddings

- `SentenceTransformerEmbeddingProvider` loads `BAAI/bge-small-en-v1.5` on CPU
  (device/batch/normalize configurable), lazy thread-safe model load.
- `EmbeddingService` exposes `generate_embedding(EmbeddingRequest)`.

### 4.6 `app/vector_store` — FAISS

- `FAISSVectorStore` + `MetadataStore` (JSON) wrapped in `VectorStoreService`
  (add/search/delete/save/health). Auto-initializes with the embedding
  dimension when the index is empty.

### 4.7 `app/chunking` — chunking

- `MarkdownRecursiveChunker` splits lesson markdown into overlapping chunks
  (default chunk 600, overlap 120) with per-chunk metadata.

### 4.8 `app/knowledge` — static knowledge ingest

- `KnowledgeIngestionPipeline.ingest()` runs:
  `sources → MarkdownRecursiveChunker → clean → bge-small embeddings → FAISS`.
  Incremental: deterministic per-chunk ids + `content_hash`; unchanged chunks
  skipped, changed chunks re-embedded in place. Runs on startup in a daemon
  thread when `KNOWLEDGE_INGEST_ON_STARTUP=true`.
- Sources: `all_lessons.json` (lesson content per course) and
  `course_catalog.json` (course/module/lesson metadata).
- `POST /api/knowledge/ingest` and `GET /api/knowledge/status` are the admin/ops
  endpoints.

### 4.9 `app/memory` — short-term memory

- `MemoryService` manages recorded conversation sessions (derived from the
  conversation history) with windowing (`max_messages`, default 10).
- `DefaultMemoryManager` (in `app/memory/default_manager.py`) implements the
  `IMemoryManager` interface used by the pipeline: `load_history(session_user,
  tenant_id)` → `recent_context`, `save_turn(...)`.
- The store is in-memory/SQLite (`data/memory.db`); blocking DB calls run on a
  worker thread.

### 4.10 `app/conversations` — Recent Conversations & Favorites

- `SQLiteConversationStore` persists `conversations` (metadata + `messages_json`).
- `ConversationService` implements CRUD, auto-titling, favorite/pin/archive,
  rename, delete, paginated listing, search, resume, and lifecycle events.
- `ConversationEventPublisher` emits created/updated/opened/renamed/favorited/
  unfavorited/deleted events (used for observability/webhooks).
- Smart conversation titles (see §7).

### 4.11 `app/freemium` — free/premium AI access

- `FreemiumService` determines premium status from Django purchases (cached
  60 s) and enforces the per-window message limit for free users.
- `FreemiumStore` (SQLite `daily_usage`) records usage per reset window
  (`daily` default; `never` → fixed `epoch` key).
- Guests are identified by a persistent `client_id` (`guest:<id>`), so anonymous
  users also receive the daily allowance.

### 4.12 `app/adaptive` — adaptive learning

- `AdaptiveLearningEngine.adapt()` builds a per-request `LearnerAdaptation`
  (explanation depth, terminology, style, temporary beginner/expert override)
  from query signals + accumulated topic confidence.
- `observe()` updates the learner profile incrementally (small deltas, clamped;
  base level derived, never stored as identity).
- `SessionMemoryManager` + `SQLiteLearnerStore` persist per-conversation session
  memory (rolling context, summary, facts, active investigation, uploaded files).

### 4.13 `app/persona` + `app/prompt_builder`

- `PersonaRegistry` holds the active BlueTeamers mentor persona; `LearnerLevelDetector`
  detects beginner/intermediate/advanced/professional.
- `PersonaPromptBuilder` assembles `[Persona]`, `[Expertise]`, `[Teaching Level]`
  (from detected level), `[Response Format]`, `[Domain Priority]`,
  `[Personality]`, and an optional `[Learning Context]` block.
- `SimplePromptBuilder` (used by the engines) builds the full system prompt:
  base system prompt (or greeting prompt) + persona block + learner level +
  `[Response Style]` (concise/progressive disclosure) + response-mode block +
  adaptive block + session-memory block + page-context block + `[Context]`
  retrieved documents (+ teaching style / source lead-in rules) + external
  tool results + `[Conversation History]` + `[User Platform Context]`.
- `app/prompts/` and `app/prompt_builder/prompt_builder_service.py` are separate
  RAG-service-layer scaffolding (PromptRequest/Response), not used by the
  runtime chat path.

### 4.14 `app/platform` — Django integration

- `PlatformApiClient`: httpx async client with connection pooling, retries,
  JWT-injection, request-id propagation, 60 s TTL cache for GETs.
- `DjangoPlatformRepository` maps Django endpoints to typed domain models,
  translating errors (auth/unavailable/missing-endpoint).
- `UserContextBuilder` compiles the user's platform context string
  (profile/courses/progress/certificates) injected into prompts.
- `RecommendationService` generates course recommendations by cyber domain
  (`generate_for_domain`) or from the static catalog for guests
  (`generate_from_catalog`).

### 4.15 `app/streaming` — legacy streaming

- `StreamingService.stream_chat()` yields SSE `TokenEvent`/`CompletionEvent`/
  `ErrorEvent` and persists memory post-stream. Used by the legacy RAG
  streaming path; the runtime `/api/chat/` path streams via engine generators
  wrapped by `ChatService._stream_response`.

### 4.16 `app/cache`, `app/observability`, `app/runtime`, `app/guardrails`

- `CacheService`/`DefaultCacheManager`: in-memory semantic cache
  (SHA-256 key of query/filters/top_k/template/version).
- `ObservabilityService`: Prometheus metrics (`api_requests_*`, LLM, retrieval,
  memory, streaming); `ObservabilityMiddleware` adds W3C trace IDs and request
  latency labels; `/metrics` endpoint.
- `RuntimeMiddleware` (`app/runtime/middleware.py`): in-process fixed-window
  chat rate limit, quota checks, and audit logging per user/IP.
- `GuardrailsService`: registered for health checks; produces refuse/fallback
  guardrail output for out-of-scope content.

---

## 5. AI Features (what users can do today)

1. **Conversational Q&A** — general security questions answered by
   `GeneralExecutionEngine` (LLM), with templated greeting/off-topic handling.
2. **Course-grounded learning answers** — `RagExecutionEngine` retrieves the
   learner's *enrolled course material first*, then the general knowledge base.
   Responses are labelled `From your course material:` vs
   `From our general knowledge base:`, emit `course_sources` cards, and can
   recommend the covering module/lesson.
3. **Platform/data queries** — `PlatformExecutionEngine` answers
   enrolled/progress/certificates/assessments/dashboard/profile questions
   deterministically from Django data (no LLM for pure data intents; LLM only
   to interpret/recommend), and recommends BlueTeamers courses grounded in
   retrieval.
4. **SOC Analyst copilot (text-only specialist engines)** — Wazuh lab, practice
   lab, investigation guidance, Windows event log, Linux log, IOC analysis,
   MITRE guidance, detection rule, and general investigation. Each is a
   *course-first mentor* that never reveals direct solutions.
5. **Threat intelligence lookups** — `ThreatIntelExecutionEngine` retrieves from
   the knowledge base and, when the entity is absent, runs the embedded
   `IndicatorFetcherTool` + `MITRETool` (mock external lookups) as
   `[External Tool Results]` evidence with a dedicated persona.
6. **File/image attachments** — `AttachmentParseStage` parses text/PDF/log/JSON
   files (truncated to 8k chars) and OCRs images via RapidOCR so screenshots of
   logs/emails become analyzable; the assistant honestly states it cannot see
   images (text-only model).
7. **Page context awareness** — the floating assistant auto-detects the page
   (Dashboard/Course/Lesson/Lab/Profile/...) and sends `request.context.page`;
   `PageContextStage` injects `[Page Context]` so the AI never asks where the
   user is.
8. **Active lab context** — lab start/resume/answer/hint actions are carried in
   `request.context.lab`; specialist engines anchor answers to the active lab,
   and lab hint reveals are folded into the LabCard.
9. **Smart conversation titles** — deterministic titles from the first
   meaningful message; greetings stay "New Chat" until a real question arrives
   (see §7).
10. **Adaptive learning** — per-request explanation depth/style adapted to the
    detected learner level; session memory (summary, facts, investigation,
    files) persists per conversation.
11. **Freemium gating** — one daily message allowance for guests + free users;
    unlimited for paid-course holders; `GET /api/chat/access` drives the
    frontend "X / Y messages remaining" indicator and the workspace gate.
12. **Recent Conversations & Favorites** — sidebar with filters (recent 7 days,
    favorites, all, type), search, rename, favorite, pin, archive, delete,
    resume.

---

## 6. RAG Pipeline

The knowledge base is **static BlueTeamers course content only** (dynamic
platform data is never embedded).

```
all_lessons.json  ─┐
course_catalog.json─┤ MarkdownRecursiveChunker ─► clean_text ─► embed (bge-small)
                    │   (chunk 600 / overlap 120)      (SHA-1 content_hash)  │
                    ▼                                                          ▼
        course-level docs + lesson chunks                               FAISS IndexFlatIP
        (metadata: course_slug, lesson_id, course_title,               + metadata.json (JSON store)
         lesson_title, source=lesson_content, chunk_index)                     ▲
                                                                               │
Query ─► embed(query) ─► vector search (top_k, metadata_filters) ─► threshold   │
         (bge-small)        (FAISS inner-product)      (MIN_SIMILARITY 0.4)     │
                                                                               ▼
                                RetrievalService.retrieve ─► IdentityReranker ─► RetrievedChunks
```

- Retrieval filters: `metadata_filters` supports scalars (equality) and
  lists/tuples (membership) — used to restrict retrieval to enrolled course
  slugs (`{"source": "lesson_content", "course_slug": [..]}`).
- **Course-material-first**: `RagExecutionEngine` searches enrolled lessons
  first; only falls back to general knowledge when there is no match, and
  labels the answer source accordingly.
- Ingest is incremental and idempotent (`content_hash` diffing); startup ingest
  runs in a daemon thread and never blocks startup.

---

## 7. Conversation System

### Persistence

- Every user+assistant turn is written by `PersistenceStage` to
  `ConversationService.record_turn(...)`, creating the conversation when absent
  and appending messages. Stored in SQLite `conversations` + `messages_json`
  (schema in `app/conversations/store.py`).
- Turn metadata derives a `conversation_type` (chat/learning/investigation/tool/
  lab/assessment) plus optional `course_title`, `assessment_score`, etc.
- Short-term memory (`DefaultMemoryManager`) is additionally scoped per
  conversation (`user::conversation_id`) when a conversation exists.

### Smart titles

`app/conversations/title.py`:

- `generate_title()` — deterministic, no LLM. If the first message is only a
  greeting (`is_greeting_message`), the title stays the **"New Chat"**
  placeholder. Otherwise leading politeness/greeting filler is stripped
  (`_LEAD_STRIP`), `_SMART_TITLES` (SOC-specific labels like "Windows Event Log
  Analysis", "Wazuh Rule Investigation") and `_COURSE_KEYWORDS`
  ("Understanding <Course>") are checked, then a title-cased keyword title.

- `is_placeholder_title()` — `{'', 'new conversation', 'new chat'}`.
- `is_greeting_title()` — matches legacy `About Hi`-style titles so they get
  re-titled too.
- `record_turn()` policy: brand-new conversations are titled from the first
  meaningful message; conversations still carrying a placeholder **or legacy
  greeting title** are re-titled the moment a meaningful question arrives.
  Manual renames are never overwritten (rename via `PATCH`).

### Frontend behaviour (`src/hooks/useChat.ts`)

- Messages + `conversation_id` are persisted to sessionStorage
  (`bt_chat_messages_v1`, `bt_chat_conversation_id_v1`). Any fresh `useChat`
  instance (workspace or floating assistant) **lazy-restores** the stored id on
  mount only when a saved message session exists, so follow-ups keep grouping
  into one conversation.
- `startNewConversation()` clears the stored id (and messages) so a subsequent
  reload cannot resume the old thread.
- `loadConversation(id)` fetches full history from `GET /api/conversations/{id}`.

---

## 8. AI Request Flow (runtime path)

```
POST /api/chat/   (ChatRequest: message|query, stream, images, files, token,
    conversation_id, context{page,lab}, client_id)
  └─ freemium gate: check_and_consume(identity, token)
        (valid JWT → user_id from token; no token + client_id → "guest:<id>";
         429 free_ai_limit_reached for exhausted free users)
  └─ ChatService.process_request(request)
       └─ resolve_user_identity(token) → session_user / tenant_id
       └─ ExecutionContext(correlation_id, streaming_mode, metadata{...})
       └─ ChatOrchestrator.execute_pipeline(context):
            1.  CacheStage            — semantic cache lookup
            2.  MemoryLoadStage       — load conversation-memory window
            3.  AttachmentParseStage  — parse files/images/OCR, inject into query
            4.  PlatformContextLoadStage — build platform context string (Django)
            5.  PersonaLoadStage      — persona block + learner level → memory
            6.  PageContextStage      — [Page Context] from request.context.page
            7.  AdaptiveContextStage  — learner adaptation + session memory
            8.  IntentAnalysisStage   — IntentIntelligenceService pipeline
            9.  RoutePlanningStage    — IntentType → engine name
            10. EngineExecutionStage  — create + run engine (RuntimePolicyProxy)
            11. CompositionStage      — ExecutionResult → ChatResponse DTO
            12. SuggestedCoursesStage — append suggested_courses metadata
            13. PersistenceStage      — memory.save_turn + record_turn
            14. AdaptivePersistenceStage — observe_turn (learner model)
  └─ Streaming: SSE events {"token"|"metadata"} + [DONE]
     Non-streaming: ChatResponse(message, metadata: latency/citations/trace_id)
```

**Routing** (`app/chat/pipeline/planning_stage.py`): the `QueryRouter.decide`
path is **not wired** (bootstrap calls `RoutePlanningStage(registry)` with
`decide=None`). Instead `PlanningService.create_plan(...)` builds a plan and the
intent's `route_recommendation.engine` is picked when it is in the known engine
list; otherwise it falls back to `"AGENT"`.

**Engines** (registrations in `bootstrap.py`):
`GENERAL, RAG, TOOL, AGENT, NOTES, SUMMARY, THREAT_INTEL, WAZUH_LAB,
PRACTICE_LAB, INVESTIGATION, INVESTIGATION_GUIDANCE, WINDOWS_EVENT_LOG,
LINUX_LOG, IOC_ANALYSIS, MITRE_GUIDANCE, DETECTION_RULE, PLATFORM`.

---

## 9. AI Providers

| Provider | Role | Endpoint | Config keys |
|---|---|---|---|
| **OmniRoute** (dev default) | Chat completion + streaming via OpenAI-compatible `/v1/chat/completions` and `/v1/models` | `OMNIROUTE_BASE_URL` (default `http://localhost:20128/v1`) | `OMNIROUTE_API_KEY`, `OMNIROUTE_MODEL` (`auto/best-chat`) |
| **Amazon Bedrock** (prod default) | AWS Bedrock runtime inference | AWS region (default `us-east-1`) | `BEDROCK_REGION`, `BEDROCK_MODEL` (`anthropic.claude-3-sonnet-...`), AWS creds |
| **Ollama** (optional dev) | Local models | `OLLAMA_BASE_URL` (default `http://localhost:11434`), `OLLAMA_MODEL` (`deepseek-r1:1.5b`) | `LLM_PROVIDER=ollama` |

Selection: `LLMFactory.get_provider()` — explicit `LLM_PROVIDER` wins;
`auto`/empty resolves from `DEVELOPMENT_MODE` (dev → OmniRoute, prod → Bedrock).

Embeddings: `SentenceTransformerEmbeddingProvider` with `BAAI/bge-small-en-v1.5`
on CPU.

---

## 10. APIs (AI service)

### Chat
- `POST /api/chat/` — runtime chat (streaming via `ChatRequest.stream`).
- `GET /api/chat/access` — freemium access status.
- `GET /api/chat/health` (in `app/chat/router.py`): chat subsystem health.

> **Not wired:** `GET /api/chat/session` is requested by the frontend
> (`initializeSession` in `useChat.ts`) to fetch a personalised welcome message,
> but `app/chat/services/session_initializer.py::SessionInitializer` is never
> registered on a router. The endpoint returns 404; the frontend catches the
> error and starts a fresh conversation. Wiring it is the fix for personalised
> workspace welcome messages.

### Conversations (`/api/conversations`)
- `GET ""` — paginated list (`filter`, `search`, `days`, `page`, `page_size`).
- `GET ""/search?q=` — text search.
- `POST ""` — create conversation.
- `GET ""/{id}` — full history (resume).
- `PATCH ""/{id}` — update (rename/favorite/pin/archive/type/course/tags).
- `DELETE ""/{id}`.
- `POST ""/{id}/favorite`, `POST ""/{id}/unfavorite`.

### Legacy chat
- `POST /api/v1/chat` — RAG answer (ChatService path, no streaming).
- `POST /api/v1/chat/stream` — SSE streaming (ChatService path).
- `GET /api/v1/chat/health`.

### Ops
- `GET /api/health`, `GET /` (service banner) — aggregated component health.
- `GET /api/me` — authenticated user profile (JWT).
- `GET /api/debug/platform-health` — Django connectivity diagnostics.
- `GET /api/knowledge/status`, `POST /api/knowledge/ingest`.
- `GET /metrics` — Prometheus metrics.

---

## 11. Database Models

The AI service uses **SQLite** (stdlib `sqlite3`, blocking calls delegated to a
worker thread; shared connection with `check_same_thread=False`).

| DB file | Tables | Purpose |
|---|---|---|
| `data/conversations.db` | `conversations` (conversation_id PK, user_id, title, created_at, updated_at, last_message, message_count, favorite, pinned, archived, conversation_type, course_id, course_title, lesson_id, topic, progress, assessment_id, assessment_score, tags, messages_json) | Full history + metadata for Recent Conversations & Favorites |
| `data/freemium.db` | `daily_usage` (user_id, reset_at, used; PK(user_id, reset_at)) | Per-window AI message usage |
| `data/memory.db` | memory sessions | Short-term conversation memory |
| `data/adaptive.db` | learner profiles / topic confidence | Adaptive learning model |
| `data/vector_store/` | FAISS `index.faiss` + `metadata.json` | Embedded knowledge chunks |

Domain models (Pydantic) in `app/conversations/models.py`:
`ConversationSummary` (list/search projection, no message bodies),
`Conversation` (full history), `ConversationListPage` (pagination),
`ConversationMessage` (message_id, role user/assistant/system, content,
created_at, metadata), `ConversationType`
(chat/assessment/learning/investigation/tool/lab), `ConversationUpdateRequest`.

Shared Django integration data (`app/platform/models.py`): `Course`, `Module`,
`Lesson`, `Progress`, `Purchase`, `Certificate`, `Assessment`, `Lab`,
`Recommendation` (with lesson deep-links + enrichment for clickable cards),
`PlatformCard`/`PlatformAction` (UI payloads), `PlatformResponsePayload`.

---

## 12. AI Agent Architecture

### Runtime-reachable agents

- **`AgentExecutor`** (`app/agents/executors/agent_executor.py`) is registered as
  engine `AGENT`. It walks an `ExecutionPlan` DAG via `SequentialScheduler`,
  resolving each step's capability to an engine through
  `CapabilityEngineResolver`, with checkpointing, reflection
  (`ReflectionService.evaluate_step`), and recovery
  (`RecoveryPolicy`: retry/skip/abort). Event bookkeeping via `agent_event_bus`.
- In practice routing usually selects a specialist **engine** directly rather
  than `AGENT`; the AGENT path is a fallback for hybrid/multi-step intent
  plans.

### Scaffolding (code exists but NOT wired into the request path)

- Specialist agent *classes* (`assessment_coach`, `investigation`,
  `knowledge_assistant`, `lab_mentor`, `learning_coach`, `threat_intelligence`,
  `soc_analyst`) — real implementations/tool definitions, but not instantiated
  by the elligible bootstrap; the wired equivalents are the specialist
  **engines** in `app/chat/engines/`.
- `AgentCoordinator`, `AgentRouter`, `DiscoveryService`, `MultiAgentPlanner`,
  `StrategyResolver`, marketplace/plugins/skills/packages/manifests — scaffolding.
- `skills/executor` and `plugins/sandbox` are stubs.

### Tool framework

- `ToolExecutionEngine` → `ToolProviderResolver` → `ProviderRegistry`
  → `LegacyToolProvider` → `LocalToolExecutor` → `ToolService`.
- The `ToolCatalog` is **empty** at runtime (never populated with tool
  registrations), so the `TOOL` engine always fails with "No provider found for
  tool <name>". Tools are therefore not executed via the TOOL route today.
- The **only** end-to-end tools at runtime are the mock external threat-intel
  tools constructed inline in `bootstrap._threat_intel_tools()`:
  `IndicatorFetcherTool` + `MITRETool`, used by `ThreatIntelExecutionEngine`
  as an external fallback.

---

## 13. Integrations

- **Django (auth/data)**: `PlatformApiClient` → `DjangoPlatformRepository`
  endpoints: `auth/verify/`, `payments/my-purchases/`, `courses/{slug}/`,
  `courses/`, `courses/{slug}/progress/`, `courses/{slug}/quiz-scores/`,
  `certificates/my/{slug}/`, `courses/?search=`. 60 s TTL GET cache, retries,
  request-id propagation.
- **OmniRoute / LLM gateway**: OpenAI-compatible chat completions.
- **MCP** (`app/mcp/config.py`): config-driven server registration
  (`stdio`/`http`/`websocket`/`sse`), environment-aware; transport layer is
  scaffold — remote MCP execution is not implemented; the legacy local provider
  is the functional path.
- **Static course knowledge**: `app/knowledge/data/all_lessons.json` +
  `course_catalog.json`.
- **Frontend**: React surfaces call `/api/chat/`, `/api/chat/access`, and
  `/api/conversations` with the Bearer JWT; streaming via `ReadableStream` SSE
  parsing in `useChat`.

---

## 14. Security

- **JWT verification** (`app/security/auth.py`): `JWTValidator` verifies RS256
  tokens with the Django `jwt_public.pem` (path from
  `JWT_PUBLIC_KEY_PATH`); when the key is absent it falls back to HS256 with
  `JWT_SECRET`. `resolve_user_identity()` returns the stable `user_id` claim.
- **Identity everywhere**: memory keys, conversation rows, and freemium usage
  are all scoped by the authenticated `user_id`; conversations queries are
  always `WHERE user_id = ?`.
- **Rate limiting**: `RuntimeMiddleware` (chat rate limit;
  `CHAT_RATE_LIMIT=60`/min per user/IP) + freemium per-window limits.
- **CORS**: `["*"]` in development, explicit `CORS_ORIGINS` in production.
- **Prompt safety**: system-prompt rules restrict the assistant to cybersecurity
  topics, refuse off-topic content (template `OffTopicResponseBuilder`), and
  forbid inventing platform data or external courses; `clean_response()`
  strips internal tags/debug/metadata from final text.
- **Errors in health** are aggregated and reported per component; startup
  failures never block the app.

---

## 15. Configuration

`APP_NAME=BlueTeamers AI Service`, `APP_VERSION=1.0.0`.

Single switch: `DEVELOPMENT_MODE` (default `true`). Everything else is derived
unless set explicitly (see `Settings._apply_mode_defaults`):

| Setting | Dev default | Prod default | Notes |
|---|---|---|---|
| `LLM_PROVIDER` | `omniroute` | `bedrock` | explicit value wins |
| `LOG_LEVEL` | `DEBUG` | `INFO` | |
| `CORS_ORIGINS` | `["*"]` | `[]` (must set) | |

Key values:
- `DJANGO_API_URL` — Django base URL (required).
- `OMNIROUTE_BASE_URL` = `http://localhost:20128/v1`, `OMNIROUTE_MODEL` = `auto/best-chat`.
- `SECRET_KEY`, `JWT_SECRET`, `JWT_PUBLIC_KEY_PATH` (points to the Django
  backend's `jwt_public.pem`).
- Embeddings: `EMBEDDING_MODEL=BAAI/bge-small-en-v1.5`, `EMBEDDING_DEVICE=cpu`.
- Vector/chunking: `VECTOR_STORE=faiss`, `VECTOR_INDEX_TYPE=IndexFlatIP`,
  `CHUNK_SIZE=600`, `CHUNK_OVERLAP=120`, `MAX_DOCUMENT_SIZE_MB=5`.
- Retrieval: `DEFAULT_TOP_K=5`, `MAX_TOP_K=20`, `MIN_SIMILARITY_SCORE=0.4`.
- `KNOWLEDGE_LESSON_JSON`, `KNOWLEDGE_COURSE_JSON`,
  `KNOWLEDGE_INGEST_ON_STARTUP=true`.
- Tokens: `MAX_CONTEXT_TOKENS=4000`, `MAX_PROMPT_TOKENS=8000`,
  `MEMORY_WINDOW=10`, `MAX_SESSION_MESSAGES=50`.
- Rate/freemium: `CHAT_RATE_LIMIT=60`, `FREEMIUM_ENABLED=true`,
  `FREEMIUM_FREE_MESSAGE_LIMIT=5`, `FREEMIUM_RESET_POLICY=daily`,
  `FREEMIUM_PREMIUM_PURCHASE_STATUSES=paid`, `FREEMIUM_PREMIUM_CHAT_GATE=true`.
- Conversations: `CONVERSATIONS_DB_PATH=data/conversations.db`,
  `CONVERSATIONS_PAGE_SIZE=20`, `CONVERSATION_TITLE_MAX_LEN=60`,
  `CONVERSATION_PERSISTENCE_ENABLED=true`.
- Observability: `OBSERVABILITY_ENABLED=true`, `METRICS_ENDPOINT=/metrics`,
  `TRACING_ENABLED=true`, `METRICS_PROVIDER=prometheus`.
- MCP: `MCP_ENABLED=true`, `MCP_SERVERS_CONFIG` / `MCP_SERVERS_CONFIG_PATH`.
- Assessment agent flags exist (`ENABLE_ASSESSMENT_AGENT`, etc.) but the
  assessment stage is not in the wired pipeline (see §16).

---

## 16. Current Limitations

- **LLM is text-only** — no vision; images are OCR'd or explicitly declared
  unreadable.
- **OmniRoute dev gateway required** — OmniRoute must be reachable at
  `OMNIROUTE_BASE_URL`; the dev environment depends on it for generation.
- **TOOL engine is inert** — the tool catalog is never populated, so tool-call
  requests fail gracefully rather than executing.
- **Reranker is identity** — `IdentityReranker` returns vector-store order.
- **QueryRouter `decide` not wired** — intent → engine uses the rule-based
  `RuleRoutePlanner.engine_map` + fallback to `AGENT`.
- **Assessment agent not wired** — `AssessmentStage` is defined but absent from
  `bootstrap.py`'s stage list.
- **Specialist agent classes (coaches) are dead code at runtime** — the
  equivalent capabilities ship as specialist *engines*.
- **MCP transport scaffold** — remote MCP server execution isn't implemented;
  only local/legacy provider tool path works today.
- **Legacy `/api/v1/chat` uses `ChatService`** but maps a different request
  schema (request_id/query/metrics) and does not pass the JWT, so it skips
  per-user persistence/memory/freemium features the `/api/chat/` path provides.
- **Django limitations surfaced honestly**: labs/learning-paths/badges have no
  Django model yet, so the repository returns empty lists and the assistant
  says so.
- **Freemium premium check depends on Django `payments/my-purchases/`** — when
  Django is down, users are treated as free (fail-closed to the limit, open to
  assistant availability).

---

## 17. Future-Ready Components

- **Provider abstraction**: swapping OmniRoute → Bedrock → Ollama is pure config
  + a provider class; `BaseLLMProvider` contract is stable.
- **Cross-encoder rerankers**: `BaseReranker` is an open/closed seam;
  `IdentityReranker` can be replaced without touching callers.
- **QueryRouter (Phase-X)**: `app/chat/routing/`, `query_router.py`, and
  `QueryRouter.decide` exist and just need wiring into `RoutePlanningStage`.
- **Agent platform**: full registry/discovery/coordinator/planner/executor/
  checkpoint/recovery/reflection scaffolding is present; single/multi-agent
  coordination, marketplace, plugins, skills, templates, manifests, versioning,
  analytics, health monitors are all present to plug in.
- **Tool framework**: ~30 `@tool`-decorated implementations exist under
  `app/tools/implementations/` with discovery/scanner/service layers ready to be
  registered into `ToolCatalog`.
- **Assessment agent**: interactive quiz agent code + config flags exist and
  could be added as the next pipeline stage.
- **Vector store**: pluggable backend interface; FAISS is the current concrete.

---

## 18. Development Summary (how to run / test)

### Services
- **Frontend (Vite)**: run from `infosecdairies/` — `npm run dev`
  (dev server on `:5173`; Vite proxies `/api/*` to the AI service).
- **Django**: `cd infosecdairies/infosec-backend/backend && python manage.py runserver`
  (port 8000).
- **AI service**: from `ai_service/`:
  `./.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001`.
  Startup also requires OmniRoute to be reachable.
- Health check: `curl http://127.0.0.1:8001/api/health`.

### Backend tests
- `ai_service/tests/` covers conversations (incl. `test_smart_titles.py`,
  `test_conversation_service.py`, `test_recent_days.py`), retrieval, and other
  units; run e.g. `cd ai_service && .venv/bin/python -m pytest tests/...`.

### Frontend checks
- TypeScript: `tsc` (clean). ESLint: `npm run lint`.

### Key entry points for maintenance
- Chat wiring: `ai_service/app/chat/bootstrap.py`.
- Routing: `ai_service/app/chat/pipeline/planning_stage.py`,
  `ai_service/app/chat/intent/`.
- Conversation titles/persistence:
  `ai_service/app/conversations/{title,service,store}.py`.
- Frontend chat state/surfaces:
  `infosecdairies/src/hooks/useChat.ts`, `src/context/AiAssistantContext.tsx`,
  `src/components/ui/chat/WorkspaceSidebar.tsx`, `src/components/ui/Chat.tsx`,
  `src/components/ai/FloatingAssistant.tsx`.