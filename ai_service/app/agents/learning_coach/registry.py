from typing import Optional, Any
from app.agents.base_interfaces import IAgentRegistry
from app.agents.manifests.models import AgentManifest
from app.agents.learning_coach.agent import LearningCoachAgent
from app.agents.learning_coach.prompts import get_prompts
import yaml
import os
import logging

logger = logging.getLogger(__name__)

try:
    from app.services.capabilities.capability import Capability
    from app.services.capabilities.capability_registry import CapabilityRegistry, ProviderRegistration
except ImportError:
    Capability = None
    CapabilityRegistry = None
    ProviderRegistration = None

try:
    from app.prompts.manager import PromptManager
except ImportError:
    PromptManager = None

def register_capabilities(cap_registry: Any, manifest: AgentManifest) -> None:
    if cap_registry and Capability and ProviderRegistration:
        try:
            capabilities = [
                "LEARNING_COACHING",
                "ROADMAP_GENERATION",
                "SKILL_ANALYSIS",
                "LEARNING_ANALYTICS"
            ]
            for cap in capabilities:
                cap_registry.register(
                    getattr(Capability, cap, cap), 
                    ProviderRegistration(agent_name=manifest.name, priority=1)
                )
            logger.info(f"Registered capabilities for {manifest.name}")
        except Exception as e:
            logger.error(f"Capability registration failed: {e}")

def register_prompts(prompt_manager: Optional[Any]) -> None:
    if not prompt_manager:
        logger.warning("PromptManager is unavailable. Skipping prompt registration.")
        return

    prompts = get_prompts()
    seen_ids = set()

    for p in prompts:
        if p.id in seen_ids:
            continue
        seen_ids.add(p.id)

        if hasattr(prompt_manager, "register"):
            prompt_manager.register(p)
    
    logger.info(f"Learning Coach | Registered | {len(prompts)} prompts")

def register_agent(agent_registry: IAgentRegistry, cap_registry: Any = None, prompt_manager: Any = None) -> None:
    manifest_path = os.path.join(os.path.dirname(__file__), "manifest.yaml")
    
    try:
        with open(manifest_path, "r") as f:
            manifest_data = yaml.safe_load(f)
            manifest = AgentManifest(**manifest_data)
            
        agent = LearningCoachAgent(manifest)
        agent_registry.register(manifest.name, agent)
        logger.info(f"Registered agent: {manifest.name}")
        
        register_capabilities(cap_registry, manifest)
        register_prompts(prompt_manager)
            
    except Exception as e:
        logger.error(f"Failed to register Learning Coach Agent: {e}")
