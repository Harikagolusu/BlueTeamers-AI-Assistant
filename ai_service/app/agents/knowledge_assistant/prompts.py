try:
    from app.prompts.models import PromptVersion
except ImportError:
    from pydantic import BaseModel, Field
    from typing import List, Optional
    class PromptVersion(BaseModel):
        id: str
        name: str
        version: str
        system_prompt: str
        user_prompt: str
        variables: List[str] = Field(default_factory=list)
import uuid

# Base system prompt for the educational persona
KNOWLEDGE_ASSISTANT_SYSTEM = """You are the BlueTeamers AI Knowledge Assistant.
Your primary role is to educate, explain cybersecurity concepts, and guide learners.
You MUST adapt your explanations to the user's provided LearnerProfile (experience level).
You MUST NOT perform active investigations or triage alerts. You are an educator, not a SOC Analyst.

Guidelines:
1. Break down complex topics clearly.
2. Provide real-world examples and visual analogies.
3. If the user's level is ELI5 or Beginner, avoid heavy jargon unless you explain it immediately.
4. If the user's level is Advanced or Expert, provide deep technical details, detection logic, and architecture constraints.
5. Structure your final output exactly according to the KnowledgeResponse schema.
6. Always check for understanding.
"""

# Tool Prompts
CONCEPT_EXPLANATION_SYSTEM = """You are an expert cybersecurity educator.
Given a concept and a LearnerProfile, break down the concept.
Your explanation must match the depth and style requested in the profile.
Output JSON matching the ConceptExplanation schema.
"""

CONCEPT_EXPLANATION_USER = """Concept: {concept}
Learner Level: {level}
Preferred Depth: {depth}
Context/Knowledge retrieved: {context}

Generate the explanation.
"""

CONCEPT_MAPPING_SYSTEM = """You are a cybersecurity curriculum architect.
Given a core concept, identify prerequisites, related concepts, and learning dependencies.
Output JSON matching the ConceptMap schema.
"""

CONCEPT_MAPPING_USER = """Core Concept: {concept}
Known Concepts: {known}

Generate the concept map.
"""

LEARNING_PATH_SYSTEM = """You are a cybersecurity curriculum developer.
Based on the user's goal, weak topics, and completed topics, generate a LearningPath.
Output JSON matching the LearningPath schema.
"""

LEARNING_PATH_USER = """Goal: {goal}
Completed Topics: {completed}
Weak Topics: {weak}

Generate a learning path.
"""

KNOWLEDGE_ASSESSMENT_SYSTEM = """You are a cybersecurity examiner.
Create exactly ONE multiple-choice question to test the user's understanding of the concept just explained.
The question should match their experience level.
Output JSON matching the AssessmentQuestion schema.
"""

KNOWLEDGE_ASSESSMENT_USER = """Concept: {concept}
Learner Level: {level}

Generate an assessment question.
"""

RESOURCE_RECOMMENDATION_SYSTEM = """You are a cybersecurity mentor.
Provide ranked resource recommendations for the learner based on their current level and the concept they are learning.
Include a strong rationale for why each resource is recommended.
Output a list of JSON objects matching the ResourceRecommendation schema.
"""

RESOURCE_RECOMMENDATION_USER = """Concept: {concept}
Learner Level: {level}

Recommend resources.
"""

def get_prompts():
    """Returns a list of PromptVersion objects to be registered."""
    return [
        PromptVersion(
            id=str(uuid.uuid4()),
            name="knowledge_assistant.system",
            version="1.0",
            system_prompt=KNOWLEDGE_ASSISTANT_SYSTEM,
            user_prompt="{query}",
            variables=["query"]
        ),
        PromptVersion(
            id=str(uuid.uuid4()),
            name="knowledge_assistant.concept_explanation",
            version="1.0",
            system_prompt=CONCEPT_EXPLANATION_SYSTEM,
            user_prompt=CONCEPT_EXPLANATION_USER,
            variables=["concept", "level", "depth", "context"]
        ),
        PromptVersion(
            id=str(uuid.uuid4()),
            name="knowledge_assistant.concept_mapping",
            version="1.0",
            system_prompt=CONCEPT_MAPPING_SYSTEM,
            user_prompt=CONCEPT_MAPPING_USER,
            variables=["concept", "known"]
        ),
        PromptVersion(
            id=str(uuid.uuid4()),
            name="knowledge_assistant.learning_path",
            version="1.0",
            system_prompt=LEARNING_PATH_SYSTEM,
            user_prompt=LEARNING_PATH_USER,
            variables=["goal", "completed", "weak"]
        ),
        PromptVersion(
            id=str(uuid.uuid4()),
            name="knowledge_assistant.knowledge_assessment",
            version="1.0",
            system_prompt=KNOWLEDGE_ASSESSMENT_SYSTEM,
            user_prompt=KNOWLEDGE_ASSESSMENT_USER,
            variables=["concept", "level"]
        ),
        PromptVersion(
            id=str(uuid.uuid4()),
            name="knowledge_assistant.resource_recommendation",
            version="1.0",
            system_prompt=RESOURCE_RECOMMENDATION_SYSTEM,
            user_prompt=RESOURCE_RECOMMENDATION_USER,
            variables=["concept", "level"]
        )
    ]
