import time
from typing import Dict, Any
from app.observability.interfaces.i_tracing import ISpan

class LocalSpan(ISpan):
    def __init__(self, name: str, trace_id: str, span_id: str, parent_id: str = None, on_end=None):
        self.name = name
        self.trace_id = trace_id
        self.span_id = span_id
        self.parent_id = parent_id
        self.attributes = {}
        self.events = []
        self.start_time = time.perf_counter()
        self.end_time = None
        self._on_end = on_end

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    def add_event(self, name: str, attributes: Dict[str, Any] = None) -> None:
        self.events.append({"name": name, "attributes": attributes, "time": time.perf_counter()})

    def end(self) -> None:
        self.end_time = time.perf_counter()
        if self._on_end:
            self._on_end(self)
