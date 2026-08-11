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
        seen = set()
        unique = []
        for c in chunks:
            if c.chunk_id not in seen:
                seen.add(c.chunk_id)
                unique.append(c)
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
        """
        sections = []
        for i, c in enumerate(chunks, 1):
            source = c.metadata.get("lesson_title", c.metadata.get("source", f"Document {i}"))
            sections.append(f"--- SOURCE: {source} ---\n{c.text}")
            
        return "\n\n".join(sections)
