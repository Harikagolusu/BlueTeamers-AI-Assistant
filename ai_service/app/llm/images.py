"""Image payload normalization for multimodal LLM providers.

Conversions:
  - data URL (data:image/png;base64,...)  -> {"mime", "format", "bytes"}
  - bare base64 string                    -> {"mime": image/png default, ...}
  - already-normalized dict                -> passed through
"""
import base64
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("app.llm.images")

_MIME_TO_FORMAT = {
    "image/png": "png",
    "image/jpeg": "jpeg",
    "image/jpg": "jpeg",
    "image/gif": "gif",
    "image/webp": "webp",
    "image/bmp": "jpeg",
    "image/tiff": "jpeg",
}


def normalize_images(images: Any) -> Optional[List[Dict[str, Any]]]:
    """Normalize a list of image payloads into {mime, format, bytes} dicts."""
    if not images:
        return None
    out: List[Dict[str, Any]] = []
    for img in images:
        if isinstance(img, dict) and isinstance(img.get("bytes"), (bytes, bytearray)):
            mime = (img.get("mime") or img.get("type") or "image/png").lower()
            fmt = img.get("format") or _MIME_TO_FORMAT.get(mime, "png")
            out.append({"mime": mime, "format": fmt, "bytes": bytes(img["bytes"])})
            continue

        if isinstance(img, dict):
            mime = (img.get("type") or img.get("mime") or "image/png").lower()
            payload = img.get("data") or img.get("content") or img.get("url")
        else:
            mime = "image/png"
            payload = img

        if not isinstance(payload, str):
            continue

        raw: bytes
        if payload.startswith("data:"):
            header, _, b64 = payload.partition(",")
            if ";" in header:
                mime = header[5:header.find(";")].lower()
            else:
                mime = header[5:].lower()
            try:
                raw = base64.b64decode(b64)
            except Exception as e:
                logger.warning("Skipping image: invalid base64 data URL (%s)", e)
                continue
        else:
            stripped = payload.strip()
            if not stripped:
                continue
            try:
                raw = base64.b64decode(stripped)
            except Exception:
                raw = payload.encode("utf-8")

        fmt = _MIME_TO_FORMAT.get(mime, "png")
        out.append({"mime": mime, "format": fmt, "bytes": raw})

    return out or None
