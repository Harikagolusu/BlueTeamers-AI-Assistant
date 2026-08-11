from app.agents.models.agent_package import AgentPackage
from app.agents.interfaces.i_manifest_validator import IManifestValidator

class PackageValidator:
    def __init__(self, manifest_validator: IManifestValidator):
        self._manifest_validator = manifest_validator
        
    def validate_package(self, package: AgentPackage) -> bool:
        if not self._manifest_validator.validate_agent_manifest(package.manifest.dict()):
            return False
        return True
