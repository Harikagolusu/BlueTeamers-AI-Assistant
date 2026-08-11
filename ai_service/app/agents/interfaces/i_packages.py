from abc import ABC, abstractmethod
from typing import List
from app.agents.models.agent_package import AgentPackage

class IPackageInstaller(ABC):
    @abstractmethod
    def install_package_contents(self, package: AgentPackage) -> None:
        pass
    
    @abstractmethod
    def uninstall_package_contents(self, package_id: str) -> None:
        pass

class IPackageManager(ABC):
    @abstractmethod
    def validate_package(self, package: AgentPackage) -> bool:
        pass
