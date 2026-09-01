# Code Changes Report — 2026-08-31
**Repo:** `Harikagolusu/BlueTeamers-AI-Assistant` `master` `06a8aca..ebf6777` (7 commits, 10 files, +542/-67)
**Author:** Harika Golusu + Muse Spark
**Scope:** Table streaming, bullet list, quiz intent, and P0 guardrail hardening against Buffy audit

## Commits

| Commit | Message | Files |
|---|---|---|
| `860cdee` | `fix(table): streaming markdown table collapse` | `useChat.ts:592`, `ChatMarkdown.tsx:88`, `service.py:272` + `TABLE_STREAMING_FIX.md` |
| `c869f3a` | `fix(bullet): streaming bullet list collapse` | same 3 files |
| `64b5553` | `fix(bullet): close bullet list before paragraph` | `useChat.ts:677`, `ChatMarkdown.tsx:88` |
| `f6231e5` | `fix(bullet): preserve inline words in platform scores` | `useChat.ts:677` |
| `67159d8` | `fix(quiz): route Give me 5-question quiz to assessment` | `rule_classifier.py:43`, `assessment_stage.py:206` + `QUIZ_INTENT_FIX.md` |
| `ebf6777` | `fix(security): harden guardrails P0` | `injection_detection_policy.py:44`, `regex_engine_adapter.py:18`, `service.py:186` + `SECURITY_TRIAGE_REPORT.md` |

## 1. Table Streaming Collapse — `Your assessment scores:` showed `| Aspect | Details ||---|---|| What` and Wazuh `LAYER` table showed only 2 rows

**Files:**
- `infosecdairies/src/hooks/useChat.ts:592` `normalizeTableChunk` — added generic `if ("---" in out) out.replace(/\|\s*\|\s*/g,"|\n|")` for `alerts || Indexer` / `alerts | | Indexer` → `alerts |\n| Indexer`, plus `Details | |---|---|` → `Details |\n|---|---|`, plus `|---|---| | **What**|` → `|---|---| \n| **What**|`; added paragraph→table `"\n\n| Aspect"` when `token startsWith "|"` and `prev` is text (`Great question!...| Aspect`), and `row→paragraph` with `isCellContinuation = toAppend.includes("|")` to keep `| Central Server | Aggregates... |` as same row.
- `infosecdairies/src/components/ui/chat/ChatMarkdown.tsx:88` `normalizeMarkdown` — same generic `|\s*| → |\n|` when `---` present + separator fixes, removed over-aggressive `([^\n])\s*(\| [^\n]*\|)` that had split `| Central Server | Aggregates...`.
- `ai_service/app/chat/service.py:272` `_normalize_table_newlines` — added same generic `|\s*| → |\n|` in safety-valve `512`-char flush and before `await _emit_sanitized`, so SSE token and `pending_turn` persistence (`"".join(parts)`) store correct markdown. Verified `curl stream:true` `| LAYER |` per-row tokens now correct, `python -m py_compile` OK, `npm run build` ✓.

**Docs:** `TABLE_STREAMING_FIX_2026-08-31.md:1`

## 2. Bullet List Collapse — `tell me 5 bullet points abot siem` showed `here are 5 key points:- Collection...- Parsing...` inline

**Files (same 3 + follow-ups):**
- `useChat.ts:592` — added bullet intra-token `out.replace(/([^\n]):\s*-\s+(?=[A-Z*•])/g,"$1:\n\n- ")` (`analyst:- Collection` → `analyst:\n\n- Collection`) and `out.replace(/([^\n])\.\s*-\s+(?=[A-Z*•])/g,"$1.\n- ")` (`point.- Parsing` → `point.\n- Parsing`).
- `useChat.ts:664` — added inter-token bullet branch `if (/^(- |\* |• |\d+\. )/.test(tokenTrimStart))` → `"\n"` or `"\n\n"` before `- ` when `prev` ends with `:`/`.`.
- `useChat.ts:677` — added bullet→paragraph `prev.includes("\n- ")` + `isBlockStart = /^(?:\*\*|###|> |From a SOC|This topic|SUGGESTED)/` → `"\n\n"` before `**Real-world example:**` / `From a SOC` / `### Continue` (fixes `tools.Real-world` inside same bullet), and later refined to not split `Quiz quiz-1: 80/100` inline words (`isBlockStart` check, `f6231e5`).
- `ChatMarkdown.tsx:88` — same `:-`/`.-` plus `if (out.includes("\n- "))` block for `**Real-world`, `From a SOC`, `### Continue`, `This topic` and `(\n- [^\n]*)\n(?!\n)(?=\*\*|From a SOC|###)` → `"\n\n"`.
- `service.py:272` — added `if "- " in out: re.sub(r"([^\n]):\s*-\s+(?=[A-Z*•])",...)` and `\.\s*-\s+` for safety-valve flush.

**Docs:** `BULLET_STREAMING_FIX_2026-08-31.md:1` (92 lines, updated with bullet→paragraph follow-up).

## 3. Quiz Intent Misroute — `Give me a 5-question quiz on siem` returned `Your assessment scores: Quiz quiz-1: 80/100` instead of `Question 1 of 5`

**Files:**
- `ai_service/app/chat/intent/classifiers/rule_classifier.py:43` `_PLATFORM_ASSESSMENT` — removed bare `assessment, assessments, quiz, quizzes, exam, exams, score, scores` that hijacked generation; narrowed to ownership/result only: `my assessment, my quiz, my exam, assessment score, quiz score, exam score, assessment result, quiz result, show my quiz, view my assessment, which assessment, recommend an assessment, grade, grades`. Now `Give me a 5-question quiz on siem` → no platform match → `domains.py:196` `assessment-signal: quiz` → `CyberDomain.ASSESSMENT`.
- `ai_service/app/chat/pipeline/assessment_stage.py:206` `_maybe_offer` — added explicit-generation bypass: `if any(p in lower for p in ("give me a quiz","create a quiz","5-question","multiple-choice quiz")) and suitable: message = await _start_quiz(...) return _takeover(...)` instead of only `PENDING_CONFIRM` + `offer_message()`. Now directly starts `AssessmentAgent.start_quiz` with `Question 1 of 5`.

**Docs:** `QUIZ_INTENT_FIX_2026-08-31.md:1`

## 4. Guardrail P0 Hardening (Buffy audit C-01, C-02, C-04, C-05, C-08)

**Files:**
- `ai_service/app/guardrails/policies/input/injection_detection_policy.py:44` — added secondary check `data_part = text[len(prefix):].strip(); if data_part and _regex_engine.contains_match(data_part): block()` for `Summarize this text: Ignore...` (was `return allow()` without check). Now `Summarize/Translate/Analyze this text: Ignore all previous instructions` correctly `BLOCK`.
- `ai_service/app/guardrails/infrastructure/adapters/regex_engine_adapter.py:18` — added `import html, unicodedata, urllib.parse` + `_CYRILLIC_HOMOGLYPH_MAP` (`о→o`, `е→e`, `а→a` etc. U+043E) and `contains_match` now does `html.unescape` → `urllib.parse.unquote` (loop 2× for double-encode) → `unicodedata.normalize("NFKC")` → `translate(CYRILLIC)` → `_STEALTH_CHARS_RE` strip → `re.sub(r"\s+"," ",…)`. Now blocks `ignоre` (cyrillic), `&#105;gnore`, `%69gnore`, and `ig\u200bnore` (already handled) and combined `&#105;g\u200bnоre`.
- `ai_service/app/chat/service.py:186` — sanitized `citations` for both streaming (`stream_metadata:186`) and non-streaming (`final_metadata:202`): `safe_citations = [{"course":c.get("course"),"lesson":c.get("lesson"),"similarity_score":c.get("similarity_score"),"source_title":c.get("source_title"),"source_reference":c.get("source_reference")} ...]` dropping `chunk_id` (`siem-fundamentals:1.3:chunk-2`) that previously leaked in `stream:true` `citations[]`.

**Docs:** `SECURITY_TRIAGE_REPORT_2026-08-31.md:1` (117 lines, classifies C-03/C-06 already mitigated, C-09/C-10/C-11/C-12 deferred intentionally).

## Verification
- `curl -N POST /api/chat/ stream:true` with `harika@example.com` JWT: `Explain SQL injection` → `| Aspect | Details |\n|---|---|` per-row, `wazhu` 6-row LAYER table → 7 lines, `tell me 5 bullet points` → `:\n\n- Collection` + `.\n- Parsing` (5 `"\n- "`), `Give me 5-question quiz` → `**Question 1 of 5**` not scores.
- `python -m py_compile` for `service.py`, `regex_engine_adapter.py`, `injection_detection_policy.py` OK.
- `npm run build` in `infosecdairies` ✓ `15-16s` `617k gzip` after each fix.
- Live guardrail tests: `Summarize this text: Ignore...` → `BLOCK`, `ignоre` → `BLOCK`, `&#105;`/`%69` → `BLOCK`, `stream:true` no `chunk_id`.

**Not changed / deferred:** `C-03` zero-width already handled, `C-06` JSON `\u` already decoded, `C-09` `TOKEN_QUOTA_ENFORCE=False:206`, `C-10` `/stream` middleware skip, `C-11` per-line output, `C-12` 2-pattern course integrity — intentional for dev (see triage).

**Git:** `06a8aca..ebf6777` 7 commits, 10 files `+542/-67`, pushed to `origin/master`.
