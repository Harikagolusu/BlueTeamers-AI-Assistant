"""Heuristic hallucination / groundedness detection for chat answers.

Uses retrieval-grounding signals (citation presence and average similarity) to
flag responses that make substantive claims without supporting sources.
"""
from typing import Any, Dict, List, Optional

from app.evaluation.metrics import calculate_metrics

_RISK_SCORE = {"low": 0.0, "medium": 0.5, "high": 1.0}


def detect_hallucination(
    response_text: str = "",
    citations: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Estimate hallucination risk for a chat answer on a 0-1 safety scale."""
    metrics = calculate_metrics(response_text, citations)
    word_count = metrics["word_count"]
    has_citations = metrics["has_citations"]
    avg_similarity = metrics["avg_similarity"]

    if word_count < 5:
        risk = "low"
        reasons = ["Response is too short to assert unsupported claims."]
    elif not has_citations:
        risk = "high"
        reasons = ["Substantive response without any retrieved grounding (no citations)."]
    elif avg_similarity is not None and avg_similarity >= 0.6:
        risk = "low"
        reasons = ["Response is grounded in retrieved sources with strong similarity."]
    elif avg_similarity is not None and avg_similarity >= 0.4:
        risk = "medium"
        reasons = ["Citations present but average retrieval similarity is moderate."]
    else:
        risk = "high"
        reasons = ["Citations present but low retrieval similarity — weak grounding."]

    return {
        "risk": risk,
        "score": round(1.0 - _RISK_SCORE[risk], 2),
        "reasons": reasons,
    }
