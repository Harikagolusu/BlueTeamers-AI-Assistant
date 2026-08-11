# Phase 6: PlatformExecutionEngine Audit

## Execution Engine Analysis

**Class:** `PlatformExecutionEngine` (located in `ai_service/app/chat/engines/platform_engine.py`)

### Verification Checklist

- **Is it registered?** ✅ Yes, in `ExecutionEngineRegistry` in `app/chat/bootstrap.py`.
- **Is it instantiated?** ✅ Yes, by `RealEngineFactory`.
- **Is it selected?** ✅ Yes, `RuleRoutePlanner` directs `PLATFORM_COURSE` queries here.
- **Is it executed?** ✅ Yes, the engine's `execute()` method is successfully invoked.
- **Does it call PlatformRepository?** ✅ Yes, indirectly via `UserContextBuilder` and `RecommendationService`.
- **Does it build platform context?** ❌ It attempts to, but receives `[]` from the `RecommendationService` due to upstream repository failures.
- **Does it invoke the LLM?** ✅ Yes, with an empty set of platform recommendations.

### Core Issue Identified
Because the upstream repository silently catches HTTP 404 errors and returns an empty array, `RecommendationService` is forced to return `[]`. 

The Engine then builds the following block into the prompt:
```json
=== Platform Data (Recommendations) ===
[]
```
With no data provided, the LLM generates a response based on its general knowledge, thereby ignoring the platform constraints and hallucinating external courses.
