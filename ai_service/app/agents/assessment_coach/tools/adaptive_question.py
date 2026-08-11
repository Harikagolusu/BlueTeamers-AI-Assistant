from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.agents.assessment_coach.models import AssessmentQuestion, QuestionDifficulty, AssessmentType, CompetencyCategory, QuestionOption
from typing import Any
import uuid

class AdaptiveQuestionTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="adaptive_question",
            metadata=ToolMetadata(
                input_schema={"learner_id": "str", "current_difficulty": "str", "previous_answers": "list"},
                output_schema={"questions": "list"},
                tags=["assessment_coach", "adaptive", "questioning"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        difficulty_str = kwargs.get("current_difficulty", "BEGINNER")
        try:
            difficulty = QuestionDifficulty(difficulty_str)
        except ValueError:
            difficulty = QuestionDifficulty.BEGINNER

        # Simulate historical checks and cooldown
        history = kwargs.get("assessment_history", [])
        recent_topics = kwargs.get("recent_topics", [])
        cooldown_applied = len(recent_topics) > 0

        text = f"Sample {difficulty.value} question?"
        if cooldown_applied:
            text = f"Sample {difficulty.value} question? (Cooldown applied, avoiding {recent_topics[0]})"

        return [
            AssessmentQuestion(
                question_id=str(uuid.uuid4()),
                type=AssessmentType.KNOWLEDGE,
                difficulty=difficulty,
                competency_category=CompetencyCategory.KNOWLEDGE,
                text=text,
                options=[
                    QuestionOption(option_id="A", text="Option A", is_correct=True),
                    QuestionOption(option_id="B", text="Option B", is_correct=False)
                ]
            )
        ]
