# Investigation Agent Architecture

## Overview
The Investigation Agent is the primary orchestration agent for the BlueTeamers AI Assistant platform. Unlike expert agents that perform deep technical tasks in a specific domain, the Investigation Agent is responsible for coordinating the overall incident response workflow.

## Responsibilities
- Orchestrate investigations
- Coordinate multiple capabilities (SOC, CTI)
- Correlate evidence across disparate sources
- Build comprehensive investigation context
- Guide the learner through investigations (pedagogical approach)
- Produce structured investigation reports

## Core Components
- **Agent (`agent.py`)**: Extends `BaseAgent`, running the 13-step lifecycle. Offloads technical execution to expert agents via the `AgentOrchestrationService`.
- **AgentOrchestrationService**: A reusable service that handles resolving, invoking, and aggregating responses from expert agents. Includes retry policies and timeouts.
- **Models (`models.py`)**: Strict Pydantic schemas validating all inputs, intermediate artifacts, and final responses.
- **Tools (`tools/`)**: Five distinct tools that handle evidence normalization, correlation, planning, timeline generation, and summarization.

## Tool Matrix
- **EvidenceCollectionTool**: Normalizes uploaded evidence.
- **EvidenceCorrelationTool**: Correlates entities (process trees, domains, IPs, URLs, hashes).
- **InvestigationPlanningTool**: Generates an investigation sequence and specifies required expert agents.
- **IncidentTimelineTool**: Maps events chronologically against MITRE ATT&CK.
- **InvestigationSummaryTool**: Generates final narrative and recommendations.

## What It Does NOT Do
The Investigation Agent **does not** contain cybersecurity business logic. It does not perform log analysis or IOC enrichment itself; it strictly orchestrates the SOC Analyst and Threat Intelligence agents to perform those tasks.
