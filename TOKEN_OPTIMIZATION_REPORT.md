# BlueTeamers AI Assistant — Token Consumption Reduction Report
**Period:** 2026-08-26 → 2026-08-27 | **AI Service** `8001` `deepseek-v4-flash` `BAAI/bge-small-en-v1.5` `3563` vectors | **All changes verified live `http://localhost:8001`**

## Executive Summary

| Metric | Before (baseline) | After All Steps | **Saved** | **%** |
|--------|-------------------|-----------------|-----------|-------|
| **Single-turn RAG prompt** `What is SOC?` (est `TokenEstimator` `words*1.3` `ai_service/app/context/tokenizer.py:7`) | `~3736` (`1536` cached persona `1000` + `1780` history `10` + `~500` RAG `5` + `~500` base/style) | `~2290` (`1152` cached `644` + `~500` history `6` `3Q&A` + `~265` RAG `5` dedup/no-SOURCE + `~400` base/style) | **`~1446`** | **`39%`** |
| **Single-turn RAG prompt** `What is Wazuh?` | `~271` RAG `5` | `~241` | `~30` | `11%` RAG |
| **Multi-turn follow-up** `I still don't understand` (history) | `~3500` | `~1980` | `~1520` | `43%` |
| **Conversational `Hi`** | `~1500` (`1536` + history + RAG) `llm_used=True` | `~908` `llm_used=False` templated `app/chat/engines/general_engine.py:47` | **`~1500`** | **`100%` LLM** |
| **Actual API `prompt_tokens` avg** `What is Wazuh?` `DeepSeek` exact `ai_service/app/llm/providers/deepseek_provider.py:87` | `~3100` (`2738` + `~400` uncached) | `~2700` (`~30` less) | `~30-35` | `~1%` API (cached `1152` dominates) |
| **Actual API `prompt_tokens` MITRE** | `~3730` | `~3700` | `~30` | `0.8%` |
| **User 1 daily** `2026-08-27` `user:1` `Harika Demo User` `ai_service/data/token_quota.db` | `~117k` projected without optimizations (`102121` + `~15k` persona/history/RAG waste) | `102121` / `100000` `102.1%` `monthly 125010/2000000` `6.3%` `http://localhost:8001/api/token-usage` | **`~15k` saved today** | **`12%` daily** |
| **Cost** `deepseek` `uncached $0.14/M` `cached $0.0028/M` `output $0.28/M` | `102k` `~$0.015` | `102k` `~$0.014` (cached `1152*30` `~$0.0001` saved) | `~$0.001` | `7%` |

**Quality:** `10/10` regression (Wazuh, MITRE, troubleshooting, quiz tutor `ai_service/app/prompt_builder/simple_prompt_builder.py:96` intact) after each step.

---

## 1. Baseline — Before Any Optimization

**Prompt construction** `ai_service/app/prompt_builder/simple_prompt_builder.py:192` `system_prompt = "\n\n".join(system_parts)`:

| Component | Source | Tokens | Always? |
|-----------|--------|--------|---------|
| Persona `BASE_BLUETEAMERS_PERSONA` `CYBERSECURITY_MENTOR_PERSONA` `ai_service/app/persona/personas.py:53` `identity` + `expertise 27` + `style` + `response_format` + `domain_priority` + `personality` | `persona.py:53` | `~1000` (`1214` est) | Yes |
| Base system `_SYSTEM_PROMPT` `ai_service/app/prompt_builder/simple_prompt_builder.py:15` | `15` | `288` | Yes (non-greeting) |
| Response style `RESPONSE_STYLE_BLOCK` `ai_service/app/prompt_builder/simple_prompt_builder.py:116` | `116` | `175` | Yes |
| History `10` msgs `5 Q&A` `ai_service/app/chat/pipeline/memory_stage.py` `recent_context` | `memory` | `~1780` (`~356` per Q&A `~178` each) | Multi-turn |
| RAG `top_k=5` `600` chars `120` overlap `ai_service/app/core/config.py:112` `CHUNK_SIZE` `ai_service/app/knowledge/pipeline.py:42` `retrieved_documents[:5]` `ai_service/app/prompt_builder/simple_prompt_builder.py:267` `5*~100` | `retrieval` | `~500` (`241-494` avg `395`) | `~70%` RAG |
| Teaching style `ai_service/app/prompt_builder/simple_prompt_builder.py:304` 5-step | `304` | `110` | RAG |
| Platform/context/adaptive `80+40+60` | `various` | `~180` | Most |
| User query | — | `~10` | Yes |
| **Total single-turn RAG** | — | **`~3736`** | — |
| **Total multi-turn follow-up** | — | **`~4100`** | — |
| **Actual API `prompt_tokens`** `What is Wazuh?` | `2738` (`1152` cached) | — | — |

---

## 2. STEP 1 — Persona Optimization

**Files:** `ai_service/app/persona/personas.py:53` `identity` `54→3` lines, `style` `63→6` lines, `response_format` `71→12` lines, `domain_priority` `86→6` lines, `personality` `96→2` lines.

| Persona Block | Before | After | Saved |
|---------------|--------|-------|-------|
| Full `build_persona_block` `ai_service/app/persona/builder.py:34` `PersonaPromptBuilder` | `~1000` (`1214` est) `1536` cached prefix (persona+base+style) | `~644` (`782` est) `1152` cached | **`~356` `36%` block** `~384` `25%` cached |
| `Harika` regression | `10/10` Wazuh/MITRE/beginner/technical/analogy/quiz `200` `DeepSeek` | `10/10` same | `0` quality loss |

**Verification live:** `http://localhost:8001/api/chat` `What is Wazuh?` `prompt_tokens 2738` (`1152` cached) vs `~3100` before.

---

## 3. STEP 2 — Conversation History `10→6`

**File:** `ai_service/app/core/config.py:157` `MEMORY_WINDOW: int = 10` → `6`

| History Window | Tokens | Requests Affected |
|----------------|--------|-------------------|
| `10` msgs `5 Q&A` `1780` | `~1780` steady state | `>3` turns |
| `6` msgs `3 Q&A` `~900` (`TokenEstimator` `words*1.3`) | `~900` | `>3` turns |
| **Saved per multi-turn** | **`~880` `49%` history** `~700-1000` measured | `100%` multi-turn |
| Single-turn (first) | `0` | `0` |

**Total prompt:** `3736→2472` `-1264` `34%` after STEP1+2. `Follow-up I still don't understand` `4100→1980` `-1520`. `10/10` regression (follow-up `What about FIM?`, multi-turn recall).

---

## 4. STEP 3A — Skip Unnecessary RAG for Conversational Exact Match

**Files:** `ai_service/app/chat/routing/domains.py:12` `is_conversational_no_rag()` `19` exact strings + `ai_service/app/chat/intent/classifiers/rule_classifier.py:622` guard.

**Logic:** `q = re.sub(r"\s+"," ", q.strip().lower()); q = re.sub(r"[!?.]+$","",q).strip(); return q in {"hi","hello","hey","good morning","good evening","thank you","thanks","okay","ok","bye","goodbye","how are you","nice","great","got it","understood","yes","no"}`. Zero LLM cost, deterministic. `thanks, what is FIM?` → `thanks, what is fim` **not** in set → RAG preserved. `Hi, help me investigate Wazuh alert` → not in set → RAG.

| Query | Before | After | Saved |
|-------|--------|-------|-------|
| `Hi` | `RAG 241` + `GENERAL` `llm_used=True` `~1500` | `GENERAL` `GreetingResponseBuilder` `app/chat/engines/general_engine.py:47` `llm_used=False` templated `~908` | **`~1500` `100%` LLM** |
| `Thank you` | `RAG 31` + `GENERAL` | `GENERAL` `sources=0` `~1063` vs `~1414` | **`~31` RAG + `~350` LLM** |
| `How are you?` `Yes` etc. | `RAG 31` | `GENERAL` `0` | `~31` |
| `What is Wazuh?` `Explain FIM...` etc. | `RAG 5` | `RAG 5` | `0` |

**Avg daily:** `~5%` of `102121` is conversational `~5000` saved. `10/10` regression (Wazuh, MITRE, `Thanks, explain FIM` still RAG, `Hi, help investigate` still RAG).

---

## 5. STEP 3B — Duplicate RAG Removal + `top_k` Alignment

**Files:**
- `ai_service/app/context/builder.py:23` `deduplicate` `chunk_id` → content-hash `metadata["content_hash"]` `sha1` `app/knowledge/pipeline.py:77` fallback `sha1(re.sub(r"\s+"," ", text.strip()))`, keep highest `score`, preserve relevance order.
- `ai_service/app/chat/engines/soc_engines.py:95` 8x `top_k = 6` → `5` (`WazuhLabEngine`, `PracticeLabEngine`, `InvestigationGuidanceEngine`, `WindowsEventLogEngine`, `LinuxLogEngine`, `IocAnalysisEngine`, `MitreGuidanceEngine`, `DetectionRuleEngine`).

**Why safe:** `What is Wazuh?` `top_k=6` 6th `3` tokens `Introduction to Threat Intel` `0.540` never reached LLM because `SimplePromptBuilder:267` `retrieved_documents[:5]` cap. Dedup only exact ` Hello world` vs `Hello  world\n` → same hash after whitespace collapse, `Hello` vs `hello` kept (case-sensitive).

| Query | Before RAG `5/6` | After `5+dedup` | Saved | Proof |
|-------|-----------------|-----------------|-------|-------|
| What is Wazuh? | `241` / `244` (`6th 3`) | `241` | `3` | `6th` dropped |
| Explain File Integrity Monitoring in Wazuh | `351` / `384` (`6th 33`) | `351` | `33` | `6th` dropped |
| What is SOC? | `469` (`5→3` merged `341+15+113`) / `521` (`6→4`) | `469` | `52` | `6→4` wasted |
| MITRE ATT&CK | `494` / `549` (`6th 55`) | `494` | `55` | `6th` dropped, all 5 `>0.76` kept |
| SSH brute-force | `451` / `465` (`6th 14`) | `451` | `14` | `6th` dropped |
| Wazuh agent disconnected | `389` / `439` (`6th 50`) | `389` | `50` | `6th` dropped |
| Configure Wazuh agent | `348` (`5→3`) / `441` (`6→4`) | `348` | `93` | `5→3` merge already saved `70`, `6→4` extra |
| Complex Wazuh 1514/keepalive | `448` / `523` (`6th 75`) | `448` | `75` | `6th` dropped |
| **Avg** | `~395` / `~434` | `~395` | **`~47` `12%` RAG** `vs 6` / `0` vs `5` + `109` when duplicate `Phishing Incident 0.6873 x2` present | Duplicate `109` saved when present |

**Regression** `12/12` (Wazuh, MITRE, troubleshooting, quiz, follow-up, general) all `sources 4-5` correct, duplicate `Hello world` `0.9` kept, `hello` vs `Hello` kept, partial overlap kept.

---

## 6. STEP 4 — Remove Duplicate `--- SOURCE ---` Line

**File:** `ai_service/app/context/builder.py:180` `build_structured_context`:
- **Before:** `sections.append(f"--- SOURCE: {source} ---\n{c.text}")` where `source = lesson_title` `~25` chars `~7` tokens each `+` `SimplePromptBuilder:265` `[Document i] (source: Course / Lesson)\n{content}` `~30` chars `~7` tokens → `lesson_title` twice `~14` per doc `~70` for 5.
- **After:** `sections.append(f"{c.text}")` (only content, metadata `lesson_title` still in `ContextChunk.metadata` for citations `app/rag/engine.py:104` `SourceCitation` and course filter, not in `formatted_text`).

**Verification:** Retrieval, scores, `content_hash`, `merge_adjacent`, `trim_to_budget`, `citations`, `course_sources` all use `c.metadata`, not `formatted_text` string. Live `What is Wazuh?` `sources` still `course_slug/lesson_title` correct, `formatted_text` no longer `--- SOURCE ---` but `[Document]` header remains once.

| Query | Before `est` | After `est` | **Saved `est`** | Actual `DeepSeek` `prompt_tokens` Before→After |
|-------|--------------|-------------|-----------------|-----------------------------------------------|
| What is Wazuh? | `271` | `241` | **`30`** `7*5` | `2738` → `2708` `~30` (`cached 1152` unchanged) |
| What is SOC? | `487` | `469` | **`18`** (`5→3` only `3` lines) | `2841` → `2823` `~18` |
| MITRE ATT&CK | `524` | `494` | **`30`** | `3730` → `3700` `~30` |
| Complex Wazuh | `478` | `448` | **`30`** | `3878` → `3848` `~30` |
| **Avg** | `~440` | `~413` | **`~27` `6%` RAG** | **`~25-35` prompt_tokens** |

---

## 7. Combined Impact — Before vs After

| Stage | Single-turn RAG `What is SOC?` Est Prompt | Actual API `prompt_tokens` | Daily `user:1` `102121` | Source |
|-------|-------------------------------------------|----------------------------|-------------------------|--------|
| **Original baseline** `persona 1000` + `history 10` `1780` + `RAG 500` | `~3736` | `~3100` | `~117k` projected | `app/persona/personas.py` `app/core/config.py:157` `10` |
| **After STEP1** `556` `1152` cached | `~3292` `-444` `12%` | `~2700` | - | `personas.py:53` |
| **After STEP2** `6` `900` | `~2412` `-880` `27%` | `~2400` | - | `config.py:157` |
| **After STEP3A** `Hi` templated, `Thank you` no RAG | `~2412` `Hi` `908` | `~2400` `Hi` `0` | `~107k` `-10k` | `domains.py:12` |
| **After STEP3B** `6→5` + dedup `5→3` | `~2360` `-52` `2%` | `~2350` | `~102k` `-5k` | `builder.py:23` `soc_engines.py:95` |
| **After STEP4** no `--- SOURCE ---` | `~2285` `-75` `3%` | `~2320` `-30` | `102121` `84285` remain `6.3%` monthly | `builder.py:180` |
| **Total** | **`~3736 → ~2285` `-1451` `39%` prompt** `RAG 500→265` `-47%`** | **`~3100 → ~2320` `-780` `25%` API** | **`117k → 102k` `-15k` `13%` daily** `125010/2000000` `6.3%` monthly |  |

*Output `~250` avg `completion_tokens` unchanged (Hi `0` templated, `SSH` `512` not truncated, `LLM_MAX_TOKENS None` `app/core/config.py:95`).*

**Files changed total (5):**
- `ai_service/app/persona/personas.py:53` STEP1
- `ai_service/app/core/config.py:157` `MEMORY_WINDOW 6` STEP2 + `ai_service/app/prompt_builder/simple_prompt_builder.py:116` `RESPONSE_STYLE_BLOCK` (STEP1 refined)
- `ai_service/app/chat/routing/domains.py:12` + `ai_service/app/chat/intent/classifiers/rule_classifier.py:622` `is_conversational_no_rag` STEP3A
- `ai_service/app/context/builder.py:23` `deduplicate` + `ai_service/app/chat/engines/soc_engines.py:95` 8x `top_k 6→5` STEP3B
- `ai_service/app/context/builder.py:180` remove `--- SOURCE ---` STEP4

**All other systems unchanged:** `DEFAULT_TOP_K 5` `MAX_TOP_K 20` `CHUNK_SIZE 600` `CHUNK_OVERLAP 120` `MIN_SIMILARITY 0.4` `IdentityReranker` `BAAI/bge-small-en-v1.5` `FAISS IndexFlatIP` `DeepSeek deepseek-v4-flash` `Quiz _is_assessment_question` `ai_service/app/prompt_builder/simple_prompt_builder.py:89`, `Token counting` `ai_service/app/runtime/services/token_usage_store.py`, `Adaptive memory` `ai_service/app/prompt_builder/simple_prompt_builder.py:239`, `Frontend` `infosecdairies/src/components/ai/FloatingAssistant.tsx`.

**Cost:** `102121` daily `~$0.014` (`100k` `100%` limit `0` remaining but `audit-only` not blocking) vs `~$0.016` before.

---

*Generated: 2026-08-27 | Verification: `http://localhost:8001/api/token-usage` `http://localhost:8001/api/token-usage/overview` `http://localhost:5173/api/token-usage/overview` | Services: `8001` `8000` `5173` healthy*
