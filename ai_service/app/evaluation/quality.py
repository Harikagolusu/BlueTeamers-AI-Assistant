"""Heuristic answer-quality evaluation for chat responses.

Scores a final answer on substance (verbosity) and grounding (presence of
citations) without calling the LLM again. Returns a 0-1 score plus a label.
"""
from typing import Any, Dict, List, Optional

from app.evaluation.metrics import calculate_metrics


def evaluate_quality(
    response_text: str = "",
    query: str = "",
    citations: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Evaluate the quality of a chat answer on a 0-1 scale."""
    metrics = calculate_metrics(response_text, citations, query)
    word_count = metrics["word_count"]
    has_citations = metrics["has_citations"]

    substance = min(1.0, word_count / 40.0)
    grounding = 1.0 if has_citations else 0.35

    score = round(0.6 * substance + 0.4 * grounding, 3)

    if score >= 0.8:
        label = "excellent"
    elif score >= 0.6:
        label = "good"
    elif score >= 0.4:
        label = "fair"
    else:
        label = "poor"

    checks = [
        {
            "check": "substantive_answer",
            "passed": word_count >= 15,
            "detail": f"{word_count} words",
        },
        {
            "check": "grounded_in_sources",
            "passed": has_citations,
            "detail": f"{metrics['citation_count']} citation(s)",
        },
        {
            "check": "reasonable_length",
            "passed": 0 < word_count <= 1500,
            "detail": f"{word_count} words",
        },
    ]

    return {
        "score": score,
        "label": label,
        "substance_score": round(substance, 3),
        "grounding_score": grounding,
        "checks": checks,
    }
