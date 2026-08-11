# Course-Aware Assessment Agent

A production-ready feature that evaluates a learner's understanding through
interactive in-chat quizzes — **only** for courses the learner is currently
enrolled in.

## 1. Architecture Summary

The feature extends the existing post-answer `AssessmentStage` that already runs the
interactive `AssessmentAgent`. The key change makes eligibility **course-aware** and
keeps the Assessment Agent **separate** from the Course Recommendation system (SOLID:
single responsibility).

```
User Question
      │
      ▼
Intent Analysis (DomainClassifier)
      │
      ▼
EngineExecutionStage (normal answer produced)
      │
      ▼
AssessmentStage (post-answer overlay)
      │  agent.resolve_offer(query, token, ...)   ← NEW course gate
      ▼
  ┌─────────────┴────────────────────────────┐
  │ Enrolled & topic matches &               │  Not enrolled / cannot verify
  │ not recently assessed                    │
  ▼                                           ▼
  OFFER_QUIZ   (requires explicit "yes")    RECOMMEND_COURSE  (NO quiz)
      │  ─ confirmation ─                          │
      ▼                                           ▼
  AssessmentAgent generates dynamic quiz    RecommendationService.generate_for_domain
  evaluate → explain → score → progress     → platform course cards (Enroll / View)
```

### Key components
| Component | Responsibility |
|---|---|
| `CourseContextService` (`app/agents/assessment/course_context.py`) | Decides **quiz eligibility** from live enrolment state + topic matching + "recently assessed" window. Contains NO recommendation logic. |
| `AssessmentAgent.resolve_offer()` | Course-aware gate returning `off / offer_quiz / recommend_course / recently_assessed`. |
| `RecommendationService` (existing) | Owns course recommendations (invoked by the stage only when NOT enrolled). |
| `AssessmentStage._recommend_course()` | Delegates to `RecommendationService`, builds platform course cards (Enroll / Go to course / Course info). |
| `InMemoryAssessmentProfileStore` | Tracks per-course learning progress (scores, weak/strong topics, completion %, last assessment date, revision topics). |

### Trigger rules (ALL must hold to offer a quiz)
1. User is **enrolled** in the course.
2. The topic **belongs to** that course (deterministic keyword matcher).
3. The user asked a **learning-related** question.
4. The user has **not recently** completed an assessment for that topic
   (default 7-day window, configurable).
5. The user **explicitly confirms** they want the quiz.

If condition 1 or 2 fails → the agent stays inactive and the stage defers to the
Course Recommendation service (no quiz).

## 2. Execution Flow

**Scenario A — Enrolled learner asks a course question**
1. User: *"Explain how SIEM correlation rules work"*
2. Engine answers normally.
3. `resolve_offer` → user enrolled in `siem-fundamentals`, topic "SIEM" matches, no recent assessment → `OFFER_QUIZ`.
4. Stage appends: *"Would you like to check your understanding of **SIEM Fundamentals** with a short quiz?"*
5. User: *"yes"* → `start_quiz(course_slug="siem-fundamentals")` → turn-by-turn questions → grading → explanations → scored summary.
6. Result recorded against the course in the profile store (progress updated).

**Scenario B — Not enrolled**
1. User: *"What is Retrieval-Augmented Generation?"*
2. Engine answers normally.
3. `resolve_offer` → no enrolment / topic doesn't match → `RECOMMEND_COURSE`.
4. Stage appends: *"...since you're not currently enrolled... here are some courses you can explore"* + **Enroll / Go to course / Course info** cards.
5. No quiz is offered. (Course recommendation is owned by the Recommendation service.)

**Scenario C — Recently assessed**
1. User answered/SIEM quiz within the window → `resolve_offer` returns `RECENTLY_ASSESSED` → nothing appended (no repeat interruption).

## 3. Files Added / Modified

**Added**
- `ai_service/app/agents/assessment/course_context.py` — `CourseContextService`, `CourseOffer`, `CourseOfferAction`.
- `ai_service/tests/agents/assessment/test_course_context.py` — course-gate & progress tests.
- `ai_service/tests/chat/test_assessment_stage_course.py` — stage recommend/offer tests.
- `ai_service/docs/course_aware_assessment.md` — this document.

**Modified**
- `ai_service/app/agents/assessment/agent.py` — `resolve_offer()`, course-aware `offer_message(course_title)`, `course_recommendation_message()`, `course_slug` tracking through `start_quiz`/`_finish`.
- `ai_service/app/agents/assessment/models.py` — `AssessmentProfile` course-aware fields.
- `ai_service/app/agents/assessment/profile_store.py` — per-course progress recording + recent-course-assessment query.
- `ai_service/app/chat/pipeline/assessment_stage.py` — course-aware `_maybe_offer`, `_recommend_course`, `_build_course_cards`, `extra` metadata support.
- `ai_service/app/chat/bootstrap.py` — wired `CourseContextService` into `AssessmentAgent` and `RecommendationService` into `AssessmentStage`.
- `ai_service/app/core/config.py` — `ASSESSMENT_REQUIRE_ENROLLMENT`, `ASSESSMENT_RECENT_WINDOW_SECONDS`, `ASSESSMENT_COURSE_RECOMMENDATION_COUNT`.
- `ai_service/tests/chat/pipeline/test_assessment_stage.py` — stage-mechanics tests run in legacy mode; course-aware path covered by new tests.
- `ai_service/docs/daily_logs/today_work.md`, `change_log.md` — feature log entries.

## 4. Manual Testing Guide

### Backend unit tests
```bash
cd ai_service
.venv/bin/python -m pytest tests/agents/assessment -q      # 26 passed
.venv/bin/python -m pytest tests/chat -q                  # 81 passed
```

### End-to-end (via Chat UI)
Start the platform (`start_all.bat` → Django 8000, Ollama, FastAPI 8001, Vite 8081),
log in as an enrolled user, then:

| Test | Expected |
|---|---|
| Ask a question about an **enrolled** course topic | Normal answer + quiz offer (course named). Say "yes" → quiz. |
| Answer a quiz question | Graded turn-by-turn with explanations; final scored summary. |
| Say "no thanks" to the offer | Conversation continues; no quiz. |
| Ask about a topic **not** in an enrolled course | Normal answer + course cards (Enroll / View) — **no quiz offer**. |
| Ask a question and immediately repeat an offer on the same course | Offer suppressed (recently assessed). |
| Type "hi" / non-learning | No offer, no recommendation. |
| Configure `.env` `ASSESSMENT_REQUIRE_ENROLLMENT=false` | Legacy mode: quiz offered without enrolment check (for demos). |

### Recommended `.env`
```env
ASSESSMENT_REQUIRE_ENROLLMENT=true
ASSESSMENT_RECENT_WINDOW_SECONDS=604800
ASSESSMENT_COURSE_RECOMMENDATION_COUNT=3
```

## 5. Example Conversations

### A. Enrolled learner (offers quiz → confirms)
```
User:    Explain how SIEM correlation rules work.
Assistant:  SIEM correlation rules combine multiple log events...
            [appended] Would you like to check your understanding of **SIEM Fundamentals**
            with a short quiz? I can help assess your grasp of this topic with a few
            questions. Just say yes to begin.
User:    yes
Assistant:  Great! Let's begin.
            **Question 1 of 5** ... (A) (B) (C) (D)
User:    A
Assistant:  Correct! ... **Question 2 of 5** ...
...
Assistant:  Quiz complete! You scored **4 / 5**.
            **Strengths** / **Needs Improvement** / **Learning Recommendations**
```

### B. Enrolled learner declines
```
User:    What is a SIEM?
Assistant:  A SIEM aggregates and correlates security logs...
            [appended] Would you like to check your understanding of **SIEM Fundamentals**
            with a short quiz? ...
User:    no thanks
Assistant:  (conversation continues normally, no quiz)
```

### C. Non-enrolled user (course recommendation, NO quiz)
```
User:    What is Retrieval-Augmented Generation (RAG)?
Assistant:  RAG combines a retriever with an LLM to ground answers in documents...
            [appended] I won't quiz you on this just yet — since you're not currently
            enrolled in a course covering this topic, I'd suggest learning it in a
            structured way first. If you'd like, here are some courses you can explore:
            [Available Courses: RAG & Vector Databases  (Enroll / Go to course)]
            (you can also say "maybe later" to skip them).
```

### D. Recently assessed course (repeat offer suppressed)
```
User:    Quiz me on SIEM correlation rules.
Assistant:  (normal explanation)   — quiz offer is suppressed because a SIEM
            assessment was completed recently (within the configured window).
```

