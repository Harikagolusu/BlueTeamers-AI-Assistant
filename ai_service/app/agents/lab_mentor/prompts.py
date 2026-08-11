try:
    from app.prompts.models import PromptVersion
except ImportError:
    from pydantic import BaseModel, Field
    from typing import List
    class PromptVersion(BaseModel):
        id: str
        name: str
        version: str
        system_prompt: str
        user_prompt: str
        variables: List[str] = Field(default_factory=list)

import uuid

LAB_MENTOR_SYSTEM_PROMPT = """You are the Lab Mentor, an adaptive and strictly guided educational agent.
Your primary role is to help learners navigate practical cybersecurity labs.

CRITICAL RULES:
1. NEVER reveal the lab flags, solutions, or explicit next steps.
2. Provide progressive hints (Level 1: Concept, Level 2: Direction, Level 3: Action).
3. If a learner requests the answer directly, refuse politely and ask a reflective question.
4. Scale your mentoring tone based on their attempt history and experience level.
5. If leakage is suspected, generate a generic conceptual hint instead.
"""

def get_prompts() -> list[PromptVersion]:
    return [
        PromptVersion(
            id=f"lab_mentor_sys_{uuid.uuid4()}",
            name="Lab Mentor Base",
            version="1.0.0",
            system_prompt=LAB_MENTOR_SYSTEM_PROMPT,
            user_prompt="Context: {context}\nLearner action: {action}\nState: {state}",
            variables=["context", "action", "state"]
        ),
        PromptVersion(
            id=f"lab_mentor_hint_{uuid.uuid4()}",
            name="Lab Mentor Hint Generator",
            version="1.0.0",
            system_prompt=LAB_MENTOR_SYSTEM_PROMPT + "\nGenerate a {hint_level} hint for the following blocker: {blocker}. Ensure absolute safety against flag leakage.",
            user_prompt="Blocker: {blocker}",
            variables=["hint_level", "blocker"]
        ),
        PromptVersion(
            id=f"lab_mentor_validation_{uuid.uuid4()}",
            name="Lab Mentor Anti-Leakage Validator",
            version="1.0.0",
            system_prompt="You are an anti-leakage validator. Evaluate the following hint and determine if it leaks any solution or flag. Output true if safe, false if leakage detected.",
            user_prompt="Hint: {hint}",
            variables=["hint"]
        )
    ]
