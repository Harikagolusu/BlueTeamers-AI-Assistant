# Phase 11: Root Cause Analysis

## Final Investigation Report

Based on a comprehensive architectural and runtime audit of the FastAPI to Django integration layer, the exact root causes for the AI hallucinating platform data have been identified. 

There is not a single failure, but a cascading series of three critical bugs that collectively prevent data retrieval and mask the errors.

### 1. HTTP Path Resolution Bug (The Trigger)
**Location:** `ai_service/app/integrations/django_client.py` & `.env`
**Evidence:** The environment configures `DJANGO_API_URL=http://localhost:8080/api`. In `DjangoClient._request`, the repository passes absolute paths with a leading slash (e.g. `"/courses/"`). `httpx.AsyncClient` applies standard RFC 3986 URI resolution: because the path has a leading slash, the `/api` segment of the base URL is stripped, resulting in an outbound request to `http://localhost:8080/courses/`.
**Result:** Django returns `404 Not Found` because the correct path is `/api/courses/`.

### 2. Silent Exception Handling (The Mask)
**Location:** `ai_service/app/platform/repositories/django_repository.py`
**Evidence:** The repository wraps HTTP calls in a catch-all `except Exception as e:` block. 
```python
    except Exception as e:
        logger.error(f"Error fetching courses: {e}")
        return []
```
**Result:** When `DjangoClient` correctly raises a `NotFoundException`, the repository silently swallows it and returns an empty list `[]`. The application proceeds as if there are simply zero courses on the platform, rather than explicitly throwing an integration error. 

### 3. Hardcoded Mock Authentication (The Secondary Blocker)
**Location:** `ai_service/app/chat/engines/platform_engine.py`
**Evidence:** The `PlatformExecutionEngine` hardcodes `token = "dummy_token"`. While this does not break the `course_list` API (which is public), it will immediately return `401 Unauthorized` responses for any personalized data (progress, assessments, etc.) once the 404 pathing issue is fixed.
**Result:** Personalized context is permanently inaccessible until real JWT tokens are passed.

### Impact on LLM
Because the repository returns an empty list, the `RecommendationService` outputs zero recommendations. The LLM prompt is populated with an empty array:
```json
=== Platform Data (Recommendations) ===
[]
```
Faced with strict negative constraints ("DO NOT invent external courses") but absolutely no data to fulfill the user's positive request ("Suggest SOC courses"), the LLM breaks the negative constraint and hallucinates Coursera, Udemy, and TryHackMe.

---

## Remediation Plan (Prioritized)

To be implemented in the next phase:

1. **Fix Path Resolution (`django_client.py` & `django_repository.py`)**
   - *Option A:* Strip the leading slash in the repository calls (e.g. `self.client.get("courses/", token)`).
   - *Option B:* Modify `DjangoClient` to strip leading slashes before making the request (`url = path.lstrip('/')`).
   - *Option C:* Ensure the base URL in `.env` ends with a trailing slash (`/api/`) AND strip the leading slash in paths.

2. **Fix Exception Handling (`django_repository.py`)**
   - Remove the blanket `except Exception` blocks in the repository.
   - Allow `DjangoUnavailableException`, `UnauthorizedException`, and `NotFoundException` to propagate up to the `ChatOrchestrator` so they can be logged correctly and handled by the global exception handler, preventing silent failures.

3. **Implement Real JWT Forwarding (`platform_engine.py`)**
   - Extract the active user's JWT from the `ExecutionContext` or FastAPI request state.
   - Replace `token = "dummy_token"` with the actual JWT string so protected endpoints can be successfully queried.
