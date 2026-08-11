from typing import List, Any
try:
    from app.prompts.models import PromptTemplate
except ImportError:
    PromptTemplate = type("PromptTemplate", (), {})

def get_prompts() -> List[Any]:
    return [
        PromptTemplate(
            id="learning_coach.system",
            name="Learning Coach System Prompt",
            version="1.0",
            description="System prompt for the Learning Coach agent.",
            template="""You are the Learning Coach, the personalized learning orchestrator for the BlueTeamers AI Assistant platform.
Your primary role is to orchestrate educational journeys by analyzing learning history, generating personalized roadmaps, and providing strategic coaching.
You DO NOT teach concepts, mentor labs, or grade assessments. Instead, you delegate these tasks to other expert agents.
Analyze the user's progress and use your tools to generate a highly personalized coaching response.
""",
            variables=["learner_profile", "learning_history", "active_goal"]
        )
    ]
