import pytest
from app.tools.context import ToolContext
from app.agents.investigation.tools import (
    EvidenceCollectionTool,
    EvidenceCorrelationTool,
    InvestigationPlanningTool,
    IncidentTimelineTool,
    InvestigationSummaryTool
)

@pytest.fixture
def context():
    return ToolContext()

@pytest.mark.asyncio
async def test_evidence_collection_tool(context):
    tool = EvidenceCollectionTool()
    raw = [{"type": "log", "content": "login failed"}, {"type": "alert", "content": "malware detected"}]
    res = await tool.execute(context, raw_evidence=raw)
    assert res["total_count"] == 2
    assert len(res["items"]) == 2

@pytest.mark.asyncio
async def test_evidence_correlation_tool(context):
    tool = EvidenceCorrelationTool()
    evidence_items = [
        {"id": "1", "content": "ip 1.1.1.1 accessed"},
        {"id": "2", "content": "user admin logged in"}
    ]
    res = await tool.execute(context, evidence_items=evidence_items)
    assert "1" in res["correlated_entities"]["ips"]
    assert "2" in res["correlated_entities"]["users"]

@pytest.mark.asyncio
async def test_investigation_planning_tool(context):
    tool = InvestigationPlanningTool()
    res = await tool.execute(context, evidence_types=["log", "ioc"])
    assert "soc_analyst" in res["required_expert_agents"]
    assert "threat_intelligence" in res["required_expert_agents"]
    assert res["confidence_score"] == 95

@pytest.mark.asyncio
async def test_incident_timeline_tool(context):
    tool = IncidentTimelineTool()
    res = await tool.execute(context, correlated_data={"correlation": {}, "ti": []})
    assert len(res["events"]) > 0
    assert res["events"][0]["event_type"] == "Initial Access"

@pytest.mark.asyncio
async def test_investigation_summary_tool(context):
    tool = InvestigationSummaryTool()
    res = await tool.execute(context, investigation_context={"plan": {}, "correlation": {}})
    assert "executive_summary" in res
    assert res["confidence"] == 90
