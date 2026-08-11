# Investigation Agent Tool Matrix

The Investigation Agent utilizes the following tools during its `execute_tools` lifecycle phase.

| Tool Name | Purpose | Inputs | Outputs | Selection Condition |
|-----------|---------|--------|---------|---------------------|
| **EvidenceCollectionTool** | Normalizes uploaded raw evidence and organizes artifacts. | `raw_evidence`: List[Dict] | `EvidenceCollection` | Always executed first if raw evidence is present. |
| **EvidenceCorrelationTool** | Correlates timestamps, hosts, IPs, process trees, and network sessions. | `evidence_items`: List[Dict] | `EvidenceCorrelation` | Executed if normalized evidence is successfully collected. |
| **InvestigationPlanningTool** | Determines investigation sequence and which expert agents to invoke. | `evidence_types`: List[str] | Investigation Plan (Dict) | Always executed after correlation to plan expert delegation. |
| **IncidentTimelineTool** | Generates a chronologically ordered MITRE ATT&CK timeline. | `correlated_data`: Dict | `Timeline` | Executed after expert agents return findings. |
| **InvestigationSummaryTool** | Generates the Executive Summary, findings, and recommendations. | `investigation_context`: Dict | `InvestigationSummary` | Executed before the final LLM reasoning step. |
