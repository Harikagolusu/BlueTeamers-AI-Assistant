from typing import Optional
from app.agents.registry.factory import AgentFactory
from app.agents.investigation.agent import InvestigationAgent

from app.tools.registry.tool_registry import ToolRegistry
from app.agents.investigation.tools import (
    EvidenceCollectionTool,
    EvidenceCorrelationTool,
    InvestigationPlanningTool,
    IncidentTimelineTool,
    InvestigationSummaryTool
)

def register_agent_and_tools(tool_registry: Optional[ToolRegistry] = None) -> None:
    """
    Registers the Investigation Agent with the AgentFactory,
    and registers all its tools with the provided ToolRegistry.
    """
    # 1. Register Agent
    AgentFactory.register_agent_class("investigation_agent", InvestigationAgent)
    
    # 2. Register Tools if registry is provided
    if tool_registry:
        tool_registry.register(EvidenceCollectionTool())
        tool_registry.register(EvidenceCorrelationTool())
        tool_registry.register(InvestigationPlanningTool())
        tool_registry.register(IncidentTimelineTool())
        tool_registry.register(InvestigationSummaryTool())
