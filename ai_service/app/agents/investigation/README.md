# Investigation Agent

The **Investigation Agent** is the primary orchestration agent for the BlueTeamers AI Assistant platform. It acts as a senior SOC investigator to coordinate comprehensive incident response workflows.

## Overview
Unlike expert agents (such as the SOC Analyst or Threat Intelligence agents) which perform highly specialized tasks, the Investigation Agent is a "Thin Agent". It contains no cybersecurity business logic of its own. Instead, it leverages the `AgentOrchestrationService` to delegate tasks to the appropriate expert agents.

## Core Capabilities
- **Orchestration**: Plans the investigation and invokes expert agents via dependency injection.
- **Evidence Correlation**: Synthesizes process trees, hashes, network sessions, etc.
- **Timeline Generation**: Produces a chronologically ordered MITRE ATT&CK timeline.
- **Investigation Summary**: Generates structured, pedagogical reports guiding junior analysts.

## Usage
The agent accepts an `InvestigationRequest` containing raw evidence. Through its 13-step lifecycle, it normalizes evidence, determines a plan, invokes expert agents concurrently, aggregates their findings, and outputs an `InvestigationResponse`.
