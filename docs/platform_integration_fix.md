# Platform Integration Fix Report

## Overview
The platform integration layer has been heavily refactored to resolve architectural drift and communication failures between the FastAPI orchestrator and the Django backend.

## Fixes Implemented

### 1. HTTP Path Resolution
- **Issue**: Standard `httpx` path resolution was stripping `/api/` from the base URL due to leading slashes in paths.
- **Fix**: Adjusted `DjangoClient` initialization to enforce trailing slashes on `base_url` (`base_url += "/"`) and stripped leading slashes from requested paths (`path.lstrip("/")`). Requests now successfully route to `/api/courses/`.

### 2. Exception Propagation & Hardening
- **Issue**: The `DjangoPlatformRepository` swallowed all connection/request errors (yielding empty lists) which forced the LLM to hallucinate missing data.
- **Fix**: Refactored `DjangoPlatformRepository` to remove blanket `except Exception:` blocks. Mapped `httpx` and `DjangoClient` errors to structured core exceptions: `PlatformUnavailable`, `PlatformAuthenticationFailed`, and `PlatformEndpointMissing`.

### 3. JWT Authentication Forwarding
- **Issue**: `PlatformExecutionEngine` hardcoded `"dummy_token"`, blocking access to any authenticated endpoints (e.g. progress, labs, assessments).
- **Fix**: Upgraded FastAPI dependencies to use `HTTPBearer(auto_error=False)` via `get_optional_raw_token()`. The token is injected into the `ChatRequest`, securely passed down through the pipeline to the `ExecutionContext`, and resolved dynamically by the `PlatformExecutionEngine` at runtime.

### 4. LLM Prompt Guardrails
- **Issue**: Missing platform data pushed the LLM into generating outside knowledge.
- **Fix**: `PlatformExecutionEngine` dynamically alters the core system prompt if the recommendation service returns an empty list, explicitly commanding the LLM to apologize instead of hallucinating outside courses.
