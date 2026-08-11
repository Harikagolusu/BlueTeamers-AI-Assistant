# Tool Matrix

| Tool | Purpose | Input | Output |
|---|---|---|---|
| `LabAnalysisTool` | Understands current lab state | `user_query` | `LabState` |
| `ProgressTrackingTool` | Tracks attempts and requests | `action`, `history` | `AttemptHistory` |
| `MistakeDetectionTool` | Detects logical blockers | `action` | `str` (blocker) |
| `HintGenerationTool` | Creates progressive hints | `blocker`, `HintLevel` | `Hint` |
| `HintValidationTool` | Enforces anti-leakage | `hint_content` | `bool`, `feedback` |
| `LabPlanningTool` | Plans the next conceptual step | `history`, `state` | `MentorFeedback` |
| `ReflectionTool` | Asks reflective questions | `action` | `ReflectionPrompt` |
