import time
import asyncio
from app.tools.infrastructure.search.providers.mock_search_provider import MockSearchProvider
from app.tools.application.search.rag_pipeline import Retriever, Ranker, ContextAssembler, RAGPipeline

async def benchmark_search():
    provider = MockSearchProvider()
    retriever = Retriever(provider)
    ranker = Ranker()
    assembler = ContextAssembler()
    pipeline = RAGPipeline(retriever, ranker, assembler)
    
    start = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        await pipeline.execute("malware behavior", limit=5)
    end = time.perf_counter()
    
    total_time = (end - start) * 1000
    print(f"Benchmark completed {iterations} RAG pipeline iterations in {total_time:.2f} ms")
    print(f"Average time per execution: {total_time / iterations:.4f} ms")

if __name__ == "__main__":
    asyncio.run(benchmark_search())
