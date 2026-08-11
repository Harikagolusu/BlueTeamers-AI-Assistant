import asyncio, sys
sys.path.insert(0, "/home/harika/BlueTeamers-AI-Assistant/ai_service")
from app.llm.factory import LLMFactory
from app.llm.adapter import LLMProviderAdapter
from app.prompt_builder.simple_prompt_builder import SimplePromptBuilder
from app.retrieval.service import RetrievalService
from app.retrieval.faiss_retriever import FAISSRetriever
from app.embeddings.dependencies import get_embedding_provider, get_embedding_service
from app.vector_store.dependencies import get_vector_store, get_metadata_store, get_vector_store_service
from app.retrieval.dependencies import get_reranker
from app.chat.engines.rag_engine import RagExecutionEngine
from app.chat.context.execution_context import ExecutionContext
from app.chat.schemas import SourceCitation

async def main():
    llm = LLMProviderAdapter(LLMFactory.get_provider())
    pb = SimplePromptBuilder()
    emb_provider = get_embedding_provider()
    emb = get_embedding_service(provider=emb_provider)
    vs = get_vector_store_service(provider=get_vector_store(), metadata_store=get_metadata_store(), embedding_provider=emb_provider)
    rs = RetrievalService(emb, vs, get_reranker())
    retriever = FAISSRetriever(rs)
    engine = RagExecutionEngine(retriever, llm, pb)
    ctx = ExecutionContext(metadata={"query": "Explain SIEM"})
    result = await engine.execute(ctx)
    print("status:", result.status)
    print("citations count:", len(result.citations))
    if result.citations:
        print("sample citation:", result.citations[0])
        for c in result.citations:
            SourceCitation(**c)
        print("SourceCitation schema validation OK")
    print("answer preview:", result.message[:150])

asyncio.run(main())
