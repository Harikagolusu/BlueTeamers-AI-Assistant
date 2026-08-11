"""Language instruction blocks injected into the system prompt.

A compact ``[Response Language]`` block is appended to the end of the system
prompt whenever the resolved language is not English. It tells the model which
language/mode to respond in, guarantees that cybersecurity terminology and raw
artefacts (logs, commands, JSON) stay in English, and preserves the existing
mentor persona, teaching depth and response style regardless of language.

For explicitly-selected (manual/stored) languages the instruction is made
unambiguous ("reply ONLY in {language}") so the model never falls back to the
language the user happens to type in.
"""
from typing import Dict, Optional

from app.multilingual.languages import (
    BASE_LANGUAGE_FOR_MIXED,
    MIXED_LANGUAGE_CODES,
    is_concrete_code,
    language_label,
)
from app.multilingual.terminology import preserved_terms_text

_LANGUAGE_NAME = {
    "hi": "Hindi", "te": "Telugu", "ta": "Tamil", "kn": "Kannada",
    "ml": "Malayalam", "bn": "Bengali", "mr": "Marathi", "gu": "Gujarati",
    "pa": "Punjabi", "or": "Odia", "ur": "Urdu", "as": "Assamese",
}

_MIX_NAME = {
    "te+en": "Tinglish",
}

_PURE_TEMPLATE = (
    "[Response Language]\n"
    "- Respond to the user in {language} (in the {language} script). Always match "
    "the language the user is speaking or typing.\n"
    "- Always keep cybersecurity terminology and industry terms in English:\n"
    "   {terms}\n"
    "- Never translate the content of commands, log/JSON/YAML extracts, code "
    "blocks, file names, tool or product names, or raw data — reproduce them "
    "exactly as-is in English.\n"
    "- Keep the same cybersecurity mentor persona, learner-level teaching depth, "
    "concise style, and Markdown formatting you normally use, just in {language}."
)

_MANUAL_PURE_TEMPLATE = (
    "[Response Language]\n"
    "- The user explicitly chose {language}. Reply to their message in {language} "
    "ONLY, written in the {language} script — even if they write in English or "
    "another language. Do NOT match the language they typed.\n"
    "- Always keep cybersecurity terminology and industry terms in English:\n"
    "   {terms}\n"
    "- Never translate the content of commands, log/JSON/YAML extracts, code "
    "blocks, file names, tool or product names, or raw data — reproduce them "
    "exactly as-is in English.\n"
    "- Keep the same cybersecurity mentor persona, learner-level teaching depth, "
    "concise style, and Markdown formatting you normally use, just in {language}."
)

_MIXED_TEMPLATE = (
    "[Response Language]\n"
    "- Write naturally in {language}, seamlessly switching into English where it "
    "feels natural — a practical, friendly {mixin} (bilingual) style, like a SOC "
    "analyst taking notes.\n"
    "- Write the {language} portions in the {language} script and keep them "
    "readable; mix in English words and phrases naturally.\n"
    "- Always keep cybersecurity terminology and industry terms in English:\n"
    "   {terms}\n"
    "- Never mix or translate the content of commands, log/JSON/YAML extracts, "
    "code blocks, file names, tool or product names, or raw data — reproduce them "
    "exactly as-is in English.\n"
    "- Keep the same cybersecurity mentor persona, learner-level teaching depth, "
    "concise style, and Markdown formatting you normally use."
)

_MANUAL_MIXED_TEMPLATE = (
    "[Response Language]\n"
    "- The user explicitly chose {mixin} (bilingual {language} + English). Write "
    "their reply in a natural {mixin} style: {language} in the {language} script, "
    "mixing in English words and phrases where it feels natural — like a SOC "
    "analyst taking notes.\n"
    "- Do NOT switch completely to the language the user typed; keep this "
    "{mixin} code-mixed style for the whole reply.\n"
    "- Always keep cybersecurity terminology and industry terms in English:\n"
    "   {terms}\n"
    "- Never mix or translate the content of commands, log/JSON/YAML extracts, "
    "code blocks, file names, tool or product names, or raw data — reproduce them "
    "exactly as-is in English.\n"
    "- Keep the same cybersecurity mentor persona, learner-level teaching depth, "
    "concise style, and Markdown formatting you normally use."
)

# Source of the resolved language, reported in API metadata.
RESOLUTION_SOURCE_MANUAL = "manual"
RESOLUTION_SOURCE_STORED = "stored"
RESOLUTION_SOURCE_DETECTED = "detected"


def build_language_block(code: str, source: Optional[str] = None) -> str:
    """Return the system-prompt language block for ``code``.

    ``source`` mirrors the LanguageContextStage resolution source; when the user
    explicitly selected the language ("manual" or "stored") an unambiguous
    "reply ONLY in {language}" block is used so the model never falls back to
    the language the user typed. English and unknown codes return an empty
    string (no block → the prompt is byte-for-byte identical to the
    pre-multilingual behaviour).
    """
    if not is_concrete_code(code) or code == "en":
        return ""
    terms = preserved_terms_text()
    if code in MIXED_LANGUAGE_CODES:
        lang = _LANGUAGE_NAME.get(BASE_LANGUAGE_FOR_MIXED.get(code, code), language_label(code))
        template = (
            _MANUAL_MIXED_TEMPLATE
            if source in (RESOLUTION_SOURCE_MANUAL, RESOLUTION_SOURCE_STORED)
            else _MIXED_TEMPLATE
        )
        return template.format(language=lang, mixin=_MIX_NAME.get(code, "mixed"), terms=terms)
    lang = _LANGUAGE_NAME.get(code, language_label(code))
    if source in (RESOLUTION_SOURCE_MANUAL, RESOLUTION_SOURCE_STORED):
        return _MANUAL_PURE_TEMPLATE.format(language=lang, terms=terms)
    return _PURE_TEMPLATE.format(language=lang, terms=terms)


# Confidence threshold above which an auto-detected language overrides a stored
# preference (i.e. the user clearly switched scripts).
SWITCH_THRESHOLD = 0.9