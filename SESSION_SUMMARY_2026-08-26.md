# BlueTeamers AI Assistant — Session Summary
**Date:** 26 August 2026
**Project:** `BlueTeamers-AI-Assistant` (AI service :8001 · Frontend :5173 · Django backend :8000)

---

## 1. Session Overview

| # | Task | Status |
|---|---|---|
| 1 | Quiz/assessment integrity fix (stop answer leakage) | ✅ Done & verified |
| 2 | Full guardrails audit | ✅ All working |
| 3 | Per-user token usage tracking system | ✅ Built & verified |
| 4 | Live team consumption monitor | ✅ Working |
| 5 | Deep token usage audit (9,421-token investigation) | ✅ Report delivered |
| 6 | Persona block optimization (~36% smaller) | ✅ Done & regression-tested 10/10 |
| 7 | Conversation-history audit | ✅ Report delivered |
| 8 | MEMORY_WINDOW optimization (10 → 6) | ✅ Done & regression-tested 10/10 |
| 9 | Environment repair (frontend port conflict, backend setup) | ✅ Fixed |

---

## 2. Quiz / Assessment Integrity Fix

**Problem:** Pasting quiz questions into chat produced direct answers (`"The correct answer is C"`).

**Fix:** Added MCQ detection + tutor-mode directive in `ai_service/app/prompt_builder/simple_prompt_builder.py`.
- Detector `_is_assessment_question()` — regex on option lines (`A)`, `B.`, bare `A <text>` ≥3 lines) + phrases like "which of the following".
- New `ASSESSMENT_TUTOR_BLOCK`: never reveal the option; name only the topic area; max ONE hint; walk through options only after the learner commits.

**Verified:** pasted SOC MCQ → guided response, no letter reveal; normal questions unaffected.

---

## 3. Guardrails Audit — All Confirmed Working

| Guardrail | Result |
|---|---|
| Prompt injection (input) | ✅ Blocks with graceful refusal; never reaches LLM |
| Length validation (>32k chars) | ✅ Blocks pre-LLM |
| Sensitive-data leak (output-only: AKIA…, sk-…, private keys) | ✅ Blocks on output |
| Freemium gate (5 free msgs/day, guest IP-keyed) | ✅ Enforces |
| Rate limit (60/min per user/IP) | ✅ Active |
| SIEM/SOC disambiguation (prompt rule) | ✅ Cybersecurity meaning always |

Key architecture fact: `EngineExecutionStage` and `CacheStage` short-circuit when a blocked `execution_result` already exists — guardrail blocks cannot be bypassed.

---

## 4. Token Tracking System (new)

Per-user **daily + monthly** LLM token accounting, persisted in SQLite, **audit-only** (records, does not block).

**Files added/changed**
- `app/runtime/services/token_usage_store.py` *(new)* — SQLite store, dual window
- `app/runtime/services/token_quota_manager.py` *(new)* — records always; blocks only if enforce=True
- `app/runtime/services/token_usage_recorder.py` *(new)* — safe recorder used by ChatService
- `app/core/config.py` — `TOKEN_QUOTA_ENABLED=True`, `TOKEN_QUOTA_ENFORCE=False`, `TOKEN_DAILY_LIMIT=100_000`, `TOKEN_MONTHLY_LIMIT=2_000_000`, `TOKEN_QUOTA_DB_PATH=data/token_quota.db`
- `app/llm/providers/deepseek_provider.py` — records real API `prompt_tokens`/`completion_tokens`
- `app/chat/service.py` — persists usage once per request with correct scope
- `app/api/routes/token_usage.py` *(new)* — reporting endpoints

**Endpoints**
- `GET /api/token-usage?client_id=<device>` → caller's daily/monthly usage
- `GET /api/token-usage/overview` → **live monitor**, all users sorted by daily usage

Scoping: authenticated = `user:<id>`, guests = `guest:<client_id>` (per-device; avoids merging colleagues behind one IP).

---

## 5. Token Usage Audit (read-only)

User reported 9,421 tokens for "4 questions". Findings:
- Tracker is **exact**: 9,421 = 3,144 + 3,532 + 2,745 — three real API calls ("what is siem", "soc", "thank you"); a 4th question was served by the exact-match cache at zero cost.
- Counter reads **actual API usage** (input incl. cached prefix + output); no double counting, no retries (exactly 1 LLM call per question).
- Intent routing and quiz detection are rule-based — **no extra LLM calls**.
- Embeddings are local (`BAAI/bge-small-en-v1.5`) — zero API tokens.
- Cost breakdown per question: fixed instructions ~1,536 tok (65% = old persona block), history up to ~900, RAG context ~500–800 (top_k=5 × 600-char chunks), output 96–346.

Optimization opportunities ranked: persona compression > history cap > RAG top_k/chunk tuning.

---

## 6. Persona Optimization (done)

Only `app/persona/personas.py` changed (+34/−66). Compressed identity/style/response-format/domain-priority/personality prose; removed wording duplicated by the base prompt and `[Response Style]`; kept expertise list and all level guidance byte-for-byte.

| Metric | Value |
|---|---|
| OLD persona tokens | ~1,000 API (1,214 heuristic) |
| NEW persona tokens | ~644 API (782 heuristic) |
| Saved per request | ~356–384 tokens (DeepSeek cached prefix dropped 1,536 → ~1,152) |
| Reduction | ~36% of the persona block |
| Regression | 10/10 scenarios passed (Wazuh, MITRE, beginner, technical, analogy, conversational, quiz-tutor, out-of-scope, concise) |

---

## 7. Conversation History Optimization (done)

Audit findings: verbatim last-10-messages sent every request (~1,780 tok steady state); RAG retrieval/intent/quiz never read history; a compacted summary/facts/investigation system already exists and is already injected — so older turns are duplicated, not lost.

**Change:** one line — `config.py:157` `MEMORY_WINDOW: int = 10` → `int = 6`.

| Metric | Value |
|---|---|
| Old window | 10 messages (5 Q&A pairs) |
| New window | 6 messages (3 Q&A pairs) |
| Saving | ~700–1,000 tokens/message once conversation exceeds 3 turns |
| Regression | 10/10 passed — incl. follow-up ("What about FIM?"), multi-turn recall, quiz tutor intact, user-specific context |

Combined with persona work: ≈45% total reduction vs original baseline on multi-turn sessions.

---

## 8. Environment Fixes

- Stopped 3 stray LifeFlow Vite dev servers occupying :5173; started the BlueTeamers frontend (now bound to all interfaces).
- Created `infosec-backend/.venv` (virtualenv workaround — system Python lacks ensurepip), installed backend requirements, ran migrations, started Django on :8000 so login works locally.
- WSL2 NAT note: colleagues need Windows `netsh interface portproxy` to reach :5173/:8001 from the LAN.

---

## 9. Current System State

- All services healthy (5173 / 8000 / 8001).
- Token tracking live: `GET /api/token-usage/overview`.
- Enforcement still OFF (`TOKEN_QUOTA_ENFORCE=False`) — flip on when limits are decided. Guest enforcement will need a pre-call scope-aligned check in ChatService when activated.

## 10. Recommended Next Steps (not yet done)

1. Decide final daily/monthly limits from measured team data; set `TOKEN_QUOTA_ENFORCE=True` + add guest-safe pre-call check.
2. Consider RAG tuning (top_k 5→3 and/or chunk 600→400) after measuring retrieval quality — est. ~200–400 tok/RAG query.
3. Optionally exclude DeepSeek *cached* input tokens from quota accounting for billing-equivalent numbers.

---

## 11. Key Files Touched This Session

```
ai_service/app/prompt_builder/simple_prompt_builder.py   (quiz detection + tutor block)
ai_service/app/persona/personas.py                       (compressed persona)
ai_service/app/core/config.py                            (MEMORY_WINDOW=6, TOKEN_QUOTA_* settings)
ai_service/app/chat/service.py                           (token usage persistence)
ai_service/app/llm/providers/deepseek_provider.py        (usage capture)
ai_service/app/runtime/dependencies.py                   (persistent quota wiring)
ai_service/app/runtime/services/token_usage_store.py     (new)
ai_service/app/runtime/services/token_quota_manager.py   (new)
ai_service/app/runtime/services/token_usage_recorder.py  (new)
ai_service/app/api/routes/token_usage.py                 (new endpoints)
ai_service/app/api/routes/__init__.py                    (router registration)
infosec-backend/.venv/*                                  (backend environment, new)
```
