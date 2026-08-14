"""AttachmentParseStage: turn user-uploaded files/images into real model context.

The chat request accepts `files` (text/log/JSON/PDF data) and `images` (base64
data URLs), but nothing downstream ever consumed them — the LLM only ever saw
the raw query. This stage parses every attachment and injects its content into
the query the model receives, so "analyze this log file" actually works.

Image attachments: the BlueTeamers LLM is text-only (no vision support), so we
cannot analyze the visual content of an image. To make image uploads useful we
run local OCR (RapidOCR/onnxruntime) and feed any extracted text into the
model's context — screenshots of logs, emails, terminal output and sandbox
reports become analyzable. If OCR finds no readable text (e.g. a diagram), we
append an explicit note so the model answers honestly that it cannot see the
image contents.
"""
import base64
import logging
from typing import Any, Dict, Optional

from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext

logger = logging.getLogger("app.chat.pipeline.attachment_parse_stage")

_MAX_FILE_CHARS = 8000
_TEXT_EXTS = (".log", ".txt", ".csv", ".json", ".xml", ".md", ".yaml", ".yml")
_PDF_EXTS = (".pdf",)
_IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff", ".tif")

# Hard cap on the *decoded* byte size of a single attachment (defense in depth
# against decompression bombs / memory-exhaustion DoS). Value mirrors
# MAX_DOCUMENT_SIZE_MB from settings but is enforced here on raw payload bytes
# so oversized uploads never reach the PDF/OCR decoders.
_MAX_DECODED_BYTES = 8 * 1024 * 1024  # 8 MiB per attachment

_ocr_engine: Any = None


def _get_ocr():
    """Lazy singleton RapidOCR engine. Returns None when unavailable."""
    global _ocr_engine
    if _ocr_engine is None:
        try:
            from rapidocr_onnxruntime import RapidOCR

            _ocr_engine = RapidOCR()
        except Exception as e:
            logger.warning("RapidOCR unavailable; image OCR disabled: %s", e)
            _ocr_engine = False
    return _ocr_engine if _ocr_engine else None


class AttachmentParseStage(IExecutionStage):
    @property
    def name(self) -> str:
        return "AttachmentParse"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        if "execution_result" in context.metadata:
            return context

        files: list = context.metadata.get("files") or []
        images: list = context.metadata.get("images") or []
        query: str = context.metadata.get("query", "") or ""

        sections: list[str] = []
        parsed_files = 0
        skipped_files = 0

        for f in files:
            name = f.get("name") or "attachment"
            ftype = (f.get("type") or "").lower()
            text = None
            if ftype.startswith("image/") or name.lower().endswith(_IMAGE_EXTS):
                text = self._extract_image_text(f.get("content"))
            else:
                try:
                    text = self._extract_text(f)
                except Exception as e:
                    logger.warning("Failed to parse attachment %s: %s", name, e)
                    text = None

            if text is None:
                skipped_files += 1
                sections.append(
                    f'<attachment name="{name}" parse="unsupported">'
                    "This file type could not be parsed.</attachment>"
                )
                continue

            parsed_files += 1
            truncated = text[:_MAX_FILE_CHARS]
            if len(text) > _MAX_FILE_CHARS:
                truncated += "\n[... attachment truncated ...]"
            sections.append(f'<attachment name="{name}">\n{truncated}\n</attachment>')

        for idx, img in enumerate(images, 1):
            text = self._extract_image_text(img)
            if text:
                parsed_files += 1
                truncated = text[:_MAX_FILE_CHARS]
                if len(text) > _MAX_FILE_CHARS:
                    truncated += "\n[... attachment truncated ...]"
                sections.append(
                    f'<attachment name="image-{idx}.png" source="ocr">'
                    f'\n{truncated}\n</attachment>'
                )
            else:
                skipped_files += 1
                sections.append(
                    "[Note: an image attachment is present but no readable text was "
                    "found. This assistant is text-only and cannot analyze the visual "
                    "contents of an image. Respond clearly that image analysis is "
                    "unsupported, do not guess the image contents.]"
                )

        if sections:
            query = "\n\n".join(sections) + "\n\nUser request:\n" + query

        new_metadata = {
            **context.metadata,
            "query": query,
            "attachments_parsed": parsed_files,
            "attachments_skipped": skipped_files,
            "images_present": len(images),
            "files": files,
            "images": images,
        }
        return context.model_copy(update={"metadata": new_metadata})

    @staticmethod
    def _decode_bytes(content: Any) -> Optional[bytes]:
        """Return decoded raw bytes for a content value (data URL, str, bytes)."""
        if content is None:
            return None
        if isinstance(content, str) and content.startswith("data:"):
            _, _, b64 = content.partition(",")
            raw = None
            try:
                raw = base64.b64decode(b64)
            except Exception:
                return None
            if len(raw) > _MAX_DECODED_BYTES:
                logger.warning("Attachment exceeds %d bytes; rejected.", _MAX_DECODED_BYTES)
                return None
            return raw
        if isinstance(content, str):
            try:
                raw = content.encode("utf-8")
            except Exception:
                return None
            if len(raw) > _MAX_DECODED_BYTES:
                logger.warning("Attachment exceeds %d bytes; rejected.", _MAX_DECODED_BYTES)
                return None
            return raw
        if isinstance(content, (bytes, bytearray)):
            raw = bytes(content)
            if len(raw) > _MAX_DECODED_BYTES:
                logger.warning("Attachment exceeds %d bytes; rejected.", _MAX_DECODED_BYTES)
                return None
            return raw
        return None

    @staticmethod
    def _extract_text(f: Dict[str, Any]) -> Optional[str]:
        """Return decoded text for a file dict, or None if the type is unsupported."""
        name = (f.get("name") or "").lower()
        raw = AttachmentParseStage._decode_bytes(f.get("content"))
        if raw is None or not raw:
            return ""

        if name.endswith(_PDF_EXTS):
            return AttachmentParseStage._extract_pdf(raw)
        if name.endswith(_TEXT_EXTS) or "." not in name:
            return raw.decode("utf-8", errors="replace")
        return None

    @staticmethod
    def _decode_image_bytes(content: Any) -> Optional[bytes]:
        """Decode an image payload that may be a data URL, raw bytes, or a bare
        base64 string (no data: prefix)."""
        if isinstance(content, str) and not content.startswith("data:"):
            import re

            stripped = content.strip()
            if len(stripped) >= 40 and re.fullmatch(r"[A-Za-z0-9+/=\s]+", stripped):
                try:
                    raw = base64.b64decode(stripped)
                except Exception:
                    pass
                else:
                    if len(raw) > _MAX_DECODED_BYTES:
                        logger.warning(
                            "Image attachment exceeds %d bytes; rejected.", _MAX_DECODED_BYTES
                        )
                        return None
                    return raw
        return AttachmentParseStage._decode_bytes(content)

    @staticmethod
    def _extract_image_text(content: Any) -> Optional[str]:
        """Run OCR on an image and return extracted text, or None if none found."""
        raw = AttachmentParseStage._decode_image_bytes(content)
        if not raw:
            return None
        ocr = _get_ocr()
        if ocr is None:
            return None
        try:
            import cv2
            import numpy as np

            nparr = np.frombuffer(raw, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                return None
            result, _ = ocr(img)
            lines = [r[1] for r in (result or []) if r and len(r) > 1 and r[1]]
            text = "\n".join(lines).strip()
            return text or None
        except Exception as e:
            logger.warning("Image OCR failed: %s", e)
            return None

    @staticmethod
    def _extract_pdf(raw: bytes) -> Optional[str]:
        try:
            from pypdf import PdfReader
        except Exception:
            return None
        try:
            reader = PdfReader(__import__("io").BytesIO(raw))
            pages = [page.extract_text() or "" for page in reader.pages]
            text = "\n".join(pages).strip()
            return text or None
        except Exception as e:
            logger.warning("PDF text extraction failed: %s", e)
            return None
