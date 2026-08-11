import logging
import threading
from typing import List, Dict, Optional, Any
from app.agents.base_interfaces import IAgent, IAgentRegistry as ILegacyAgentRegistry
from app.agents.interfaces.i_agent_registry import IAgentRegistry as INewAgentRegistry
from app.agents.models.agent_descriptor import AgentDescriptor

logger = logging.getLogger(__name__)

class AgentRegistry(ILegacyAgentRegistry, INewAgentRegistry):
    """
    Centralized catalog of available agents.
    Supports both legacy instantiated IAgent registration and the new metadata-based AgentDescriptor registration.
    Thread-safe implementation using RLock.
    """
    def __init__(self):
        self._agents: Dict[str, IAgent] = {}
        self._descriptors: Dict[str, AgentDescriptor] = {}
        self._lock = threading.RLock()

    # --- Hybrid Registration (Supports both APIs) ---

    def register(self, name_or_agent: Any, agent: Optional[IAgent] = None) -> None:
        """
        Overloaded registration method to support both architectures.
        Legacy API: register(name: str, agent: IAgent)
        New API: register(agent: AgentDescriptor)
        """
        with self._lock:
            if isinstance(name_or_agent, AgentDescriptor):
                self._descriptors[name_or_agent.agent_id] = name_or_agent
            elif isinstance(name_or_agent, str) and agent is not None:
                self._agents[name_or_agent] = agent
                
                # Auto-derive a lightweight descriptor to ensure it's available to the new API
                capabilities = getattr(getattr(agent, "manifest", None), "capabilities", [])
                desc = AgentDescriptor(
                    agent_id=name_or_agent,
                    name=getattr(getattr(agent, "manifest", None), "name", name_or_agent),
                    description=getattr(getattr(agent, "manifest", None), "description", ""),
                    version=getattr(getattr(agent, "manifest", None), "version", "1.0.0"),
                    capabilities=capabilities
                )
                self._descriptors[name_or_agent] = desc
                logger.info(f"Registered agent (legacy): {name_or_agent}")

    def unregister(self, name_or_id: str) -> None:
        """Unregister an agent by ID/name from both internal stores."""
        with self._lock:
            if name_or_id in self._agents:
                del self._agents[name_or_id]
                logger.info(f"Unregistered agent (legacy): {name_or_id}")
            if name_or_id in self._descriptors:
                del self._descriptors[name_or_id]

    # --- Legacy IAgent API ---

    def get(self, name: str) -> Optional[IAgent]:
        with self._lock:
            return self._agents.get(name)

    def discover(self) -> List[IAgent]:
        with self._lock:
            return list(self._agents.values())

    def list(self) -> List[str]:
        with self._lock:
            return list(self._agents.keys())

    def filter(self, capabilities: List[str]) -> List[IAgent]:
        matched = []
        with self._lock:
            for agent in self._agents.values():
                if hasattr(agent, "manifest") and agent.manifest:
                    agent_caps = getattr(agent.manifest, "capabilities", [])
                    if all(cap in agent_caps for cap in capabilities):
                        matched.append(agent)
        return matched

    def reload(self) -> None:
        logger.info("Agent Registry reloaded")


    # --- New AgentDescriptor API (Module 8) ---

    def get_agent(self, agent_id: str) -> Optional[AgentDescriptor]:
        with self._lock:
            return self._descriptors.get(agent_id)

    def list_agents(self) -> List[AgentDescriptor]:
        with self._lock:
            return list(self._descriptors.values())

    def get_agents_by_capability(self, capability: str) -> List[AgentDescriptor]:
        with self._lock:
            results = []
            for agent in self._descriptors.values():
                # agent.capabilities might be objects or strings; handle both
                for cap in agent.capabilities:
                    if hasattr(cap, "capability_name") and cap.capability_name == capability:
                        results.append(agent)
                        break
                    elif isinstance(cap, str) and cap == capability:
                        results.append(agent)
                        break
            return results
