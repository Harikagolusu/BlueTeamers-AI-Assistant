from app.agents.models.agent_package import AgentPackage
from app.agents.interfaces.i_marketplace import IMarketplaceRepository
from app.agents.interfaces.i_packages import IPackageInstaller

class AgentInstaller:
    def __init__(self, repository: IMarketplaceRepository, package_installer: IPackageInstaller):
        self._repository = repository
        self._package_installer = package_installer
        
    def install(self, package: AgentPackage) -> None:
        self._package_installer.install_package_contents(package)
        self._repository.save_package(package)
