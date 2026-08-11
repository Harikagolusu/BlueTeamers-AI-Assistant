"""Adaptive Learning Intelligence for the BlueTeamers AI Workspace.

Sprint 4: a mentor that continuously learns from interactions without ever
permanently classifying the learner. Provides:
  - a multi-signal learner model (signals, base level, per-topic confidence),
  - topic-wise knowledge confidence across 13 cyber domains,
  - dynamic conversation adaptation with gradual (never jumpy) adjustments,
  - temporary learning overrides for a single request,
  - conversation-scoped session memory (rolling context, summary, facts,
    investigation continuity, uploaded-file memory).
"""
