from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import uuid


class QuestionType(str, Enum):
    """Supported interactive question types (extensible)."""

    MCQ = "mcq"
    TRUE_FALSE = "true_false"
    FILL_IN_BLANK = "fill_in_blank"
    SHORT_ANSWER = "short_answer"
    SCENARIO = "scenario"
    INTERVIEW = "interview"
    CODE = "code"


class DifficultyLevel(str, Enum):
    """Supported difficulty levels (extensible)."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    INTERVIEW = "interview"
    REAL_WORLD = "real-world"


class QuizSessionStatus(str, Enum):
    PENDING_CONFIRM = "pending_confirm"
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class QuizQuestion(BaseModel):
    """A single dynamically generated question."""

    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: QuestionType = QuestionType.MCQ
    text: str
    options: List[str] = Field(default_factory=list)
    correct_answer: str = ""
    explanation: str = ""
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    topic: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AnswerRecord(BaseModel):
    """A recorded answer for a quiz question."""

    question_id: str
    question_type: QuestionType = QuestionType.MCQ
    user_answer: str = ""
    correct: bool = False
    partial: bool = False
    feedback: str = ""
    correct_answer: str = ""
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    topic: str = ""


class QuizSession(BaseModel):
    """Mutable session state for an in-chat quiz."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    session_key: str
    topic: str = ""
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    length: int = 5
    questions: List[QuizQuestion] = Field(default_factory=list)
    current_index: int = 0
    answers: List[AnswerRecord] = Field(default_factory=list)
    status: QuizSessionStatus = QuizSessionStatus.PENDING_CONFIRM
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def is_active(self) -> bool:
        return self.status == QuizSessionStatus.ACTIVE

    @property
    def current_question(self) -> Optional[QuizQuestion]:
        if self.questions and self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None


class QuizResult(BaseModel):
    """Final assessment outcome."""

    score: int = 0
    total: int = 0
    passed: bool = False
    strengths: List[str] = Field(default_factory=list)
    weak_areas: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    next_topic: str = ""
    difficulty_reached: DifficultyLevel = DifficultyLevel.BEGINNER


class SuitabilityAssessment(BaseModel):
    """Whether the current turn is a good candidate for an assessment offer."""

    suitable: bool = False
    confidence: float = 0.0
    reason: str = ""
    signals: List[str] = Field(default_factory=list)
    topic: str = ""


class AssessmentProfile(BaseModel):
    """Per-user learning memory tracked across assessments."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    user_key: str
    topics_completed: List[str] = Field(default_factory=list)
    weak_topics: List[str] = Field(default_factory=list)
    strong_topics: List[str] = Field(default_factory=list)
    difficulty_reached: DifficultyLevel = DifficultyLevel.BEGINNER
    assessment_count: int = 0
    average_score: float = 0.0
    last_assessment_at: Optional[datetime] = None
    quiz_history: List[Dict[str, Any]] = Field(default_factory=list)
    progress: Dict[str, Any] = Field(default_factory=dict)

    # Course-aware learning progress (keyed by course slug).
    course_progress: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    completion_percentage: float = 0.0
    revision_topics: List[str] = Field(default_factory=list)
