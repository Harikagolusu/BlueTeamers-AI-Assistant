from typing import List, Dict, Optional
import threading
from app.agents.interfaces.i_templates import ITemplateRegistry
from app.agents.models.agent_package import AgentPackage

class TemplateRegistry(ITemplateRegistry):
    def __init__(self):
        self._templates: Dict[str, AgentPackage] = {}
        self._lock = threading.RLock()

    def register_template(self, template_id: str, package: AgentPackage) -> None:
        with self._lock:
            self._templates[template_id] = package

    def get_template(self, template_id: str) -> Optional[AgentPackage]:
        with self._lock:
            return self._templates.get(template_id)

    def list_templates(self) -> List[AgentPackage]:
        with self._lock:
            return list(self._templates.values())
