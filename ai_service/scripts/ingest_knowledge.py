"""
CLI entry point for static knowledge ingestion.

Usage (from ai_service/):
    .venv/bin/python scripts/ingest_knowledge.py
    .venv/bin/python scripts/ingest_knowledge.py --status
    .venv/bin/python scripts/ingest_knowledge.py --force
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.embeddings.dependencies import get_embedding_provider
from app.vector_store.dependencies import get_vector_store, get_metadata_store
from app.vector_store.service import VectorStoreService
from app.knowledge.pipeline import KnowledgeIngestionPipeline
from app.knowledge.sources import load_lesson_content, load_course_catalog


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest static course knowledge into the vector store.")
    parser.add_argument("--status", action="store_true", help="Print ingestion status and exit.")
    args = parser.parse_args()

    provider = get_embedding_provider()
    store = get_vector_store()
    meta = get_metadata_store()
    pipeline = KnowledgeIngestionPipeline(VectorStoreService(store, meta, provider), provider)

    if args.status:
        lessons = load_lesson_content()
        catalog = load_course_catalog()
        status = pipeline.status()
        print(f"Courses in catalog    : {len(catalog)}")
        print(f"Courses with lessons  : {len(lessons)}")
        print(f"Total lessons         : {sum(len(v) for v in lessons.values())}")
        print(f"Vectors in store      : {status['vector_count']}")
        print(f"Store loaded          : {status['loaded']}")
        return 0

    summary = pipeline.ingest()
    print(f"Ingestion complete: {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
