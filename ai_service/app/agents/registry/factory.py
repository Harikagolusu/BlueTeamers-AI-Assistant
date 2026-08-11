from app.agents.base import BaseAgent
from app.agents.manifests.models import AgentManifest
from typing import Type, Dict

class AgentFactory:
    """
    Factory to decouple Agent instantiation from the Registry.
    Constructs agents dynamically based on Manifest definitions.
    """
    _agent_classes: Dict[str, Type[BaseAgent]] = {}

    @classmethod
    def register_agent_class(cls, name: str, agent_class: Type[BaseAgent]):
        cls._agent_classes[name] = agent_class

    @classmethod
    def create_agent(cls, manifest: AgentManifest) -> BaseAgent:
        agent_class = cls._agent_classes.get(manifest.name)
        if not agent_class:
            raise ValueError(f"No agent class registered for {manifest.name}. Cannot instantiate.")
        return agent_class(manifest)
