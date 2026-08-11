# Tool Matrix

The following tools are available to the Threat Intelligence Agent. They form the core execution capabilities ("hands") of the agent.

| Tool Name | Description | Inputs | Outputs | Capabilities |
| :--- | :--- | :--- | :--- | :--- |
| `ioc_lookup_tool` | Looks up Indicators of Compromise | `indicator` (string) | IOC metadata (dict) | `threat_intelligence` |
| `reputation_tool` | Analyzes risk and reputation | `indicator` (string) | Risk assessment (dict) | `threat_intelligence` |
| `threat_actor_tool` | Looks up threat actors and TTPs | `actor_name` (string) | Actor details (dict) | `threat_intelligence` |
| `campaign_lookup_tool` | Looks up known campaigns | `campaign_name` (string) | Campaign details (dict) | `threat_intelligence` |
| `indicator_correlation_tool` | Correlates multiple indicators | `indicators` (list) | Correlation results (dict) | `threat_intelligence` |
| `mitre_mapping_tool` | Maps entities to MITRE ATT&CK | `entity` (string) | Mapped techniques (list) | `threat_intelligence` |

All tools rely on the `ThreatIntelligenceProvider` interface to resolve queries provider-agnostically.
