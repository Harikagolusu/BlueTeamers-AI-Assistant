from app.agents.interfaces.i_packages import IPackageManager
from app.agents.models.agent_package import AgentPackage
from app.agents.packages.package_validator import PackageValidator

class PackageManager(IPackageManager):
    def __init__(self, validator: PackageValidator):
        self._validator = validator
        
    def validate_package(self, package: AgentPackage) -> bool:
        return self._validator.validate_package(package)
