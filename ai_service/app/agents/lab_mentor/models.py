# Deprecated: Models have been moved to app.services.lab.models
# These imports are provided for backward compatibility

from app.services.lab.models import (
    LabState,
    HintLevel,
    MistakeCategory,
    HintValidationPolicy as HintPolicy,
    AttemptHistory,
    MentoringMetrics,
    MentorFeedback,
    Hint,
    ReflectionPrompt,
    LabSession as LabMentoringContext
)
