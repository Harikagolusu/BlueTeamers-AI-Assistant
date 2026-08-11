# Sprint 7 Completion Report: Multilingual AI Experience

All Sprint 7 features are implemented, tested, and verified. The AI assistant
now auto-detects the learner's language, honors an explicit language preference
persisted across conversations, responds in 13 Indian languages plus bilingual
code-mixed modes, keeps cybersecurity terminology in English, and does all of
this **without breaking any existing functionality**.

## Success Criteria Met

1. **Auto Language Detection (Feature 1)** — the assistant detects the user's
   language from the message: native scripts (Telugu, Hindi, Tamil, Kannada,
   Malayalam, Bengali, Gujarati, Punjabi, Marathi, Odia, Urdu, Assamese),
   romanized/transliterated text, or English.
2. **Manual Preference (Features 2 & 3)** — a language selector in the chat
   composer (workspace + floating assistant) lets the learner pin a language
   (e.g. **Telugu**, **Telugu + English / Teluglish**, Hindi, Tamil, …).
3. **Cybersecurity Terms Stay in English (Feature 4)** — a curated terminology
   list is injected into the system prompt so SIEM, SOC, MITRE ATT&CK, IOC,
   commands, logs, JSON/YAML, code and file names are never translated.
4. **Adaptive Responses (Feature 5)** — the mentor persona, learner level and
   adaptive teaching depth are preserved verbatim; only the *language* of the
   output changes.
5. **Conversation Memory (Feature 6)** — the resolved/selected language is
   remembered per user (and per guest device) in a dedicated SQLite store, so
   future conversations automatically continue in that language until changed.
6. **RAG Compatibility (Feature 7)** — retrieved documents, tool results and
   platform context blocks are never translated; the language block only
   dictates the language of the *narrative* around them.
7. **AI Persona (Feature 8)** — greetings/small talk/off-topic refusals fall
   back to the LLM (with the language block) whenever the response language is
   not English, so even templated turns stay multilingual.
8. **No Breaking Changes** — all 758 backend tests pass; frontend typechecks
   and builds cleanly.

## Architecture

```
Frontend (workspace + floating assistant)
   └─ useChat (language state → localStorage → /api/language/preference)
        └─ POST /api/chat/  { query, stream, language? , ... }

Backend Chat Pipeline (app/chat/bootstrap.py — stage order):
   [0] LanguageContextStage            <- NEW: resolve + persist language
   [1] CacheStage                      <- namespaced by explicit language
   [2] MemoryLoadStage
   [3] AttachmentParseStage
   [4] PlatformContextLoadStage / PersonaLoadStage / PageContextStage
   [5] AdaptiveContextStage
   [6] IntentAnalysisStage -> RoutePlanningStage
   [7] EngineExecutionStage (General/RAG/Tool/…)
   [8] CompositionStage / SuggestedCoursesStage
   [9] PersistenceStage / AdaptivePersistenceStage

SimplePromptBuilder.build_prompt():
   ... existing persona/level/style/memory blocks ...
   + "[Response Language]" block (appended LAST, only when language != en)

REST:  GET  /api/language/preference   (user's stored mode)
       PUT  /api/language/preference   (set mode; "auto" resets)
       DELETE /api/language/preference (reset to Auto Detect)
```

### Language resolution precedence (LanguageContextStage)

1. **Explicit concrete `language` in the request** (manual selection) → used and
   persisted to the user's preference.
2. **Stored concrete preference** (remembered language) → continues, **unless**
   the current message is clearly typed in a *different script* (confidence
   ≥ 0.9, e.g. English → Telugu script), in which case the detected language
   wins and is re-persisted (Feature 1 + 6).
3. **Auto / no preference** → rule-based detection from the message; the result
   is remembered so the next conversation continues in it.

Detection is a dependency-free two-pass heuristic: Unicode script ranges first
(Devanagari disambiguated Hindi/Marathi via a function-word lexicon), then a
romanized lexicon pass for bilingual modes (e.g. `te+en`), then English.

## Feature-by-Feature Implementation Notes

| # | Feature | Implementation |
|---|---------|----------------|
| 1 | Auto detection | `app/multilingual/detector.py` (`LanguageDetector`) |
| 2 | Manual selection | `language` field on `ChatRequest` + `LanguageContextStage` |
| 3 | Telugu + English | `te+en` mode — `[Response Language]` block uses the "Teluglish" instruction; catalog includes `te+en`, `hi+en`, `ta+en`, … |
| 4 | Terms in English | `app/multilingual/terminology.py` + block text "always keep … in English" |
| 5 | Adaptive responses | language block never overrides `[Persona]`/`[Learner Level]`; it is appended last so it only tunes *language* |
| 6 | Conversation memory | `app/multilingual/preferences.py` (`LanguagePreferenceStore`, SQLite) + auto-persist |
| 7 | RAG compatible | retrieved docs/tool results appended as-is; never translated |
| 8 | AI persona | `GeneralExecutionEngine` uses English templates only when `language == en`; otherwise the LLM handles greetings/refusals with the language block |

## Files Changed / Added

### Backend (ai_service)
- **New `app/multilingual/`**: `languages.py` (catalog), `detector.py`,
  `terminology.py`, `prompts.py` (language block), `preferences.py` (SQLite
  store), `stage.py` (pipeline stage), `router.py` (REST API), `dependencies.py`.
- `app/models/chat/chat_models.py` — added optional `language` to `ChatRequest`.
- `app/chat/service.py` — passes `language`/`client_id` into metadata; exposes
  resolved `language`, `language_label`, `language_source` in API metadata.
- `app/chat/bootstrap.py` — wired `LanguageContextStage` as the first stage.
- `app/chat/pipeline/cache_stage.py` — cache key namespaced by explicit language.
- `app/prompt_builder/simple_prompt_builder.py` — appends the `[Response Language]`
  block last.
- `app/chat/engines/general_engine.py` — English templates only for English.
- `app/main.py` — mounted the language router under `/api/language`.

### Frontend (infosecdairies)
- `src/hooks/useChat.ts` — `language` state (localStorage) + `setLanguage`
  (persists to `/api/language/preference`), sent in the chat payload.
- `src/components/ui/chat/LanguageSelector.tsx` — new compact dropdown
  (lucide `Languages` icon, shadcn DropdownMenu) listing the full catalog.
- `src/components/ui/chat/ChatInput.tsx` — renders the selector (both surfaces).
- `src/components/ui/Chat.tsx` and `src/components/ai/FloatingAssistant.tsx` —
  thread `language`/`onLanguageChange` into `ChatInput`.

## Testing & Verification

- **New tests** (`tests/multilingual/`, 48 cases): detector (script, romanized,
  English, disambiguation), prompt blocks, terminology, SQLite preference store,
  `LanguageContextStage` resolution/persistence, and prompt-builder integration.
- **Full backend suite**: `758 passed` (no regressions).
- **Frontend**: `tsc --noEmit` clean; `npm run build` succeeds; ESLint reports
  only pre-existing issues (no new ones from this sprint).

Sample detector output:

| Input | Detected mode |
|-------|---------------|
| `SIEM ante enti` | `te+en` (Teluglish) |
| `SIEM kya hai` | `hi+en` (Hinglish) |
| `SIEM అంటే ఏంటి` | `te` (Telugu script) |
| `Wazuh log pannunga` | `ta+en` (Tanglish) |
| `What is a firewall?` | `en` |

## Deployment & Configuration

- No new environment variables required.
- The preference store auto-creates `data/language_prefs.db` (next to the
  existing `data/adaptive.db`) on first use.
- Existing chat clients that omit `language` keep the exact same English
  behavior (no `[Response Language]` block, cache keys unchanged).
- Restart the AI service (`~/start_ai.sh`) and rebuild/restart the frontend to
  pick up the new stage and selector.

## Backward-Compatibility & Risk Register

| Risk | Mitigation |
|------|------------|
| Prompt changes affect non-English users only | block is empty for `en`/unknown → byte-identical prompts |
| Cache could serve wrong-language replies | cache key namespaced by explicit language |
| Detection misreads | low-confidence romanized matches never override a stored preference; script changes use a 0.9 confidence threshold |
| Circular import when importing `app.multilingual` first | `stage.py` defers `app.chat` imports to method bodies |
| Guests have no user profile | preferences keyed by `guest:<client_id>` in the same SQLite store |
| Template greetings/refusals are English-only | engines skip templates for non-English and let the LLM answer in-language |
