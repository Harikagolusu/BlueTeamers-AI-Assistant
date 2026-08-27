# BlueTeamers AI Assistant — Production Integration Guide

> Purpose: Help the **BlueTeamers Arena** team safely integrate this AI Assistant
> (FastAPI AI service + Django/React frontend) into their production platform.
> Covers architecture, auth, API contracts, security, config, known gotchas and
> the exact things that must be aligned before going to production.

---

## 1. What this project is

Two parts:

| Part | Stack | Port (dev) | Role |
|------|-------|-----------|------|
| **ai_service** | FastAPI + RAG (FAISS) + agents + freemium + memory | 8001 | LLM orchestration, chat, retrieval, streaming |
| **frontend + backend** (`infosecdairies`) | React 18 + Vite + Tailwind/shadcn, Django 6 + DRF + SimpleJWT | 5173 / 8000 | Auth, platform (courses/lessons), chat UI, conversation list |

The AI service is a **self-contained microservice**. It calls LLM providers
(DeepSeek currently; OmniRoute/Bedrock supported) and does NOT need Django for
chat — but it DOES use Django to validate JWTs and to pull user/course/payment
context. The frontend shares one conversation between the floating assistant and
the full `/chat` workspace via `sessionStorage` + a `BroadcastChannel`.

---

## 2. Component boundary & trust model

```
Browser (React)
   │  JWT (Bearer) OR client_id (guest)
   ▼
[Vite proxy dev / reverse proxy prod]
   │  /api/*                 → Django :8000
   │  /api/chat*, /api/conversations*, /api/health → AI :8001
   ▼
AI SERVICE (FastAPI) ── (retrieve → embed → rerank → LLM) ──> LLM provider
   │
   └── calls Django /api/* for platform context
```

- AI service is **stateless** (only SQLite stores for memory/conversations).
- Every AI-service request must be authenticated by a **valid Django JWT** or a
  **guest `client_id`**. Identity is resolved **server-side only** — never trust
  a client-supplied `user_id`.

---

## 3. Authentication (MOST IMPORTANT)

### Shared-key contract
- **Django** signs access tokens with **RS256** using `jwt_private.pem`, and
  stamps every token with `aud = "infosecdairies"`, `iss = "infosecdairies"`.
- **AI service** verifies them with the **public** key (`jwt_public.pem`) via
  `JWT_PUBLIC_KEY_PATH`.
- Nothing else may sign for the AI service. `JWT_SECRET` is only a dev-mode HS256
  fallback; with an RS256 public key configured the service is RS256-only.

### Production rules
1. One key pair: Django gets the **private** key, AI service the **public** key.
2. Ship keys as secrets (KMS/vault), never committed.
3. Keep `JWT_ISSUER`/`JWT_AUDIENCE` **in sync** with Django — same values, or
   both empty. Do not set one without the other: a token carrying `aud` with no
   `audience` configured raises PyJWT `InvalidAudienceError` and 401s every
   logged-in request.
4. **Rotate** keys; keep a short overlap where both old/new public keys verify.

### Demo / dev
- `ENABLE_DEMO_MODE=true`, `DEMO_USER_EMAIL`, `DEMO_USER_PASSWORD`.
- Seed via `infosec-backend/backend/seed_demo_user.py` (`harika@example.com` /
  `password123`, paid enrollments, progress, quiz scores).
- Production: demo mode OFF, never run seed in prod.
---

## 4. Identity & Freemium

Every chat request resolves to an identity, in priority order:

1. **Valid JWT** → `user_id` (premium once they purchased a course).
2. **No JWT but `client_id`** → `guest:<client_id>` (namespaced, free daily allowance).
3. **Neither** → **401 fail-closed** (anonymous callers never run the LLM at cost).

Key rules:
- Frontend sends `client_id` **only when NOT logged in**; logged-in users send
  only the JWT. If the JWT fails validation, a logged-in user gets 401 (no guest
  fallback).
- Freemium limit `FREEMIUM_FREE_MESSAGE_LIMIT` per window; over-limit → **429**
  with structured `free_ai_limit_reached` payload (UI shows upgrade dialog).
- Premium users are **never** limited.
- Conversation persistence only for authenticated users; guest threads feed
  short-term memory only.

---

## 5. API surface (endpoints & contracts)

### Chat
- `POST /api/chat/` — the **frontend path**. Body `{query, stream, conversation_id, client_id?, language?, context?}`.
  - `stream: true` → **SSE** (`text/event-stream`): `data: {"token": ...}` chunks,
    then `data: {"metadata": {...}}`, then `data: [DONE]`.
  - `stream: false` → JSON `ChatResponse`.
- `POST /api/v1/chat` — non-streaming RAG chat (JSON).
- `POST /api/v1/chat/stream` — streaming variant.
- `GET /api/chat/access` — freemium access/allowance status.

Chat accepts the JWT via **`Authorization: Bearer <token>`** OR a body `token`
field (header wins if both).

### Other AI routes
- `GET /` pulse; `GET /health` deep health (LLM, RAG, vector store, memory).
- `/api/conversations/*` — listing, favorites, rename, delete.
- `/api/language/*` — per-user language preference (multilingual).
- `/api/v1/rag`, `/api/v1/chat/health` sub-APIs; `/metrics` Prometheus.

### Django endpoints used
`/api/auth/*`, `/api/courses/*`, `/api/certificates/*`, `/api/payments/*`,
`/api/leads/*`. Set `DJANGO_API_URL` on the AI service to reach these.

---

## 6. Environment variables for the AI service

| Var | Meaning | Prod |
|-----|---------|------|
| `DEVELOPMENT_MODE` | true=dev defaults; false=production | **must be false** |
| `SECRET_KEY`, `JWT_SECRET` | secrets (JWT_SECRET = legacy fallback) | yes |
| `JWT_PUBLIC_KEY_PATH` | Django public key PEM | **required** (prod refuses to start without it) |
| `JWT_ISSUER` / `JWT_AUDIENCE` | align with Django or both empty | align |
| `DJANGO_API_URL` | Django API base URL | yes |
| `CORS_ORIGINS` | allowed origins (dev=`["*"]`) | **explicit list in prod** |
| `LLM_PROVIDER` | `deepseek`/`omniroute`/`bedrock`/`ollama`/`auto` | yes |
| `DEEPSEEK_API_KEY`/`_BASE_URL`/`_MODEL` | DeepSeek provider | if used |
| `OMNIROUTE_API_KEY`/`_BASE_URL`/`_MODEL` | OmniRoute provider | if used |
| `INTERNAL_ADMIN_TOKEN` | internal tooling token (`X-Internal-Token`) | yes |
| `VECTOR_DB_PATH`/`VECTOR_PATH`/`VECTOR_METADATA_FILE` | FAISS store location | yes |
| `KNOWLEDGE_*`/`EMBEDDING_*`/`CHUNK_*` | RAG ingest/tuning | as needed |
| `FREEMIUM_ENABLED`, `FREEMIUM_FREE_MESSAGE_LIMIT` | allowance | as needed |
| `CHAT_RATE_LIMIT*`, `MAX_SESSION_MESSAGES` | abuse control | enable |
| `POSTGRES_URL`, `REDIS_URL` | optional external stores | if enabling |
| `MCP_ENABLED`, `MCP_SERVERS_CONFIG` | MCP servers | audit/off in prod |
| `LOG_LEVEL` | prod = `INFO` | yes |

Keep a `.env.example`; never commit real `.env`.

---

## 7. Security hardening checklist (safe production)

- [ ] **Auth enforced**: all chat ingress needs JWT or `client_id` (built-in fail-closed — keep it).
- [ ] **Secrets**: keys, LLM tokens, JWT private key in a secret manager; never in git/logs.
- [ ] **CORS**: lock `CORS_ORIGINS` to the real prod domain(s); `["*"]` is dev-only.
- [ ] **TLS** at the proxy; trust `X-Forwarded-*` only from the proxy for client IP.
- [ ] **Rate limiting**: keep `CHAT_RATE_LIMIT_ENABLED` + freemium caps; add per-IP and per-user budgets at the edge.
- [ ] **Body limits**: `MaxBodySizeMiddleware` caps at 2 MiB. Send a `Content-Length` — see the streaming gotcha below.
- [ ] **Prompt injection / guardrails**: guardrails run on `/api/v1/chat` & `/api/v1/rag` (non-streaming). Streaming skips guardrails; consider client-side or streaming-safe validation.
- [ ] **LLM cost**: cap file/image upload sizes and counts (images/files travel as base64).
- [ ] **PII/retention**: memory & conversation SQLite stores — set retention + geo for prod; logging masks PII.
- [ ] **Observability**: keep `/metrics` + request IDs (`X-Trace-ID`), route logs, alert on 5xx and freemium 429 spikes.
- [ ] **Model/provider**: verify the chosen LLM has quota and is not blocked from the prod egress IP (some free providers 403 from datacenter IPs).

---

## 8. Known gotchas (save your friend time)

1. **JWT audience rejection (fixed in repo).** Django tokens carry `aud`/`iss`;
   verify them only when `JWT_AUDIENCE`/`JWT_ISSUER` are configured, else PyJWT
   raises `InvalidAudienceError` and every logged-in chat 401s. Align with Django.
2. **Empty streaming responses.** `POST /api/chat/` (stream) can return **0 bytes**
   when a `BaseHTTPMiddleware` re-reads the POST body around a `StreamingResponse`
   (Starlette: `Unexpected message received: http.request` in an ASGI TaskGroup).
   Repo stays reliable by **skipping body re-read on streaming chat routes**
   (Content-Length check only). Do not wrap stream endpoints in body-buffering
   BaseHTTPMiddleware.
3. **Free LLM tier throttling.** Free providers (`oc/*`, some DeepSeek tiers)
   share rate limits: 429 under load, slow (25–30 s). Dev-only. Production should
   use a paid model + client timeout/retry. Some `tllm/*` providers are
   **403-blocked from datacenter egress IPs** by Vercel — use a residential/clean
   proxy or another provider.
4. **Token lifecycle.** Frontend stores `accessToken`/`refreshToken` in
   `localStorage`, auto-refreshes every ~10 min. Ensure `/api/auth/token/refresh/`
   works and stale tokens clear instead of looping 401s.
5. **Session storage is per-tab.** Use the existing `BroadcastChannel` sync when a
   "open full workspace" flow opens a new tab.

---

## 9. Deployment & scaling

- Run the AI service as a separate container, reachable by the frontend via an
  authenticated reverse-proxy path and by the AI service to call Django.
- API processes are **stateless** — scale horizontally behind a load balancer.
  Keep memory/conversation/vector stores on shared/persistent storage or wire to
  real DBs:
  - `MEMORY_DB_PATH` (SQLite) → Postgres for HA.
  - FAISS `VECTOR_*` → object storage or a vector DB.
- `KNOWLEDGE_INGEST_ON_STARTUP=true` rebuilds the index; coordinate replicas to
  avoid races.
- Health: use `GET /health` for probes (not `GET /`).
- Resources: embeddings run on CPU (`BAAI/bge-small-en-v1.5`); size RAM
  accordingly; GPU only for larger embedding models.

---

## 10. First 30 minutes of integration

1. Diff both repos' auth: confirm JWT keys, `iss/aud`, algorithm (RS256).
2. Set `DEVELOPMENT_MODE=false`, tight `CORS_ORIGINS`, real secrets.
3. Point the frontend `VITE_API_BASE_URL` (or proxy): `/api/chat*` & `/api/conversations*` → AI service; everything else → Django.
4. Run `/health` and a real chat with a valid JWT; expect a streamed answer.
5. Verify freemium: guest `client_id` → limited; JWT premium → unlimited.
6. Verify BOTH non-stream `/api/v1/chat` and stream `/api/chat/` return content
   (guards the empty-stream gotcha).
7. Turn on observability + alerts before user traffic.

---

## 11. Do / Don't summary

- **DO** share the RS256 public key with the AI service; keep the private key only in Django.
- **DO** keep `JWT_AUDIENCE`/`JWT_ISSUER` consistent (or both unset).
- **DO** fail closed on identity (already built in).
- **DON'T** wrap streaming chat routes with body-buffering middleware.
- **DON'T** run dev free-tier LLM providers in production.
- **DON'T** expose `/metrics`, `/docs`, `/health` publicly without auth/proxy.
- **DON'T** log prompts, tokens, or secrets.

---

_Generated from the actual codebase (ai_service + infosecdairies) and validated
behaviors (auth 401 fix, streaming SSE, freemium gating)._

