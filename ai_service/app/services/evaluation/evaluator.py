import logging
from typing import List
from app.services.evaluation.models import ExecutionEvaluation, WorkflowEvaluation, ToolEvaluation, CapabilityEvaluation

logger = logging.getLogger(__name__)

class ExecutionEvaluator:
    """
    Evaluates workflow execution, capability routing, tool selection, 
    retry behavior, latency, cost, and recovery.
    """
    def __init__(self):
        self._history: List[ExecutionEvaluation] = []
        
    def record_evaluation(self, eval_result: ExecutionEvaluation) -> None:
        """
        Records the evaluation. Can be sent to observability layers.
        """
        self._history.append(eval_result)
        logger.info(f"Recorded evaluation for execution {eval_result.execution_id} (Agent: {eval_result.agent_name})")
        if not eval_result.recovery_successful:
            logger.warning(f"Execution {eval_result.execution_id} failed to recover from errors.")
            
    def get_evaluations(self) -> List[ExecutionEvaluation]:
        return self._history
