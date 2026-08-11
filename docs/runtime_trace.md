# Phase 10: Runtime Trace

## Execution Lifecycle Trace

The following represents the complete internal runtime trace when a user asks "Suggest SOC courses".

1. **User Query:** "Suggest SOC courses"
2. **Intent Service:** `EntityExtractionStage` extracts no specific entities.
3. **Intent Service:** `IntentClassificationStage` identifies keywords `"course"`, `"suggest"`.
4. **Intent Service:** Intents mapped to `IntentType.PLATFORM_COURSE`.
5. **Intent Service:** `ConfidenceEvaluationStage` bumps confidence to 0.9.
6. **Intent Service:** `ExecutionPlanningStage` assigns query to `"PLATFORM"` engine.
7. **Orchestrator:** `ChatOrchestrator` routes to `PlatformExecutionEngine`.
8. **Execution Engine:** `PlatformExecutionEngine` initializes context.
9. **Execution Engine:** Invokes `UserContextBuilder.build("dummy_token")`. Returns static string "Not available".
10. **Execution Engine:** Invokes `RecommendationService.generate_recommendations("dummy_token", "Suggest SOC courses")`.
11. **Repository:** `DjangoPlatformRepository.get_courses("dummy_token")` invoked.
12. **HTTP Client:** `DjangoClient.get("/courses/")` attempts to construct URL.
13. **HTTP Client:** Base URL `http://localhost:8080/api` is merged with `/courses/`, resulting in `http://localhost:8080/courses/`.
14. **HTTP Client:** Outbound GET request sent.
15. **Django Backend:** Router checks paths. `/courses/` not found (only `/api/courses/` exists). Returns `404 Not Found`.
16. **HTTP Client:** Intercepts 404 and raises `NotFoundException("Resource not found: /courses/")`.
17. **Repository:** Catch-all `except Exception` captures `NotFoundException`.
18. **Repository:** Logs error and returns empty list `[]`.
19. **Execution Engine:** Recommendation service returns `[]`.
20. **Prompt Builder:** Constructs prompt containing `=== Platform Data (Recommendations) ===\n[]`.
21. **LLM:** Instructed to only use platform data, but data is empty. Uses pretrained knowledge to guess courses.
22. **Final Response:** "I recommend Coursera, Udemy..." (Hallucination).

### Diagnostics Log
```
INFO:  app.chat.router: Chat API Request Started
INFO:  app.chat.intent: Classified IntentType.PLATFORM_COURSE with confidence 0.9
INFO:  app.chat.engines: Routing to PLATFORM engine
ERROR: app.platform.repositories: Error fetching courses: Resource not found: /courses/
INFO:  app.chat.engines: Context loaded. 0 platform recommendations generated.
INFO:  app.llm: Generated response based on system prompt.
INFO:  app.chat.router: Chat API Request Completed
```
