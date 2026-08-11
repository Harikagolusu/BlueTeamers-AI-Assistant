from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class LabState(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    INITIALIZING = "INITIALIZING"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    AWAITING_HINT = "AWAITING_HINT"
    AWAITING_REFLECTION = "AWAITING_REFLECTION"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"

class HintLevel(int, Enum):
    LEVEL_1 = 1  # Conceptual nudges
    LEVEL_2 = 2  # Directional advice
    LEVEL_3 = 3  # Explicit next-step guidance (but still no answers)

class MistakeCategory(str, Enum):
    CONCEPT = "CONCEPT"
    SYNTAX = "SYNTAX"
    WORKFLOW = "WORKFLOW"
    TOOL_USAGE = "TOOL_USAGE"
    CONFIGURATION = "CONFIGURATION"
    REASONING = "REASONING"
    UNKNOWN = "UNKNOWN"

class HintValidationPolicy(BaseModel):
    max_level: HintLevel = HintLevel.LEVEL_3
    anti_leakage_enabled: bool = True
    delay_between_hints_seconds: int = 30
    requires_reflection_after_level: Optional[HintLevel] = HintLevel.LEVEL_2
    
    # New validation policies
    check_flags: bool = True
    check_exact_answers: bool = True
    check_passwords: bool = True
    check_api_keys: bool = True
    check_secrets: bool = True
    check_hashes: bool = True
    check_tokens: bool = True
    check_direct_solution_wording: bool = True
    check_explicit_lab_answers: bool = True
    check_step_by_step_disclosure: bool = True

class AttemptHistory(BaseModel):
    attempt_number: int = 1
    retry_count: int = 0
    hint_requests: int = 0
    hint_level_used: HintLevel = HintLevel.LEVEL_1
    repeated_mistakes: int = 0
    mistake_category: Optional[MistakeCategory] = None
    time_on_current_step: int = 0
    total_time_spent: int = 0
    reflections_completed: int = 0
    last_progress_timestamp: Optional[datetime] = None
    submitted_flags: List[str] = Field(default_factory=list)

class MentoringMetrics(BaseModel):
    hints_generated: int = 0
    hints_rewritten: int = 0
    hints_blocked: int = 0
    average_hint_level: float = 0.0
    retry_rate: float = 0.0
    reflection_completion_rate: float = 0.0
    average_completion_time: float = 0.0
    completion_rate: float = 0.0
    blocker_frequency: float = 0.0

class MentorFeedback(BaseModel):
    positive_reinforcement: str
    observed_strengths: List[str] = Field(default_factory=list)
    observed_weaknesses: List[str] = Field(default_factory=list)
    recommended_next_action: str
    confidence: float

class Hint(BaseModel):
    level: HintLevel
    content: str
    reasoning: str
    is_safe: bool = True

class ReflectionPrompt(BaseModel):
    what_happened: str = Field(default="What exactly occurred during this step?")
    why_it_happened: str = Field(default="Why did the system respond this way?")
    evidence: str = Field(default="What logs or output support your conclusion?")
    alternative_approach: str = Field(default="What is another way to achieve this?")
    detection_opportunity: str = Field(default="How could a defender detect this action?")
    prevention_strategy: str = Field(default="How could this vulnerability be prevented?")
    mitre_attack_mapping: str = Field(default="Which MITRE ATT&CK technique does this map to?")
    real_soc_applicability: str = Field(default="How does this apply to a real SOC environment?")
    expected_concept: str

class LabSession(BaseModel):
    session_id: str
    learner_id: str
    lab_id: str
    learner_profile: Dict = Field(default_factory=dict)
    current_state: LabState = LabState.NOT_STARTED
    current_stage: str = "init"
    attempt_history: AttemptHistory = Field(default_factory=AttemptHistory)
    learning_metrics: MentoringMetrics = Field(default_factory=MentoringMetrics)
    current_hint: Optional[Hint] = None
    started_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    # Internal flag used by tools
    is_leakage_detected: bool = False
    feedback: Optional[MentorFeedback] = None
    reflection: Optional[ReflectionPrompt] = None
