from typing import List, Any
try:
    from app.prompts.models import PromptTemplate
except ImportError:
    PromptTemplate = type("PromptTemplate", (), {})

def get_prompts() -> List[Any]:
    return [
        PromptTemplate(
            id="assessment_coach.system",
            name="Assessment Coach System Prompt",
            version="1.0",
            description="System prompt for the Assessment Coach agent.",
            template="""You are the Assessment Coach for the BlueTeamers AI Assistant platform.
Your ONLY role is to evaluate learner understanding, measure competencies, and generate adaptive assessments.
You MUST NOT teach concepts, solve labs, or mentor users. Maintain an objective, educational, and constructive tone.
Never leak direct solutions or step-by-step answers. 
Focus entirely on evaluating the learner's knowledge, practical skills, and readiness against the competency framework.
""",
            variables=["assessment_context"]
        ),
        PromptTemplate(
            id="assessment_coach.feedback_generation",
            name="Feedback Generation Prompt",
            version="1.0",
            description="Prompt to generate constructive feedback.",
            template="""Based on the recent assessment results, generate constructive feedback for the learner.
Highlight strengths and pinpoint areas for improvement. Do not explain the concepts they failed; simply point out what they need to study next.
Assessment Results: {results}
""",
            variables=["results"]
        )
    ]
