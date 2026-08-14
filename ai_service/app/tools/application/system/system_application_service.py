import os
import platform
import sys
from urllib.parse import urlparse
from app.core.config import settings
from app.tools.application.interfaces.i_system_service import ISystemService
from app.tools.infrastructure.base.base_service import BaseService
from app.tools.domain.schemas.system_schemas import (
    EnvironmentSchema, ConfigSchema, PlatformSchema, VersionSchema
)
from app.tools.domain.results.system_results import (
    EnvironmentResult, ConfigResult, PlatformResult, VersionResult
)

class SystemApplicationService(BaseService, ISystemService):
    async def _on_initialize(self) -> None:
        self._logger.info("Initializing SystemApplicationService")

    async def get_environment(self, schema: EnvironmentSchema) -> EnvironmentResult:
        # Never dump arbitrary environment variables (they may contain secrets).
        # Only a small allow-list of harmless variables is ever returned,
        # regardless of what the caller requests.
        safe_keys = ["PATH", "USER", "LANG", "HOME", "OS", "SHELL", "TERM"]
        if schema.keys:
            keys = [k for k in schema.keys if k in safe_keys]
        else:
            keys = safe_keys
        env_vars = {k: os.environ.get(k, "") for k in keys}
        return EnvironmentResult(environment_variables=env_vars)

    def _database_config(self) -> dict:
        """Derive database config from POSTGRES_URL (no hardcoded host/port)."""
        url = settings.POSTGRES_URL or ""
        parsed = urlparse(url)
        if parsed.hostname:
            return {
                "host": parsed.hostname,
                "port": parsed.port or 5432,
                "dbname": (parsed.path or "/").lstrip("/"),
            }
        return {}

    async def get_config(self, schema: ConfigSchema) -> ConfigResult:
        mock_config = {
            "database": self._database_config(),
            "security": {"tls_enabled": not settings.is_development},
        }
        val = mock_config.get(schema.section, {})
        return ConfigResult(config_values=val)

    async def get_platform(self, schema: PlatformSchema) -> PlatformResult:
        return PlatformResult(
            os_name=platform.system(),
            python_version=platform.python_version(),
            architecture=platform.machine()
        )

    async def get_version(self, schema: VersionSchema) -> VersionResult:
        return VersionResult(
            app_version=settings.APP_VERSION,
            api_version="v1"
        )
