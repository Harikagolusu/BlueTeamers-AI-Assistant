import pytest
import asyncio
from app.observability.health.registry import HealthRegistry
from app.observability.health.probes import DatabaseProbe, LLMProviderProbe
from app.observability.health.scheduler import HealthMonitor, AsyncHealthScheduler

@pytest.mark.asyncio
async def test_health_scheduler():
    reg = HealthRegistry()
    reg.register_check("db", DatabaseProbe())
    reg.register_check("llm", LLMProviderProbe())
    
    monitor = HealthMonitor()
    scheduler = AsyncHealthScheduler(reg, monitor, interval_seconds=1)
    
    # Run once manually to avoid waiting
    await scheduler._run_checks()
    
    status = monitor.get_status()
    assert status["status"] == "Healthy"
    assert status["components"]["db"]["status"] == "Healthy"
