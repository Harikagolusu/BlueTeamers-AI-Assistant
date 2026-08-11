from typing import List


def build_citations(documents) -> List[dict]:
    """
    Build citations conforming to SourceCitation
    (course / lesson / chunk_id / similarity_score / source_title).
    """
    citations = []
    for d in documents:
        meta = d.metadata or {}
        course = meta.get("course_title") or meta.get("course_slug") or "course"
        lesson = meta.get("lesson_title") or meta.get("lesson_id") or "lesson"
        chunk_id = meta.get("chunk_id") or str(d.content[:32])
        source_title = f"{course} - {lesson}"
        citations.append({
            "course": course,
            "lesson": lesson,
            "chunk_id": chunk_id,
            "similarity_score": round(float(getattr(d, "score", 0.0) or 0.0), 4),
            "source_title": source_title,
            "source_reference": meta.get("source"),
        })
    return citations
