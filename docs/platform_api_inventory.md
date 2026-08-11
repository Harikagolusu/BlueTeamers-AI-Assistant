# Phase 2: Platform API Inventory

## Django Backend Audit

The Django backend exposes a variety of APIs via `backend.urls` and `courses.urls`.

### Base Configuration
- Django Base URL (Dev): `http://localhost:8080`
- API Prefix: `/api/`

### Existing Endpoints

| Endpoint | Path | Protected? | Method | Status |
|---|---|---|---|---|
| Course List | `/api/courses/` | No | GET | ✅ Exists |
| Course Detail | `/api/courses/<slug>/` | No | GET | ✅ Exists |
| Enroll | `/api/courses/<slug>/enroll/` | Yes | POST | ✅ Exists |
| Enrollment Status | `/api/courses/<slug>/enrollment/` | Yes | GET | ✅ Exists |
| Course Access Token | `/api/courses/<slug>/access-token/` | Yes | GET | ✅ Exists |
| Lesson Progress | `/api/courses/<slug>/progress/` | Yes | GET | ✅ Exists |
| Course Completion | `/api/courses/<slug>/completion/` | Yes | GET | ✅ Exists |
| My Quiz Scores | `/api/courses/<slug>/quiz-scores/` | Yes | GET | ✅ Exists |

### Missing Endpoints
Based on the expectations of `DjangoPlatformRepository`:
- **Labs**: No dedicated endpoint for Labs exists (noted in `DjangoPlatformRepository.get_labs` as "The Django backend does not yet have a dedicated labs endpoint").
- **Learning Paths**: Not implemented in Django (no DB model exists).
- **Badges**: Not implemented in Django (no DB model exists).
- **Certificates List**: The API supports fetching a specific certificate, but lacks an endpoint to get all certificates for a user.

### Conclusion
The necessary endpoints to satisfy "Suggest SOC courses" (e.g. `/api/courses/`) exist in the Django backend. The backend is healthy and fully capable of serving this data.
