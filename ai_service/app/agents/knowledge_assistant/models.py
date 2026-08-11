from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from enum import Enum

class ExplanationLevel(str, Enum):
    ELI5 = "ELI5"
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"

class LearnerProfile(BaseModel):
    experience_level: ExplanationLevel = Field(ExplanationLevel.BEGINNER, description="Current experience level")
    completed_topics: List[str] = Field(default_factory=list, description="Topics the learner has already completed")
    weak_topics: List[str] = Field(default_factory=list, description="Topics the learner struggles with")
    preferred_learning_style: str = Field("balanced", description="visual, practical, theoretical, balanced")
    preferred_explanation_depth: str = Field("medium", description="shallow, medium, deep")
    learning_goals: List[str] = Field(default_factory=list, description="What the learner is trying to achieve")
    known_concepts: List[str] = Field(default_factory=list, description="Specific concepts already understood")

class LearningMetrics(BaseModel):
    session_topics_covered: List[str] = Field(default_factory=list)
    questions_asked: int = 0
    correct_assessments: int = 0
    total_assessments: int = 0
    time_spent_minutes: int = 0

class KnowledgeRequest(BaseModel):
    query: str = Field(..., description="The user's question or topic to learn")
    learner_profile: Optional[LearnerProfile] = None

class ConceptExplanation(BaseModel):
    concept_name: str
    summary: str
    detailed_explanation: str
    real_world_example: str
    visual_analogy: str
    common_mistakes: List[str] = Field(default_factory=list)
    detection_defense_notes: Optional[str] = None

class ConceptMap(BaseModel):
    core_concept: str
    prerequisites: List[str] = Field(default_factory=list)
    related_concepts: List[str] = Field(default_factory=list)
    learning_dependencies: Dict[str, List[str]] = Field(default_factory=dict)

class LearningPathStep(BaseModel):
    step_number: int
    topic: str
    description: str
    estimated_minutes: int

class LearningPath(BaseModel):
    title: str
    steps: List[LearningPathStep] = Field(default_factory=list)

class AssessmentQuestion(BaseModel):
    question: str
    options: List[str] = Field(default_factory=list)
    correct_answer: str
    explanation: str

class ResourceRecommendation(BaseModel):
    title: str
    url: Optional[str] = None
    type: str = Field(..., description="Article, Lab, Video, Documentation")
    difficulty: str
    rationale: str = Field(..., description="Why this resource is recommended")
    rank: int = 1

class KnowledgeContext(BaseModel):
    raw_request: Optional[KnowledgeRequest] = None
    profile: Optional[LearnerProfile] = None
    metrics: LearningMetrics = Field(default_factory=LearningMetrics)
    retrieved_knowledge: List[Dict[str, Any]] = Field(default_factory=list)
    explanation: Optional[ConceptExplanation] = None
    concept_map: Optional[ConceptMap] = None
    knowledge_check: Optional[AssessmentQuestion] = None
    recommendations: List[ResourceRecommendation] = Field(default_factory=list)
    learning_path: Optional[LearningPath] = None

class KnowledgeResponse(BaseModel):
    summary: str
    detailed_explanation: str
    real_world_example: str
    visual_analogy: str
    common_mistakes: List[str] = Field(default_factory=list)
    detection_defense_notes: Optional[str] = None
    related_concepts: List[str] = Field(default_factory=list)
    knowledge_check: Optional[AssessmentQuestion] = None
    recommended_resources: List[ResourceRecommendation] = Field(default_factory=list)
    next_learning_topics: List[str] = Field(default_factory=list)
