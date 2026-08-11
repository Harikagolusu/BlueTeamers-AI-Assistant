from typing import List, Dict, Any
from app.agents.interfaces.i_aggregator import IAggregator
from app.models.chat.chat_models import ExecutionResult, ExecutionStatus

class Aggregator(IAggregator):
    """
    Merges outputs, removes duplicates, and preserves execution metadata from multiple agents.
    """
    def aggregate(self, results: List[ExecutionResult]) -> ExecutionResult:
        if not results:
            return ExecutionResult.failed("AGGREGATOR", [{"error": "No results to aggregate."}])

        messages = []
        citations = []
        documents = []
        tool_outputs = []
        aggregated_metadata: Dict[str, Any] = {
            "execution_times_ms": [],
            "confidences": [],
            "agent_ids": [],
            "tool_usages": []
        }
        cost = 0.0
        latency = 0.0
        all_success = True

        for result in results:
            if not result.success:
                all_success = False
            
            if result.message and result.message not in messages:
                messages.append(result.message)
                
            citations.extend(result.citations)
            documents.extend(result.documents)
            tool_outputs.extend(result.tool_outputs)
            
            cost += result.cost
            latency += result.latency_ms
            
            # Extract metadata
            if result.metadata:
                if "agent_id" in result.metadata:
                    aggregated_metadata["agent_ids"].append(result.metadata["agent_id"])
                if "confidence" in result.metadata:
                    aggregated_metadata["confidences"].append(result.metadata["confidence"])
                if "tool_usage" in result.metadata:
                    aggregated_metadata["tool_usages"].append(result.metadata["tool_usage"])
                    
        # Remove duplicates
        unique_citations = {c.get("url", str(i)): c for i, c in enumerate(citations)}.values()
        unique_docs = {d.get("id", str(i)): d for i, d in enumerate(documents)}.values()

        final_message = "\n\n".join(messages)
        
        status = ExecutionStatus.SUCCESS if all_success else ExecutionStatus.FAILED
        
        return ExecutionResult(
            status=status,
            engine_name="MULTI_AGENT_AGGREGATOR",
            message=final_message,
            metadata=aggregated_metadata,
            citations=list(unique_citations),
            documents=list(unique_docs),
            tool_outputs=tool_outputs,
            cost=cost,
            latency_ms=latency
        )
