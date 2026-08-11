from typing import List
from app.integrations.django_client import DjangoClient
from app.models.django_models import Certificate

class CertificatesAPI:
    """Wrapper for Django Certificates endpoints."""
    def __init__(self, client: DjangoClient):
        self.client = client

    async def get_certificates(self, token: str) -> List[Certificate]:
        data = await self.client.get("/certificates/", token)
        return [Certificate(**item) for item in data]
