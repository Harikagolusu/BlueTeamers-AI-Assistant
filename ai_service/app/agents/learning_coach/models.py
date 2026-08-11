from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime, timedelta, timezone

class LearningJourneyState(str, Enum):
    ONBOARDING = "ONBOARDING"
    LEARNING = "LEARNING"
    PRACTICING = "PRACTICING"
    ASSESSING = "ASSESSING"
    REMEDIATION = "REMEDIATION"
    CERTIFICATION_READY = "CERTIFICATION_READY"
    COMPLETED = "COMPLETED"
    PAUSED = "PAUSED"

class CompetencyCategory(str, Enum):
    KNOWLEDGE = "KNOWLEDGE"
    PRACTICAL_SKILLS = "PRACTICAL_SKILLS"
    INVESTIGATION_SKILLS = "INVESTIGATION_SKILLS"
    DETECTION_ENGINEERING = "DETECTION_ENGINEERING"
    INCIDENT_RESPONSE = "INCIDENT_RESPONSE"
    CLOUD_SECURITY = "CLOUD_SECURITY"
    THREAT_HUNTING = "THREAT_HUNTING"

class GoalLevel(str, Enum):
    CAREER = "CAREER"
    CERTIFICATION = "CERTIFICATION"
    LEARNING = "LEARNING"
    MILESTONE = "MILESTONE"
    TASK = "TASK"

class LearningGoal(BaseModel):
    id: str
    level: GoalLevel
    title: str
    description: str
    parent_goal_id: Optional[str] = None
    target_date: Optional[datetime] = None
    completed: bool = False
    progress_percentage: float = 0.0

class Competency(BaseModel):
    category: CompetencyCategory
    name: str
    current_level: float = 0.0  # 0.0 to 10.0
    target_level: float = 10.0
    confidence: float = 0.0
    evidence_count: int = 0
    evidence_sources: List[str] = Field(default_factory=list)
    supporting_evidence: List[str] = Field(default_factory=list)
    last_updated: Optional[datetime] = None

class SkillProfile(BaseModel):
    competencies: List[Competency] = Field(default_factory=list)
    weak_skills: List[str] = Field(default_factory=list)
    strong_skills: List[str] = Field(default_factory=list)

class JourneyTransition(BaseModel):
    timestamp: datetime
    previous_state: LearningJourneyState
    new_state: LearningJourneyState
    trigger: str
    reason: str

class LearnerProfile(BaseModel):
    learner_id: str
    goals: List[LearningGoal] = Field(default_factory=list)
    skill_profile: SkillProfile = Field(default_factory=SkillProfile)
    journey_timeline: List[JourneyTransition] = Field(default_factory=list)
    preferred_learning_style: str = "visual"
    preferred_difficulty: str = "intermediate"
    available_study_time_weekly_hours: float = 10.0

class RecommendationPolicy(BaseModel):
    consider_prerequisites: bool = True
    consider_competency_gaps: bool = True
    consider_learner_goals: bool = True
    consider_available_time: bool = True
    consider_preferred_difficulty: bool = True
    consider_certification_objectives: bool = True
    consider_learning_history: bool = True

class RecommendationExplanation(BaseModel):
    recommendation_id: str
    recommendation_reason: str
    supporting_evidence: str
    competency_gap_addressed: str
    priority_reason: str
    expected_outcome: str
    estimated_benefit: str
    prerequisites: List[str] = Field(default_factory=list)
    confidence_score: float

class LearningRecommendation(BaseModel):
    id: str
    title: str
    type: str # CONCEPT, LAB, ASSESSMENT, CERTIFICATION, PROJECT
    priority: int # 1 (High) to 5 (Low)
    rationale: str
    estimated_time_minutes: int
    difficulty: str
    prerequisites: List[str] = Field(default_factory=list)
    expected_impact: str
    explanation: Optional[RecommendationExplanation] = None

class LearningRoadmap(BaseModel):
    roadmap_id: str
    long_term_goals: List[LearningGoal] = Field(default_factory=list)
    milestones: List[str] = Field(default_factory=list)
    recommendations: List[LearningRecommendation] = Field(default_factory=list)

class RoadmapVersion(LearningRoadmap):
    version_number: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool = True
    superseded_by: Optional[str] = None
    reason_for_change: str = ""
    changed_goals: List[str] = Field(default_factory=list)

class DailyPlan(BaseModel):
    date: datetime
    tasks: List[LearningGoal] = Field(default_factory=list)

class WeeklyPlan(BaseModel):
    week_start: datetime
    focus_areas: List[str] = Field(default_factory=list)
    daily_plans: List[DailyPlan] = Field(default_factory=list)

class StudyPlan(BaseModel):
    weekly_plans: List[WeeklyPlan] = Field(default_factory=list)

class CompetencyTrend(BaseModel):
    category: CompetencyCategory
    growth_rate: float
    trend_description: str

class LearningAnalytics(BaseModel):
    learning_velocity: float = 0.0
    knowledge_growth: float = 0.0
    lab_completion_rate: float = 0.0
    assessment_trends: str = ""
    goal_completion_rate: float = 0.0
    estimated_certification_readiness: float = 0.0
    competency_trends: List[CompetencyTrend] = Field(default_factory=list)

class AnalyticsSnapshot(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    analytics: LearningAnalytics
    competency_profile: SkillProfile
    roadmap_completion: float = 0.0
    engagement_score: float = 0.0

class ProgressForecast(BaseModel):
    readiness_score: float = 0.0
    estimated_completion_date: Optional[datetime] = None
    expected_improvement: str = ""
    risk_of_stagnation: str = "Low"
    confidence_score: float = 0.0
    assumptions: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)

class LearningInsight(BaseModel):
    insight_type: str
    description: str

class LearningPattern(BaseModel):
    study_consistency: str = ""
    plateaus_detected: bool = False
    rapid_improvement: bool = False
    repeated_misconceptions: List[str] = Field(default_factory=list)
    avoidance_of_difficult_topics: bool = False
    theory_practical_imbalance: str = ""
    preferred_learning_style: str = ""

class CoachingSession(BaseModel):
    session_id: str
    learner_profile: LearnerProfile
    journey_state: LearningJourneyState = LearningJourneyState.ONBOARDING
    active_goal: Optional[LearningGoal] = None
    roadmap: Optional[LearningRoadmap] = None
    roadmap_version: Optional[RoadmapVersion] = None
    analytics: Optional[LearningAnalytics] = None
    analytics_snapshot: Optional[AnalyticsSnapshot] = None
    forecast: Optional[ProgressForecast] = None
    recommendations: List[LearningRecommendation] = Field(default_factory=list)
    competency_summary: Optional[SkillProfile] = None
    collaboration_history: List[str] = Field(default_factory=list)
    next_review_date: Optional[datetime] = None
    patterns: Optional[LearningPattern] = None

class CoachingResponse(BaseModel):
    session_id: str
    message: str
    roadmap: Optional[LearningRoadmap] = None
    recommendations: List[LearningRecommendation] = Field(default_factory=list)
    forecast: Optional[ProgressForecast] = None
