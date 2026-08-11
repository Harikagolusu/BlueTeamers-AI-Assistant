import asyncio
import threading
from typing import Dict, Any
from app.observability.interfaces.i_health import IHealthScheduler, IHealthRegistry, IHealthMonitor
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import AgentEvent

class HealthCheckPassedEvent(AgentEvent):
    type: str = "HealthCheckPassed"
    component: str

class HealthCheckFailedEvent(AgentEvent):
    type: str = "HealthCheckFailed"
    component: str
    reason: str

class HealthMonitor(IHealthMonitor):
    def __init__(self):
        self._cache = {}
        self._lock = threading.RLock()

    def update_status(self, name: str, status: Dict[str, Any]):
        with self._lock:
            self._cache[name] = status
            
    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            overall = "Healthy"
            for status in self._cache.values():
                if status.get("status") == "Unhealthy":
                    overall = "Unhealthy"
                    break
                if status.get("status") == "Degraded":
                    overall = "Degraded"
            return {"status": overall, "components": self._cache.copy()}

class AsyncHealthScheduler(IHealthScheduler):
    def __init__(self, registry: IHealthRegistry, monitor: HealthMonitor, interval_seconds: int = 60):
        self._registry = registry
        self._monitor = monitor
        self._interval = interval_seconds
        self._task = None

    def start(self) -> None:
        if self._task is None:
            loop = asyncio.get_running_loop()
            self._task = loop.create_task(self._run_loop())

    def stop(self) -> None:
        if self._task:
            self._task.cancel()
            self._task = None

    async def _run_loop(self):
        try:
            while True:
                await self._run_checks()
                await asyncio.sleep(self._interval)
        except asyncio.CancelledError:
            pass

    async def _run_checks(self):
        checks = self._registry.get_checks()
        for name, check in checks.items():
            try:
                res = await check.check_health()
                self._monitor.update_status(name, res)
                
                if res.get("status") == "Unhealthy":
                    agent_event_bus.publish(HealthCheckFailedEvent(session_id="sys", component=name, reason="Probe returned unhealthy"))
                else:
                    agent_event_bus.publish(HealthCheckPassedEvent(session_id="sys", component=name))
                    
            except Exception as e:
                self._monitor.update_status(name, {"status": "Unhealthy", "error": str(e)})
                agent_event_bus.publish(HealthCheckFailedEvent(session_id="sys", component=name, reason=str(e)))
