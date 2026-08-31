# Quiz Intent Fix — 2026-08-31

**Issue:** `Give me a 5-question quiz on siem` (and `Give me a 5-question multiple-choice quiz on Network Security Monitoring`) returned `Your assessment scores: Quiz quiz-1: 80/100 (passed) Quiz quiz-2: 60/100 (not passed) SUGGESTED: SIEM Fundamentals` as in screenshot `Give me a 5-question quiz on siem` `Harika Demo User`. Expected: generate a new 5-question quiz on the topic, not show past scores. Same for `Network Security Monitoring` variant previously.

**Root Cause:**
- `ai_service/app/chat/intent/classifiers/rule_classifier.py:43` `_PLATFORM_ASSESSMENT` contained bare `assessment, assessments, quiz, quizzes, exam, exams, grade, grades, score, scores` and was first-match winner. Any query containing `quiz` (even `Give me a 5-question quiz on siem`) was classified `IntentType.PLATFORM_ASSESSMENT` → `app/chat/routing/domains.py:124` `PLATFORM_ASSESSMENT → CyberDomain.PLATFORM` (not overridden because `PLATFORM_ASSESSMENT` not in `_AMBIGUOUS_INTENTS`) → `app/chat/routing/agents.py:82` `platform_assistant` → `app/chat/engines/platform_engine.py:637` deterministic `Your assessment scores: ...` via `get_assessments` (view past results, not generation). Generation should route to `CyberDomain.ASSESSMENT` (`assessment_coach` / `AssessmentAgent`) via `domains.py:196` `assessment-signal: quiz`.

**Files Changed (2 files):**

### 1. `ai_service/app/chat/intent/classifiers/rule_classifier.py:43`
- Narrowed `_PLATFORM_ASSESSMENT` to ownership/result context only:
  ```py
  _PLATFORM_ASSESSMENT = [
      "my assessment", "my assessments", "my quiz", "my quizzes",
      "my exam", "my exams", "my grade", "my grades", "my score", "my scores",
      "assessment score", "assessment scores", "quiz score", "quiz scores",
      "exam score", "exam scores", "assessment result", "assessment results",
      "quiz result", "quiz results", "exam result", "exam results",
      "show my assessment", "show my quiz", "view my assessment", "view my quiz",
      "which assessment", "recommend an assessment",
      "grade", "grades",
  ]
  ```
- Removed bare `quiz, quizzes, assessment, assessments, exam, exams, score, scores` that hijacked generation. Now `Give me a 5-question quiz on siem` → no platform match → falls through to `RAG_CHAT`/`ASSESSMENT` via `domains.py:196` `quiz` signal → `ASSESSMENT` domain.
- `What are my quiz scores?` / `Show my quiz results` / `my assessment scores` still match `my quiz` / `quiz scores` → correctly stays `PLATFORM_ASSESSMENT`.

### 2. `ai_service/app/chat/pipeline/assessment_stage.py:206`
- In `_maybe_offer`, added explicit-generation bypass before creating `PENDING_CONFIRM`:
  ```py
  _is_explicit_generation = any(p in query.lower() for p in (
      "give me a quiz", "give me quiz", "create a quiz", "generate a quiz",
      "5-question", "5 question", "multiple-choice quiz", "quiz me on", "test me on"))
  if _is_explicit_generation and assessment.suitable:
      topic = assessment.topic or "cybersecurity"
      message = await self._start_quiz(context, session_key, topic, query)
      if message:
          meta = {"mode":"started","session":session_key,"quiz":self._current_quiz_payload(session_key),"topic":topic}
          return self._takeover(result, message, meta), meta
  ```
- Previously `_maybe_offer` only created `PENDING_CONFIRM` and returned `offer_message()` (`Would you like to test your understanding?`), so even after routing fix the user would get an offer not the quiz. Now explicit `Give me a 5-question quiz` starts immediately via `AssessmentAgent.start_quiz` (uses `LLM` to generate 5 questions, respects `count=5`), matching user expectation `Don't show answers until I respond`.

**Verification:**
- `curl` with `Authorization: Bearer harika@example.com`:
  - `Give me a 5-question quiz on siem` → before: `Your assessment scores: Quiz quiz-1: 80/100...`; after: `**Question 1 of 5** ...` via `assessment_coach`.
  - `Network Security Monitoring` variant similarly now `Question 1 of 5` not scores.
  - `What are my quiz scores?` still `Your assessment scores: ...` (platform).
  - `python -m py_compile rule_classifier.py` OK, `assessment_stage.py` OK.

**User Action:** Pull `origin/master` and restart `ai_service` (port `8001`) to load `rule_classifier.py:43` and `assessment_stage.py:206`.

**Commits:** Part of `QUIZ_INTENT_FIX_2026-08-31.md` (this file). Code already in working tree, now pushed.
