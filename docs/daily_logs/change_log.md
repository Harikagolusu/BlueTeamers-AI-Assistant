# BlueTeamers AI Assistant - Change Log

## Date: 2026-08-04
### Hybrid Knowledge Architecture + Live Platform Data

**Additions & Updates:**
- New `app/knowledge/` ingestion package (sources, pipeline, dependencies, router, schemas) with FAISS vector store (3681 vectors: 10 course overviews + 3671 lesson chunks).
- Started the Django backend (port 8000) locally with seeded demo user `harika@example.com` — platform queries now return real account data end-to-end.

**Fixes & Resolutions:**
- Fixed `planning_stage.py` crash (`AttributeError: 'dict' object has no attribute 'get_recent_context'`) by passing `context.memory or {}` directly.
- Fixed `DjangoPlatformRepository._map_courses` to construct `Course` with the pydantic alias `slug=` instead of `id=`, restoring enrolled-course/progress data.

**Ops:**
- Backend venv bootstrapped at `infosecdairies/infosec-backend/backend/.venv` (no system ensurepip; used `--without-pip` + get-pip.py). Django runs HS256 JWT (no local private key). Seed script: `backend/seed_demo_user.py`.

## Date: 2026-08-03
### Phase 5 Production Stabilization


**Additions & Updates:**
- Migrated legacy datetime.utcnow() to timezone-aware datetime.now(timezone.utc) everywhere in the codebase (total 14 files updated) to eliminate Python 3.12+ deprecation warnings.
- Fully implemented Pydantic V2 migrations by replacing class Config: with model_config = ConfigDict(frozen=True) across various configuration models (plan.py, context.py, capability.py, gent_descriptor.py, guardrails_config.py).
- Updated LegacyToolProvider to officially adopt the IToolProvider interface defined in pp/mcp/interfaces/i_tool_provider.py, bringing it in parity with MCPToolProvider.
- Consolidated provider interfaces by deprecating and implicitly removing the usage of the redundant interface module pp.mcp.providers.interfaces.
- Modified ToolExecutionEngine to call the correctly standardized .execute() on IToolProvider instances and access .provider_id for tracking tool outputs.

**Fixes & Resolutions:**
- Fixed AttributeError for .execute_tool() and .provider_type() properties resolving 	est_stress_validation.py failures.
- Fixed 	est_integration.py execution by returning standard provider_id identifiers rather than provider literal strings.
- Fixed ValidationError within ToolRegistration mock data in 	est_resolver.py.
- Restored ToolExecutionEngine provider resolutions to synchronous invocation in alignment with standard ToolProviderResolver definitions, fixing dependency injection integration test anomalies.
- Hardened full test suite resulting in 0 failed tests (340 passing) across integrations, orchestration, discovery, observability, security, memory, chat, and agents.
- Resolved FastAPI to Django communication failure (404 Not Found) by fixing `httpx` RFC 3986 path resolution bug in `DjangoClient`.
- Refactored `DjangoPlatformRepository` to explicitly throw structured exceptions (`PlatformUnavailable`, `PlatformAuthenticationFailed`, `PlatformEndpointMissing`) instead of masking failures.
- Implemented robust JWT token passing via `ExecutionContext` through `ChatRequest`, resolving static 'dummy_token' blocking.
- Added `/api/debug/platform-health` diagnostics endpoint.
- **Feature**: Added OmniRouteProvider to dynamically route LLM requests to OmniRoute AI.

