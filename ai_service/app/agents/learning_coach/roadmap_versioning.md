# Roadmap Versioning

Learning Roadmaps are strictly versioned. They are never overwritten in place.

## Structure
The `RoadmapVersion` object inherits the standard `LearningRoadmap` structures but extends it with:
- `version_number`: Iterative counter.
- `created_at`: Generation timestamp.
- `active`: Boolean denoting the currently active roadmap for the learner.
- `superseded_by`: Identifier linking to the next generation roadmap.
- `reason_for_change`: Explainability string stating why a new roadmap was required.
- `changed_goals`: List of target goals that shifted between versions.

## Rationale
Versioning allows the Learning Coach to explain to the learner exactly *why* their path has changed (e.g., "Your roadmap shifted because you rapidly mastered Nmap Scanning and we are pulling advanced Threat Hunting forward.").
