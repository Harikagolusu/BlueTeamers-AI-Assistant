# Wazuh-Backed Practice Labs — Design & Discussion Log

**Date:** 2026-07-16
**Status:** Design approved by user; several items flagged open for team discussion before implementation planning.

## 1. Problem Statement

The `/labs` "Practice" tab (`src/pages/Labs.tsx`, `src/pages/LabsLogs.tsx`, and the `src/components/soc/*` components) is currently a fully static React mockup: hardcoded fake alert/log data, rendered behind a permanent blurred "You don't have access to this page — please upgrade your plan or contact the administrator" overlay. It's a marketing teaser, not a working product.

The goal is to replace this with a real, working SOC practice environment backed by an actual Wazuh SIEM instance, seeded with synthetic ("fake" but realistic) log data, so students get genuine hands-on log-investigation practice — in the style of platforms like LetsDefend/blueteamers.io.

## 2. Decision Log (questions asked, options given, what was chosen, and why)

### Q1 — What should the end result feel like to a student?
- **Options offered:** (a) Embed Wazuh's own dashboard directly; (b) Build a custom UI wired to Wazuh's API; (c) Both — custom UI for guided labs, plus a link into the real dashboard for free exploration.
- **Chosen: (c) Both.**
- **Why:** Guided/scored labs need a controlled, branded UI tied into the course/quiz system. But advanced students benefit from being able to poke around the real tool once they've done the guided exercise — and it's genuinely useful to have practiced the real Wazuh UI, not just a lookalike.

### Q2 — How should the fake logs/environment be shared across students? (tenancy)
- **Options offered:** (a) One shared instance, identical data for everyone; (b) Fully isolated Wazuh stack per user/session; (c) Shared backend with per-user data tagging/filtering.
- **Initially chosen:** (b) Per-user isolated sandbox.
- **Reconsidered:** The user's own infra notes (`aws txt.txt`) show the current production box is an AWS Lightsail instance with 0.5GB RAM ($5/mo). A single working Wazuh stack (manager + indexer/OpenSearch + dashboard) needs roughly 4GB RAM minimum — so spinning up a *separate full stack per concurrent student* would be far more infrastructure than the project's current scale/budget supports.
- **Further clarified by user:** The intended experience is actually the **LetsDefend model** — every student investigates the *same* case/log data, but each student's own *progress on a case* starts fresh independently. This is not the same as per-user isolated infrastructure.
- **Final decision:** Shared Wazuh backend, shared case data. What's per-student is only their *attempt/progress* (started, answers, score), stored in the app's own database — not a full duplicated environment per user. See §3 for the resulting architecture. This also resolves the cost/scale concern from Q2's initial answer.

### Q3 — What does "solving a case" look like for the student?
- **Options offered:** (a) Browse logs + answer guided questions (quiz-style, scored); (b) Free-form investigation only, no questions/scoring; (c) Full incident-response workflow (triage, notes, severity classification, close).
- **Chosen: Open — flagged for team discussion.**
- **User's direction:** Questions should be tied into the existing course structure — something like a "Solve the Lab" step alongside lessons/quizzes, CTF-style. Exact format (MCQ vs. flag-submission vs. full workflow) still needs to be decided with the team.

### Q4 — Who is responsible for standing up the Wazuh infrastructure?
- **Options offered:** (a) User/team sets it up; (b) Someone else owns infra, this design just assumes a reachable Wazuh URL; (c) Not decided.
- **Chosen: (a).** User and team will provision the Wazuh server themselves.

### Q5 — How should fake log content (the actual scenario data) be created?
- **Options offered:** (a) Team manually hand-authors realistic logs per scenario; (b) Simulate real attacks in a disposable lab VM (with a Wazuh agent installed) and capture genuine output; (c) Script-generate synthetic logs at volume for background noise.
- **Chosen: Hybrid — all three combined.**
- **Why:** Hand-authored logs give full creative/pedagogical control over what's discoverable; captured real-attack output adds authenticity that's hard to fake by hand; generated background noise/volume prevents the malicious events from being trivially obvious (a real SOC log isn't just the 5 interesting lines).

### Q6 — Should Practice/Labs access be free or paid?
- **Options offered:** (a) Paid, tied to course/bundle purchase; (b) One free case as a teaser, rest paid; (c) Free for everyone.
- **Chosen: (a).** Matches the existing "upgrade your plan" lock already present in the current mockup — labs unlock the same way lessons/quizzes do, via course or bundle purchase.

### Q7 — Rollout scope: pilot one course, or build generically for all courses at once?
- **Options offered:** (a) Pilot on one course first, expand later; (b) Build generically, content team produces cases for multiple courses in parallel from day one; (c) Not decided.
- **Chosen initially: (a), pilot first.**
- **Follow-up — which course to pilot on:** Claude suggested "Log Analysis for Beginners" as the pilot, since its existing modules (`Detecting Brute Force Attacks`, `Detecting Lateral Movement`, `Detecting Data Exfiltration`, `Hands-On: Windows/Linux Log Investigation`, `Final Practical Challenge` — see `src/data/courses.ts`) already map directly onto lab scenarios with minimal content rework.
- **User's answer:** The long-term goal is to support labs across *all* courses — but the specific pilot course and rollout order are **not yet decided**, to be settled with the team later.
- **Final status:** Direction confirmed (phased rollout, starting small), but the specific first course and ordering is an **open item**.

## 3. Architecture

- **Infrastructure:** One shared Wazuh stack (Manager + Indexer/OpenSearch + Dashboard), deployed via Wazuh's official Docker Compose setup, on a VM sized for Wazuh's real requirements (~4GB+ RAM) — an upgrade from the current 0.5GB Lightsail production box. Exact sizing/budget is an open item for the team.
- **New backend app (Django), e.g. `labs`:**
  - `Case` — title, course/module FK, scenario brief, a tag/index identifier used to scope which ingested logs belong to this case, status (draft/published).
  - `CaseQuestion` — case FK, question text, format (TBD per §2 Q3), correct answer/flag, points.
  - `CaseAttempt` — user FK, case FK, started_at, completed_at, submitted answers, score, status (in-progress/completed). Mirrors the existing quiz-attempt pattern already used for `quizData.ts`-driven quizzes.
- **Data flow (content authoring, offline/ahead of time):**
  1. Team authors a case's log dataset using the hybrid approach from Q5.
  2. Dataset is bulk-ingested into the shared Wazuh instance, tagged with that case's identifier.
  3. This happens once per case — not per-student, not live/real-time.
- **Data flow (student-facing, per attempt):**
  1. Student reaches a "Solve the Lab" step inside a course module.
  2. Backend checks course/bundle purchase (extending the existing `useCourseAccess` hook/pattern used for lessons and quizzes).
  3. Backend creates a fresh `CaseAttempt` row for that student + case.
  4. Frontend labs UI (rewired `SOCSidebar`, `AlertSummaryCards`, `AlertsChart`, `RecentAlertsTable`, `LabsLogs`, etc. — currently hardcoded, see `src/pages/Labs.tsx` / `src/pages/LabsLogs.tsx`) queries the backend, which proxies/queries Wazuh's API scoped to that case's tag only. Students never get unrestricted query access to the full Wazuh cluster.
  5. Student investigates (search/filter/drill into logs and alerts, same interaction model as today's `LabsLogs.tsx`), then answers the case's guided questions.
  6. Backend scores the submission and updates `CaseAttempt`.
  7. "Start over" resets that student's `CaseAttempt` only — the underlying case log dataset in Wazuh is untouched and shared by everyone.
  8. Optional: an "Open in Wazuh" link/button gives the student a scoped, read-only path into Wazuh's own native dashboard UI for open-ended exploration of that same case's data, beyond the guided questions.

## 4. Workflow — From the Student's Point of View

1. Student purchases a course (or the all-courses bundle) that includes labs.
2. Inside a module, alongside its lessons and quiz, there's a new step: **"Solve the Lab: <scenario name>"** (e.g. "Detecting Brute Force Attacks").
3. Opening it shows a scenario brief — what allegedly happened, what they're being asked to find.
4. They land in the SOC-styled Practice UI (the same look as today's dashboard/log explorer, but now backed by real data) scoped to just this case's logs and alerts.
5. They search, filter, and drill into log entries and alerts to investigate — read-only, can't affect other students.
6. They answer the case's guided questions (exact format still to be decided by the team — MCQ, flag submission, or a fuller incident write-up).
7. They submit; it's scored and stored, same as an existing quiz.
8. They can hit "Start Over" to reset their own attempt and retry from scratch — the case data itself never resets or changes.
9. Optionally, they can click "Open in Wazuh" to explore the same case's data inside the real Wazuh dashboard, for open-ended practice beyond the scripted questions.

## 5. Open Items for the Team Meeting

1. **Case question/answer format** — MCQ, CTF-style flag submission, or a fuller incident-response workflow (triage/notes/severity/close)? (§2 Q3)
2. **Infra sizing and budget** — how big a box, hosted where, roughly what monthly cost, to replace/supplement the current Lightsail instance? (§2 Q2, §3)
3. **Pilot course and rollout order** — direction is "eventually all courses," but which course goes first and in what order is undecided. (§2 Q7)
4. **First case's exact content sourcing mix** — how much hand-authored vs. captured-from-real-attack vs. generated-noise content goes into the very first pilot case. (§2 Q5)

## 6. Explicitly Out of Scope (for this phase)

- Per-user isolated Wazuh environments/containers (considered in Q2, rejected on cost/complexity grounds in favor of shared backend + per-user progress tracking).
- Students being able to modify/attack a live environment themselves (this phase is investigation of pre-seeded data only, not an offensive/interactive range).
