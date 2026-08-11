"""Language catalog for the BlueTeamers AI multilingual experience.

Defines every language mode the assistant can respond in, including the single
special bilingual code-mixed mode ``te+en`` "Tinglish", which keeps technical
terms in English while switching naturally between Telugu and English.

Codes follow BCP-47-style tags so they interoperate with browser ``signal.format``
apart from the mixed mode, which uses a simple ``lang+en`` convention.
"""
from enum import Enum
from typing import Dict, Generator, Tuple


class LanguageMode(str, Enum):
    """Enumerated language codes usable in the chat request / preference store."""

    AUTO = "auto"
    ENGLISH = "en"

    # Indian languages (native script modes)
    HINDI = "hi"
    TELUGU = "te"
    TAMIL = "ta"
    KANNADA = "kn"
    MALAYALAM = "ml"
    BENGALI = "bn"
    MARATHI = "mr"
    GUJARATI = "gu"
    PUNJABI = "pa"
    ODIA = "or"
    URDU = "ur"
    ASSAMESE = "as"

    # Bilingual code-mixed mode (Telugu + English)
    TELUGLISH = "te+en"

    @classmethod
    def auto_code(cls) -> str:
        return cls.AUTO.value

    @classmethod
    def english(cls) -> str:
        return cls.ENGLISH.value


# Display metadata per language mode.
#   name    -> language name in English
#   native  -> language name in its own script
#   script  -> human-readable script label
LANGUAGE_META: Dict[str, Dict[str, str]] = {
    "auto": {"name": "Auto Detect", "native": "Auto", "script": "Automatic"},
    "en": {"name": "English", "native": "English", "script": "Latin"},
    "hi": {"name": "Hindi", "native": "हिन्दी", "script": "Devanagari"},
    "te": {"name": "Telugu", "native": "తెలుగు", "script": "Telugu"},
    "ta": {"name": "Tamil", "native": "தமிழ்", "script": "Tamil"},
    "kn": {"name": "Kannada", "native": "ಕನ್ನಡ", "script": "Kannada"},
    "ml": {"name": "Malayalam", "native": "മലയാളം", "script": "Malayalam"},
    "bn": {"name": "Bengali", "native": "বাংলা", "script": "Bengali"},
    "mr": {"name": "Marathi", "native": "मराठी", "script": "Devanagari"},
    "gu": {"name": "Gujarati", "native": "ગુજરાતી", "script": "Gujarati"},
    "pa": {"name": "Punjabi", "native": "ਪੰਜਾਬੀ", "script": "Gurmukhi"},
    "or": {"name": "Odia", "native": "ଓଡ଼ିଆ", "script": "Odia"},
    "ur": {"name": "Urdu", "native": "اردو", "script": "Perso-Arabic"},
    "as": {"name": "Assamese", "native": "অসমীয়া", "script": "Bengali"},
    "te+en": {"name": "Tinglish", "native": "తెలుగు + English", "script": "Telugu"},
}

# Codes that represent a concrete response language (excludes "auto").
CONCRETE_LANGUAGE_CODES = frozenset(code for code in LANGUAGE_META if code != "auto")

# Codes that always render the response in the *base* language only (no mixing).
PURE_LANGUAGE_CODES = frozenset(
    {
        "en", "hi", "te", "ta", "kn", "ml", "bn", "mr",
        "gu", "pa", "or", "ur", "as",
    }
)

# Codes that purposely code-mix English with the native language.
MIXED_LANGUAGE_CODES = frozenset(
    {code for code in CONCRETE_LANGUAGE_CODES if code not in PURE_LANGUAGE_CODES}
)

# Map a mixed code to its base language code (e.g. te+en -> te).
BASE_LANGUAGE_FOR_MIXED: Dict[str, str] = {
    code: code.split("+")[0] for code in MIXED_LANGUAGE_CODES
}


def is_supported_code(code: str) -> bool:
    """True if the string is a known language code (including ``auto``)."""
    return bool(code) and code in LANGUAGE_META


def is_concrete_code(code: str) -> bool:
    """True if the string is a known *concrete* (non-auto) language code."""
    return bool(code) and code in CONCRETE_LANGUAGE_CODES


def language_label(code: str) -> str:
    """Human-readable primary label for a language code."""
    meta = LANGUAGE_META.get(code) or LANGUAGE_META["auto"]
    return meta["name"]


def native_label(code: str) -> str:
    """Native-script name for a language code."""
    meta = LANGUAGE_META.get(code) or LANGUAGE_META["auto"]
    return meta["native"]


def display_label(code: str) -> str:
    """Combined label used in the UI selector, e.g. 'Telugu (తెలుగు)'."""
    if code in ("auto", "en"):
        return language_label(code)
    native = native_label(code)
    return f"{language_label(code)} ({native})" if native and native != language_label(code) else language_label(code)


def catalog_options() -> Generator[Tuple[str, str], None, None]:
    """Yield (code, display_label) pairs ordered for the UI selector."""
    order = [
        "auto", "en", "te", "te+en", "hi", "ta",
        "kn", "ml", "mr", "bn", "gu", "pa", "or",
    ]
    for code in order:
        if code in LANGUAGE_META:
            yield code, display_label(code)