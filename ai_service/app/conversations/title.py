"""Deterministic conversation title generation.

Produces a short, meaningful title from the first user message (no LLM needed),
e.g. "What is Retrieval Augmented Generation?" -> "Understanding RAG". If the
message maps to a known course, the title is a friendly "Understanding <Course>".
"""
import re
from typing import List, Optional

_LEAD_WORDS = (
    r"\b(?:"
    r"please\s+|could you\s+|can you\s+|would you\s+|help me\s+|"
    r"tell me\s+|explain\s+|what is\s+|what are\s+|what's\s+|whats\s+|"
    r"how does\s+|how do\s+|how to\s+|how\s+|why\s+|when\s+|where\s+|"
    r"define\s+|describe\s+|explain\s+"
    r")+"
)

# Greetings / small talk that must never become a conversation title. When a
# chat only contains these, the conversation stays labelled "New Chat" until the
# first meaningful question arrives (smart title generation).
_GREETING_TOKENS: frozenset = frozenset({
    # plain greetings
    "hi", "hii", "hiii", "hiiii", "hiya", "hello", "helloo", "hellooo",
    "hi there", "hello there", "hey", "heyy", "heya", "hey there", "howdy",
    "hiya", "yo", "hola", "sup", "wassup", "wazzup", "namaste", "namaskar",
    "assalamualaikum", "salam", "ji",
    # time-of-day greetings
    "good morning", "morning", "good afternoon", "good evening", "evening",
    "good night", "goodnight", "good day", "gm", "gn",
    # thanks / acknowledgement
    "thanks", "thank you", "thankyou", "thank u", "thank you so much",
    "thanks a lot", "thanx", "thx", "thankq", "tq", "ty", "cheers", "merci",
    # quick acknowledgements
    "ok", "okay", "k", "sure", "done", "great", "nice", "cool", "yes",
    "yeah", "yep", "no", "nope",
})

# Leading politeness/greeting filler that may precede a real question, e.g.
# "hi can you explain X" -> "explain X". Stripped before deciding if a message
# is meaningful, so greetings + a real question still get a proper title.
_LEAD_STRIP = re.compile(
    r"^(?:(?:please|plz|pls|thanks|thank you|hey|yo|ok|okay|could you|could u|"
    r"can you|can u|would you|would u|hi|hello|good morning|good afternoon|"
    r"good evening|good night|ji|sure|yes|yeah)\b[\s,.]*)+",
    re.IGNORECASE,
)

# Catalog aliases used to turn a topic onto a friendly course-like title.
_COURSE_KEYWORDS: List[tuple] = [
    (("rag", "retrieval augmented", "vector database"), "RAG & Vector Databases"),
    (("python",), "Python Fundamentals"),
    (("aws", "cloud practitioner", "cloud"), "AWS Cloud Practitioner"),
    (("prompt engineering", "prompt"), "Prompt Engineering"),
    (("cyber", "security basics", "blue team", "soc"), "Cybersecurity Basics"),
    (("siem",), "SIEM Fundamentals"),
    (("log analysis", "log"), "Log Analysis"),
    (("incident response",), "Incident Response"),
    (("network",), "Network Fundamentals"),
]

# Sprint 4 smart titles: precise, intent-aware names for SOC topics instead of
# the generic "Understanding <Topic>" form (e.g. "Windows Event Log Analysis").
_SMART_TITLES: List[tuple] = [
    (("windows event", "event id", "windows event log", "windows logs"), "Windows Event Log Analysis"),
    (("wazuh",), "Wazuh Rule Investigation"),
    (("indicator of compromise", "ioc analysis", "ioc"), "IOC Analysis"),
    (("mitre",), "MITRE ATT&CK"),
    (("threat hunt", "threat hunting", "hunting"), "Threat Hunting"),
    (("review my resume", "resume review", "resume feedback", "my resume"), "Resume Review"),
    (("sigma",), "Sigma Rule Analysis"),
    (("yara",), "YARA Rule Analysis"),
    (("splunk",), "Splunk Investigation"),
    (("kql", "kusto", "sentinel"), "KQL Investigation"),
    (("threat intelligence", "threat intel"), "Threat Intelligence"),
    (("triage", "security operations", "security operation center", "soar"), "SOC Operations"),
    (("linux", "syslog", "bash"), "Linux Security"),
    (("cloud security",), "Cloud Security"),
    (("tcp", "wireshark", "network traffic", "packet capture"), "Networking"),
]


def _slugify_topic(text: str) -> str:
    # Normalise to a compact set of significant tokens for title casing.
    text = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    text = " ".join(t for t in text.split() if len(t) > 1)
    return text


def _normalise_message(text: str) -> str:
    """Lowercase, strip punctuation/emoji, and collapse whitespace."""
    text = re.sub(r"[^a-z0-9'\s]+", " ", (text or "").lower())
    return re.sub(r"\s+", " ", text).strip()


def is_greeting_message(message: str) -> bool:
    """True when the message is only a greeting / small talk (no real question).

    Used both to keep greeting-only chats at the "New Chat" placeholder title
    and to know when a title should be re-derived from the meaningful content.
    """
    if not message or not message.strip():
        return True

    norm = _normalise_message(message)
    # Whole message is a known greeting phrase ("hi", "good morning", "hi there").
    if norm in _GREETING_TOKENS:
        return True
    tokens = norm.split()
    if tokens and len(tokens) <= 3 and all(t in _GREETING_TOKENS for t in tokens):
        return True

    # After removing leading politeness/greeting filler, e.g. "hi can you ...".
    leftover = _LEAD_STRIP.sub("", message)
    if not leftover or not leftover.strip():
        return True
    lnorm = _normalise_message(leftover)
    if lnorm in _GREETING_TOKENS:
        return True
    ltokens = lnorm.split()
    if ltokens and len(ltokens) <= 3 and all(t in _GREETING_TOKENS for t in ltokens):
        return True
    return False


# Titles that mean "no real title yet" — a conversation should be re-titled the
# moment a meaningful question arrives.
PLACEHOLDER_TITLES: frozenset = frozenset({"", "new conversation", "new chat"})


def is_placeholder_title(title: str) -> bool:
    return (title or "").strip().lower() in PLACEHOLDER_TITLES


def is_greeting_title(title: str) -> bool:
    """True for legacy greeting-derived titles like "About Hi" / "About Hello"."""
    m = re.match(r"^about\s+(.+)$", (title or "").strip(), re.IGNORECASE)
    if not m:
        return False
    return is_greeting_message(m.group(1))


def _title_case(topic: str) -> str:
    import string
    smalls = {"a", "an", "the", "and", "or", "of", "for", "in", "on", "to", "with"}
    words = topic.split()
    out = []
    for i, w in enumerate(words):
        if i > 0 and w.lower() in smalls:
            out.append(w.lower())
        else:
            out.append(w[:1].upper() + w[1:].lower())
    return " ".join(out)


def generate_title(first_message: str, course_title: Optional[str] = None, max_len: int = 60) -> str:
    """Create a short conversation title from the first meaningful user message."""
    text = (first_message or "").strip()
    if not text:
        return "New Conversation"

    # A message that is only a greeting / small talk gets no title yet. The
    # conversation stays at the "New Chat" placeholder until a meaningful
    # question arrives, which then derives the real title.
    if is_greeting_message(text):
        return _clip("New Chat", max_len)

    # Drop any leading greeting/politeness filler so it never leaks into the
    # title (e.g. "Hi, explain X" is titled from "explain X").
    meaningful = _LEAD_STRIP.sub("", text).strip()
    if meaningful:
        text = meaningful

    # 1) Prefer an explicit course -> friendly title.
    if course_title:
        return _clip(f"Understanding {course_title}", max_len)

    text_lower = text.lower()
    # 1b) Sprint 4 smart titles: intent-aware SOC topic names. Checked before
    # the broad course keywords so e.g. "windows event log" wins over the
    # generic "log" -> "Log Analysis" mapping.
    for keywords, label in _SMART_TITLES:
        if any(kw in text_lower for kw in keywords):
            return _clip(label, max_len)

    # 1) Course keywords -> friendly "Understanding <Course>" titles.
    for keywords, label in _COURSE_KEYWORDS:
        if any(kw in text_lower for kw in keywords):
            return _clip(f"Understanding {label}", max_len)

    # 2) Strip lead words/question words, keep the core topic.
    stripped = re.sub(_LEAD_WORDS, "", text, flags=re.IGNORECASE).strip(" \t\r\n.?!:;, ")
    # Drop any trailing question mark / punctuation already handled; fall through.
    if not stripped:
        stripped = re.sub(r"^what's\s*", "", text_lower)
        stripped = re.sub(r"[^a-z0-9 ]+", "", stripped).strip()

    if len(stripped.split()) <= 2 and len(stripped) < 10 and stripped:
        return _clip(_title_case(f"About {stripped}"), max_len)

    topic = _title_case(_slugify_topic(stripped)) if stripped else _title_case(_slugify_topic(text))
    topic = topic or "General Chat"
    return _clip(topic, max_len)


def _clip(text: str, max_len: int) -> str:
    text = " ".join(text.split())
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"
