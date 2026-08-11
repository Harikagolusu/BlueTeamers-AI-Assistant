import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

from app.vector_store.dependencies import get_vector_store, get_metadata_store
from app.embeddings.dependencies import get_embedding_provider
from app.vector_store.service import VectorStoreService
from app.knowledge.pipeline import KnowledgeIngestionPipeline


def main():
    vector_store = get_vector_store()
    metadata_store = get_metadata_store()
    embedding_provider = get_embedding_provider()
    service = VectorStoreService(vector_store, metadata_store, embedding_provider)
    pipeline = KnowledgeIngestionPipeline(service, embedding_provider)
    summary = pipeline.ingest()
    print("REBUILD SUMMARY:", summary)
    print("vector_count:", pipeline.status()["vector_count"])


if __name__ == "__main__":
    sys.exit(main())
