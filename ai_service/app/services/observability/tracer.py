import logging
import uuid
import time
from typing import Optional, Dict
from app.services.observability.models import TraceNode, TraceNodeType, TraceGraph

logger = logging.getLogger(__name__)

class ExecutionTracer:
    """
    Traces execution graphs across workflows, agents, tools, LLMs, and memory.
    """
    def __init__(self):
        self.active_traces: Dict[str, TraceGraph] = {}
        
    def start_trace(self, name: str, node_type: TraceNodeType, attributes: Optional[Dict] = None) -> TraceGraph:
        trace_id = str(uuid.uuid4())
        root = TraceNode(
            node_id=str(uuid.uuid4()),
            node_type=node_type,
            name=name,
            start_time=time.time(),
            attributes=attributes or {}
        )
        graph = TraceGraph(trace_id=trace_id, root=root)
        self.active_traces[trace_id] = graph
        return graph
        
    def start_span(self, parent_node: TraceNode, name: str, node_type: TraceNodeType, attributes: Optional[Dict] = None) -> TraceNode:
        child = TraceNode(
            node_id=str(uuid.uuid4()),
            node_type=node_type,
            name=name,
            start_time=time.time(),
            attributes=attributes or {}
        )
        parent_node.add_child(child)
        return child
        
    def end_span(self, node: TraceNode, success: bool, **kwargs) -> None:
        node.complete(success, **kwargs)
        
    def end_trace(self, trace_id: str, success: bool, **kwargs) -> Optional[TraceGraph]:
        if trace_id not in self.active_traces:
            logger.warning(f"Trace {trace_id} not found when ending trace.")
            return None
            
        graph = self.active_traces[trace_id]
        graph.root.complete(success, **kwargs)
        
        # In a real system, you'd export the graph to Jaeger, OpenTelemetry, etc.
        logger.info(f"Completed trace {trace_id} for {graph.root.name} (Success: {success})")
        
        return self.active_traces.pop(trace_id)
