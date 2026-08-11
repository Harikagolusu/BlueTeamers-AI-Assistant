from typing import Dict, Any
from app.integrations.django_client import DjangoClient
from app.models.django_models import Progress

class ProgressAPI:
    """Wrapper for Django Progress endpoints."""
    def __init__(self, client: DjangoClient):
        self.client = client

    async def get_progress(self, user_id: int, token: str) -> Progress:
        data = await self.client.get(f"/progress/{user_id}/", token)
        return Progress(**data)

    async def update_progress(self, user_id: int, payload: Dict[str, Any], token: str) -> Progress:
        data = await self.client.put(f"/progress/{user_id}/", token, json=payload)
        return Progress(**data)
