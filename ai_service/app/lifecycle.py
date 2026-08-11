import logging
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging

logger = logging.getLogger("app.lifecycle")

def _background_ingest() -> None:
    """Ingests static knowledge into the vector store on a daemon thread."""
    try:
        from app.embeddings.dependencies import get_embedding_provider
        from app.vector_store.dependencies import get_vector_store, get_metadata_store
        from app.vector_store.service import VectorStoreService
        from app.knowledge.pipeline import KnowledgeIngestionPipeline

        provider = get_embedding_provider()
        store = get_vector_store()
        meta = get_metadata_store()
        pipeline = KnowledgeIngestionPipeline(
            VectorStoreService(store, meta, provider), provider
        )
        summary = pipeline.ingest()
        logger.info(f"Startup knowledge ingestion finished: {summary}")
    except Exception as e:  # pragma: no cover - never block startup
        logger.warning(f"Startup knowledge ingestion skipped/failed: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifecycle context manager.
    """
    # Validate Configuration & Setup Logging
    setup_logging()
    
    print("==================================================")
    print(f"Starting {settings.APP_NAME}")
    print(f"Version     : {settings.APP_VERSION}")
    print(f"Environment : {settings.APP_ENV}")
    print(f"Mode        : {'DEVELOPMENT' if settings.is_development else 'PRODUCTION'}")
    print(f"LLM Provider: {settings.LLM_PROVIDER}")
    print("==================================================")
    
    logger.info("Application startup sequence initiated.")
    
    # Initialize required global services if needed here
    # (FastAPI DI handles most initializations statelessly)
    # The SentenceTransformerEmbeddingProvider handles its own thread-safe lazy loading
    # Pre-loading here via run_in_threadpool causes httpx 'client closed' errors during model download.
    
    if getattr(settings, "KNOWLEDGE_INGEST_ON_STARTUP", False):
        threading.Thread(target=_background_ingest, daemon=True, name="knowledge-ingest").start()
    
    logger.info("Application successfully started and ready for traffic.")
    
    yield
    
    # Shutdown sequence
    logger.info("Application shutdown sequence initiated.")
    
    # Gracefully release resources here
    
    logger.info("Application successfully shut down.")
