from abc import ABC, abstractmethod
from typing import List, Optional
from app.agents.models.agent_package import AgentPackage

class IMarketplaceRepository(ABC):
    @abstractmethod
    def save_package(self, package: AgentPackage) -> None: pass
    @abstractmethod
    def remove_package(self, package_id: str) -> None: pass
    @abstractmethod
    def get_package(self, package_id: str) -> Optional[AgentPackage]: pass
    @abstractmethod
    def list_packages(self) -> List[AgentPackage]: pass
    @abstractmethod
    def set_enabled_state(self, package_id: str, enabled: bool) -> None: pass
    @abstractmethod
    def is_enabled(self, package_id: str) -> bool: pass

class IMarketplaceProvider(ABC):
    @abstractmethod
    def fetch_package(self, package_id: str, version: Optional[str] = None) -> AgentPackage: pass
    @abstractmethod
    def search(self, query: str) -> List[AgentPackage]: pass

class IAgentLifecycleManager(ABC):
    @abstractmethod
    def install(self, package: AgentPackage) -> None: pass
    @abstractmethod
    def remove(self, package_id: str) -> None: pass
    @abstractmethod
    def update(self, package_id: str, new_package: AgentPackage) -> None: pass
    @abstractmethod
    def enable(self, package_id: str) -> None: pass
    @abstractmethod
    def disable(self, package_id: str) -> None: pass
    @abstractmethod
    def restart(self, package_id: str) -> None: pass
    @abstractmethod
    def reload(self, package_id: str) -> None: pass

class IMarketplaceService(ABC):
    @abstractmethod
    def install_package(self, package_id: str, version: Optional[str] = None) -> None: pass
    @abstractmethod
    def remove_package(self, package_id: str) -> None: pass
    @abstractmethod
    def upgrade_package(self, package_id: str, version: str) -> None: pass
    @abstractmethod
    def downgrade_package(self, package_id: str, version: str) -> None: pass
    @abstractmethod
    def enable_package(self, package_id: str) -> None: pass
    @abstractmethod
    def disable_package(self, package_id: str) -> None: pass
    @abstractmethod
    def search_packages(self, query: str) -> List[AgentPackage]: pass
    @abstractmethod
    def list_installed_packages(self) -> List[AgentPackage]: pass
