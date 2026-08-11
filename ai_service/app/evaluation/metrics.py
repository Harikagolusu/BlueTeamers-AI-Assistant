"""Lightweight response metrics computed over the final chat answer.

These are deterministic, in-process heuristics (no extra LLM call) used to
annotate every chat response with basic grounding/quality telemetry.
"""
from typing import Any, Dict, List, Optional


def _avg_similarity(citations: List[Dict[str, Any]]) -> Optional[float]:
    scores = [
        float(c.get("similarity_score"))
        for c in citations
        if c.get("similarity_score") is not None
    ]
    if not scores:
        return None
    return round(sum(scores) / len(scores), 4)


def calculate_metrics(
    response_text: str = "",
    citations: Optional[List[Dict[str, Any]]] = None,
    query: str = "",
) -> Dict[str, Any]:
    """Compute structural metrics for a chat response."""
    citations = citations or []
    text = response_text or ""
    words = text.split()
    return {
        "response_length": len(text),
        "word_count": len(words),
        "citation_count": len(citations),
        "has_citations": bool(citations),
        "avg_similarity": _avg_similarity(citations),
        "query_length": len(query or ""),
    }
