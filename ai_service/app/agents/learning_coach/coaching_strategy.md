# Coaching Strategy & Personalization

The Learning Coach leverages a structured personalization strategy driven by the `RecommendationPolicy` and `LearningPatternTool`. 

## Competency Model
The agent utilizes a 7-pillar model:
- Knowledge
- Practical Skills
- Investigation Skills
- Detection Engineering
- Incident Response
- Cloud Security
- Threat Hunting

## Journey States
Learners progress through specific states governed by the `LearningJourneyState` enum:
- `ONBOARDING` -> `LEARNING` -> `PRACTICING` -> `ASSESSING` -> `CERTIFICATION_READY` -> `COMPLETED`. 
- `REMEDIATION` and `PAUSED` handle exceptions.

## Recommendation Policy
Recommendations (concepts, labs, assessments) are ranked according to:
- Prerequisite completion (strict check)
- Competency gaps (highest gap = highest priority)
- Career & Certification goal alignment
- Preferred difficulty and learning style
- Available weekly study time (ensures realistic scheduling)

The engine avoids generic advice and dynamically references past metrics from `AttemptHistory` and `MentoringMetrics`.
