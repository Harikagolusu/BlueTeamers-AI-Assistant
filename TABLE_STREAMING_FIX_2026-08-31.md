# Table Streaming Fix — 2026-08-31

**Issue:** Markdown tables rendered only partially while streaming (e.g., `wazhu in table format` showed `Agent-based Collection` + `Central Server (Manager)` then raw `| Aggregates... || Indexer...` below table as in screenshot `BlueTeamers AI Workspace` `Harika Demo User`). Clicking sidebar `History` (`GET /api/conversations/{id}`) loaded the same answer correctly, but live stream was broken. Also `Explain SQL injection in table format` showed `| Aspect | Details ||---|---|| What it is |` collapsed.

**Root Cause:**
- `ai_service/app/chat/service.py:272` streams per-line via `buffer` + `"\n"` split, but safety-valve flush at `512` chars emitted a single SSE token containing `alerts || Indexer & Dashboard` (two data rows collapsed as `||` / `| |` with no `\n`). Frontend `infosecdairies/src/hooks/useChat.ts:586` only fixed `|`+`|` when `---` was involved (`\|\s*\|\s*(?=-)`), so `alerts || Indexer` (data-row → data-row) stayed collapsed.
- Intro paragraph → table header arrived as separate tokens `"Great question! ...you asked for."` + `"| Aspect | Details |"` with no blank line, so `remarkGfm` in `ChatMarkdown.tsx:88` did not recognize the table until it was reloaded from DB (history).
- `| Central Server (Manager) |` + ` Aggregates... | Runs... |` split across tokens: previous fix treated `prevEndsPipe && !nextStartsPipe` as `row→paragraph` and inserted `\n\n`, breaking the row into `| Central Server (Manager) |` alone (as seen in image).

**Files Changed (3 files, table fix only):**

### 1. `infosecdairies/src/hooks/useChat.ts:592`
- Added `normalizeTableChunk(s)`:
  ```ts
  if (out.includes("---") || out.includes("||") || out.includes("| |"))
    out = out.replace(/\|\s*\|\s*/g, "|\n|"); // "alerts || Indexer" → "alerts |\n| Indexer"
  // + existing separator fixes
  out.replace(/([^\n])\s+(\|\s*:?-{3,}:?...\|)/g, ...) // "Details | |---|---|" → "Details |\n|---|---|"
  out.replace(/(\|[-:\s|]+\|)\s+(\|)/g, ...) // "|---|---| | **What** |" → "|---|---| \n| **What** |"
  ```
- Paragraph → table header handling:
  ```ts
  if (nextStartsPipe && !(prevEndsPipe||prevEndsSep)) {
    // "you asked for." + "| Aspect |" → "\n\n| Aspect |"
    if (!prev.endsWith("\n")) toAppend = "\n\n" + toAppend.trimStart();
  }
  ```
- Row → paragraph vs. cell continuation:
  ```ts
  else if (prevEndsPipe && toAppend.trim().length>0) {
    const isCellContinuation = toAppend.includes("|"); // " Aggregates... |" → same row, no newline
    if (!isCellContinuation) toAppend = "\n\n" + toAppend.trimStart(); // "**Real-world..." → blank line to close table
  }
  ```
- Final safety: `if (combined.includes("||")||combined.includes("|---|")) combined = normalizeTableChunk(combined).replace(/\n{3,}/g,"\n\n")` else `combined = prev+toAppend`.

### 2. `infosecdairies/src/components/ui/chat/ChatMarkdown.tsx:88`
- Simplified `normalizeTableMarkdown(s)`:
  ```ts
  if (out.includes("---")) out = out.replace(/\|\s*\|\s*/g, "|\n|");
  else if (out.includes("||")) out = out.replace(/\|\s*\|\s*(?=-)/g, "|\n|");
  // + existing separator fixes
  out.replace(/([^\n])\s+(\|\s*:?-{3,}:?...\|)/g, ...) 
  out.replace(/(\|[-:\s|]+\|)\s+(\|)/g, ...)
  out.replace(/\n{3,}/g,"\n\n")
  ```
- Removed over-aggressive `([^\n])\s*(\| [^\n]*\|)` paragraph→table that had split `| Central Server | Aggregates...` incorrectly. History already has `\n\n` before table; streaming is fixed in `useChat`, so `ChatMarkdown` stays as idempotent defense.

### 3. `ai_service/app/chat/service.py:272`
- Added `_normalize_table_newlines(text)` inside `_stream_response`:
  ```py
  if "---" in out and "||" in out: out = re.sub(r"\|\s*\|\s*", "|\n|", out) # "alerts || Indexer"
  # + separator fixes
  re.sub(r"([^\n])\s+(\|\s*:?-{3,}:?...\|)", ...) # "Details | |---|---|"
  re.sub(r"(\|[-:\s|]+\|)\s+(\|)", ...) # "|---|---| | What"
  ```
- Called before `await _emit_sanitized(line+"\n")` and before safety-valve flush. If `_normalize` introduces `\n`, buffer is re-split line-by-line to emit proper SSE `data: {"token":"| LAYER...|\n"}` etc., so both streaming and `pending_turn` persistence (`"".join(parts)`) store correct markdown.

**Verification:**
- `curl -N POST http://localhost:8001/api/chat/ stream:true` with `client_id` and with `Authorization: Bearer harika@example.com`:
  - `Explain SQL injection in table format` → `| Aspect | Details |` `\n` `|---|---|` `\n` `| **What it is** | ... |` per-row tokens, now `Great question!...\n\n| Aspect` via frontend.
  - `wazhu in table format` (general) → `| Aspect | Detail |` 2-col per-row correct.
  - `Explain Wazuh architecture layers | LAYER | FUNCTION | KEY DETAIL |` (Wazuh lab) → `| LAYER | FUNCTION | KEY DETAIL |\n|---|---|---|\n| Agent | ... |\n| Manager | ... |\n| Dashboard | ... |` per-row.
- Simulated 6-row Wazuh `| Agent-based Collection | ... || Indexer & Dashboard | ... || FIM | ...` → after `normalize` → 7 lines `| LAYER|\n|---|`...`\n| Indexer...` correctly.
- Simulated cell continuation `| Central Server (Manager) |` + ` Aggregates... | Runs... |` → no `\n\n` (stays same row); `| ... |` + `**Real-world...` → `\n\n**Real...` to close table.
- `npm run build` `✓ 13.59s` `index-*.js` `617k gzip`, `python -m py_compile ai_service/app/chat/service.py` OK.

**User Action:** Hard refresh `Ctrl+Shift+R` ×2 on `https://192.168.1.17:3001/chat` and `http://192.168.1.6:5173` to load new `useChat.js` / `ChatMarkdown.js`. No DB migration.

**Commits:** This fix is 3 files; repo also contains separate `rule_classifier.py` + `assessment_stage.py` quiz intent fix (not described here) in same working tree.
