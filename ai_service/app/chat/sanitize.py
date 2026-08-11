"""Sanitize assistant replies so internal artifacts never reach the user.

The prompt pipeline tells the model not to emit internal tags, but a safety-net
pass is cheap insurance. It strips only patterns that are clearly not
user-facing content:

  - ``[Document N]`` prefixes / inline source markers
  - ``Source:`` / ``--- SOURCE: ...`` lines
  - ``Agent:`` / ``Latency:`` / ``Trace-ID`` style debug footers

It deliberately does NOT touch markdown (tables, lists, code) or the actual
answer content.
"""
import re

_DOCUMENT_TAG_RE = re.compile(
    r"^\s*\[Document \d+\]\s*(?:\([^)]*\))?\s*:?\s*$", re.MULTILINE
)
_DOCUMENT_TAG_INLINE_RE = re.compile(
    r"\[Document \d+\]\s*(?:\([^)]*\))?\s*:?\s*", re.MULTILINE
)
_SOURCE_LINE_RE = re.compile(
    r"^\s*(?:---\s*)?SOURCE\s*[: -].*$", re.IGNORECASE | re.MULTILINE
)
_SOURCES_HEADER_RE = re.compile(
    r"^\s*#+\s*(?:Sources?|References?)\s*$", re.IGNORECASE | re.MULTILINE
)
_SOURCES_FOOTER_RE = re.compile(
    r"^\s*(?:Sources?|References?)\s*[:—-].*$", re.IGNORECASE | re.MULTILINE
)
_DEBUG_TAG_RE = re.compile(
    r"(?:^|\s)(?:agent|latency|trace\s*-?\s*id|request\s*-?\s*id|tokens?|engine)"
    r"\s*[:=]\s*[^\s,;\n]{0,60}",
    re.IGNORECASE,
)


def clean_response(text: str) -> str:
    """Return `text` with internal-tag artifacts removed."""
    if not text:
        return text

    cleaned = _DOCUMENT_TAG_RE.sub("", text)
    cleaned = _DOCUMENT_TAG_INLINE_RE.sub("", cleaned)
    cleaned = _SOURCE_LINE_RE.sub("", cleaned)
    cleaned = _SOURCES_HEADER_RE.sub("", cleaned)
    cleaned = _SOURCES_FOOTER_RE.sub("", cleaned)
    cleaned = _DEBUG_TAG_RE.sub("", cleaned)

    # Collapse runs of blank lines left by removals and tidy the edges.
    cleaned = re.sub(r"[ \t]+$", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned
