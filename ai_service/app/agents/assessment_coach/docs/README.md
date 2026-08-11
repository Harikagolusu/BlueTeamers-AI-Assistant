# Assessment Coach Agent

The Assessment Coach is the final educational product agent for the BlueTeamers AI Assistant platform. Its primary role is to evaluate learner understanding, measure competencies, generate adaptive assessments, identify knowledge gaps, and produce structured competency reports.

## Core Principles

- **Evaluation Only:** The Assessment Coach strictly evaluates. It does not teach, solve labs, or mentor users.
- **Thin Orchestrator:** The agent logic orchestrates workflows and delegates execution to specialized tools.
- **Shared Analytics & Competencies:** Reuses the existing Learning Coach models for competencies, recommendations, and analytics.

## Workflows

The Assessment Coach relies on the platform `WorkflowBuilder` to execute a structured DAG, analyzing knowledge, practical skills, gaps, readiness, and generating detailed feedback and recommendations.
