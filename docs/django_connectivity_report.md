# Phase 8: Django Connectivity Audit

## Cross-Service Communication Analysis

### Configurations
- **Django App:** Runs locally on `http://localhost:8080`.
- **FastAPI Config:** `.env` defines `DJANGO_API_URL=http://localhost:8080/api`.

### Connection Tests

- **Base URL:** Valid. The Django server is reachable.
- **DNS / Port:** Valid. `localhost:8080` successfully maps to the Django instance.
- **Health Endpoint:** Valid. Reachable at `http://localhost:8080/`.

### HTTP Request Failure Matrix

| Request Source | Intended Path | Actual URL Sent by httpx | Django Response |
|---|---|---|---|
| get_courses | `/api/courses/` | `http://localhost:8080/courses/` | 404 Not Found |
| get_course | `/api/courses/{slug}/` | `http://localhost:8080/courses/{slug}/` | 404 Not Found |
| get_progress | `/api/courses/{slug}/progress/` | `http://localhost:8080/courses/{slug}/progress/` | 404 Not Found |

### Root Cause of Disconnect
`httpx` applies standard RFC 3986 URI resolution. Because the base URL `http://localhost:8080/api` does not end in a trailing slash, AND the requested path `"/courses/"` begins with a leading slash, `httpx` interprets `"/courses/"` as an absolute path and aggressively strips the `/api` segment. 

All outbound calls are sent to non-existent root-level endpoints in Django, completely bypassing the `/api/` routing prefix.
