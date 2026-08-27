# BlueTeamers AI Assistant — Project Structure & Integration Guide

> For the backend engineer joining the project. Covers the repo layout, how the three services talk to each other, the AI-service API surface, and how to run everything locally.

---

## 1. Big picture

The platform is **three services running side by side**:

```text
Browser (React SPA)
   │
   ├── /api/*              ──▶  Django REST backend  (:8000)   — auth, courses, payments, certificates
   └── /api/chat/*         ──▶  FastAPI AI service    (:8001)   — AI chat, streaming, conversations
        /api/conversations ──▶  FastAPI AI service    (:8001)   — conversation history & favorites
        /api/health        ──▶  FastAPI AI service    (:8001)
```

- Django issues the JWT (access/refresh) that **both** backends honour.
- The FastAPI AI service verifies those JWTs itself (RS256 with Django's public key, HS256 dev fallback) — it is **not** reached through Django.
- In dev, the Vite dev server proxies `/api/*` → Django and `/api/chat/*`, `/api/conversations`, `/api/health` → FastAPI so the browser only ever talks to one origin (`http://localhost:5173`).

### Repo layout

```text
BlueTeamers-AI-Assistant/
├── ai_service/                 # FastAPI AI microservice (Python)
│   ├── app/
│   │   ├── main.py             # App wiring: routers + middleware + exception handlers
│   │   ├── api/                # Primary chat router  (POST /api/chat/)
│   │   ├── chat/               # Legacy v1 chat router, service, pipeline
│   │   ├── conversations/      # Conversation history REST API
│   │   ├── freemium/           # Daily guest/free quota (client_id + IP keyed)
│   │   ├── security/           # JWT validation, rate limiting
│   │   ├── core/               # Pydantic settings, logging, middleware
│   │   ├── llm/                # Provider abstraction (DeepSeek, OmniRoute)
│   │   ├── rag, retrieval, embeddings, vector_store/
│   │   └── health.py, observability/, multilingual/, knowledge/
│   ├── .env.example            # Copy to .env (gitignored) with your own keys
│   ├── requirements.txt
│   └── tests/                  # pytest suite
│
├── infosecdairies/             # React + Vite frontend
│   ├── src/
│   │   ├── services/api.ts             # Single API base-url helper
│   │   ├── services/conversationsApi.ts# /api/conversations client
│   │   ├── hooks/useChat.ts            # Chat + SSE streaming client
│   │   ├── context/AuthContext.tsx     # JWT login/refresh state
│   │   └── components/ai/              # Floating assistant, workspace Chat
│   ├── vite.config.ts          # Dev proxy rules (chat→8001, api→8000)
│   └── infosec-backend/backend # Django project
│
├── start_all.sh                # One-shot: Django + FastAPI + React
├── start_django.sh / start_backend.sh / start_frontend.sh
└── SETUP.md                    # Full setup for a fresh machine
```

---

## 2. FastAPI AI service — the part you'll mostly touch

Run (Python 3.13, own venv):

```sh
cd ai_service
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then set DEVELOPMENT_MODE / LLM keys
```

Start:

```sh
bash start_ai_service.sh     # uvicorn app.main:app on :8001
```

Interactive docs: <http://localhost:8001/docs>

### Key config switch (`.env`)

```ini
DEVELOPMENT_MODE=true        # deepseek is overridden in dev; use omniroute setting
LLM_PROVIDER=deepseek|omniroute
DEEPSEEK_API_KEY=sk-...      # your own key; .env is gitignored
INTERNAL_ADMIN_TOKEN=        # gates detailed /health payload + admin ops
JWT_PUBLIC_KEY_PATH=         # RS256 pub key to verify Django JWTs (prod: required)
```

`app/core/config.py` is a pydantic-settings class — everything is env-driven and `DEVELOPMENT_MODE` flips most defaults (logging level, CORS, LLM provider, JWT algorithm).

### Endpoint surface (all under `:8001`)

| Method | Path | Purpose | Auth |
|---|---|---|---|
| POST | `/api/chat/` | Non-streaming chat (RAG pipeline) | Bearer JWT **or** `client_id` |
| POST | `/api/chat/session` | Session bootstrap / access status | depends on payload |
| GET | `/api/chat/access?client_id=…` | Free-tier access status / carry-over on login | Bearer (optional) |
| POST | `/api/v1/chat` | Legacy non-stream chat | Bearer JWT or `client_id` |
| POST | `/api/v1/chat/stream` | SSE streaming chat | Bearer JWT or `client_id` |
| GET | `/api/v1/chat/health` | Chat-pipeline health | none |
| GET/POST/PATCH/DELETE | `/api/conversations[/…]` | Conversation history & favorites | Bearer JWT |
| GET | `/api/health`, `/health`, `/` | Health (detailed payload needs `INTERNAL_ADMIN_TOKEN`) | optional |

### Chat request payload (`POST /api/chat/`)

```json
{
  "query": "What is a SIEM?",
  "conversation_id": "uuid-or-null",
  "request_id": "optional-uuid",
  "metadata": {},
  "images": [],
  "files": [],
  "client_id": "persistent-browser-guest-id"
}
```

**Identity rules** (fail closed — important):
- Valid JWT → identity is the token's `user_id`; premium users are **not** free-limited.
- No JWT but a `client_id` → treated as guest `guest:<client_id>`, always on the free tier, consumes the daily allowance (bucketed per `client_id` **and** per source IP — `FREEMIUM_GUEST_IP_KEYED=true` prevents id-rotation bypass).
- Neither → HTTP 401. Guests can never drive the LLM unlimited.
- Guest limit reached → HTTP **429** with body `{"detail": {"code": "free_ai_limit_reached", ...}}`. The frontend reacts to that code by showing an upgrade dialog.

### Streaming format (`POST /api/v1/chat/stream`)

`text/event-stream`. The frontend (`useChat.ts`) does minimal SSE line splitting; metadata events must stay on their own line. The `/api/chat/` endpoint also streams today — same SSE shape.

### Body-size protection

`app/middleware.py` caps POST/PUT/PATCH bodies (drains actual bytes, 413 over 16 MiB) so chunked-encoding bypasses don't work. Don't reintroduce skip-read exclusions for chat/SSE routes.

---

## 3. Django backend (::8000) — what the AI service expects from it

The Django project lives at `infosecdairies/infosec-backend/backend`.

Services you own that the AI service integrates with:

1. **JWT issuance** — Django's SimpleJWT access tokens must carry a **stable `user_id` claim** (email may vanish after refresh; conversations are keyed by `user_id`). The AI service verifies expiry/issuer/audience and reads `user_id`/`email`.
2. **Refresh tokens** — frontend auto-refreshes every ~10 min (`AuthContext`), and the AI service re-resolves identity on each call, so a refreshed token must still map to the same `user_id`.
3. **RS256 integration** — generate `jwt_private.pem`/`jwt_public.pem` (`generate_jwt_keys.py`); the AI service loads the **public** key via `JWT_PUBLIC_KEY_PATH` (required in production, HS256 dev fallback otherwise).

### Auth contract

- Login stores `accessToken`, `refreshToken`, `userEmail`, `userFullName` in `localStorage`.
- Frontend sends `Authorization: Bearer <accessToken>` to **both** backends.
- Guest → login carry-over: frontend calls `GET /api/chat/access?client_id=…` with the fresh Bearer so the guest's used count merges into the new account (no free-quota trick from logging in).

---

## 4. Frontend ↔ backend paths (dev proxy in `infosecdairies/vite.config.ts`)

```ts
"/api/chat":        { target: "http://127.0.0.1:8001", xfwd: true },
"/api/conversations": { target: "http://127.0.0.1:8001" },
"/api/health":      { target: "http://127.0.0.1:8001" },
"/api":             { target: "http://127.0.0.1:8000" },   // Django
```

`xfwd: true` on `/api/chat` matters: the AI service's `extract_client_ip()` uses `X-Forwarded-For` to enforce the per-IP guest bucket. A reverse proxy in front of the AI service must set it too, else all guests share the IP bucket in production.

`VITE_API_BASE_URL=""` in `infosecdairies/.env` → relative URLs, so the proxy above does the routing. In production (Vercel `vercel.json` rewrites) the same paths must forward accordingly.

---

## 5. Running everything locally

```sh
cd BlueTeamers-AI-Assistant
bash start_all.sh          # starts all three, logs to ./logs/
```

| Service | Port | Log |
|---|---|---|
| Django | 8000 | `logs/django_8000.log` |
| FastAPI AI service | 8001 | `logs/ai_service_8001.log` |
| React (Vite) | 5173 | `logs/frontend_5173.log` |

Smoke test:

```sh
curl -s -o /dev/null -w "frontend %{http_code}\n" http://localhost:5173/
curl -s -o /dev/null -w "django   %{http_code}\n" http://localhost:8000/
curl -s -o /dev/null -w "ai       %{http_code}\n" http://localhost:8001/health
```

Open <http://localhost:5173>, register/login, then use the chat (floating assistant button bottom-right, or the full workspace at `/chat`).

### AI-service tests

```sh
cd ai_service
.venv/bin/python -m pytest tests/ -q --ignore=tests/integration    # expect ~820 passed
```

Common failure points:
- Missing/incorrect `DEEPSEEK_API_KEY` → service logs errors, chat 500s.
- Port already bound → `pkill -f uvicorn ; pkill -f runserver ; pkill -f "vite --port 5173"`.
- Frontend `401` on chat but OK on courses → JWT key path mismatch (AI service can't verify RS256).

---

## 6. Checklist when you make changes

- [ ] Chat endpoints fail closed: no JWT and no `client_id` ⇒ 401, never free rein to the LLM.
- [ ] Guests stay IP+browser limited (`FREEMIUM_GUEST_IP_KEYED=true`), 429 with `free_ai_limit_reached`.
- [ ] Conversation history keyed by `user_id` (stable claim), not email.
- [ ] Production requires `JWT_PUBLIC_KEY_PATH` (RS256-only) and explicit `CORS_ORIGINS`.
- [ ] Request bodies stay capped (no body-skip for chat/SSE).
- [ ] Detailed health payload only behind `INTERNAL_ADMIN_TOKEN`; anonymous gets `{"status":"ok"}`.
- [ ] No secrets committed — `.env`, `jwt_*.pem` are gitignored.