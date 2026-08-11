import re
from typing import List, Pattern
from app.guardrails.domain.interfaces.regex_interface import IRegexEngine

class RegexEngineAdapter(IRegexEngine):
    """Infrastructure adapter for fast regex-based evaluation."""
    
    def __init__(self, patterns: List[str]):
        self._compiled_patterns: List[Pattern] = [
            re.compile(p, re.IGNORECASE) for p in patterns
        ]

    def contains_match(self, text: str) -> bool:
        """Returns True if any pattern matches the text."""
        for pattern in self._compiled_patterns:
            if pattern.search(text):
                return True
        return False
