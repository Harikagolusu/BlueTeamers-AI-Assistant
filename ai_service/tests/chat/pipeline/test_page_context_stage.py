"""Tests for the page-context awareness stage (Sprint 5, Feature 5)."""
import uuid

import pytest

from app.chat.context.execution_context import ExecutionContext
from app.chat.pipeline.page_context_stage import (
    PageContextStage,
    build_page_context_block,
)


def _context(page=None, context_meta=None):
    return ExecutionContext(
        correlation_id=uuid.uuid4(),
        session_user="u1",
        tenant_id=None,
        streaming_mode=False,
        metadata={
            "query": "Explain this lesson",
            "context": {"page": page} if page is not None else (context_meta or {}),
        },
    )


@pytest.mark.asyncio
async def test_lesson_page_context_injected():
    stage = PageContextStage()
    ctx = _context(page={
        "type": "lesson",
        "course_title": "SOC Fundamentals",
        "lesson_title": "Phishing Analysis",
    })
    out = await stage.execute(ctx)
    assert "page_context" in out.memory
    assert "Phishing Analysis" in out.memory["page_context"]
    assert "SOC Fundamentals" in out.memory["page_context"]


@pytest.mark.asyncio
async def test_wazuh_lab_context_injected():
    stage = PageContextStage()
    ctx = _context(page={
        "type": "wazuh",
        "lab_title": "Wazuh Alert Triage",
        "alert_id": "rule-800",
    })
    out = await stage.execute(ctx)
    assert "Wazuh Alert Triage" in out.memory["page_context"]
    assert "rule-800" in out.memory["page_context"]


@pytest.mark.asyncio
async def test_no_page_context_is_noop():
    stage = PageContextStage()
    ctx = _context()
    out = await stage.execute(ctx)
    assert "page_context" not in out.memory


@pytest.mark.asyncio
async def test_non_page_context_is_noop():
    stage = PageContextStage()
    ctx = _context(context_meta={"lab": {"action": "start"}})
    out = await stage.execute(ctx)
    assert "page_context" not in out.memory


@pytest.mark.asyncio
async def test_preserves_existing_memory():
    stage = PageContextStage()
    ctx = _context(page={"type": "dashboard"})
    ctx = ctx.with_memory({"recent_context": "previous turns"})
    out = await stage.execute(ctx)
    assert out.memory["recent_context"] == "previous turns"
    assert "page_context" in out.memory


def test_build_block_empty_for_unknown():
    assert build_page_context_block({}) == ""
    assert build_page_context_block({"type": ""}) == ""
