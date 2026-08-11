# Analytics Snapshots

The Learning Coach engine periodically bundles `LearningAnalytics` evaluations into `AnalyticsSnapshot` objects. 

## Purpose
Rather than recalculating metrics dynamically on every request, snapshots provide a historical benchmark. This enables trend analysis—determining whether a learner's velocity is increasing or decreasing over a specified time horizon.

## Snapshot Structure
- `timestamp`: Point in time of the snapshot.
- `analytics`: The raw metrics (`learning_velocity`, `knowledge_growth`).
- `competency_profile`: The learner's `SkillProfile` at the time of the snapshot.
- `roadmap_completion`: Percentage completion of the currently active roadmap.
- `engagement_score`: Heuristic evaluating session frequency and completion momentum.
