# Threat Intelligence Agent

The Threat Intelligence Agent is a specialized cyber threat intelligence agent designed to enrich indicators, correlate intelligence, identify threat actors, analyze campaigns, and provide intelligence-driven recommendations.

## Overview
This agent acts as the "Threat Intel Brain", utilizing a suite of tools (the "Hands") to investigate Indicators of Compromise (IOCs), map threats to MITRE ATT&CK, and produce structured, factual assessments.

## Tools
- **IOCLookupTool**: Detects and normalizes IOCs (IP, Domain, Hash, URL).
- **ReputationTool**: Analyzes risk and reputation.
- **ThreatActorTool**: Looks up known threat actors and their TTPs.
- **CampaignLookupTool**: Looks up known campaigns.
- **IndicatorCorrelationTool**: Correlates multiple indicators.
- **MITREMappingTool**: Maps indicators or entities to MITRE ATT&CK.

## Usage
The agent accepts a list of indicators or context and orchestrates the necessary tool calls. It then passes the aggregated tool context to the LLM (using the generic platform LLM provider) to generate a structured `ThreatIntelligenceResponse`.

```python
# Assuming you have an instantiated agent and context
result = await agent.execute(context)
print(result.response) # JSON structured response
```

## Architecture
The agent strictly adheres to the BlueTeamers AI Assistant SDK architecture, extending `BaseAgent` and relying on the existing `AgentRegistry`, `ToolRegistry`, and `MemoryService`. It operates provider-agnostically.
