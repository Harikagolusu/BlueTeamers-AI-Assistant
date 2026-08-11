from typing import Dict, Any
from app.observability.interfaces.i_diagnostics import IDiagnosticsAnalyzer
from app.observability.diagnostics.snapshots import DiagnosticSnapshot
import uuid

class DiagnosticsAnalyzer(IDiagnosticsAnalyzer):
    def create_snapshot(self, context: Any) -> Dict[str, Any]:
        snapshot = DiagnosticSnapshot(
            snapshot_id=str(uuid.uuid4()),
            correlation_id=context.get("correlation_id", "unknown"),
            trace_data=context.get("trace", {}),
            logs=context.get("logs", []),
            metrics=context.get("metrics", []),
            timeline=context.get("timeline", [])
        )
        return snapshot.model_dump()
