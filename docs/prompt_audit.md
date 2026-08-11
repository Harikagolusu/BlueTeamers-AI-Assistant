# Phase 7: LLM Prompt Audit

## Prompt Construction Analysis

When the user queries "Suggest SOC courses", the `PlatformExecutionEngine` constructs the following system prompt block:

```text
You are the BlueTeamers AI Assistant. The user is asking about courses, labs, or platform features. You MUST ONLY recommend or mention items from the 'Platform Data' below. DO NOT invent external courses (like CompTIA, SANS). Use the 'Technical Knowledge' to answer cybersecurity questions accurately.

=== User Context ===
### User Platform Context ###
Active Enrollments: Not available.
Recent Progress: Not available.
Badges: This feature is not yet available on the platform.
Learning Paths: This feature is not yet available on the platform.

=== Platform Data (Recommendations) ===
[]
```

### Analysis
- **Does the prompt contain Courses?** No, the array is empty `[]`.
- **Does the prompt contain Platform Data?** No, it is missing due to repository failures.
- **Does it contain constraint instructions?** Yes, it explicitly states "You MUST ONLY recommend or mention items from the 'Platform Data' below." 
- **LLM Behavior:** Because the 'Platform Data' array is literally empty (`[]`), the LLM has zero internal data to fulfill the user's request. As language models inherently attempt to answer questions, it breaks the negative constraint ("DO NOT invent external courses") to satisfy the positive constraint of suggesting SOC courses, resulting in hallucinations (Coursera, Udemy, TryHackMe).
