# Tool Matrix

| Tool | Purpose | Schema | Output |
|---|---|---|---|
| KnowledgeAssessmentTool | Evaluate concepts | `answers` | `KnowledgeAssessment` |
| PracticalAssessmentTool | Evaluate labs | `lab_data` | `PracticalAssessment` |
| ScenarioAssessmentTool | Evaluate scenarios | `responses` | `dict` |
| CompetencyEvaluationTool | Compute competencies | `assessment_results`| `CompetencyScore` |
| GapAnalysisTool | Detect missing skills | `competency_profile`| `CompetencyGap` |
| AdaptiveQuestionTool | Generate questions | `current_difficulty`| `AssessmentQuestion` |
| FeedbackGenerationTool | Produce feedback | `assessment_results`| `AssessmentFeedback` |
| ReadinessAssessmentTool | Measure readiness | `competency_profile`| `ReadinessLevel` |
| RecommendationEngineTool | Suggest next steps | `gaps` | `LearningRecommendation` |
| AssessmentAnalyticsTool | Track trends | `assessment_results`| `LearningAnalytics` |
