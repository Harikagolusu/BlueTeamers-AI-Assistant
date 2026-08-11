# Platform Health Diagnostics Report

## Introduction
A new diagnostic endpoint `GET /api/debug/platform-health` has been introduced to permanently monitor the integration status between FastAPI and the Django backend.

## Output Specification
When invoked, the endpoint tests internal routing and backend availability in real-time, verifying whether the connection path, repository layer, and target endpoints are healthy.

### Example Payload
```json
{
    "django_connection": true,
    "authentication": true,
    "courses_endpoint": true,
    "labs_endpoint": true,
    "progress_endpoint": true,
    "platform_repository": true,
    "platform_engine": true
}
```

## Diagnostic Guidance
- If `django_connection` is `false`, check `DJANGO_API_URL` and ensure the Django container/service is running.
- If `authentication` is `false`, the JWT token signing key might be out of sync between FastAPI and Django.
- If `courses_endpoint` is `false`, Django might have undergone a URL schema migration away from `/api/courses/`.
