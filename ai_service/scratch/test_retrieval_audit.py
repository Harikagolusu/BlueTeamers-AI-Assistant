import asyncio, json, sys
sys.path.insert(0, "/home/harika/BlueTeamers-AI-Assistant/ai_service")

from app.embeddings.dependencies import get_embedding_provider
from app.vector_store.dependencies import get_vector_store, get_metadata_store
from app.vector_store.service import VectorStoreService
from app.embeddings.dependencies import get_embedding_service
from app.retrieval.dependencies import get_reranker
from app.retrieval.service import RetrievalService
from app.retrieval.schemas import RetrievalRequest

provider = get_embedding_provider()
store = get_vector_store()
meta = get_metadata_store()
vs = VectorStoreService(store, meta, provider)

emb_service = get_embedding_service(provider=provider)
reranker = get_reranker()
rs = RetrievalService(emb_service, vs, reranker)

for q in ["Explain SIEM", "Explain MITRE ATT&CK", "Explain Windows Event Logs", "What is a SYN Flood?", "Explain IOC", "Explain Sigma Rules", "Explain SOC Analyst workflow", "what is python", "hello"]:
    resp = rs.retrieve(RetrievalRequest(query=q, top_k=3))
    print(f"QUERY: {q!r} -> results: {len(resp.results)}")
    for r in resp.results[:3]:
        print(f"   score={r.score:.4f} id={r.chunk_id} src={r.metadata.get('course_slug','?')}/{r.metadata.get('lesson_title','?')}")
