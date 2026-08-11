from typing import List
from app.integrations.django_client import DjangoClient
from app.models.django_models import Course, Lesson

class CoursesAPI:
    """Wrapper for Django Courses endpoints."""
    def __init__(self, client: DjangoClient):
        self.client = client

    async def get_courses(self, token: str) -> List[Course]:
        data = await self.client.get("/courses/", token)
        return [Course(**item) for item in data]

    async def get_course(self, course_id: int, token: str) -> Course:
        data = await self.client.get(f"/courses/{course_id}/", token)
        return Course(**data)

    async def get_lessons(self, course_id: int, token: str) -> List[Lesson]:
        data = await self.client.get(f"/courses/{course_id}/lessons/", token)
        return [Lesson(**item) for item in data]
