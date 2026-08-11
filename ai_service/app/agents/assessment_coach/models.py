from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

# Reuse existing platform models (Shared Competency Framework & Analytics)
from app.agents.learning_coach.models import (
    CompetencyCategory,
    Competency,
    SkillProfile,
    LearnerProfile,
    LearningRecommendation,
    RecommendationExplanation,
    LearningAnalytics,
    AnalyticsSnapshot,
    CompetencyTrend
)

class AssessmentType(str, Enum):
    KNOWLEDGE = "KNOWLEDGE"
    PRACTICAL = "PRACTICAL"
    SCENARIO_BASED = "SCENARIO_BASED"
    CASE_STUDY = "CASE_STUDY"
    RAPID_QUIZ = "RAPID_QUIZ"
    CERTIFICATION = "CERTIFICATION"
    MIXED = "MIXED"

class AssessmentState(str, Enum):
    CREATED = "CREATED"
    PREPARING = "PREPARING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    SCORING = "SCORING"
    GENERATING_FEEDBACK = "GENERATING_FEEDBACK"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class GapPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    OPTIONAL = "OPTIONAL"

class QuestionDifficulty(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"

class AssessmentRequest(BaseModel):
    learner_id: str
    assessment_type: AssessmentType
    target_competencies: List[CompetencyCategory] = Field(default_factory=list)
    requested_difficulty: Optional[QuestionDifficulty] = None
    context_data: Dict[str, Any] = Field(default_factory=dict)

class AssessmentContext(BaseModel):
    request: AssessmentRequest
    learner_profile: Optional[LearnerProfile] = None
    historical_metrics: Dict[str, Any] = Field(default_factory=dict)
    historical_assessments: List['AssessmentResult'] = Field(default_factory=list)

class QuestionOption(BaseModel):
    option_id: str
    text: str
    is_correct: bool
    explanation: Optional[str] = None

class AssessmentQuestion(BaseModel):
    question_id: str
    type: AssessmentType
    difficulty: QuestionDifficulty
    competency_category: CompetencyCategory
    text: str
    options: List[QuestionOption] = Field(default_factory=list)
    scenario_context: Optional[str] = None

class AssessmentAnswer(BaseModel):
    question_id: str
    selected_option_id: Optional[str] = None
    text_response: Optional[str] = None
    is_correct: bool = False
    time_taken_seconds: float = 0.0

class CompetencyScore(BaseModel):
    category: CompetencyCategory
    score: float  # 0.0 to 10.0
    confidence: float
    previous_confidence: Optional[float] = None
    confidence_delta: float = 0.0
    confidence_trend: str = "stable"
    evidence: List[str] = Field(default_factory=list)
    last_assessment_id: Optional[str] = None

class CompetencyGap(BaseModel):
    category: CompetencyCategory
    current_score: float
    target_score: float
    description: str
    severity: GapPriority = GapPriority.MEDIUM
    business_impact: str = ""
    prerequisite_dependency: str = ""
    recommended_remediation: str = ""

class SkillAssessment(BaseModel):
    assessed_skills: List[str] = Field(default_factory=list)
    demonstrated_proficiency: float

class KnowledgeAssessment(BaseModel):
    assessed_concepts: List[str] = Field(default_factory=list)
    conceptual_understanding_score: float

class PracticalAssessment(BaseModel):
    scenario_id: str
    completion_rate: float
    technical_accuracy: float

class ReadinessDimension(str, Enum):
    LAB_READINESS = "LAB_READINESS"
    CERTIFICATION_READINESS = "CERTIFICATION_READINESS"
    SOC_READINESS = "SOC_READINESS"
    THREAT_HUNTING_READINESS = "THREAT_HUNTING_READINESS"
    INCIDENT_RESPONSE_READINESS = "INCIDENT_RESPONSE_READINESS"
    CLOUD_SECURITY_READINESS = "CLOUD_SECURITY_READINESS"
    DETECTION_ENGINEERING = "DETECTION_ENGINEERING"
    THREAT_INTELLIGENCE = "THREAT_INTELLIGENCE"

class ReadinessLevel(BaseModel):
    dimension: ReadinessDimension
    score: float # 0.0 to 100.0
    confidence: float = 0.0
    is_ready: bool
    missing_competencies: List[str] = Field(default_factory=list)
    blocking_requirements: List[str] = Field(default_factory=list)
    recommended_next_steps: List[str] = Field(default_factory=list)
    estimated_readiness_time: str = ""

class AssessmentFeedback(BaseModel):
    overall_comments: str
    constructive_feedback: str
    strengths: List[str] = Field(default_factory=list)
    areas_for_improvement: List[str] = Field(default_factory=list)

class AssessmentRecommendation(LearningRecommendation):
    recommended_order: int = 1

class AssessmentResult(BaseModel):
    assessment_id: str
    version: int = 1
    workflow_version: str = "2.0"
    trace_id: str = ""
    state: AssessmentState = AssessmentState.CREATED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    type: AssessmentType
    overall_score: float
    answers: List[AssessmentAnswer] = Field(default_factory=list)
    competency_scores: List[CompetencyScore] = Field(default_factory=list)
    identified_gaps: List[CompetencyGap] = Field(default_factory=list)
    feedback: AssessmentFeedback
    readiness_levels: List[ReadinessLevel] = Field(default_factory=list)
    competency_snapshot: Optional[SkillProfile] = None
    analytics_snapshot: Optional[AnalyticsSnapshot] = None

class AssessmentHistory(BaseModel):
    learner_id: str
    assessments: List[AssessmentResult] = Field(default_factory=list)

class AssessmentSession(BaseModel):
    session_id: str
    context: AssessmentContext
    current_questions: List[AssessmentQuestion] = Field(default_factory=list)
    answers: List[AssessmentAnswer] = Field(default_factory=list)
    final_result: Optional[AssessmentResult] = None
    analytics_snapshot: Optional[AnalyticsSnapshot] = None
    recommendations: List[AssessmentRecommendation] = Field(default_factory=list)

class AssessmentResponse(BaseModel):
    session_id: str
    result: AssessmentResult
    recommendations: List[AssessmentRecommendation] = Field(default_factory=list)
    analytics_updated: bool = True
