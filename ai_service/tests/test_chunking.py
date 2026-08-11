import pytest
from app.chunking.schemas import ChunkRequest, ChunkingConfig
from app.chunking.chunker import MarkdownRecursiveChunker
from app.chunking.exceptions import EmptyContentException, OversizedContentException

@pytest.fixture
def chunking_config():
    return ChunkingConfig(
        chunk_size=600,
        chunk_overlap=120,
        max_document_size_mb=1
    )

@pytest.fixture
def chunker(chunking_config):
    return MarkdownRecursiveChunker(config=chunking_config)

@pytest.fixture
def base_request():
    return ChunkRequest(
        content="Test content",
        course_slug="network-security",
        lesson_id="lesson-12",
        lesson_title="Introduction to Firewalls"
    )

def test_empty_lesson(chunker, base_request):
    base_request.content = "   \n  "
    with pytest.raises(EmptyContentException):
        chunker.chunk(base_request)

def test_oversized_lesson(chunker, base_request):
    # Mock size limit to 0 MB (0 bytes) to force error
    chunker.config.max_document_size_mb = 0
    base_request.content = "This content is too large."
    with pytest.raises(OversizedContentException):
        chunker.chunk(base_request)

def test_metadata_generation(chunker, base_request):
    response = chunker.chunk(base_request)
    assert response.total_chunks == 1
    
    metadata = response.chunks[0].metadata
    assert metadata.chunk_id == "network-security:lesson-12:chunk-0"
    assert metadata.chunk_index == 0
    assert metadata.course_slug == "network-security"
    assert metadata.lesson_id == "lesson-12"
    assert metadata.lesson_title == "Introduction to Firewalls"

def test_markdown_code_blocks(chunking_config, base_request):
    # Small chunk size to force splitting, but we hope code block stays intact
    chunking_config.chunk_size = 50
    chunking_config.chunk_overlap = 0
    chunker = MarkdownRecursiveChunker(config=chunking_config)
    
    code = "```python\ndef hello():\n    print('world')\n```"
    base_request.content = f"Some text here.\n\n{code}\n\nMore text here."
    
    response = chunker.chunk(base_request)
    assert response.total_chunks > 1
    
    # Langchain MarkdownTextSplitter keeps code blocks together 
    # even if they exceed chunk_size if possible, or splits strictly if it must.
    # We verify the code block text exists in the chunks.
    found_code = any("```python" in chunk.text for chunk in response.chunks)
    assert found_code is True

def test_chunk_overlap_correctness(base_request):
    config = ChunkingConfig(chunk_size=100, chunk_overlap=20, max_document_size_mb=1)
    chunker = MarkdownRecursiveChunker(config=config)
    
    # Text without spaces to force arbitrary character split and overlap
    text = "A" * 90 + "B" * 70
    base_request.content = text
    response = chunker.chunk(base_request)
    
    assert response.total_chunks == 2
    # Chunk 1 (length 100): 90 'A's + 10 'B's
    # Chunk 2 (starts at 80): 10 'A's + 70 'B's
    assert "B" in response.chunks[0].text
    assert "A" in response.chunks[1].text
