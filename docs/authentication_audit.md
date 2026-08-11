# Phase 9: Authentication Audit

## JWT Integration Analysis

### Token Forwarding
In `PlatformExecutionEngine`, the engine explicitly sets a hardcoded dummy token for backend requests:
```python
        # Mock token for now; in a real app, extract from session
        token = "dummy_token" 
```

### Django Authentication Logic
- The `course_list` API (`GET /api/courses/`) does **not** have the `@permission_classes([IsAuthenticated])` decorator. It is public. Therefore, a dummy token does not trigger a 401 response for course listings.
- However, personalized endpoints such as `lesson_progress` and `my_quiz_scores` **do** require a valid JWT.
- If the `PlatformExecutionEngine` were to call these protected endpoints with `"dummy_token"`, Django's `JWTAuthentication` class would reject it, returning a `401 Unauthorized`.
- Because `DjangoPlatformRepository` uses blanket exception handling (`except Exception`), any 401 error raised by `DjangoClient` would be silently swallowed and ignored, returning `None` or `[]`.

### Conclusion
Authentication is currently bypassed for course listings, meaning it is not the primary reason why "Suggest SOC courses" fails (the 404 path issue kills the request first). However, the hardcoded `dummy_token` is a secondary critical failure point that will block all personalized data access (progress, badges, assessments) once the pathing issue is resolved.
