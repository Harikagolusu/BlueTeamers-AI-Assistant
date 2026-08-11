import json
from typing import Dict, Any
from datetime import datetime, timezone
from app.observability.interfaces.i_logging import ILogFormatter

class JSONLogFormatter(ILogFormatter):
    def format(self, level: str, message: str, context: Dict[str, Any]) -> str:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "message": message,
            "correlation_id": context.get("correlation_id"),
            "trace_id": context.get("trace_id"),
            "tenant": context.get("tenant"),
            "user": context.get("user")
        }
        # Merge extra args safely
        if "metadata" in context:
            record.update(context["metadata"])
            
        return json.dumps(record)
