from typing import Any, List
from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.agents.knowledge_assistant.models import ResourceRecommendation

class ResourceRecommendationTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="resource_recommendation",
            metadata=ToolMetadata(
                input_schema={"concept": "str", "level": "str"},
                output_schema={"recommendations": "list"},
                tags=["education", "resources"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        concept = kwargs.get("concept", "Unknown")
        level = kwargs.get("level", "Beginner")
        
        return [
            ResourceRecommendation(
                title=f"Introduction to {concept}",
                url="https://example.com/intro",
                type="Article",
                difficulty=level,
                rationale="Provides a solid foundation for the concept.",
                rank=1
            ),
            ResourceRecommendation(
                title=f"Interactive Lab: {concept}",
                url="https://example.com/lab",
                type="Lab",
                difficulty=level,
                rationale="Hands-on practice to solidify understanding.",
                rank=2
            )
        ]
