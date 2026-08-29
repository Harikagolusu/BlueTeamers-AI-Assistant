import re
from typing import List, Pattern
from app.guardrails.domain.interfaces.regex_interface import IRegexEngine

# Characters attackers insert to split trigger words past naive regex matching:
# zero-width spaces/joiners, bidi controls and soft hyphens.
_STEALTH_CHARS_RE = re.compile(r"[\u200b-\u200f\u202a-\u202e\u2060\ufeff\u00ad]")


class RegexEngineAdapter(IRegexEngine):
    """Infrastructure adapter for fast regex-based evaluation."""
    
    def __init__(self, patterns: List[str]):
        self._compiled_patterns: List[Pattern] = [
            re.compile(p, re.IGNORECASE) for p in patterns
        ]

    def contains_match(self, text: str) -> bool:
        """Returns True if any pattern matches the text.

        The text is normalized before matching (audit A-02): stealth
        characters (zero-width/bidi/soft-hyphen) are removed and runs of
        whitespace are collapsed, so ``ig\u200bnore previous instructions`` or
        ``ignore    previous`` cannot slip past the policy by obfuscation.
        """
        if not text:
            return False
        normalized = _STEALTH_CHARS_RE.sub("", text)
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
