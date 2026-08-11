import json
import re
from typing import List, Optional

GENERATION_SYSTEM_PROMPT = (
    "You are the BlueTeamers Assessment Agent. You generate short, accurate, "
    "context-aware practice quizzes inside a chat conversation. Follow the "
    "requested format exactly and never add anything outside the JSON."
)

EVALUATION_SYSTEM_PROMPT = (
    "You are the BlueTeamers Assessment Agent. You grade a learner's answer "
    "constructively and empathetically. Never simply say 'wrong'; explain the "
    "confusion briefly and point to the correct concept."
)

SUMMARY_SYSTEM_PROMPT = (
    "You are the BlueTeamers Assessment Agent. Summarize a completed quiz into "
    "strengths, weak areas, learning recommendations, and a suggested next topic. "
    "Return JSON only."
)

_QUESTION_TYPE_NAMES = {
    "mcq": "Multiple Choice",
    "true_false": "True / False",
    "fill_in_blank": "Fill in the blank",
    "short_answer": "Short answer",
    "scenario": "Scenario-based",
    "interview": "Interview-style",
    "code": "Code-related",
}


def question_type_names(types: List[str]) -> str:
    return ", ".join(_QUESTION_TYPE_NAMES.get(t, t) for t in types)


def build_generation_prompt(
    topic: str,
    difficulty: str,
    count: int,
    question_types: List[str],
    conversation: str = "",
    previous_topics: Optional[List[str]] = None,
) -> str:
    """Builds the user prompt requesting a strict JSON array of questions."""
    type_line = question_type_names(question_types)
    context_line = f"\nConversation context:\n{conversation[:2000]}" if conversation else ""
    prev_line = ""
    if previous_topics:
        prev_line = (
            "\nPreviously assessed topics to avoid repeating: "
            + ", ".join(previous_topics[:10])
        )
    return f"""Generate exactly {count} practice questions about: {topic}

Constraints:
- Difficulty: {difficulty}
- Question types: {type_line}
- Each question must be context-aware and specific to the topic.
- Options must be concise and plausible.
- Include one correct answer and a short explanation for each.
- For true_false questions provide options: ["True", "False"].
- For mcq questions provide 3-4 options.

Return STRICT JSON: a JSON array of objects with keys:
- "type": one of {question_type_names(list(_QUESTION_TYPE_NAMES.keys()))}
- "text": the question
- "options": array of strings ([] for fill_in_blank / short_answer / code unless multiple acceptable)
- "correct_answer": string
- "explanation": short explanation
- "difficulty": "{difficulty}"
- "topic": the topic

Output ONLY the JSON array. No markdown fences.{prev_line}{context_line}"""


def build_evaluation_prompt(question: str, options: List[str], correct_answer: str, user_answer: str) -> str:
    """Builds the user prompt asking the LLM to grade an answer."""
    options_line = "\n".join(f"- {o}" for o in options) if options else "None"
    return f"""Grade the learner's answer to this question.

Question: {question}
Options:
{options_line}
Correct answer: {correct_answer}
Learner's answer: {user_answer}

Return STRICT JSON (no markdown fences) with keys:
- "correct": true|false (false if partially correct, see "partial")
- "partial": true if the answer shows understanding but is incomplete or has minor errors
- "feedback": constructive feedback (2-4 sentences). If correct, confirm why.
- "correct_answer": the correct answer string

Output ONLY the JSON object."""


def build_summary_prompt(topic: str, qa_pairs: str) -> str:
    """Builds the user prompt asking the LLM to summarize the quiz results."""
    return f"""Topic assessed: {topic}

Question/answer transcript:
{qa_pairs[:3000]}

Return STRICT JSON (no markdown fences) with keys:
- "strengths": array of short concepts the learner did well on
- "weak_areas": array of short concepts to improve
- "recommendations": array of concrete study recommendations
- "next_topic": a suggested related topic

Output ONLY the JSON object."""


def parse_json(text: str) -> Optional[object]:
    """Robustly extracts a JSON array/object from an LLM response."""
    if not text:
        return None
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except Exception:
        pass

    start = cleaned.find("[")
    end = cleaned.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(cleaned[start : end + 1])
        except Exception:
            pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(cleaned[start : end + 1])
        except Exception:
            pass

    return None
