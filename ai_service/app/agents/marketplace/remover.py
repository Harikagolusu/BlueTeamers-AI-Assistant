from app.agents.interfaces.i_marketplace import IMarketplaceRepository
from app.agents.interfaces.i_packages import IPackageInstaller

class AgentRemover:
    def __init__(self, repository: IMarketplaceRepository, package_installer: IPackageInstaller):
        self._repository = repository
        self._package_installer = package_installer
        
    def remove(self, package_id: str) -> None:
        self._package_installer.uninstall_package_contents(package_id)
        self._repository.remove_package(package_id)
