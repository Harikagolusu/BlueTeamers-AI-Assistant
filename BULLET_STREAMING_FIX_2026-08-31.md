# Bullet List Streaming Fix — 2026-08-31

**Issue:** Bullet points rendered inline instead of as list (screenshot `tell me 5 bullet points abot siem` `Harika Demo User`). Response showed:
`From your course material: here are 5 key points about SIEM for a SOC analyst:- Collection & Ingestion – Pulls logs ...- Parsing & Normalization – Standardizes...- Correlation & Rules – Links...- Alerting & Dashboards – ...- Investigation Pivot – ...Real-world example: ...` all on one line with `- ` without newlines, so `remarkGfm` in `ChatMarkdown.tsx` did not parse as `<ul><li>`.

**Root Cause:**
- Same as table collapse: streaming via `ai_service/app/chat/service.py:272` `_stream_response` emits per-line SSE tokens `data: {"token":"- **Collection..."}` etc., but frontend `infosecdairies/src/hooks/useChat.ts:610` concatenated `prev="here are 5 key points about SIEM for a SOC analyst:"` + `token="- **Collection..."` as `points:- Collection` without `\n`, and intra-token collapsed `entry point.- Parsing & Normalization` as `point.- Parsing` inside a single 512-char safety-valve flush (`".- "`).
- Markdown lists require `"\n- "` at line start (and `"\n\n- "` after paragraph ending with `:`). Without it, `:- ` and `.- ` stayed inline and history (`GET /api/conversations/{id}` via `parts` join) was correct only when backend had `\n`, but live stream was not.

**Reproduction:**
- `curl -s -N POST http://localhost:8001/api/chat/ stream:true` `{"query":"tell me 5 bullet points abot siem"}` with `Authorization: Bearer harika@example.com`:
  ```
  data: {"token":"From your course material, here are 5 key points about **SIEM**:"}
  data: {"token":"- **Aggregates everything** – Collects logs..."}
  data: {"token":"- **Normalizes data** – Parses raw..."}
  ...
  ```
  Frontend `lastMsg.content += token` produced `SIEM:- **Aggregates...` and `entry point.- Parsing` without newline → inline.

**Files Changed (3 files):**

### 1. `infosecdairies/src/hooks/useChat.ts:592`
- Extended `normalizeTableChunk(s)` (now handles `|` and `- `):
  ```ts
  if (out.includes("- ")) {
    out = out.replace(/([^\n]):\s*-\s+(?=[A-Z*•])/g, "$1:\n\n- "); // "analyst:- Collection" → "analyst:\n\n- Collection"
    out = out.replace(/([^\n])\.\s*-\s+(?=[A-Z*•])/g, "$1.\n- "); // "entry point.- Parsing" → "entry point.\n- Parsing"
  }
  ```
- Added inter-token bullet branch after table handling:
  ```ts
  else if (/^(- |\* |• |\d+\. )/.test(tokenTrimStart)) {
    if (!prev.endsWith("\n")) {
      if (prevTrimEnd.endsWith(":") ) toAppend = "\n\n" + tokenTrimStart; // "points:" → blank line before first bullet
      else toAppend = "\n" + tokenTrimStart; // "entry point." → "\n- Parsing"
    }
  }
  else if (prev.includes("\n- ") && toAppend.trim().length>0 && !toAppend.includes("|")) {
    // bullet list -> paragraph after list: last bullet "tools." + "**Real-world example:**" / "### Continue" / "From a SOC"
    // Without blank line, paragraph is swallowed into last bullet (image: "tools.Real-world example:")
    const nextIsListContinuation = /^(- |\* |• |\d+\. )/.test(tokenTrimStart) || tokenTrimStart.startsWith("|");
    if (!nextIsListContinuation) {
      if (!prev.endsWith("\n")) toAppend = "\n\n" + toAppend.trimStart();
      else if (!prev.endsWith("\n\n")) toAppend = "\n" + toAppend.trimStart();
    }
  }
  ```
- Table `prevEndsPipe && !nextStartsPipe` now checks `isCellContinuation = toAppend.includes("|")` to avoid breaking `| Central Server |` + ` Aggregates... |` same-row cells (keeps same row, only `**Real-world...` without `|` gets `\n\n`).

### 2. `infosecdairies/src/components/ui/chat/ChatMarkdown.tsx:88`
- Renamed `normalizeTableMarkdown` → `normalizeMarkdown` and added bullet defense for persisted/history:
  ```ts
  if (out.includes("- ")) {
    out = out.replace(/([^\n]):\s*-\s+(?=[A-Z*•])/g, "$1:\n\n- ");
    out = out.replace(/([^\n])\.\s*-\s+(?=[A-Z*•])/g, "$1.\n- ");
    if (out.includes("\n- ") || out.match(/(^|\n)\s*-\s+\*\*/))
      out = out.replace(/([^\n\u2013])\s+-\s+(?=\*\*|[A-Z])/g, ...);
    out = out.replace(/([^\n:])\n(- \*\*[^\n]*)/g, "$1\n\n$2");
    // Bullet list -> paragraph after list: last bullet "tools." + "**Real-world example:" / "From a SOC" / "### Continue"
    if (out.includes("\n- ")) {
      out = out.replace(/([^\n])\s*(\*\*Real-world example:)/g, "$1\n\n$2");
      out = out.replace(/([^\n])\s*(From a SOC analyst's perspective:)/g, "$1\n\n$2");
      out = out.replace(/([^\n])\s*(### Continue Learning)/g, "$1\n\n$2");
      out = out.replace(/([^\n])\s*(This topic is covered in:)/g, "$1\n\n$2");
      out = out.replace(/(\n- [^\n]*)\n(?!\n)(?=\*\*|From a SOC|###|This topic|> \*\*)/g, "$1\n\n");
      out = out.replace(/([a-z0-9\.])\s*(\*\*Real-world)/g, "$1\n\n$2");
    }
  }
  out = out.replace(/\n{3,}/g, "\n\n");
  ```
- Table part unchanged (generic `|\s*|\s*` when `---` present).

### 3. `ai_service/app/chat/service.py:272`
- Renamed `_normalize_table_newlines` doc to include bullets and added:
  ```py
  if "- " in out:
      out = re.sub(r"([^\n]):\s*-\s+(?=[A-Z*•])", r"\1:\n\n- ", out)
      out = re.sub(r"([^\n])\.\s*-\s+(?=[A-Z*•])", r"\1.\n- ", out)
  ```
  Called before `await _emit_sanitized` and safety-valve flush, so both streaming SSE and `pending_turn` persistence (`"".join(parts)`) store correct `:\n\n- ` / `.\n- `.

**Verification:**
- Simulated inter-token: `["here are 5 key points:", "- **Collection...","- **Parsing..."]` → `points:\n\n- Collection\n- Parsing\n- Correlation` (has `"\n\n- **Collection"` and `"\n- **Parsing"`).
- Simulated intra-token: `"here are 5 key points:- Collection ... point.- Parsing ..."` → `points:\n\n- Collection ... point.\n- Parsing ...` (5 `"\n- "`).
- `curl` same query now streams per-bullet tokens already correct, plus intra-token collapsed case fixed.
- `npm run build` `✓ 15.98s` `index-*.js` `617k gzip`, `python -m py_compile ai_service/app/chat/service.py` OK.

**User Action:** Hard refresh `Ctrl+Shift+R` ×2 on `https://192.168.1.17:3001/chat` and `http://192.168.1.6:5173` to load new `useChat.js` / `ChatMarkdown.js`. No DB migration.

**Follow-up (2026-08-31 later):** Everything coming in bullets (`Investigation Pivot – ...tools.Real-world example:` inside same bullet). Added bullet->paragraph blank line: `prev.includes("\n- ")` + next is `**Real-world` / `From a SOC` / `### Continue` → `"\n\n"` in `useChat.ts:677` and `ChatMarkdown.tsx:88` plus `service.py` defense. Ensures last bullet `Investigation Pivot – ...tools.` + `**Real-world example:**` closes list instead of swallowing paragraph.

**Commits:** `c869f3a` `fix(bullet): streaming bullet list collapse` (3 files) + `1113046` docs: bullet report (this file) + follow-up fix pending push (same 3 files + this MD update).
