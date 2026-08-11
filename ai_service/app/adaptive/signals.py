"""Signal extraction for the adaptive learner model.

Signals are soft evidence: they move confidence in small steps and are never
interpreted as a hard classification of the learner.
"""
from typing import Iterable, List

from app.adaptive.models import QuerySignals
from app.persona.modes import ResponseMode, detect_mode

_BEGINNER_OVERRIDE = (
    "explain like i'm a beginner", "explain like i am a beginner",
    "beginner here", "i'm new to", "im new to", "i am new to",
    "dumb it down", "keep it simple", "for a beginner", "total beginner",
    "newbie", "novice", "explain for beginners",
)

_EXPERT_OVERRIDE = (
    "expert explanation", "expert level", "advanced level", "deep dive",
    "go deep", "in depth", "advanced detail", "senior level",
    "i'm advanced", "im advanced", "advanced explanation",
    "professional explanation", "deep technical",
)

_BEGINNER_VOCAB = (
    "what is", "what are", "what's", "explain simply", "easy terms",
    "simple terms", "confused", "don't understand", "do not understand",
    "stuck", "does that mean", "am i right", "is it like", "what does",
    "meaning of", "beginner", "basic", "new to", "i'm new", "im new",
    "i am new", "just started learning", "just learning", "noob",
)

_EXPERT_VOCAB = (
    "ttps", "sigma", "yara", "kql", "spl", "detection engineering",
    "hunting hypothesis", "beaconing", "lateral movement",
    "privilege escalation", "persistence mechanism", "evasion",
    "correlation rule", "hunting query", "reg key", "sysmon", "etw",
    "amcache", "prefetch", "shimcache", "threat intelligence",
    "intrusion analysis", "tactics techniques", "chain of custody",
)

_PRACTICAL = (
    "example", "hands-on", "practical", "lab", "walk me through",
    "demo", "how do i", "steps", "walkthrough", "scenario", "use case",
    "sample", "template", "show me", "write a rule", "build a",
)

_STRUGGLE = (
    "i don't get", "i don't understand", "i do not understand", "confusing",
    "too fast", "what does that mean", "can you repeat", "rephrase",
    "still confused", "that didn't help", "didn't help", "lost me",
)

_REINFORCE = (
    "thanks", "thank you", "that makes sense", "got it", "understood",
    "makes sense now", "great explanation", "helpful", "perfect",
    "exactly what i needed", "gotcha", "clear now",
)

_QUESTION = (
    "?", "what", "how", "why", "when", "where", "which", "who", "explain",
    "compare", "difference between", "is it", "can you",
)


def _count(markers: Iterable[str], text: str) -> int:
    lowered = text.lower()
    return sum(1 for m in markers if m in lowered)


def extract_signals(query: str, recent_texts: Iterable[str] = ()) -> QuerySignals:
    """Extract soft learning signals from the current query and recent turns.

    Recent turns contribute only reinforcement/struggle evidence (e.g. a
    follow-up "thanks" should never be mistaken for a hard level marker).
    """
    text = query or ""
    signals = QuerySignals(
        beginner_override=any(m in text.lower() for m in _BEGINNER_OVERRIDE),
        expert_override=any(m in text.lower() for m in _EXPERT_OVERRIDE),
        beginner_vocab=_count(_BEGINNER_VOCAB, text),
        expert_vocab=_count(_EXPERT_VOCAB, text),
        practical=_count(_PRACTICAL, text),
        struggle=_count(_STRUGGLE, text),
        reinforce=_count(_REINFORCE, text),
        question=_count(_QUESTION, text),
    )

    if detect_mode(text) == ResponseMode.ELI5:
        signals.beginner_override = True

    for recent in recent_texts:
        if recent and recent.lower() != text.lower():
            signals.reinforce += _count(_REINFORCE, recent)
            signals.struggle += _count(_STRUGGLE, recent)

    return signals
