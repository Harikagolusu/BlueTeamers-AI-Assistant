from app.agents.interfaces.i_versioning import ICompatibilityResolver
from typing import Dict, Any

class CompatibilityResolver(ICompatibilityResolver):
    def check_compatibility(self, required_version: str, current_version: str) -> bool:
        # Basic semver compatibility logic (stubbed for prototype)
        # Typically would use `semver` or `packaging.version` package
        if required_version.startswith(">="):
            min_ver = required_version[2:]
            return current_version >= min_ver
        return current_version == required_version

    def validate_platform_compatibility(self, package_metadata: dict) -> bool:
        # Check against platform version
        req = package_metadata.get("platform_compatibility", ">=1.0.0")
        current_platform = "1.0.0"
        return self.check_compatibility(req, current_platform)
