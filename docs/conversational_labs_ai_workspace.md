# Conversational Practice Labs in the AI Workspace

Deliverables for transforming the AI Workspace into the primary interactive
practice lab: learners complete whole cybersecurity practice labs conversationally
(mentor guides, asks questions, evaluates answers, gives progressive hints, and
offers an assessment only when enrolled + confirmed, or recommends courses
otherwise). Existing `/labs/*` dashboard pages are untouched.

## What was built

### Backend (`ai_service/`)

| File | Purpose |
| --- | --- |
| `app/services/lab/scenarios.py` | `LabScenario`/`LabStep` models + 2 conversational scenarios (`phishing-email-analysis`, `siem-alert-triage`), each with 4 steps, keyword signals, 3-level anti-leakage hints, and mentor acknowledgements. Scenario text is NOT RAG-ingested, so answers/hints can't leak through retrieval. |
| `app/services/lab/session_store.py` | In-memory `ConversationalLabSession` + `LabSessionStore` keyed by `(user, lab)`, one active lab per user, per-step hints/attempts/score tracking. |
| `app/services/lab/evaluator.py` | `LabAnswerEvaluator`: keyword matching first (deterministic), LLM semantic evaluation as fallback. |
| `app/services/lab/manager.py` | `LabManager` coordinator: start/resume/catalog, answer evaluation, progressive hints, status, quit/restart, and completion → quiz offer (enrolled) or course recommendation (not enrolled). Emits the `metadata.lab` payload the frontend renders. |
| `app/chat/pipeline/lab_context_stage.py` | `LabContextStage`: takes over routing to `LAB_MENTOR` when a structured `context.lab` action arrives, an active lab session exists, or the intent is `LAB_ASSISTANT`/`PLATFORM_LAB`. |
| `app/chat/engines/specialist_engines.py` | `LabMentorExecutionEngine` now takes an optional `lab_manager` and routes active-lab turns through it (falls back to RAG mentor otherwise). |
| `app/chat/bootstrap.py` | Wires `LabManager` + `LabContextStage` into the pipeline (after `RoutePlanningStage`, before `EngineExecutionStage`). |
| `app/models/chat/chat_models.py`, `app/chat/routing/decisions.py`, `app/api/routes/chat.py`, `app/chat/routing/query_router.py`, `app/chat/service.py` | Thread `request.context` (`context.lab`) through `ChatRequest → RouterRequest → QueryRouter → ChatService → ExecutionContext.metadata`. |
| `app/chat/pipeline/assessment_stage.py` | Guard: never interrupts an active lab (completion offers are owned by the LabManager). |
| `app/agents/assessment/agent.py` | New `queue_offer()` (mirrors `_maybe_offer`'s PENDING_CONFIRM) for lab completion; `is_confirmation` is now word-boundary aware (fixes "I got it" → accidental quiz start). |

### Frontend (`infosecdairies/`)

| File | Purpose |
| --- | --- |
| `src/lib/labContext.ts` | Practice-lab catalog + `buildLabStartContext()` payload helper. |
| `src/hooks/useChat.ts` | `sendMessage(..., labContext)` sends `context.lab` in the request payload. |
| `src/components/ui/chat/LabCard.tsx` | Interactive card: stepper, current question, answer input, progressive Hint button (used/total), score, "Run again" on completion. |
| `src/components/ui/chat/EmptyStateDashboard.tsx` | New "Practice Labs" section with Start Lab buttons. |
| `src/components/ui/Chat.tsx` | Renders `LabCard` from `metadata.lab`, wires Start Lab / hint / restart / answer to `sendMessage`. |

## User journey

1. **Empty state** → Practice Labs section lists the 2 labs with Start buttons.
2. **Start Lab** → sends `context.lab: {action:'start', lab_id}` → `LabContextStage` routes to `LAB_MENTOR` → `LabManager` opens the scenario and asks Step 1.
3. **Answer** → keyword match (fast) or LLM evaluation → correct advances, wrong keeps the step with constructive feedback.
4. **Hint** → `LabManager` hands out progressive levels 1→3 (never the answer).
5. **Status / quit / restart** → recognized intents handled by the mentor.
6. **Completion** → score + per-step takeaways; then:
   - enrolled + topic match → quiz offer (queued PENDING_CONFIRM; "yes" starts the existing AssessmentStage quiz),
   - otherwise → course recommendation cards (`CyberDomain.LAB` domain).
7. **Everything streams**; each turn's `metadata.lab` re-renders the LabCard.

## Data / event flow

```
Frontend (Start Lab)
  └─ POST /api/chat/ {context:{lab:{action,lab_id}}, stream:true}
       └─ QueryRouter.process
            └─ ChatService.process_request  (metadata["context"] = request.context)
                 └─ ChatOrchestrator stages
                      InputGuardrails → Cache → MemoryLoad → PlatformContext →
                      AttachmentParse → Intent → RoutePlanning →
                      LabContextStage ──takes over──▶ selected_engine = LAB_MENTOR
                      EngineExecutionStage → LabMentorExecutionEngine
                           └─ LabManager.handle(ctx)
                                ├─ start/resume/catalog/evaluate/hint/status/quit
                                ├─ keyword → LLM evaluation
                                └─ completion → AssessmentAgent.resolve_offer
                                     ├─ offer_quiz        → queue_offer (PENDING_CONFIRM)
                                     └─ recommend_course  → RecommendationService cards
                      AssessmentStage (skipped while lab.active)
                      OutputGuardrails → Evaluation → Composition → Persistence
                 └─ SSE: token events + final {metadata:{lab, agent, ...}}
```

## Verification

- `pytest` (ai_service): **440 passed** — including new `tests/services/test_lab_manager.py` (14 unit tests: start/answer/hint/quit/status/catalog/completion-offer/completion-recommend/stage takeover/engine routing) and `tests/chat/test_lab_api_integration.py` (end-to-end via the chat API with `context.lab`).
- `npm run build` (frontend): succeeds.
- Live curl run against `:8001` verified: start → wrong answer (feedback) → hint (level 1) → correct (advance) → 4/4 completion with takeaways → quiz offer → "yes" starts the quiz.

## Notes / decisions

- **Reuse, no duplication**: the existing `LabState`/`HintLevel`/`AssessmentStage`/`RecommendationService`/`CyberDomain.LAB` infrastructure is reused; no new agent or RAG pipeline was added.
- **Scenario answers/hints are kept out of the RAG index** (existing `sources.py` behavior preserved) so the mentor can't leak them.
- **Enrollment gating** is respected on completion: quiz offers only when `resolve_offer` returns `offer_quiz`; otherwise course cards.
- **Fixes shipped along the way**: `is_confirmation` substring bug (word-boundary aware), `CourseOfferAction` value comparison in the manager.

## Files changed

Backend: `app/services/lab/{scenarios,session_store,evaluator,manager}.py` (new),
`app/chat/pipeline/lab_context_stage.py` (new), `app/chat/engines/specialist_engines.py`,
`app/chat/bootstrap.py`, `app/models/chat/chat_models.py`,
`app/chat/routing/decisions.py`, `app/api/routes/chat.py`,
`app/chat/routing/query_router.py`, `app/chat/service.py`,
`app/chat/pipeline/assessment_stage.py`, `app/agents/assessment/agent.py`,
tests: `tests/services/test_lab_manager.py` (new),
`tests/chat/test_lab_api_integration.py` (new),
`tests/agents/assessment/test_agent.py`.

Frontend: `src/lib/labContext.ts` (new), `src/components/ui/chat/LabCard.tsx` (new),
`src/hooks/useChat.ts`, `src/components/ui/chat/EmptyStateDashboard.tsx`,
`src/components/ui/Chat.tsx`.
