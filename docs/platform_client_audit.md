# Phase 3: PlatformApiClient Audit

## Client Configuration

**Class:** `DjangoClient` (located in `ai_service/app/integrations/django_client.py`)

### Verification Checklist

- **Is it instantiated?** ✅ Yes, as a singleton `django_client = DjangoClient()`.
- **Is it registered in DI?** ✅ Yes, available in `app/api/dependencies.py` via `get_django_client()`.
- **Is it injected into PlatformRepository?** ✅ Yes, via `DjangoPlatformRepository(platform_client)` in `app/chat/bootstrap.py`.
- **Is it actually used?** ✅ Yes, repository methods invoke `self.client.get(...)`.
- **Are requests reaching Django?** ❌ Yes, but they hit the wrong URL (`/courses/` instead of `/api/courses/`), resulting in 404s.
- **Are responses returned?** ❌ Returns 404 Not Found error responses.
- **Are exceptions swallowed?** ❌ `DjangoClient` accurately raises `NotFoundException`, but the caller (`DjangoPlatformRepository`) swallows it.
- **Are retries working?** ✅ Yes, exponential backoff is implemented for 502/503/504 errors, but not for 404s (which is correct behavior).
- **Is timeout configured?** ✅ Yes, timeout is configured `httpx.Timeout(10.0, connect=5.0, read=30.0, write=10.0)`.

### Core Issue Identified
The client relies on `httpx.AsyncClient(base_url=settings.DJANGO_API_URL)`. 
`DJANGO_API_URL` is configured as `http://localhost:8080/api` in `.env`. 
When `DjangoPlatformRepository` passes an absolute path starting with a forward slash (e.g. `"/courses/"`), standard RFC 3986 URI resolution discards the `/api` prefix of the base URL, resulting in an outbound request to `http://localhost:8080/courses/`.
