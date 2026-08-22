from app.vector_store.service import VectorStoreService

def get_vector_store_health(service: VectorStoreService) -> dict:
    return service.get_health()
