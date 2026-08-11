from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Course(BaseModel):
    id: int
    title: str
    slug: str
    description: Optional[str] = None

class Lesson(BaseModel):
    id: int
    title: str
    content: Optional[Dict[str, Any]] = None
    course_id: int

class Progress(BaseModel):
    user_id: int
    course_id: int
    completed_lessons: List[int]
    progress_percentage: float

class Assessment(BaseModel):
    id: int
    title: str
    course_id: int
    questions: List[Dict[str, Any]]

class Certificate(BaseModel):
    id: int
    user_id: int
    course_id: int
    url: str
