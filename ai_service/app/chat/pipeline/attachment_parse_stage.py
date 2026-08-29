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
import asyncio
from typing import Any, Dict, Optional

from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.chat.pipeline.guardrails_stage import (
    BLOCKED_MESSAGE,
    _guardrail_context,
)
from app.guardrails.domain.services.guardrails_service import GuardrailsService
from app.guardrails.exceptions.guardrail_exceptions import PolicyViolationError
from app.models.chat.chat_models import ExecutionResult, ExecutionStatus

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

# Maximum pixel count for decoded images (a ~4000x4000 image). Prevents tiny
# crafted PNG/WebP headers declaring enormous dimensions from allocating GBs of
# memory in cv2/PIL before we ever touch the pixel data.
_MAX_IMAGE_PIXELS = 16_000_000  # 16 MP

# Maximum number of pages extracted from a PDF and max cumulative extracted
# characters, so a few-KB "PDF bomb" cannot expand to hundreds of MB of text.
_MAX_PDF_PAGES = 200
_MAX_PDF_CHARS = 200_000

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
    """Parses user attachments and injects their content into the model query.

    Security (audit A-01): attachment-derived text bypasses
    ``InputGuardrailsStage`` (which runs on the raw query only, earlier in the
    pipeline). After injection, the combined query is therefore re-validated
    through the same input-guardrails pipeline here, so injected attachment
    content (e.g. template smuggling or instruction-override text) cannot
    reach the model unchecked. Benign attachments are unaffected.
    """

    def __init__(self, guardrails_service: Optional[GuardrailsService] = None):
        self._guardrails = guardrails_service

    @property
    def name(self) -> str:
        return "AttachmentParse"

    @staticmethod
    def _sanitize_label(value: str, default: str) -> str:
        """Sanitize a user-supplied attachment label for prompt interpolation.

        Strips control characters and HTML marker bytes so a crafted ``name``
        (e.g. ``x</attachment> ignore previous instructions ...``) cannot break
        out of the delimiters or smuggle tags into the model's context.
        """
        cleaned = "".join(
            ch for ch in value if (ch.isprintable() and ch not in "<>")
        ).strip()
        return (cleaned or default)[:200]

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        if "execution_result" in context.metadata:
            return context

        files: list = context.metadata.get("files") or []
        images: list = context.metadata.get("images") or []
        query: str = context.metadata.get("query", "") or ""

        # Keep the user's original, unmodified request available for
        # persistence/history stages. The injected OCR/attachment text below
        # must reach the LLM, but it must never be persisted back into
        # conversation memory — otherwise the fallback note ("text-only...")
        # would be replayed into every follow-up turn of the same chat.
        original_query = context.metadata.get("user_query") or query

        sections: list[str] = []
        parsed_files = 0
        skipped_files = 0

        for f in files:
            name = self._sanitize_label(f.get("name") or "attachment", "attachment")
            ftype = (f.get("type") or "").lower()
            text = None
            if ftype.startswith("image/") or name.lower().endswith(_IMAGE_EXTS):
                text = await self._extract_image_text(f.get("content"))
            else:
                try:
                    text = await self._extract_text(f)
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
            text = await self._extract_image_text(img)
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

            # Audit A-01: re-run the input-guardrails pipeline over the combined
            # query (user request + attachment-derived text). Attachment content
            # never passed through InputGuardrailsStage, so without this check
            # injected instructions/template tokens inside an upload reached the
            # model unchecked. A violation short-circuits the same graceful way
            # as InputGuardrailsStage (blocked ExecutionResult).
            if self._guardrails is not None:
                try:
                    await self._guardrails.validate_input(
                        _guardrail_context(context, query, stage="attachment_input")
                    )
                except PolicyViolationError as e:
                    logger.warning(
                        "Input blocked by guardrails (attachment content): %s", e
                    )
                    result = ExecutionResult(
                        status=ExecutionStatus.BLOCKED,
                        engine_name="guardrails",
                        message=BLOCKED_MESSAGE,
                        metadata={
                            "guardrail_blocked": True,
                            "guardrail_reason": str(e),
                            "guardrail_stage": "attachment_input",
                        },
                    )
                    return context.model_copy(
                        update={
                            "metadata": {
                                **context.metadata,
                                "execution_result": result,
                                "guardrail_blocked": True,
                                "guardrail_reason": str(e),
                            }
                        }
                    )

        new_metadata = {
            **context.metadata,
            "query": query,
            "user_query": original_query,
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
    async def _extract_text(f: Dict[str, Any]) -> Optional[str]:
        """Return decoded text for a file dict, or None if the type is unsupported."""
        name = (f.get("name") or "").lower()
        raw = AttachmentParseStage._decode_bytes(f.get("content"))
        if raw is None or not raw:
            return ""

        if name.endswith(_PDF_EXTS):
            return await AttachmentParseStage._extract_pdf(raw)
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
    async def _extract_image_text(content: Any) -> Optional[str]:
        """Run OCR on an image and return extracted text, or None if none found."""
        raw = AttachmentParseStage._decode_image_bytes(content)
        if not raw:
            logger.warning("Image attachment could not be decoded from payload.")
            return None
        ocr = _get_ocr()
        if ocr is None:
            logger.warning("OCR engine unavailable; skipping image text extraction.")
            return None

        def _run() -> Optional[str]:
            import cv2
            import numpy as np

            nparr = np.frombuffer(raw, np.uint8)
            # Decode metadata first (no pixel allocation) so a bomb image
            # declaring huge dimensions is rejected before memory is used.
            img = cv2.imdecode(nparr, cv2.IMREAD_REDUCED_COLOR_2)
            half_scale = True
            if img is None:
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                half_scale = False
            if img is None:
                logger.warning("Image OCR: cv2 could not decode attachment.")
                return None
            if img.size > _MAX_IMAGE_PIXELS:
                logger.warning(
                    "Image exceeds %d pixels; rejected.", _MAX_IMAGE_PIXELS
                )
                return None

            def _ocr_once(candidate: Any) -> Optional[str]:
                # Default thresholds (text_score=0.5, box_thresh=0.5) silently
                # drop low-confidence detections — bad for small/anti-aliased
                # screenshot text. Loosen them so more lines survive; the
                # prompt can tolerate a few OCR artifacts more easily than
                # losing all the text.
                result, _ = ocr(
                    candidate,
                    box_thresh=0.25,
                    text_score=0.3,
                    unclip_ratio=1.8,
                )
                lines = [
                    r[1] for r in (result or []) if r and len(r) > 1 and r[1]
                ]
                text = "\n".join(lines).strip()
                return text or None

            def _upscale(img: Any, factor: float = 2.0) -> Any:
                try:
                    return cv2.resize(
                        img, None, fx=factor, fy=factor,
                        interpolation=cv2.INTER_CUBIC,
                    )
                except Exception:
                    return img

            text = _ocr_once(img)

            # Fallback passes for images the first OCR call read nothing from:
            #  - full-resolution decode (half-res reduced pass may blur small text)
            #  - grayscale + contrast enhancement (screenshots/photos with
            #    glare or low contrast frequently fail naive color OCR)
            #  - 2x upscale (large screenshots shrink text below the detector's
            #    min_height, so doubling size makes lines readable)
            attempts = []
            if text:
                logger.info(
                    "Image OCR ok (half=%s, chars=%d)", half_scale, len(text)
                )
                return text

            if half_scale:
                attempts.append("full-res")
                full = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if full is not None and full.size <= _MAX_IMAGE_PIXELS:
                    text = _ocr_once(full)

            if not text:
                attempts.append("grayscale-contrast")
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Clip high/low percentile so dark-on-dark / washed-out text
                # becomes legible for the OCR model.
                try:
                    gray = cv2.convertScaleAbs(gray, alpha=1.6, beta=10)
                except Exception:
                    pass
                text = _ocr_once(gray)

            if not text:
                attempts.append("2x-upscale")
                up = _upscale(img, 2.0)
                if up.size <= _MAX_IMAGE_PIXELS:
                    text = _ocr_once(up)

            if text:
                logger.info(
                    "Image OCR recovered via fallback (%s), chars=%d",
                    ",".join(attempts), len(text),
                )
                return text

            logger.warning(
                "Image OCR found no readable text after passes: %s "
                "(decoded=%sx%s pixels=%d bytes=%d)",
                ",".join(attempts) or "initial",
                img.shape[1], img.shape[0], img.size, len(raw),
            )
            # Save a copy of the failed frame so the cause can be inspected
            # (best-effort; safe path only, never user-influential).
            try:
                import os
                p = "/tmp/ai_failed_image.png"
                cv2.imwrite(p, img)
            except Exception:
                pass
            return None

        # CV2 decode + OCR are blocking CPU/IO; never block the event loop.
        return await asyncio.to_thread(_run)

    @staticmethod
    async def _extract_pdf(raw: bytes) -> Optional[str]:
        def _run() -> Optional[str]:
            try:
                from pypdf import PdfReader
            except Exception:
                return None
            try:
                import io

                reader = PdfReader(io.BytesIO(raw))
                parts: list[str] = []
                total_chars = 0
                for page in reader.pages[:_MAX_PDF_PAGES]:
                    page_text = page.extract_text() or ""
                    total_chars += len(page_text)
                    if total_chars > _MAX_PDF_CHARS:
                        # Truncate mid-extraction so a decompression bomb cannot
                        # keep consuming memory past the cap.
                        parts.append(page_text[:_MAX_PDF_CHARS - (total_chars - len(page_text))])
                        logger.warning("PDF extraction truncated at %d chars.", _MAX_PDF_CHARS)
                        break
                    parts.append(page_text)
                text = "\n".join(parts).strip()
                return text or None
            except Exception as e:
                logger.warning("PDF text extraction failed: %s", e)
                return None

        return await asyncio.to_thread(_run)
