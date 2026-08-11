# Enterprise Guardrails Module

The Enterprise Guardrails Module provides a unified, highly performant, and extensible architecture to enforce security, compliance, and validation rules across all AI Assistant requests and responses.

## Architecture Overview

The Guardrails module strictly adheres to Clean Architecture and SOLID principles. It is completely stateless, provider-agnostic, and relies entirely on dependency injection for composition. 

### Core Concepts

- **Guardrail Context**: A standardized `GuardrailContext` object encapsulates the request payload (or response payload), `trace_id`, `request_id`, and other metadata.
- **Policies**: Individual rules (e.g., `LengthValidationPolicy`, `InjectionDetectionPolicy`) that evaluate the context and return a `GuardrailResult` (ALLOW, BLOCK, WARN). Policies implement the `IGuardrailPolicy` interface.
- **Groups**: Collections of policies organized by functional area (e.g., `ValidationGroup`, `SecurityGroup`, `ComplianceGroup`). Groups dictate the execution priority.
- **Pipelines**: The `InputPipeline` and `OutputPipeline` execute the groups. They run all policies within a priority group in parallel and aggregate the results. Fail-fast behavior is triggered if any policy within a group issues a BLOCK result.
- **Middleware**: The `GuardrailsMiddleware` intercepts requests, dynamically extracts payloads, invokes the `GuardrailsService`, and either allows the request to proceed or returns an HTTP 403. It also validates the final JSON response before it is sent to the client.

## Execution Flow

1. **Request Interception**: `GuardrailsMiddleware` intercepts a request to a supported endpoint (`/api/v1/chat`, `/api/v1/rag`).
2. **Payload Extraction**: The middleware reads the request body and extracts the user prompt dynamically.
3. **Input Validation**: `GuardrailsService.validate_input()` is invoked.
4. **Pipeline Execution**: The `InputPipeline` evaluates the `GuardrailContext` through all registered groups (Validation -> Security -> Compliance).
5. **Business Logic**: If allowed, the request continues to the RAG or Chat service.
6. **Output Interception**: The middleware intercepts the generated JSON response.
7. **Output Validation**: `GuardrailsService.validate_output()` is invoked via the `OutputPipeline`.
8. **Response Return**: The finalized response is returned to the client.

### Streaming Consideration
*Note: The current middleware architecture supports request/response HTTP endpoints only. Streaming endpoints (e.g. `/stream`) natively bypass this middleware to avoid hanging generators. In future versions, a dedicated streaming interceptor or Streaming Guardrails pipeline will be implemented.*

## Dependency Injection & Registration

Dependencies are wired in `dependencies.py` using a lightweight dependency injection approach without external IoC containers. 
- Configuration (`GuardrailsConfig`), `PolicyRegistry`, and `GuardrailsService` are instantiated as Singletons (using `@lru_cache`).
- Policies depend only on domain interfaces (e.g. `IRegexEngine`), and concrete adapters (e.g., `RegexEngineAdapter`) are injected during registration.

## Configuration

Configuration is validated at startup using Pydantic via `GuardrailsConfig`. 

Key settings (managed via env vars prefixed with `GUARDRAILS_`):
- `GUARDRAILS_ENABLED` (bool)
- `GUARDRAILS_AUDIT_MODE_ENABLED` (bool) - When true, blocked requests are only logged (WARN), not dropped.
- `GUARDRAILS_MAX_PROMPT_LENGTH` (int) - Must be > 0.
- `GUARDRAILS_TIMEOUT_MS` (int) - Must be > 0.

## Observability & Health

The module natively integrates with the Enterprise Observability and Health systems:
- **Health**: Exposed via `GuardrailsService.get_health_status()`, aggregating registered groups and policies into the global `/health` endpoint.
- **Observability**: Exposes metrics for latency (`guardrails_input_latency_ms`), evaluations (`guardrails_input_evaluated`), and blocks (`guardrails_input_blocked`). Tracing and structured logging are injected via `ObservabilityService`.

## Developer Guide

### How to Add a New Policy
1. Create a new class in `app/guardrails/policies/` implementing `IGuardrailPolicy`.
2. Implement the `name`, `metadata`, and async `evaluate()` methods.
3. Return `GuardrailResult.allow()` or `GuardrailResult.block(reason=...)`.
4. Register the policy in the appropriate group within `dependencies.py`.

### How to Add a New Policy Group
1. Create a new class in `app/guardrails/groups/` inheriting from `BasePolicyGroup`.
2. Assign it a name and a `PolicyPriority`.
3. Register the group in `dependencies.py` via `registry.register_group()`.

### How to Add a New Adapter
1. Create an interface in `app/guardrails/domain/interfaces/`.
2. Create the concrete adapter in `app/guardrails/infrastructure/adapters/`.
3. Inject the interface into the policy constructor.
4. Supply the concrete adapter in `dependencies.py`.
