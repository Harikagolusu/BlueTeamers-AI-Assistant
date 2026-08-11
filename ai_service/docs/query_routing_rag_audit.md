# Query Routing & RAG Pipeline — Root Cause Analysis

Date: 2026-08-04
Scope: End-to-end audit of the BlueTeamers AI Assistant request pipeline
(routing, platform engine, RAG pipeline, prompt construction, vector store).

## Implementation Status (2026-08-04)

All findings below were fixed in the same session. Live-validated against
`uvicorn :8001` (OmniRoute `:20128`; Django down):

- **R1–R5 (Router):** `rule_classifier.py` rewritten (word-boundary + plural matching,
  cyber-domain lexicon, specificity-ordered platform detection, domain/entity-gated RAG).
  `rule_evaluator.py` re-scored for deterministic priority. Verified: `'sigma rule example'`
  -> RAG, `'What courses do I have?'` -> PLATFORM_COURSE, `'How do firewalls work?'` -> RAG,
  `'What is Python?'` -> GENERAL, `'T1059'` -> RAG (0.90).
- **P1–P5 (Platform):** `platform_engine.py` is now intent-aware (dispatch by `PLATFORM_*`
  intent; LLM summarizes only fetched data). `DjangoPlatformRepository` implements
  `get_enrolled_courses()` (paid purchases + catalog, bundle-aware), real `get_certificates()`
  (`certificates/my/<slug>/`), profile via `auth/verify/` (no GET profile endpoint exists),
  progress % from static lesson counts. `UserContextBuilder` fetches live repo data instead of
  the session cache. Django-down → honest apology, no hallucination (validated live).
- **G1/G3 (RAG):** `Document` now carries `score`; `FAISSRetriever` passes chunk ids/scores;
  engines emit `SourceCitation`-shaped citations (fixes the `/api/v1/chat` 500 validation
  errors). `MIN_SIMILARITY_SCORE` default raised 0.0 -> 0.4. Validated: `/api/v1/chat` RAG
  queries return HTTP 200 with proper citations.
- **C1/C2 (Prompt):** platform engine now composes the `SimplePromptBuilder` system prompt
  with a strict data-bound instruction; system prompt updated to BlueTeamers identity +
  no-invent rules.
- **Tests:** updated `tests/chat/engines/*`, added `tests/chat/intent/test_routing_decisions.py`;
  fixed pre-existing stale fixtures (`_MockType.value`, single-string `build_prompt`).
  `tests/chat` + `tests/chat/intent` fully green (61 passed).

Remaining follow-ups: (1) start Django and live-verify enrolled-courses/certificates/progress
fetch; (2) verify `payments/my-purchases/` payload mapping is unchanged; (3) re-enable
`RuntimePolicyProxy` guardrails if desired.

---

## 1. Router Issues

| # | Root Cause | Evidence |
|---|-----------|----------|
| R1 | **Naive substring keyword matching causes false positives.** The platform classifier matched substrings anywhere in the query. `"example"` contains `"exam"`, so `"sigma rule example"` classified as `PLATFORM_ASSESSMENT` (confidence 0.90) and never reached RAG. | `rule_classifier.py` lines 61–148; live routing test: `'sigma rule example' -> PLATFORM_ASSESSMENT conf=0.90` |
| R2 | **Incomplete platform phrase coverage causes false negatives.** `"What courses do I have?"` and `"Resume my current course"` matched no platform keyword and fell through to `GENERAL_CHAT`, so the LLM answered (and hallucinated) instead of the Platform Engine. | Live response for `"What courses do I have?"` routed to GENERAL: the LLM asked *"Which platform are you using? (e.g. Coursera, CyberVista, SANS...)"* |
| R3 | **Knowledge queries without an explicit trigger phrase fell to GENERAL.** `"SIEM vs SOC"`, `"How do firewalls work?"`, `"Windows event log IDs"`, `"phishing detection"` contained no `"what is"/"explain"` phrase, so they never hit the vector store. | Routing test output — all routed `GENERAL` |
| R4 | **General-knowledge queries with RAG trigger phrases were wrongly routed to RAG.** `"What is Python?"` matched `"what is"` and hit the vector store, violating the Hybrid Knowledge Architecture (general knowledge = LLM only). | Routing test: `'What is Python?' -> RAG_CHAT conf=0.50` |
| R5 | **No cyber-domain awareness.** RAG detection relied only on generic phrases (`"what is"`, `"explain"`) and never on cybersecurity domain terms, so both domain queries (R3) and non-domain queries (R4) were misclassified. | `rule_classifier.py` lines 150–172 |

## 2. Platform Engine Issues

| # | Root Cause | Evidence |
|---|-----------|----------|
| P1 | **`PlatformExecutionEngine` ignores the classified intent.** It always calls `RecommendationService.generate_recommendations()` and returns *course recommendation cards*, regardless of whether the user asked about certificates, progress, assessments, profile, or enrolled courses. `"Show my certificates"` and `"What is my progress?"` would both return course recommendations. | `platform_engine.py` lines 44–62; dispatch is entirely absent |
| P2 | **Repository methods for certificates/labs/learning-paths/badges return hard-coded empty lists** (`get_certificates`, `get_badges`, `get_learning_paths`, `get_labs` → `[]`), so even an intent-aware engine would return nothing. | `django_repository.py` lines 65–89 |
| P3 | **`get_user_profile` calls `GET /api/auth/profile/`, which is a PATCH-only endpoint** (`update_profile`). Every profile fetch raises an HTTP error and degrades to `None`. | `django_repository.py` line 33; `accounts/urls.py` |
| P4 | **Platform context depends on a session cache** populated only when the frontend calls `/api/chat/session`. If that call is skipped, `UserContextBuilder` reports *"Active Enrollments: Not available."* and the LLM has no real data. | `user_context.py` lines 28–58 |
| P5 | When Django is down / token missing, the engine's LLM prompt says *"Do not invent external courses"* and apologizes — correct honesty, but the deterministic path that *could* answer from cache/catalog is not attempted first. | `platform_engine.py` lines 76–90 |

## 3. RAG Issues

| # | Root Cause | Evidence |
|---|-----------|----------|
| G1 | **Response schema mismatch breaks every RAG response on the `/api/v1/chat` endpoint.** Engines emit citations as `[{"source": "..."}]` but `app/chat/schemas.ChatResponse` requires `SourceCitation` (`course`, `lesson`, `chunk_id`, `similarity_score`, `source_title`). Result: **HTTP 500** for every RAG query with retrieved documents. | Live: `POST /api/v1/chat {"query":"Explain SIEM"}` → `25 validation errors ... citations.0.course Field required` |
| G2 | **Retrieval itself works, but the RAG engine is never invoked for many queries** because of router issues R2/R3. | Retrieval micro-test returned high-score chunks (0.69–0.85) for all target queries |
| G3 | **No similarity threshold** (`MIN_SIMILARITY_SCORE=0.0`), so irrelevant chunks can be injected into prompts. | `config.py` line 90; `retrieval/service.py` line 42 |

## 4. Prompt Construction Issues

| # | Root Cause | Evidence |
|---|-----------|----------|
| C1 | **The platform engine builds its own `system_instruction` and discards the `SimplePromptBuilder` system prompt** — so retrieved technical documents (already embedded in the builder's system prompt) are dropped for platform queries. | `platform_engine.py` lines 76–102 |
| C2 | **The base system prompt does not tell the LLM it is the BlueTeamers platform assistant.** When platform queries leak to GENERAL (R2), the LLM hallucinates that the user may be on *"Coursera, CyberVista, SANS, RangeForce"*. | `simple_prompt_builder.py` lines 13–20; live response |
| C3 | `PromptBuilder`'s `[Context]` block and `[Teaching Style]` are correctly wired for the RAG engine (verified live), so this is not the primary break. | Verified via `/api/chat/` responses with grounded answers |

## 5. Vector Store Issues

| # | Root Cause | Evidence |
|---|-----------|----------|
| V1 | **Not a data problem — the store is populated and searchable.** 3,681 chunks exist and queries return relevant chunks with high scores. The failure is upstream (routing) and downstream (schema). | `index.faiss` 5.6 MB, `metadata.json` 3.3 MB; retrieval test scores |
| V2 | `RetrievedChunk.text` is read from metadata key `"text"`, which ingestion stores correctly — no issue. | `pipeline.py` lines 67–79; `retrieval/service.py` line 97 |
| V3 | **Similarity scores are discarded** at the `IRetriever` boundary (the `Document` object carries no score), so citations/quality gates cannot use them. | `rag/interfaces.py` lines 4–11; `faiss_retriever.py` lines 23–28 |

## 6. Missing Context Issues

| # | Root Cause | Evidence |
|---|-----------|----------|
| M1 | Platform responses are never guaranteed to contain real user data because the engine only fetches recommendations and depends on the session cache (P4). | `platform_engine.py` |
| M2 | There is no "list my enrolled courses" call in the repository; enrolled courses must be derived from `/api/payments/my-purchases/` + `/api/courses/`. The engine never attempted this. | `django_repository.py` |
| M3 | Certificates exist per-course (`/api/certificates/my/<slug>/`) but were never enumerated for the user. | `certificates/views.py` |

---

## Recommended Fixes (implemented)

1. **Rewrite the intent classifier** (`rule_classifier.py`) with word-boundary matching, a cybersecurity domain lexicon, a specificity-ordered platform detection, and a domain-gated RAG rule (fixes R1–R5).
2. **Align the confidence evaluator** (`rule_evaluator.py`) so platform > RAG > tool > general priorities are deterministic (fixes R1, R4).
3. **Make `PlatformExecutionEngine` intent-aware**: dispatch per intent to deterministic repository data (enrolled courses, progress, certificates, assessments, profile, dashboard) and let the LLM only summarize (fixes P1, P2, M1, M2, M3).
4. **Extend `DjangoPlatformRepository`**: add `get_enrolled_courses()` (from purchases→catalog), implement `get_certificates()` (enumerate per-course certs), and make `get_user_profile()` resilient (fixes P2, P3).
5. **Fix the citation contract**: carry `similarity_score` through the retriever and emit `SourceCitation`-compatible dicts (fixes G1, V3).
6. **Remove the session-cache hard dependency** in `UserContextBuilder` and fetch live data from the repository (fixes P4).
7. **Strengthen the system prompt**: state the assistant serves the BlueTeamers platform, inject platform data through the prompt builder, and keep retrieved docs in the prompt (fixes C1, C2).
8. **Raise `MIN_SIMILARITY_SCORE`** to a sane default so irrelevant chunks are filtered (fixes G3).
9. **Add debug logging** for the router decision, selected engine, retrieval counts/scores, platform API calls, returned objects, and prompt context size.

No architectural layers were bypassed or merged: Router → Intent Pipeline → Engine Selection → (Platform | RAG | General) → Prompt Builder → LLM remains intact.
