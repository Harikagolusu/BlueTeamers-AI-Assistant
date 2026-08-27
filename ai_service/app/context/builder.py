import hashlib
import re
import time
import logging
from typing import List

from app.core.config import settings
from app.core.logging import request_id_var

from app.retrieval.schemas import RetrievedChunk
from app.context.schemas import (
    ContextRequest, ContextChunk, ContextDocument, ContextResponse
)
from app.context.tokenizer import TokenEstimator

logger = logging.getLogger("app.context.builder")

class ContextProcessingLogic:
    """
    Encapsulates the pure data transformations: deduplication, merging, ranking, trimming.
    """
    @staticmethod
    def deduplicate(chunks: List[RetrievedChunk]) -> List[RetrievedChunk]:
        """Content-based deduplication for exact duplicate content only.

        - Uses existing metadata["content_hash"] when available (SHA1 of original
          text stored at ingestion, reliable per app/knowledge/pipeline.py:77).
        - Fallback: SHA1 of whitespace-normalized content (collapse spaces/newlines
          via regex, preserve case/punctuation).
        - For each exact duplicate group, keep the highest-scoring occurrence.
        - Preserve original relevance-ranked order (retrieval order, already sorted
          by score descending from VectorStore/RetrievalService).
        - Do NOT remove partially overlapping, adjacent, or similar chunks.
        """
        if not chunks:
            return []

        def _content_hash(c: RetrievedChunk) -> str:
            # Preferred: existing content_hash from ingestion (exact, reliable)
            meta_hash = (c.metadata or {}).get("content_hash")
            if isinstance(meta_hash, str) and meta_hash:
                return f"hash:{meta_hash}"
            # Fallback: SHA1 of whitespace-normalized text (no lowercasing)
            normalized = re.sub(r"\s+", " ", (c.text or "").strip())
            return hashlib.sha1(normalized.encode("utf-8")).hexdigest()

        # Group by hash, track highest score per hash and its representative
        best_by_hash: dict[str, RetrievedChunk] = {}
        for c in chunks:
            h = _content_hash(c)
            existing = best_by_hash.get(h)
            if existing is None or c.score > existing.score:
                best_by_hash[h] = c

        # Preserve original relevance-ranked order: iterate in input order,
        # keep only the chosen representative for each hash (first occurrence
        # of the best). This retains order without global resort.
        seen_hash = set()
        unique: List[RetrievedChunk] = []
        for c in chunks:
            h = _content_hash(c)
            best = best_by_hash[h]
            # Only keep the exact chosen instance (identity by chunk_id+score)
            # and only once per hash.
            if h not in seen_hash and c.chunk_id == best.chunk_id and c.score == best.score:
                # This is the highest-scoring occurrence; keep it
                seen_hash.add(h)
                unique.append(c)
            elif h not in seen_hash and best_by_hash[h].chunk_id == c.chunk_id:
                # Fallback when scores tie and we kept the first encountered best
                seen_hash.add(h)
                unique.append(best)
            elif h in seen_hash:
                # Duplicate already kept, skip
                continue
            else:
                # Not the best for this hash, skip (duplicate)
                # But ensure we eventually keep the best even if it appears later:
                # If current chunk is not the best, we skip it now; the best will
                # be kept when we encounter it in order.
                continue

        # Edge: if best was later in order, the earlier duplicate was skipped
        # and best not yet added; ensure all bests are present in original order
        # of their first appearance as best. Reconcile by second pass if needed.
        if len(unique) != len(best_by_hash):
            # Rebuild in original order of bests
            unique = []
            seen_hash.clear()
            for c in chunks:
                h = _content_hash(c)
                if h not in seen_hash and c.chunk_id == best_by_hash[h].chunk_id:
                    seen_hash.add(h)
                    unique.append(best_by_hash[h])

        return unique

    @staticmethod
    def merge_adjacent(chunks: List[RetrievedChunk]) -> List[ContextChunk]:
        """
        Merges chunks from the same lesson that are sequentially adjacent.
        Requires metadata to contain 'lesson_id' and 'chunk_index'.
        """
        if not chunks:
            return []

        # Sort by lesson_id, then chunk_index to find adjacencies easily
        # Ensure we only process chunks that have the necessary metadata
        valid_chunks = [c for c in chunks if "lesson_id" in c.metadata and "chunk_index" in c.metadata]
        invalid_chunks = [c for c in chunks if "lesson_id" not in c.metadata or "chunk_index" not in c.metadata]

        valid_chunks.sort(key=lambda x: (x.metadata["lesson_id"], x.metadata["chunk_index"]))

        merged = []
        current = None

        for c in valid_chunks:
            if current is None:
                current = ContextChunk(
                    id=c.chunk_id,
                    text=c.text,
                    score=c.score,
                    metadata=c.metadata.copy()
                )
            else:
                c_lesson = c.metadata["lesson_id"]
                c_index = c.metadata["chunk_index"]
                curr_lesson = current.metadata["lesson_id"]
                curr_index = current.metadata["chunk_index"]

                if c_lesson == curr_lesson and c_index == curr_index + 1:
                    # Merge text
                    current.text += "\n\n" + c.text
                    # Keep the higher score
                    current.score = max(current.score, c.score)
                    # Update metadata index to the latest to chain multiple merges
                    current.metadata["chunk_index"] = c_index
                else:
                    merged.append(current)
                    current = ContextChunk(
                        id=c.chunk_id,
                        text=c.text,
                        score=c.score,
                        metadata=c.metadata.copy()
                    )

        if current is not None:
            merged.append(current)

        # Convert invalid chunks directly
        for c in invalid_chunks:
            merged.append(ContextChunk(id=c.chunk_id, text=c.text, score=c.score, metadata=c.metadata))

        return merged

    @staticmethod
    def trim_to_budget(chunks: List[ContextChunk], max_tokens: int) -> tuple[List[ContextChunk], int, int]:
        """
        Trims the lowest scoring chunks to fit within the max_tokens budget.
        Returns: (trimmed_chunks, final_token_count, num_trimmed)
        """
        # Rank by score descending
        chunks.sort(key=lambda x: x.score, reverse=True)

        final_chunks = []
        current_tokens = 0
        num_trimmed = 0

        for c in chunks:
            tokens = TokenEstimator.estimate_tokens(c.text)
            if current_tokens + tokens <= max_tokens:
                final_chunks.append(c)
                current_tokens += tokens
            else:
                num_trimmed += 1

        return final_chunks, current_tokens, num_trimmed

    @staticmethod
    def build_structured_context(chunks: List[ContextChunk]) -> str:
        """
        Builds the raw string context formatted with citations.

        NOTE: Source title is NOT repeated here; SimplePromptBuilder already
        adds "[Document i] (source: Course / Lesson)" header for each doc.
        Keeping it here would duplicate the same lesson_title twice in the
        final LLM prompt (STEP 4 Option C).
        """
        sections = []
        for c in chunks:
            sections.append(f"{c.text}")
            
        return "\n\n".join(sections)
