from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Core Domain Models
# ---------------------------------------------------------

class UserProfile(BaseModel):
    id: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None

class Purchase(BaseModel):
    id: Optional[int] = None
    user: Optional[int] = None
    course_slug: str
    status: str
    amount: Optional[float] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class Module(BaseModel):
    id: str
    title: str
    order: int

class Lesson(BaseModel):
    id: str
    title: str
    module_id: str
    type: str = "video" # video, text, lab
    is_completed: bool = False

class Course(BaseModel):
    id: str = Field(alias="slug", default="") # We use slug as ID often
    title: str
    description: str
    level: str
    duration_hours: int
    modules: List[Module] = []
    lessons: List[Lesson] = []

class Lab(BaseModel):
    id: str
    title: str
    description: str
    course_slug: str
    difficulty: str

class Assessment(BaseModel):
    id: str
    title: str
    course_slug: str
    passed: bool = False
    score: int = 0

class Certificate(BaseModel):
    id: str
    course_slug: str
    issued_at: str
    url: str

class Progress(BaseModel):
    course_slug: str
    percent_complete: int
    completed_lessons: List[str] = []

class Enrollment(BaseModel):
    course_slug: str
    enrolled_at: str
    is_active: bool = True

class Recommendation(BaseModel):
    type: str # course, lab
    item_id: str # slug or id
    title: str
    reason: str
    difficulty: str
    # Enrichment fields (optional, used to render clickable lesson cards):
    course_slug: str = ""            # canonical course slug
    level: str = ""                  # normalized "beginner" | "intermediate" | "advanced"
    score: float = 0.0               # internal relevance score (used for ordering)
    lessons: List[Dict[str, Any]] = Field(default_factory=list)  # [{id, title, module}]
    lesson_url: str = ""             # direct deep-link to the top recommended lesson
    course_url: str = ""             # deep-link to the course detail page


class LearningPath(BaseModel):
    id: str
    title: str
    description: str
    courses: List[str] = []

class Badge(BaseModel):
    id: str
    title: str
    image_url: str
    earned_at: str

# ---------------------------------------------------------
# UI & Output Models (Platform Metadata Schema)
# ---------------------------------------------------------

class PlatformAction(BaseModel):
    label: str
    action_type: str # 'open_course', 'launch_lab', 'view_certificate'
    payload: Dict[str, str]

class PlatformCard(BaseModel):
    title: str
    type: str # 'course', 'lab'
    difficulty: str = ""
    duration: str = ""
    progress: str = ""
    action: Optional[PlatformAction] = None

class PlatformResponsePayload(BaseModel):
    cards: List[PlatformCard] = []
    actions: List[PlatformAction] = []
    context_used: List[str] = []
