from datetime import datetime, timezone
from app.chunking.schemas import ChunkMetadata, ChunkRequest

class MetadataGenerator:
    """Utility to generate consistent and deterministic metadata for chunks."""
    
    @staticmethod
    def generate(request: ChunkRequest, chunk_index: int) -> ChunkMetadata:
        """
        Generates deterministic metadata for a chunk.
        
        Args:
            request: The original chunking request containing context.
            chunk_index: The sequential index of the chunk.
            
        Returns:
            ChunkMetadata: A strongly-typed Pydantic model with deterministic IDs.
        """
        # Deterministic chunk ID
        chunk_id = f"{request.course_slug}:{request.lesson_id}:chunk-{chunk_index}"
        
        return ChunkMetadata(
            chunk_id=chunk_id,
            chunk_index=chunk_index,
            course_slug=request.course_slug,
            lesson_id=request.lesson_id,
            lesson_title=request.lesson_title,
            source=request.source or "lesson_content",
            created_at=datetime.now(timezone.utc).isoformat()
        )
