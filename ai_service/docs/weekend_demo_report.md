# Project Analysis — InfoSec Dairies + BlueTeamers AI Assistant

**Weekend Demo Report · Verified from source & live runtime**

> Every claim below was verified against running services, the test suite, and the database on 2026-08-08. Features marked **(partial)** exist but are limited or not fully wired end-to-end. Live state: Django `:8000` ✅ · AI service `:8001` ✅ · Frontend `:5173` ✅ · **685 backend tests passing**.

---

## 1. Project Overview

A **cybersecurity e-learning platform** ("InfoSec Dairies") with an **AI study assistant** ("BlueTeamers") embedded in it. It is three cooperating services:

| Service | Tech | Port | Role |
|---|---|---|---|
| **Django backend** | Django 6.0.7, DRF 3.17.1, SimpleJWT | 8000 | Auth, courses, payments, certificates, leads |
| **FastAPI AI service** | FastAPI, LangGraph-style pipelines, FAISS RAG | 8001 | Chat, RAG, specialist engines, freemium, assessments |
| **React frontend** | React 18, Vite, TypeScript, Tailwind, shadcn/ui | 5173 | Landing, course store, lessons, quizzes, AI workspace, floating assistant |

The AI assistant is not bolted-on: it reads the learner's **enrolled courses, lesson progress, quiz scores, and purchases from Django**, personalizes answers to their level, grounds answers in the platform's **own course content (RAG)**, and ends responses with **"Continue Learning"** pointers back into the actual courses.

---

## 2. Working Features

### Platform (Django)
- **Email + OTP auth** with JWT (RS256, 2h access / 60d refresh, rotation + blacklist). Auto-refresh every 10 min on the frontend. `POST /api/auth/login/` verified → returns user + access/refresh tokens.
- **Google OAuth** flows implemented (`google/jwt`, `google/onboarding`, `google/start-otp`, `google/verify-otp`) — but **no OAuth provider keys configured**, so the button won't complete in this demo. **(partial)**
- **Course catalog**: 10 courses in DB (Beginner→Advanced), course detail, secure lesson access, quiz player.
- **Enrollment + progress**: enrollment status, lesson completion, quiz score submission. Demo user has 4 enrollments (3 paid + 1 free) and 19 lesson-progress records.
- **Payments**: Razorpay order creation, signature verification, **webhook**, promo codes, **country-based pricing** (₹499/₹799/₹1,199 by difficulty; ₹3,999 bundle). Code is complete but **no live Razorpay keys** → real checkout returns 500. Free course + 100%-off promo codes work. **(partial)**
- **Certificates**: upload, share, public verification (`/verify/:slug/:emailHash`); 4 in DB.
- **Leads**: capture + admin list.

### AI Assistant (FastAPI)
- **Intent-aware chat**: rule-based classifier → 16 execution engines (GENERAL, RAG, TOOL, AGENT, NOTES, SUMMARY, THREAT_INTEL, WAZUH_LAB, PRACTICE_LAB, INVESTIGATION_GUIDANCE, WINDOWS_EVENT_LOG, LINUX_LOG, IOC_ANALYSIS, MITRE_GUIDANCE, DETECTION_RULE, PLATFORM).
- **RAG grounded in platform courses**: FAISS vector store, 3,563 chunks from 442 lessons across 11 courses, `bge-small-en-v1.5` embeddings, course-first retrieval, reranking, course/lesson citations. Verified live: "what is event id 4625" returns an answer with citations `{course, lesson, chunk_id, similarity_score}`.
- **SSE streaming**: token-by-token streaming verified live.
- **Continue Learning footer**: RAG answers end with `### Continue Learning — Covered in Module '…' of <Course>` linking back to the real course.
- **Specialist engines**: Windows event log analysis, Linux log analysis, IOC analysis, MITRE ATT&CK guidance, detection-rule guidance, threat intel (CVE/IP/hash extraction), investigation guidance, lab mentors.
- **Personalization**: persona tuned to 5 learner levels; adaptive learning engine adjusts answer depth to the user's level.
- **Freemium (guests + free tier)**: 5 free messages/day incl. logged-out guests; premium unlocked by having a paid course. Guest course suggestions come from the catalog (no leak of user-specific data).
- **Course-aware assessment coach**: turn-by-turn quiz with adaptive difficulty, LLM question generation + deterministic fallback.
- **Memory**: session memory (summary, facts, investigation, files) + SQLite conversation history (list/search verified).
- **Sanitization**: strips internal tags, debug traces, citation chips, and `[Document N]` artifacts from answers before they reach the UI.

### Frontend
- 36 routes; landing, course store (10 courses), lessons, quiz player (77 quizzes / 331 questions), checkout, dashboard, certificates.
- **AI Workspace** (`/chat`): premium gate, conversation sidebar (persisted), streaming markdown (GFM: tables, lists, code, blockquotes, checkboxes), course source cards, quiz/lab result cards.
- **Floating assistant**: launcher on every page, page-context detection, free-limit ticket tray, guest flow, shared conversation state with the workspace.

---

## 3. End-to-End User Flow

1. **Landing** (`/`) → browse 10 courses, pricing, AI assistant launcher (guest = 5 free messages).
2. **Register/Login** → email + OTP → JWT issued → frontend verifies token locally (`/api/auth/verify/`) → auto-refresh every 10 min.
3. **Enroll** → free course ("Network Fundamentals") immediate; paid course → Razorpay checkout → webhook → `CoursePurchase` + `Enrollment(is_paid=True)`.
4. **Learn** → lesson viewer (RS256-signed access token) → mark complete → `LessonProgress`; quiz player → `QuizScore`.
5. **Ask AI** → workspace or floating assistant → intent classification → engine execution (RAG for content, specialist engines for analysis) → streamed markdown answer + **Continue Learning** card → conversation saved to SQLite.
6. **Assessment** → AI quiz coach checks the learner's understanding and adapts.
7. **Certify** → certificate upload + public share/verification link.

Demo user `harika@example.com` is enrolled+paid in 3 courses with progress, quiz scores, and purchases — perfect for the demo.

---

## 4. Architecture

```
┌───────────────────────┐   HTTPS/JSON + SSE    ┌───────────────────────────┐
│   React Frontend      │◄─────────────────────►│   FastAPI AI Service      │
│  src/ (189 files)     │   /api/chat (SSE)     │  app/ (993 .py, 40K LOC)  │
│  Vite :5173           │                       │  :8001                    │
└──────────┬────────────┘                       └───────┬───────────────────┘
           │ REST (/api/*)                              │
           ▼                                             │
┌───────────────────────┐                       ┌───────▼───────────────────┐
│   Django 6.0.7        │                       │  AI internals:           │
│   accounts/courses/   │  platform repo       │  • 17-stage pipeline      │
│   certificates/       │  (httpx + JWT, 60s   │  • rule intent classifier │
│   payments/leads      │  cache) ◄────────────►  • 16 engines / 17 agents │
│   :8000 (85 app .py)  │                       │  • FAISS RAG (3,563 chk)  │
│   SQLite DB           │                       │  • LLM providers:         │
└───────────────────────┘                       │    omniroute (dev/live),  │
                                                │    bedrock (prod), ollama │
                                                │    (local)                │
                                                └───────────────────────────┘
```

- **Auth boundary**: the AI service never stores credentials — it exchanges JWT access tokens with Django via `DjangoPlatformRepository` (60s cache) to fetch the learner's courses/progress/purchases.
- **Engine registry**: `ExecutionEngineRegistry` + factory (`app/chat/bootstrap.py:200-226`) selects the engine from the classified intent.
- **RAG**: MarkdownRecursiveChunker → `bge-small-en-v1.5` embeddings → FAISS (3,563 vectors) → course-first retrieval → reranker → context builder → LLM.

---

## 5. AI Pipeline

```
 query ──► sanitize ──► intent classifier (rule-based, confidence)
             │              │
             ▼              ▼
        guardrails ──► planner / router
                           │
        ┌──────────────────┼───────────────────┐
        ▼                  ▼                   ▼
   RAG engine       specialist engines    platform engine
 (knowledge)       (logs/IOC/MITRE/labs)  (courses/progress)
        │                  │                   │
        ▼                  ▼                   ▼
   context builder ──► LLM (streaming SSE) ──► response sanitize
                          │
                          ▼
              memory (session + conversation store)
                          │
                          ▼
            answer + Continue Learning footer + citations
```

Key design decisions:
- **No LLM routing** — intent routing is deterministic (rule classifier + confidence), so the demo is fast and predictable.
- **Course-first retrieval** — RAG prefers the user's own enrolled courses; answers cite course+lesson.
- **Personalized depth** — learner level (Beginner→Advanced) adjusts persona and response length.
- **Guests handled gracefully** — no token → catalog-based recommendations + "browsing as a guest" messaging.

---

## 6. Demo Flow (recommended walkthrough)

1. `start_all.sh` → services up (Django :8000, AI :8001, Vite :5173).
2. Landing → floating AI assistant opens → **ask as a guest** "what courses should i take to become a soc analyst" → catalog recommendations + guest note (no login needed).
3. Login as `harika@example.com` / `password123` → dashboard shows 3 paid enrollments + progress.
4. **AI Workspace** `/chat` → ask "explain event id 4625" → streaming SSE → RAG answer **with table**, citations, and a **Continue Learning** card pointing at the real course module.
5. Ask "windows failed logon event" → **specialist engine** (Windows Event Log) structured walkthrough + course pointer.
6. Ask "what is the difference between tcp and udp" → markdown **table** rendered.
7. Ask "should i take malware analysis" → course recommendation from BlueTeamers catalog.
8. Ask something off-topic ("what's the weather") → polite refusal.
9. Open the free course "Network Fundamentals" → complete a lesson → quiz player.
10. Show certificate verification page (public link).
11. Mention **685 passing tests** and the deep stack (Django+FastAPI+React+RAG+SSE).

---

## 7. Unique Features

- **Course-grounded RAG**: AI answers are tied to *this platform's* curriculum (course+lesson citations), not generic web text.
- **Continue Learning cards**: every content answer ends with a concrete next-step link into the learner's courses.
- **Freemium guest AI**: a logged-out visitor can try the assistant (5 msgs/day) and get course recommendations that drive signup — a full product funnel.
- **Specialist analysis engines**: Windows/Linux log analysis, IOC extraction, MITRE ATT&CK mapping, detection-rule guidance — beyond generic chatbot behavior.
- **Zero-LLM routing**: deterministic intent classification keeps the demo fast, cheap, and reproducible.
- **Tri-service auth integration**: AI service consumes Django JWTs to personalize answers per user without storing credentials.
- **Adaptive assessment coach**: course-aware quiz with difficulty adaptation and deterministic fallback (works offline).

---

## 8. Current Limitations (honest list)

- **Razorpay checkout requires live keys** — order creation/webhook code is complete but unconfigured; free course + promo codes work. **(partial)**
- **Google OAuth button won't complete** — allauth/dj-rest-auth flows present, `GoogleSocialApp` keys not set. **(partial)**
- **`LessonContent` table empty (0 rows)** — 442 lessons exist on disk (`all_lessons.json`) and lesson access uses signed frontend-backed content; DB-backed lesson endpoint not seeded. **(partial)**
- **Live labs/SOC pages are mock simulations** — frontend simulates real-time events; no backend lab engine.
- **Threat-intel external tools are mocked** (VirusTotal-like/MITRE lookups simulated).
- **Ollama local** provider is implemented and validated but the demo runs on **omniroute** (live LLM).
- **Doc/PDF ingestion & OCR** are implemented but not wired into the default bootstrap pipeline. **(partial)**
- **`Dashboard stats` points are placeholders** — analytics charts have no live data source.
- **Compliance guardrail group is empty** (input-length + injection-detection policies are active).

---

## 9. Demo Questions (audience talking points)

1. *How does the AI know which course to recommend?* — It pulls your enrollments/progress from Django via JWT and ranks the catalog with `_rank_courses()`.
2. *Is the answer hallucinating?* — No: RAG retrieves from the platform's own 3,563 lesson chunks and cites course+lesson; deterministic fallbacks exist for every specialist path.
3. *How does streaming work?* — SSE: the FastAPI route yields LLM tokens + metadata events, the frontend renders them as live markdown.
4. *What happens without a subscription?* — 5 free messages/day for everyone, incl. guests; premium activates the moment you hold a paid course.
5. *Why two backends?* — Django owns commerce/data; FastAPI owns the AI. They talk over HTTPS with short-lived JWTs and a 60s cache — no shared credentials.
6. *How is the response formatted?* — GFM markdown (tables/checklists/code) + a fixed structure (Overview → Why It Matters → Example → Continue Learning), with internal tags stripped before rendering.
7. *How reliable is it?* — 685 passing tests across the AI service; frontend passes `tsc --noEmit` and production build.

---

## 10. Project Statistics (measured)

| Metric | Value |
|---|---|
| AI service Python files | 993 |
| AI service lines of code | ~40,487 |
| Backend test files | 127 |
| Backend tests passing | **685** |
| Frontend source files (tsx/ts) | 189 |
| Frontend lines of code | ~37,348 |
| Frontend build | ✅ `tsc --noEmit` + `vite build` |
| Django app code files | 85 |
| Engines in registry | 16 |
| Agents in catalog | 17 |
| Pipeline stage classes | 17 |
| AI REST routes | 15+ (chat, access, me, conversations CRUD+search, knowledge status/ingest, health, metrics) |
| Courses in DB | 10 |
| Lessons on disk (`all_lessons.json`) | 442 (11 courses) |
| RAG vectors loaded | 3,563 |
| Quiz questions (frontend) | 331 (77 quizzes) |
| Users / Enrollments / Progress | 2 / 4 / 19 |
| Purchases / Certificates / Leads | 3 / 4 / 1 |

---

## 11. Feature Status Table

| Feature | Status | Evidence |
|---|---|---|
| Email+OTP auth, JWT refresh | ✅ | `/api/auth/login/` verified; frontend 10-min refresh |
| Google OAuth | 🟡 partial | Flows implemented; no provider keys |
| Course catalog (10 courses) | ✅ | DB rows + storefront routes |
| Lesson viewer + progress | ✅ | 19 LessonProgress rows; signed access |
| Quiz player + scores | ✅ | 331 questions; QuizScore writes |
| Razorpay checkout | 🟡 partial | Full code; needs live keys |
| Promo codes / country pricing | ✅ | Backend logic verified |
| Certificates + public verify | ✅ | 4 issued; verify route live |
| Lead capture | ✅ | 1 lead in DB |
| AI chat (SSE streaming) | ✅ | Live token-by-token |
| RAG (course-grounded) | ✅ | 3,563 vectors; citations returned |
| Continue Learning footer | ✅ | Live on RAG answers |
| Specialist engines (logs/IOC/MITRE) | ✅ | Windows Event Log live-tested |
| Threat-intel external lookups | 🟡 partial | Mocked providers |
| Freemium guests (5/day) | ✅ | Guest flow live-tested |
| Course recommendations | ✅ | Catalog-driven, BlueTeamers-only |
| Course-aware assessments | ✅ | LLM gen + deterministic fallback |
| Session/conversation memory | ✅ | SQLite; list/search verified |
| Response sanitization | ✅ | 7 dedicated tests |
| Live labs / SOC simulations | 🟡 partial | Frontend mock simulations |
| Doc/PDF/OCR ingestion | 🟡 partial | Implemented, not in default bootstrap |
| Dashboard analytics charts | 🟡 partial | Points placeholder, no data source |
| Tests + build | ✅ | 685 pass; tsc/build clean |

---

## 12. Demo Script (concise)

```
1. start_all.sh  →  verify :8000, :8001, :5173 respond 200.
2. Landing page  →  click floating AI assistant.
3. GUEST MODE    →  "what courses should i take to become a soc analyst"
                     → catalog cards + guest note (no login).
4. LOGIN         →  harika@example.com / password123  → dashboard (3 paid).
5. /chat         →  "explain event id 4625"
                     → SSE stream → table + citation + Continue Learning card.
6. /chat         →  "failed logon event windows" → specialist engine walkthrough.
7. /chat         →  "tcp vs udp" → markdown table.
8. /chat         →  "weather in mumbai" → polite off-topic refusal.
9. Courses       →  Network Fundamentals (free) → open lesson → quiz.
10. Certificates →  public verify link page.
11. Closing      →  stack depth (Django + FastAPI + React + FAISS RAG + SSE),
                    guest→freemium funnel, 685 tests.
```

---

*Compiled 2026-08-08. All live checks re-run at report time: 685/685 tests pass, three services up, demo login + streaming + RAG citations verified.*
