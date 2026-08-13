"""Rule-based language detector for Indian-language chat inputs.

Two-pass detection, deliberately dependency-free and fast:

1. **Script pass** — scans Unicode code points for Indic / Perso-Arabic scripts
   and returns the matching native-script mode (confidence ~0.95). Devanagari
   is disambiguated between Hindi and Marathi with a Marathi function-word
   lexicon.
2. **Language-request pass** — for Latin-script text, matches explicit
   requests to answer in a specific language — English ("explain in Telugu",
   "in Hindi please") or romanized ("telugu lo cheppava", "hindi me batao") —
   and returns the matching native-script mode (confidence ~0.95, above the
   stored-preference switch threshold).
3. **Romanized pass** — for Latin-script text, matches lightweight romanized
   word lexicons for Telugu and returns the Tinglish bilingual code-mixed mode (
   ``te+en``) so a query like "SIEM ante enti?" is answered in Tinglish
   (confidence ~0.65).
4. **Fallback** — anything else is English.

The detector is a pure, synchronous, dependency-free heuristic. It never
touches IO and is safe to call on every request.
"""
import re
from collections import defaultdict
from typing import Dict, Tuple

# --------------------------------------------------------------------------
# Unicode script ranges
# --------------------------------------------------------------------------
_SCRIPT_RANGES: Dict[str, Tuple[int, int]] = {
    "devanagari": (0x0900, 0x097F),  # Hindi / Marathi / Sanskrit
    "bengali": (0x0980, 0x09FF),     # Bengali / Assamese
    "gurmukhi": (0x0A00, 0x0A7F),    # Punjabi
    "gujarati": (0x0A80, 0x0AFF),
    "oriya": (0x0B00, 0x0B7F),
    "tamil": (0x0B80, 0x0BFF),
    "telugu": (0x0C00, 0x0C7F),
    "kannada": (0x0C80, 0x0CFF),
    "malayalam": (0x0D00, 0x0D7F),
    "sinhala": (0x0D80, 0x0DFF),
    "arabic": (0x0600, 0x06FF),      # Urdu
    "thai": (0x0E00, 0x0E7F),
    "greek": (0x0370, 0x03FF),
    "cyrillic": (0x0400, 0x04FF),
}

# Script -> detection code (native-script mode).
_SCRIPT_TO_CODE = {
    "devanagari": "hi",  # disambiguated hi/mr in detect()
    "telugu": "te",
    "tamil": "ta",
    "kannada": "kn",
    "malayalam": "ml",
    "bengali": "bn",
    "gujarati": "gu",
    "gurmukhi": "pa",
    "oriya": "or",
    "sinhala": "si",
    "arabic": "ur",
    "thai": "th",
    "greek": "el",
    "cyrillic": "ru",
}

# Persian/Arabic supplementary ranges used by Urdu/Urduish.
_ARABIC_EXT_RANGES = ((0x0750, 0x077F), (0xFB50, 0xFDFF), (0xFE70, 0xFEFF))

# Extra vowel signs that are already inside the base ranges — nothing extra needed.

# --------------------------------------------------------------------------
# Devanagari disambiguation: Marathi vs Hindi function words
# --------------------------------------------------------------------------
_MARATHI_DEVAWORDS = (
    "आहे", "नाही", "होते", "होती", "करण्यासाठी", "मध्ये", "त्यामुळे",
    "पाहिजे", "झाले", "झाली", "काय", "का", "आणि", "साठी", "वरून",
    "नंतर", "आत्ता", "आहेत", "वाटते", "बरं", "होतं",
)

# --------------------------------------------------------------------------
# Romanized lexicons (Latin-script transliteration) -> Tinglish mode
# --------------------------------------------------------------------------
_ROMANIZED: Dict[str, Tuple[str, Dict[str, int]]] = {
    # (bilingual mode, word -> weight)
    "te+en": ("te+en", {
        "ante": 3, "enti": 3, "kavali": 2, "avali": 2, "ledu": 2, "undi": 2,
        "vundi": 2, "untundi": 2, "cheppu": 2, "cheppandi": 2, "ela": 2,
        "enduku": 2, "yendi": 2, "tappu": 2, "bagundi": 2, "ippudu": 2,
        "appudu": 2, "inko": 2, "emanna": 2, "oka": 1, "chala": 2, "baaga": 2,
        "ra": 2, "rando": 2, "raa": 2, "sare": 2, "thamanam": 1, "endi": 2,
        # Natural conversational Telugu (romanized) — user-friendly Tinglish
        # queries like "wazuh ela work avtundi?" or "phishing ni ela cheyali?".
        "avtundi": 2, "avutundi": 2, "untadi": 2, "cheyali": 2, "cheyochu": 2,
        "chudali": 2, "kosam": 2, "nundi": 2, "valla": 2, "manam": 2,
        "ardham": 2, "em": 1, "kuda": 1, "tho": 1, "vasthundi": 2,
        "raavali": 2, "kavaliante": 2, "elaanti": 2, "eppudu": 2, "eppati": 2,
        "gurinchi": 2, "chepthava": 2, "chepthara": 2, "chepthe": 2,
        # Common conversational words that were previously missed, causing a
        # Tinglish query to fall below SWITCH_THRESHOLD and be overridden by a
        # stored preference (e.g. "siem ante emiti", "hacker ante evaru",
        # "log analysis ela chestaru").
        "emiti": 3, "evaru": 3, "evadiki": 2, "evadi": 2, "chestaru": 3,
        "chestunnaru": 3, "cheyyali": 2, "cheyadam": 2, "unnayi": 2,
        "untayi": 2, "cheptanu": 2, "cheptaa": 2, "teliyadu": 2, "chudandi": 2,
        "chudam": 2, "evad": 2,
        # Casual Tenglish requests like "easy gaa cheppava" / "cheppandi easy
        # ga" — previously these fell through detection as English.
        "gaa": 2, "ga": 1, "cheppava": 3, "cheppavaa": 3, "cheppara": 3,
        "chepthavaa": 3, "cheppamante": 2, "chepthaga": 2, "thaamane": 2,
        "echi": 2, "panikostundi": 2, "baguntundi": 2, "avate": 2, "kadu": 2,
        "idi": 2, "adi": 2, "ivanni": 2, "aavi": 2, "cheyagalava": 3,
        "cheyachu": 2, "cheppagalava": 3, "arpudu": 2, "easyga": 3,
    }),
}

# --------------------------------------------------------------------------
# Explicit language-request detection (Latin-script text)
# --------------------------------------------------------------------------
# Language name (romanized/English alias) -> native-script mode code.
_LANGUAGE_NAMES: Dict[str, str] = {
    "telugu": "te",
    "hindi": "hi",
    "tamil": "ta",
    "tamizh": "ta",
    "kannada": "kn",
    "malayalam": "ml",
    "bengali": "bn",
    "bangla": "bn",
    "marathi": "mr",
    "gujarati": "gu",
    "punjabi": "pa",
    "odia": "or",
    "oriya": "or",
    "urdu": "ur",
    "english": "en",
}

# Words that signal the user explicitly wants a reply in that language:
# English request verbs / prepositions + romanized request words from each
# Indian language ("lo cheppandi", "me batao", "la solunga", "dalli heli" ...).
_REQUEST_MARKERS = {
    # English
    "in", "please", "explain", "answer", "reply", "respond", "tell",
    "translate", "write",
    # Telugu
    "lo", "cheppu", "cheppandi", "cheppava", "cheppavaa", "entha", "nuvvu",
    # Hindi / Urdu
    "me", "mein", "batao", "bataiye", "kaho", "bolo", "bol",
    # Tamil
    "la", "il", "solunga", "sollunga", "sollu",
    # Kannada
    "dalli", "alli", "heli", "helli", "heelli",
    # Malayalam
    "parayu", "parayoo", "paranj",
    # Marathi
    "madhe", "sanga", "bolava",
    # Bengali
    "bolo", "bol", "lekh",
    # Gujarati
    "ma", "keh", "keho",
    # Punjabi
    "vich", "dasso", "dass",
    # Odia
    "re", "kuhu", "kahile",
}

# Max token distance between a language name and a request marker.
_REQUEST_WINDOW = 5


def _char_script(char: str) -> str | None:
    """Return the script name a single character belongs to, or None."""
    cp = ord(char)
    for name, (lo, hi) in _SCRIPT_RANGES.items():
        if lo <= cp <= hi:
            return name
    for lo, hi in _ARABIC_EXT_RANGES:
        if lo <= cp <= hi:
            return "arabic"
    return None


_WORD_RE = re.compile(r"[a-zA-Z\u0100-\u024F]+")

# Codes we know how to detect at all (native or romanized).
_SUPPORTED_NATIVE = {"te", "ta", "kn", "ml", "bn", "gu", "pa", "or", "si", "ur", "th", "el", "ru"}
_ROMAN_CODES = {meta[0] for meta in _ROMANIZED.values()}


class LanguageDetector:
    """Stateless, dependency-free heuristic language detector."""

    def detect(self, text: str) -> Tuple[str, float]:
        """Detect the language of ``text``.

        Returns ``(code, confidence)`` where ``code`` is a concrete mode
        (native-script code or bilingual code-mixed code) or ``en``.
        """
        text = text or ""
        stripped = text.strip()
        if not stripped:
            return "en", 0.3

        # ---- Pass 1: native script ------------------------------------
        script_counts: Dict[str, int] = defaultdict(int)
        total = 0
        for ch in stripped:
            script = _char_script(ch)
            if script:
                script_counts[script] += 1
                total += 1

        if total > 0:
            dominant, count = max(script_counts.items(), key=lambda kv: kv[1])
            ratio = count / total
            code = _SCRIPT_TO_CODE.get(dominant)
            if code:
                # Devanagari -> Hindi or Marathi (function-word disambiguation).
                if dominant == "devanagari" and code == "hi":
                    code = self._disambiguate_devanagari(stripped)
                elif code == "bn":
                    # Assamese also uses the Bengali script — default to Bengali.
                    code = "bn"
                confidence = min(0.99, 0.7 + 0.25 * ratio)
                return code, confidence

        # ---- Pass 2: explicit language request (Latin script) ------------
        if self._is_latin(stripped):
            req_code = self._match_language_request(stripped)
            if req_code:
                # Romanized request -> bilingual mixed mode (e.g. "telugu lo
                # cheppava" -> te+en) so the reply mirrors the user's style.
                return self._as_mixed(req_code), 0.95

            roman_code, score = self._match_romanized(stripped)
            if roman_code:
                # Confidence scales with lexical match strength so a clear
                # Tinglish query overrides a stored preference in the stage
                # (>= SWITCH_THRESHOLD 0.9). A score-3 match (e.g. "SOC oka
                # example kavali") must already reach 0.9, otherwise a stored
                # preference would wrongly win over an obvious romanized query.
                confidence = min(0.95, 0.6 + 0.1 * score)
                return roman_code, confidence

        # ---- Pass 3: fallback ------------------------------------------
        return "en", 0.9

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _is_latin(text: str) -> bool:
        return all(ord(ch) < 0x2800 for ch in text)  # latin/basic only

    def _disambiguate_devanagari(self, text: str) -> str:
        """Decide Hindi vs Marathi for Devanagari text via Marathi markers."""
        score = 0
        for word in _MARATHI_DEVAWORDS:
            if word in text:
                score += 1
        if score >= 2:
            return "mr"
        # Single strong marker plus short text is enough for "हो" style queries.
        if score == 1 and len(text) <= 40:
            return "mr"
        return "hi"

    def _match_romanized(self, text: str) -> Tuple[str | None, int]:
        """Score romanized lexicons and return the strongest match."""
        words = [w.lower() for w in _WORD_RE.findall(text)]
        if not words:
            return None, 0
        best_code, best_score = None, 0
        for code, (_mode, lexicon) in _ROMANIZED.items():
            score = sum(lexicon.get(w, 0) for w in words)
            if score > best_score:
                best_code, best_score = code, score
        if best_score >= 3:
            return best_code, best_score
        return None, 0

    @staticmethod
    def _as_mixed(code: str) -> str:
        """Convert a native code to its romanized bilingual mode (te -> te+en)."""
        if code == "en":
            return "en"
        return f"{code}+en"

    @staticmethod
    def _match_language_request(text: str) -> str | None:
        """Return the code for an explicit "answer in <language>" request.

        Looks for a language name near a request marker. Both directions are
        supported ("explain in Telugu", "telugu lo cheppandi", "in Hindi
        please"). Returns ``None`` when no confident request is present so the
        callers can fall back to the romanized lexicon / English.
        """
        tokens = [t.lower() for t in _WORD_RE.findall(text)]
        if not tokens:
            return None

        # Language-name token indices.
        name_idx = [i for i, t in enumerate(tokens) if t in _LANGUAGE_NAMES]
        if not name_idx:
            return None

        # Marker token indices.
        marker_idx = [i for i, t in enumerate(tokens) if t in _REQUEST_MARKERS]
        if not marker_idx:
            return None

        # Pick the language whose name is closest to a marker; if that pair is
        # out of window we do not treat it as a request.
        best_name, best_dist = None, None
        for ni in name_idx:
            name = tokens[ni]
            for mi in marker_idx:
                dist = abs(ni - mi)
                if dist <= _REQUEST_WINDOW and (best_dist is None or dist < best_dist):
                    best_name, best_dist = name, dist

        if best_name is None:
            return None
        return _LANGUAGE_NAMES[best_name]