import asyncio
from typing import List, Any
from app.observability.interfaces.i_alerts import IAlertManager, IAlertRule, INotifier

class AlertManager(IAlertManager):
    def __init__(self, notifier: INotifier):
        self._rules: List[IAlertRule] = []
        self._notifier = notifier

    def register_rule(self, rule: IAlertRule) -> None:
        self._rules.append(rule)

    def process_alerts(self, metrics: Any) -> None:
        for rule in self._rules:
            alert = rule.evaluate(metrics)
            if alert:
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(self._notifier.notify(alert))
                except RuntimeError:
                    asyncio.run(self._notifier.notify(alert))
