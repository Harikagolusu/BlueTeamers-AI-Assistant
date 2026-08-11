import pytest
from app.tools.context import ToolContext
from app.providers.threat_intelligence.mock_provider import MockThreatIntelligenceProvider
from app.agents.threat_intelligence.tools.ioc_lookup_tool import IOCLookupTool
from app.agents.threat_intelligence.tools.reputation_tool import ReputationTool
from app.agents.threat_intelligence.tools.threat_actor_tool import ThreatActorTool
from app.agents.threat_intelligence.tools.campaign_lookup_tool import CampaignLookupTool
from app.agents.threat_intelligence.tools.indicator_correlation_tool import IndicatorCorrelationTool
from app.agents.threat_intelligence.tools.mitre_mapping_tool import MITREMappingTool

@pytest.fixture
def provider():
    return MockThreatIntelligenceProvider()

@pytest.fixture
def context():
    return ToolContext()

@pytest.mark.asyncio
async def test_ioc_lookup_tool(provider, context):
    tool = IOCLookupTool(provider=provider)
    res = await tool.execute(context, indicator="8.8.8.8")
    assert res["value"] == "8.8.8.8"
    assert res["malicious"] is False

    res = await tool.execute(context, indicator="44d88612fea8a8f36de82e1278abb02f")
    assert res["malicious"] is True

@pytest.mark.asyncio
async def test_reputation_tool(provider, context):
    tool = ReputationTool(provider=provider)
    res = await tool.execute(context, indicator="8.8.8.8")
    assert res["risk_level"] == "LOW"

    res = await tool.execute(context, indicator="44d88612fea8a8f36de82e1278abb02f")
    assert res["risk_level"] == "HIGH"

@pytest.mark.asyncio
async def test_threat_actor_tool(provider, context):
    tool = ThreatActorTool(provider=provider)
    res = await tool.execute(context, actor_name="APT29")
    assert "SolarWinds" in res["campaigns"]

@pytest.mark.asyncio
async def test_campaign_lookup_tool(provider, context):
    tool = CampaignLookupTool(provider=provider)
    res = await tool.execute(context, campaign_name="SolarWinds")
    assert "APT29" in res["threat_actors"]

@pytest.mark.asyncio
async def test_indicator_correlation_tool(provider, context):
    tool = IndicatorCorrelationTool(provider=provider)
    res = await tool.execute(context, indicators=["8.8.8.8", "44d88612fea8a8f36de82e1278abb02f"])
    assert "malicious" in res["relationships"]
    assert res["confidence"] == 85

@pytest.mark.asyncio
async def test_mitre_mapping_tool(provider, context):
    tool = MITREMappingTool(provider=provider)
    res = await tool.execute(context, entity="T1003")
    assert len(res) == 1
    assert res[0]["technique_name"] == "OS Credential Dumping"
    
    res_actor = await tool.execute(context, entity="APT29")
    assert len(res_actor) > 0
