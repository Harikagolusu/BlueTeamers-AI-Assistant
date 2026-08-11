from app.agents.models.agent_package import AgentPackage
from app.agents.interfaces.i_marketplace import IMarketplaceRepository
from app.agents.interfaces.i_packages import IPackageInstaller

class AgentUpdater:
    def __init__(self, repository: IMarketplaceRepository, package_installer: IPackageInstaller):
        self._repository = repository
        self._package_installer = package_installer
        
    def update(self, package_id: str, new_package: AgentPackage) -> None:
        # Simplistic approach: remove and install
        self._package_installer.uninstall_package_contents(package_id)
        self._repository.remove_package(package_id)
        
        self._package_installer.install_package_contents(new_package)
        self._repository.save_package(new_package)
