from typing import List, Dict, Any
from app.integrations.django_client import DjangoClient
from app.models.django_models import Assessment

class AssessmentsAPI:
    """Wrapper for Django Assessments endpoints."""
    def __init__(self, client: DjangoClient):
        self.client = client

    async def get_assessments(self, token: str) -> List[Assessment]:
        data = await self.client.get("/assessments/", token)
        return [Assessment(**item) for item in data]

    async def get_assessment(self, assessment_id: int, token: str) -> Assessment:
        data = await self.client.get(f"/assessments/{assessment_id}/", token)
        return Assessment(**data)

    async def submit_assessment(self, assessment_id: int, answers: Dict[str, Any], token: str) -> Dict[str, Any]:
        data = await self.client.post(f"/assessments/{assessment_id}/submit/", token, json=answers)
        return data
