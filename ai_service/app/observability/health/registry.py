from typing import Dict
from app.observability.interfaces.i_health import IHealthRegistry, IHealthCheck

class HealthRegistry(IHealthRegistry):
    def __init__(self):
        self._checks: Dict[str, IHealthCheck] = {}

    def register_check(self, name: str, check: IHealthCheck) -> None:
        self._checks[name] = check

    def get_checks(self) -> Dict[str, IHealthCheck]:
        return self._checks
