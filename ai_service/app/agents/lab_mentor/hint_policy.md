# Hint Policy

## Core Principle
**Never reveal flags or solutions.**

## Hint Escalation
1. The first hint request defaults to Level 1.
2. Subsequent consecutive hint requests escalate to Level 2, then Level 3.
3. Once Level 3 is reached, the learner is directed to Reflection before more hints are given.

## Anti-Leakage Sandbox
- The `HintValidationTool` strictly evaluates the generated hint string.
- If it contains `flag{` or any literal answer sequence, the hint is destroyed and replaced with a generic message.
