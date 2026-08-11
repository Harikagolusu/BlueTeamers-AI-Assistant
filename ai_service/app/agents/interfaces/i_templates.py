from abc import ABC, abstractmethod
from typing import List, Optional
from app.agents.models.agent_package import AgentPackage

class ITemplateRegistry(ABC):
    @abstractmethod
    def register_template(self, template_id: str, package: AgentPackage) -> None: pass
    @abstractmethod
    def get_template(self, template_id: str) -> Optional[AgentPackage]: pass
    @abstractmethod
    def list_templates(self) -> List[AgentPackage]: pass
