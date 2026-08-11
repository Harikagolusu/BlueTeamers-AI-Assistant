from typing import Any
from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.agents.knowledge_assistant.models import LearningPath, LearningPathStep

class LearningPathTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="learning_path",
            metadata=ToolMetadata(
                input_schema={"goal": "str", "weak_topics": "list", "completed_topics": "list"},
                output_schema={"learning_path": "LearningPath"},
                tags=["education", "path"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        goal = kwargs.get("goal", "General Cybersecurity")
        
        return LearningPath(
            title=f"Path towards: {goal}",
            steps=[
                LearningPathStep(
                    step_number=1,
                    topic="Foundations",
                    description="Understand the basics of the requested topic.",
                    estimated_minutes=30
                ),
                LearningPathStep(
                    step_number=2,
                    topic="Advanced Concepts",
                    description="Dive deeper into the mechanics.",
                    estimated_minutes=60
                )
            ]
        )
