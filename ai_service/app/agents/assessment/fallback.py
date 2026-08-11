import re
from typing import List, Tuple

from app.agents.assessment.models import (
    DifficultyLevel,
    QuestionType,
    QuizQuestion,
    AnswerRecord,
)

_FILL_TEMPLATES = [
    ("{topic} is the process of applying security controls to protect systems and data.", "security"),
    ("A common technique used to validate {topic} correctness is to compare expected and observed behavior.", "correctness"),
    ("In the context of {topic}, a 'baseline' refers to a known-good state used for comparison.", "baseline"),
]

_TRUE_FALSE_FACTS = [
    ("{topic} involves monitoring, detecting, and responding to security events.", True),
    ("{topic} is unrelated to risk assessment in cybersecurity.", False),
    ("Proper documentation of {topic} procedures improves repeatability and auditability.", True),
    ("{topic} does not require ongoing training or practice.", False),
]

_MCQ_POOL = [
    (
        "Which of the following best describes the core goal of {topic}?",
        [
            "Defending systems and responding to security incidents",
            "Guaranteeing that no attack can ever succeed",
            "Only monitoring network traffic for fun",
            "Removing all security controls",
        ],
        "Defending systems and responding to security incidents",
    ),
    (
        "When studying {topic}, why is hands-on practice important?",
        [
            "It builds real, transferable skills",
            "It is the only way to earn a certificate",
            "It has no impact on learning",
            "It replaces theory entirely",
        ],
        "It builds real, transferable skills",
    ),
    (
        "Which skill is most relevant to mastering {topic}?",
        [
            "Analyzing logs and correlating evidence",
            "Memorizing every vendor dashboard",
            "Avoiding documentation",
            "Ignoring anomalies",
        ],
        "Analyzing logs and correlating evidence",
    ),
]

_INTERVIEW_POOL = [
    "Explain {topic} as if you were describing it in a job interview, in 2-3 sentences.",
    "Walk through how you would apply {topic} to investigate a real security incident.",
]

_CODE_PROMPT = (
    "Write a short Python function that simulates a basic check related to {topic} "
    "(e.g. validating an indicator or normalizing a log line). Include a one-line "
    "explanation."
)

_SHORT_ANSWER_PROMPTS = [
    "In one or two sentences, what does {topic} mean to you?",
    "Name one concrete example where {topic} would be used in a security operations center.",
]


def _normalise(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _topic_for(topic: str) -> str:
    return topic if topic else "cybersecurity concepts"


def generate_questions(topic: str, difficulty: str, count: int, question_types: List[str]) -> List[QuizQuestion]:
    """Deterministic fallback question generator used when the LLM is unavailable."""
    types = [t for t in question_types if t in (
        "mcq", "true_false", "fill_in_blank", "short_answer", "scenario", "interview", "code"
    )] or ["mcq", "true_false", "short_answer"]
    resolved = _topic_for(topic)
    questions: List[QuizQuestion] = []
    idx = 0

    while len(questions) < count:
        qtype = types[idx % len(types)]
        idx += 1

        if qtype == "mcq":
            q, options, correct = _MCQ_POOL[idx % len(_MCQ_POOL)]
            questions.append(QuizQuestion(
                type=QuestionType.MCQ,
                text=q.format(topic=resolved),
                options=list(options),
                correct_answer=correct,
                explanation=f"Understanding {resolved} fundamentals is the foundation for advanced topics.",
                difficulty=difficulty,
                topic=resolved,
            ))
        elif qtype == "true_false":
            fact, answer = _TRUE_FALSE_FACTS[idx % len(_TRUE_FALSE_FACTS)]
            questions.append(QuizQuestion(
                type=QuestionType.TRUE_FALSE,
                text=fact.format(topic=resolved),
                options=["True", "False"],
                correct_answer="True" if answer else "False",
                explanation=f"For {resolved}, this statement is {'true' if answer else 'false'}.",
                difficulty=difficulty,
                topic=resolved,
            ))
        elif qtype == "fill_in_blank":
            template, expected = _FILL_TEMPLATES[idx % len(_FILL_TEMPLATES)]
            questions.append(QuizQuestion(
                type=QuestionType.FILL_IN_BLANK,
                text=template.format(topic=resolved) + " (type the missing word)",
                options=[],
                correct_answer=expected,
                explanation=f"The missing concept is '{expected}'.",
                difficulty=difficulty,
                topic=resolved,
            ))
        elif qtype == "code":
            questions.append(QuizQuestion(
                type=QuestionType.CODE,
                text=_CODE_PROMPT.format(topic=resolved),
                options=[],
                correct_answer="",
                explanation="Focus on clear logic, input handling, and a brief explanation.",
                difficulty=difficulty,
                topic=resolved,
            ))
        elif qtype == "interview":
            questions.append(QuizQuestion(
                type=QuestionType.INTERVIEW,
                text=_INTERVIEW_POOL[idx % len(_INTERVIEW_POOL)].format(topic=resolved),
                options=[],
                correct_answer="",
                explanation="Structure your answer as: what, why, and a concrete example.",
                difficulty=difficulty,
                topic=resolved,
            ))
        else:
            prompt = _SHORT_ANSWER_PROMPTS[idx % len(_SHORT_ANSWER_PROMPTS)]
            questions.append(QuizQuestion(
                type=QuestionType.SHORT_ANSWER,
                text=prompt.format(topic=resolved),
                options=[],
                correct_answer="",
                explanation="A good answer names the core idea and a concrete application.",
                difficulty=difficulty,
                topic=resolved,
            ))

    return questions[:count]


def evaluate_fallback(question: QuizQuestion, user_answer: str) -> Tuple[bool, bool, str]:
    """Deterministic fallback evaluation. Returns (correct, partial, feedback)."""
    answer = user_answer.strip()
    qtype = question.type
    correct_answer = (question.correct_answer or "").strip()

    if not answer:
        return False, False, "Please provide an answer so we can assess your understanding."

    if qtype == QuestionType.MCQ:
        letter = _normalise(answer)
        if letter in ("a", "b", "c", "d", "e"):
            options = question.options
            index = ord(letter[0]) - ord("a")
            if 0 <= index < len(options) and options[index].strip() == correct_answer:
                return True, False, "Correct! Good job."
            if 0 <= index < len(options):
                return False, False, f"Not quite. The correct answer is: {correct_answer}"
        if _normalise(answer) == _normalise(correct_answer):
            return True, False, "Correct! Good job."
        return False, False, f"Not quite. The correct answer is: {correct_answer}"

    if qtype == QuestionType.TRUE_FALSE:
        norm = _normalise(answer)
        expected = _normalise(correct_answer)
        mapped = {"true": "true", "false": "false", "yes": "true", "no": "false",
                  "t": "true", "f": "false", "correct": "true", "incorrect": "false"}
        if norm in mapped:
            if mapped[norm] == expected:
                return True, False, "Correct! Good job."
            return False, False, f"Not quite. The correct answer is: {correct_answer}"
        return False, True, f"Please answer True or False. The correct answer is: {correct_answer}"

    if qtype == QuestionType.FILL_IN_BLANK:
        if correct_answer and _normalise(correct_answer) in _normalise(answer):
            return True, False, "Correct! Good job."
        if correct_answer and _normalise(answer) and _normalise(answer) in _normalise(correct_answer):
            return True, False, "Correct! Good job."
        if correct_answer:
            return False, True, f"Close, but the expected word was: {correct_answer}"
        return False, True, "Good attempt. Compare your answer with the expected concept."

    # Free text: code / short_answer / scenario / interview
    if not correct_answer:
        return False, True, (
            "Thanks for your answer. For open-ended questions, review whether you "
            "covered the core concept, gave a concrete example, and structured your reply."
        )

    a_tokens = set(_normalise(answer).split())
    c_tokens = set(_normalise(correct_answer).split())
    if not a_tokens or not c_tokens:
        return False, True, "Partial credit given. Compare your answer with the expected response."

    overlap = len(a_tokens & c_tokens) / len(c_tokens)
    if overlap >= 0.6:
        return True, False, "Correct! Your answer captured the key ideas."
    if overlap >= 0.3:
        return False, True, (
            "Almost correct. You understood part of it, but a few key details were "
            f"missing. Compare with: {correct_answer}"
        )
    return False, False, f"Not quite. Here is a concise version of the key points: {correct_answer}"


def build_summary_fallback(questions: List[QuizQuestion], answers: List[AnswerRecord], topic: str) -> dict:
    """Deterministic fallback summary builder."""
    strengths = []
    weak_areas = []
    seen = set()
    for record in answers:
        key = record.topic or topic
        if key in seen:
            continue
        seen.add(key)
        if record.correct:
            strengths.append(key)
        elif not record.partial:
            weak_areas.append(key)

    return {
        "strengths": strengths or [topic],
        "weak_areas": weak_areas or ["Review the incorrect questions and retry"],
        "recommendations": [
            "Re-read the material for the questions you missed.",
            "Practice with a follow-up quiz on the same topic.",
        ],
        "next_topic": _suggest_next_topic(topic),
    }


def _suggest_next_topic(topic: str) -> str:
    suggestions = {
        "rag": "Vector databases",
        "iam": "Multi-factor authentication",
        "python": "Python for security automation",
        "siem": "Incident response",
        "threat": "Threat hunting",
        "firewall": "Network segmentation",
        "encryption": "Key management",
        "soc": "SOAR automation",
    }
    norm = _normalise(topic)
    for key, suggestion in suggestions.items():
        if key in norm:
            return suggestion
    return f"Advanced {topic if topic else 'cybersecurity'} topics"
