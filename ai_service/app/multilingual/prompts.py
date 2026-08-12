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
    "hi+en": "Hinglish",
    "ta+en": "Tanglish",
    "kn+en": "Kanglish",
    "ml+en": "Manglish",
    "bn+en": "Banglish",
    "mr+en": "Marathish",
    "gu+en": "Gujarlish",
    "pa+en": "Punglish",
    "or+en": "Odia-English",
    "ur+en": "Urlish",
}

# Natural romanized function words / connectives per base language, used to
# teach the model the native conversational skeleton the reply must follow.
_MIX_FUNCTION_WORDS = {
    "te": "ante, enti, ela, enduku, kosam, nundi, tho, valla, cheyali, cheyochu, "
          "untundi, avtundi, chudali, ardham chesukovali, okavela, appudu, "
          "ippudu, inka, kuda, manam, naa",
    "hi": "matlab, kya, kaise, kyun, ke liye, se, isliye, chahiye, sakte hain, "
          "hai, hota hai, dekhte hain, phir, ab, bhi, hi, toh, hum",
    "ta": "naan, enna, eppadi, yen, ku, la, irukku, mudiyum, pannanum, "
          "pannalam, paakkalaam, appo, ippo, um, kooda, mattum",
    "kn": "enu, hege, yake, gagi, inda, jote, alli, maadbodu, madabahudu, "
          "ide, aagutte, noda, ardham maadkoloo, aaga, eega, kooda, matra",
    "ml": "aa, enthu, enggane, enthinu, kaayi, il, oru, kond, cheyyanam, "
          "cheyyaam, kaanam, ennu, appol, ippol, um, koode, mathram",
    "bn": "matlab, ki, kivabe, keno, jonno, theke, sathe, hole, korte hobe, "
          "kora jay, dekhte hobe, tahole, ekhon, o, abar, sudhu",
    "mr": "matlab, kay, kase, kashala, sathi, madhe, sobat, kartat, karto, "
          "karu shakto, pahila, mag, aata, pan, fakt",
    "gu": "matlab, shu, kem, mate, thi, sathe, joie, karvu pade, kari shakay, "
          "jovu, pachhi, have, pan, matra",
    "pa": "matlab, ki, kive, kyon, layi, ton, naal, hona chahida, ho sakda, "
          "dekho, phir, hun, vi, sirf",
    "or": "matlab, ki, kivabe, kenh, paai, ru, sahit, karibaku, kariba, "
          "dekhiba, achi, pare, bhi, kebal",
    "ur": "matlab, kya, kaise, kyun, ke liye, se, ke saath, chahiye, sakte "
          "hain, hai, dekhte hain, phir, ab, bhi, sirf",
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
    "- Respond in natural conversational {mixin}: this is {language} spoken the way "
    "a {language} person casually types in English letters (romanized). The reply "
    "must sound like a {language} person chatting, NOT like an English answer with "
    "a few {language} words inserted.\n"
    "- Build every sentence on {language} grammar and word order. Use the natural "
    "{language} function words and connectives: {funcs}\n"
    "- Keep ONLY technical cybersecurity terminology and industry terms in "
    "English:\n"
    "   {terms}\n"
    "- Never translate commands, log/JSON/YAML extracts, code blocks, file "
    "names, tool or product names, or raw data — reproduce them exactly as-is "
    "in English.\n"
    "- Do not translate the {mixin} connective/grammar words into English and do "
    "not write English sentences with {language} words sprinkled in.\n"
    "- Keep the same cybersecurity mentor persona, learner-level teaching depth, "
    "concise style, and Markdown formatting you normally use."
)

_MANUAL_MIXED_TEMPLATE = (
    "[Response Language]\n"
    "- The user explicitly chose {mixin} (bilingual {language} + English). Write "
    "their reply in natural conversational {mixin}: {language} spoken the way a "
    "{language} person casually types in English letters (romanized). The reply "
    "must sound like a {language} person chatting, NOT like an English answer "
    "with a few {language} words inserted.\n"
    "- Build every sentence on {language} grammar and word order. Use the natural "
    "{language} function words and connectives: {funcs}\n"
    "- Keep ONLY technical cybersecurity terminology and industry terms in "
    "English:\n"
    "   {terms}\n"
    "- Never translate commands, log/JSON/YAML extracts, code blocks, file "
    "names, tool or product names, or raw data — reproduce them exactly as-is "
    "in English.\n"
    "- Do not write English sentences with {language} words sprinkled in; keep "
    "this {mixin} code-mixed style for the whole reply.\n"
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
        base = BASE_LANGUAGE_FOR_MIXED.get(code, code)
        lang = _LANGUAGE_NAME.get(base, language_label(code))
        funcs = _MIX_FUNCTION_WORDS.get(base, "")
        template = (
            _MANUAL_MIXED_TEMPLATE
            if source in (RESOLUTION_SOURCE_MANUAL, RESOLUTION_SOURCE_STORED)
            else _MIXED_TEMPLATE
        )
        return template.format(language=lang, mixin=_MIX_NAME.get(code, "mixed"), funcs=funcs, terms=terms)
    lang = _LANGUAGE_NAME.get(code, language_label(code))
    if source in (RESOLUTION_SOURCE_MANUAL, RESOLUTION_SOURCE_STORED):
        return _MANUAL_PURE_TEMPLATE.format(language=lang, terms=terms)
    return _PURE_TEMPLATE.format(language=lang, terms=terms)


# Confidence threshold above which an auto-detected language overrides a stored
# preference (i.e. the user clearly switched scripts).
SWITCH_THRESHOLD = 0.9