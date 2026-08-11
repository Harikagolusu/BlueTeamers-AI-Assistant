from app.chat.sanitize import clean_response


def test_clean_response_keeps_normal_markdown_untouched():
    md = (
        "### Overview\n"
        "Event ID 4624 means a successful logon.\n\n"
        "| Event ID | Meaning |\n"
        "|----------|---------|\n"
        "| 4624 | Successful Logon |\n\n"
        "- first\n- second\n\n"
        "```python\nprint('hi')\n```\n\n"
        "> blockquote\n"
    )
    assert clean_response(md) == md.strip()


def test_clean_response_strips_document_tag_lines():
    text = "[Document 1] (source: SOC Fundamentals / Intro)\nSome real answer.\n"
    cleaned = clean_response(text)
    assert "[Document 1]" not in cleaned
    assert "Some real answer." in cleaned


def test_clean_response_strips_inline_document_tags():
    text = "Answer here.\n\n[Document 2] Additional context is fine.\n"
    cleaned = clean_response(text)
    assert "[Document 2]" not in cleaned
    assert "Additional context is fine." in cleaned


def test_clean_response_strips_source_lines():
    text = "Useful content.\n--- SOURCE: log_analysis.md\nMore content.\n"
    cleaned = clean_response(text)
    assert "SOURCE" not in cleaned
    assert "Useful content." in cleaned
    assert "More content." in cleaned


def test_clean_response_strips_sources_footer():
    text = "The answer.\n\nSources:\n- doc1.md\n- doc2.md\n"
    cleaned = clean_response(text)
    assert "Sources:" not in cleaned
    assert "The answer." in cleaned


def test_clean_response_strips_debug_metadata():
    text = "Answer text.\nAgent: rag_engine LATENCY: 1234MS\n"
    cleaned = clean_response(text)
    assert "AGENT" not in cleaned.upper()
    assert "LATENCY" not in cleaned.upper()
    assert "Answer text." in cleaned


def test_clean_response_handles_empty():
    assert clean_response("") == ""
    assert clean_response(None) is None
