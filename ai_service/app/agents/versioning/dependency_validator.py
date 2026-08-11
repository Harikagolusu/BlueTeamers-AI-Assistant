from typing import List
from app.agents.models.agent_package import AgentPackage

class DependencyValidator:
    """
    Validates that all external dependencies required by a package are satisfied.
    """
    def validate_dependencies(self, package: AgentPackage, installed_packages: List[str]) -> bool:
        for dep in package.manifest.dependencies:
            if dep not in installed_packages:
                return False
        return True
