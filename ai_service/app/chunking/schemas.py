from pydantic import BaseModel, Field
from typing import List, Optional

class ChunkingConfig(BaseModel):
    """Configuration model for the Chunking Service."""
    chunk_size: int = Field(..., description="Maximum character length of a single chunk.")
    chunk_overlap: int = Field(..., description="Number of overlapping characters between chunks.")
    max_document_size_mb: int = Field(..., description="Maximum allowed size of a document in MB.")

class ChunkMetadata(BaseModel):
    """Metadata attached to each individual chunk for vector storage."""
    chunk_id: str
    chunk_index: int
    course_slug: str
    lesson_id: str
    lesson_title: str
    source: str
    created_at: str

class Chunk(BaseModel):
    """Represents a single piece of text and its strongly typed metadata."""
    text: str
    metadata: ChunkMetadata

class ChunkRequest(BaseModel):
    """Payload required to process a raw lesson."""
    content: str
    course_slug: str
    lesson_id: str
    lesson_title: str
    source: Optional[str] = "lesson_content"
    
class ChunkResponse(BaseModel):
    """The result of the chunking process."""
    lesson_id: str
    total_chunks: int
    chunks: List[Chunk]
