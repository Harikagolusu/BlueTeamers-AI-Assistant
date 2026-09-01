import re
import html
import unicodedata
import urllib.parse
from typing import List, Pattern
from app.guardrails.domain.interfaces.regex_interface import IRegexEngine

# Characters attackers insert to split trigger words past naive regex matching:
# zero-width spaces/joiners, bidi controls and soft hyphens.
_STEALTH_CHARS_RE = re.compile(r"[\u200b-\u200f\u202a-\u202e\u2060\ufeff\u00ad]")

# Cyrillic homoglyphs that visually mimic Latin (audit C-02): map to Latin for detection
# Only the subset that appears in "ignore previous instructions" etc. — not full alphabet
# to avoid over-folding legitimate Cyrillic course content (e.g., Russian lesson titles).
_CYRILLIC_HOMOGLYPH_MAP = str.maketrans({
    "\u0430": "a",  # а -> a
    "\u0435": "e",  # е -> e
    "\u043e": "o",  # о -> o (audit payload "ignоre")
    "\u0440": "p",  # р -> p
    "\u0441": "c",  # с -> c
    "\u0443": "y",  # у -> y
    "\u0445": "x",  # х -> x
    "\u0456": "i",  # і -> i
    "\u043a": "k",  # к -> k
    "\u043c": "m",  # м -> m
    "\u043d": "n",  # н -> n
    "\u0432": "b",  # в -> b
    "\u0442": "t",  # т -> t
})


class RegexEngineAdapter(IRegexEngine):
    """Infrastructure adapter for fast regex-based evaluation."""
    
    def __init__(self, patterns: List[str]):
        self._compiled_patterns: List[Pattern] = [
            re.compile(p, re.IGNORECASE) for p in patterns
        ]

    def contains_match(self, text: str) -> bool:
        """Returns True if any pattern matches the text.

        The text is normalized before matching (audit C-02/C-04/C-05): HTML
        entities (&#105;), URL percent-encoding (%69), Unicode NFKC, and
        Cyrillic homoglyphs (о->o) are decoded/folded, stealth characters
        (zero-width/bidi/soft-hyphen) are removed and runs of whitespace are
        collapsed, so ``ig\u200bnore``, ``ignоre``, ``&#105;gnore``,
        ``%69gnore`` cannot slip past.
        """
        if not text:
            return False
        # C-04/C-05: decode HTML entities and URL percent-encoding before matching
        # Loop until stable in case of double-encoding (e.g., %26#105;)
        normalized = text
        for _ in range(2):
            html_decoded = html.unescape(normalized)
            url_decoded = urllib.parse.unquote(html_decoded)
            if url_decoded == normalized:
                normalized = html_decoded
                break
            normalized = url_decoded
        else:
            normalized = html.unescape(normalized)
        # C-02: Unicode NFKC + Cyrillic homoglyph folding (audit payload "ignоre")
        try:
            normalized = unicodedata.normalize("NFKC", normalized)
        except Exception:
            pass
        # Fold common Cyrillic lookalikes to Latin (only subset to avoid FP on real Cyrillic)
        normalized = normalized.translate(_CYRILLIC_HOMOGLYPH_MAP)
        normalized = _STEALTH_CHARS_RE.sub("", normalized)
        normalized = re.sub(r"\s+", " ", normalized)
        for pattern in self._compiled_patterns:
            if pattern.search(normalized):
                return True
        # Space-stuffing defence: also test the text with all whitespace
        # removed against whitespace-stripped patterns, so ``ig nore
        # previous instructions`` cannot slip through. A benign sentence is
        # vanishingly unlikely to contain an injection phrase contiguously
        # once spaces are stripped.
        squeezed = re.sub(r"\s+", "", normalized)
        if squeezed != normalized:
            for pattern in self._compiled_patterns:
                spaced_pattern = re.sub(r"\\s\+|\s+", "", pattern.pattern)
                try:
                    if re.search(spaced_pattern, squeezed, re.IGNORECASE):
                        return True
                except re.error:
                    continue
        return False
