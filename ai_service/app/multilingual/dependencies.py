"""DI helpers for the multilingual subsystem."""
from app.multilingual.detector import LanguageDetector
from app.multilingual.preferences import LanguagePreferenceStore

_store: LanguagePreferenceStore | None = None


def get_language_detector() -> LanguageDetector:
    """Return a shared, stateless detector."""
    return LanguageDetector()


def get_language_preference_store() -> LanguagePreferenceStore:
    """Return a process-wide singleton preference store."""
    global _store
    if _store is None:
        _store = LanguagePreferenceStore()
    return _store