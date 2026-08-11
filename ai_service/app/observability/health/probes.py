from typing import Dict, Any
from app.observability.interfaces.i_health import IHealthCheck

class DatabaseProbe(IHealthCheck):
    async def check_health(self) -> Dict[str, Any]:
        # Stub logic
        return {"status": "Healthy", "latency_ms": 10}

class LLMProviderProbe(IHealthCheck):
    async def check_health(self) -> Dict[str, Any]:
        return {"status": "Healthy", "latency_ms": 120}

class CacheProbe(IHealthCheck):
    async def check_health(self) -> Dict[str, Any]:
        return {"status": "Healthy", "latency_ms": 2}
