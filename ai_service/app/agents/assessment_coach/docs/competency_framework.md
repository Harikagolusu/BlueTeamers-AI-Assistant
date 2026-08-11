# Competency Framework

The Assessment Coach relies on the platform's unified `CompetencyCategory` definitions to guarantee interoperability with the Learning Coach and Lab Mentor.

Categories:
- KNOWLEDGE
- PRACTICAL_SKILLS
- INVESTIGATION_SKILLS
- DETECTION_ENGINEERING
- INCIDENT_RESPONSE
- CLOUD_SECURITY
- THREAT_HUNTING

## Competency Evolution

All `CompetencyScore` objects track confidence evolution over time, allowing the platform to analyze trends natively:
- `previous_confidence`
- `confidence_delta`
- `confidence_trend`
- `last_assessment_id`

