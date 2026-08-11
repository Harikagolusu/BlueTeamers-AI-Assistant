from typing import Optional
from app.agents.registry.factory import AgentFactory
from app.agents.threat_intelligence.agent import ThreatIntelligenceAgent

from app.tools.registry.tool_registry import ToolRegistry
from app.agents.threat_intelligence.tools.ioc_lookup_tool import IOCLookupTool
from app.agents.threat_intelligence.tools.reputation_tool import ReputationTool
from app.agents.threat_intelligence.tools.threat_actor_tool import ThreatActorTool
from app.agents.threat_intelligence.tools.campaign_lookup_tool import CampaignLookupTool
from app.agents.threat_intelligence.tools.indicator_correlation_tool import IndicatorCorrelationTool
from app.agents.threat_intelligence.tools.mitre_mapping_tool import MITREMappingTool

from app.providers.threat_intelligence import provider_instance

def register_agent_and_tools(tool_registry: Optional[ToolRegistry] = None) -> None:
    """
    Registers the Threat Intelligence Agent with the AgentFactory,
    and registers all its tools with the provided ToolRegistry.
    """
    # 1. Register Agent
    AgentFactory.register_agent_class("threat_intelligence", ThreatIntelligenceAgent)
    
    # 2. Register Tools if registry is provided
    if tool_registry:
        tool_registry.register(IOCLookupTool(provider=provider_instance))
        tool_registry.register(ReputationTool(provider=provider_instance))
        tool_registry.register(ThreatActorTool(provider=provider_instance))
        tool_registry.register(CampaignLookupTool(provider=provider_instance))
        tool_registry.register(IndicatorCorrelationTool(provider=provider_instance))
        tool_registry.register(MITREMappingTool(provider=provider_instance))
