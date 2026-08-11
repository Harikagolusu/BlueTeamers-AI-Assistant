# Phase 5: Query Router Audit

## Intent Classification & Routing

**Class:** `RuleIntentClassifier`, `RuleRouteEvaluator`, `RuleRoutePlanner`

### Flow for "Suggest SOC courses"

1. **User Query:** "Suggest SOC courses"
2. **Intent Classification (`RuleIntentClassifier`):**
   - The string contains the keywords `"course"` and `"suggest"`.
   - Matches rule: `course_keywords = ["course", "enroll", "module", "lesson", "suggest", "recommend", "study"]`.
   - Classification: `IntentType.PLATFORM_COURSE`.
   - Base Confidence: `0.0`.
3. **Confidence Evaluation (`RuleConfidenceEvaluator`):**
   - Evaluator boosts `IntentType.PLATFORM_COURSE` base score (0.5) by 0.4 because `len(intent.matched_features) > 0`.
   - Final Confidence: `0.9`
4. **Execution Planning (`RuleRoutePlanner`):**
   - Maps `IntentType.PLATFORM_COURSE` to target engine: `"PLATFORM"`.

### Routing Decision
The Query Router behaves exactly as intended. It perfectly classifies the user's intent to request platform course recommendations and correctly routes execution to the `PlatformExecutionEngine`.

Misclassification is **NOT** the root cause of the failure.
