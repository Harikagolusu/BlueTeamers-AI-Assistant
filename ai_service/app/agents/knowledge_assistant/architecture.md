# Knowledge Assistant Architecture

## Overview
The Knowledge Assistant leverages the **Platform Shared Services (v1.3.5)**. It consists of thin orchestration logic wrapping 6 highly cohesive educational tools.

## Workflow Execution
The agent utilizes the `WorkflowBuilder` to create a directed acyclic graph (DAG) executed asynchronously by the `WorkflowExecutor`:

1. **Understand & Assess**: The agent extracts the user's `LearnerProfile`.
2. **Retrieve**: The `KnowledgeRetrievalTool` fetches external context.
3. **Explain**: The `ConceptExplanationTool` processes context and adapts explanation depth based on the learner's experience level (ELI5 to Expert).
4. **Map**: The `ConceptMappingTool` maps prerequisites.
5. **Assess**: The `KnowledgeAssessmentTool` generates questions.
6. **Recommend**: The `ResourceRecommendationTool` ranks external resources.
7. **Path Generation**: The `LearningPathTool` tracks future steps.

## Encapsulation
- No active incident investigation logic is present.
- All educational business logic is encapsulated in the specific educational tools.
- Responses strictly adhere to the `KnowledgeResponse` Pydantic schema, ensuring consistent output across all interaction levels.
