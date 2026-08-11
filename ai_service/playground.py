import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.services.workflow.workflow_engine import WorkflowEngine
from app.services.workflow.workflow_builder import WorkflowBuilder
from app.services.capabilities.capability_registry import CapabilityRegistry
from app.services.capabilities.capability_resolver import CapabilityResolver
from app.services.capabilities.capability import Capability
from app.services.orchestration.service import AgentOrchestrationService
from app.agents.base_interfaces import IAgentRegistry, IAgent
from app.agents.context import AgentContext, ExecutionContext, UserContext, ConversationContext
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("playground")

class DummyRegistry(IAgentRegistry):
    def register(self, name, agent): pass
    def get(self, name): return None
    def discover(self): return []
    def list(self): return []
    def filter(self, capabilities): return []
    def unregister(self, name): pass
    def reload(self): pass

async def main():
    logger.info("Initializing Developer Playground...")
    
    # 1. Setup minimal dependencies
    agent_registry = DummyRegistry()
    cap_registry = CapabilityRegistry(agent_registry)
    cap_resolver = CapabilityResolver(cap_registry)
    orchestration_service = AgentOrchestrationService(agent_registry, cap_resolver)
    
    logger.info("Playground environment ready. You can test workflow, capabilities, and orchestration here.")
    
    print("\n--- Developer Playground ---")
    print("Dependencies loaded successfully.")
    print("Ready for modular manual testing.")
    print("----------------------------\n")
    
if __name__ == "__main__":
    asyncio.run(main())
