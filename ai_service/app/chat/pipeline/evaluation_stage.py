"""Evaluation stage: annotates every chat response with quality/hallucination
telemetry computed from the final answer (no extra LLM call)."""
from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.evaluation.metrics import calculate_metrics
from app.evaluation.quality import evaluate_quality
from app.evaluation.hallucination import detect_hallucination


class EvaluationStage(IExecutionStage):
    """Runs after the engines produce a final answer and before composition."""

    @property
    def name(self) -> str:
        return "Evaluation"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        result = context.metadata.get("execution_result")
        if not result or getattr(result, "stream", False):
            return context

        text = result.message or ""
        citations = list(result.citations or [])
        query = context.metadata.get("query", "")

        metrics = calculate_metrics(text, citations, query)
        quality = evaluate_quality(text, query=query, citations=citations)
        hallucination = detect_hallucination(text, citations)

        score = round(0.6 * quality["score"] + 0.4 * hallucination["score"], 3)
        if score >= 0.8:
            label = "excellent"
        elif score >= 0.6:
            label = "good"
        elif score >= 0.4:
            label = "fair"
        else:
            label = "poor"

        evaluation = {
            "metrics": metrics,
            "quality": quality,
            "hallucination": hallucination,
            "score": score,
            "label": label,
        }

        new_result = result.model_copy(
            update={"metadata": {**result.metadata, "evaluation": evaluation}}
        )
        new_metadata = {
            **context.metadata,
            "execution_result": new_result,
            "evaluation": evaluation,
        }
        return context.model_copy(update={"metadata": new_metadata})
