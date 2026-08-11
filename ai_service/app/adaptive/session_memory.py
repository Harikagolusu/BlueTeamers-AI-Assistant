"""SessionMemoryManager: conversation-scoped memory for follow-ups and continuity.

Implements Sprint 4 session memory:
  - rolling context (recent turns, capped),
  - a compacted running summary,
  - important extracted facts (questions/topics),
  - investigation continuity (Wazuh/Practice labs and SOC investigations),
  - uploaded-file memory (PDFs, images, screenshots, logs, IOC files).

State is scoped per (user_id, conversation_id) so conversations never bleed
into each other (context isolation).
"""
import datetime
from typing import Dict, List, Optional, Sequence

from app.adaptive.models import SessionMemoryState
from app.adaptive.store import SQLiteLearnerStore
from app.adaptive.topics import topic_by_key

INVESTIGATION_ENGINES = {
    "INVESTIGATION",
    "INVESTIGATION_GUIDANCE",
    "WINDOWS_EVENT_LOG",
    "LINUX_LOG",
    "IOC_ANALYSIS",
    "WAZUH_LAB",
    "PRACTICE_LAB",
}

LAB_ENGINES = {"WAZUH_LAB", "PRACTICE_LAB"}

MAX_ROLLING_MESSAGES = 6
MAX_SUMMARY_LENGTH = 1200
MAX_FACTS = 8
MAX_FILES = 10


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def _clip(text: str, max_len: int) -> str:
    text = " ".join((text or "").split())
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


class SessionMemoryManager:
    def __init__(self, store: SQLiteLearnerStore):
        self.store = store

    async def load(self, user_id: str, conversation_id: Optional[str]) -> SessionMemoryState:
        return await self.store.load_session(user_id, conversation_id)

    async def record_turn(
        self,
        user_id: str,
        conversation_id: Optional[str],
        query: str,
        ai_message: str,
        topic_keys: Sequence[str] = (),
        engine: Optional[str] = None,
        files: Optional[List[dict]] = None,
        images: Optional[List[str]] = None,
    ) -> SessionMemoryState:
        state = await self.store.load_session(user_id, conversation_id)
        now = _now()
        state.updated_at = now

        # Rolling context: cap the recent window so token usage stays bounded.
        if query:
            state.rolling_messages.append({"role": "user", "content": _clip(query, 300), "timestamp": now.isoformat()})
        if ai_message:
            state.rolling_messages.append({"role": "assistant", "content": _clip(ai_message, 300), "timestamp": now.isoformat()})
        state.rolling_messages = state.rolling_messages[-MAX_ROLLING_MESSAGES:]

        # Running summary: compact one line per turn, trim oldest when too big.
        primary = topic_keys[0] if topic_keys else None
        topic_name = topic_by_key(primary).name if primary else "general"
        summary_line = (
            f"- Q: {_clip(query, 90)} | A: {_clip(ai_message, 90)}"
            if query and ai_message
            else f"- User: {_clip(query or ai_message, 180)}"
        )
        summary = (state.summary + "\n" + summary_line).strip()
        while len(summary) > MAX_SUMMARY_LENGTH and "\n" in summary:
            summary = summary.split("\n", 1)[1]
        state.summary = summary[:MAX_SUMMARY_LENGTH]

        # Facts: dedupe and cap.
        fact = _clip(query, 120) if query else ""
        if primary and fact:
            fact = f"[{topic_name}] {fact}"
        if fact and fact not in state.facts:
            state.facts.append(fact)
        state.facts = state.facts[-MAX_FACTS:]

        # Investigation continuity (Feature 7).
        if engine in INVESTIGATION_ENGINES and topic_name:
            state.investigation = {
                "active": True,
                "engine": engine,
                "topic": topic_name,
                "is_lab": engine in LAB_ENGINES,
                "updated_at": now.isoformat(),
            }
        elif not state.investigation:
            state.investigation = {"active": False}

        # Uploaded-file memory (Feature 8).
        merged = list(state.uploaded_files)
        seen = {f.get("name") or f.get("filename") for f in merged}
        for item in list(files or []):
            name = item.get("name") or item.get("filename")
            if not name:
                continue
            if name in seen:
                continue
            merged.append({"name": name, "kind": item.get("kind") or item.get("type") or "file"})
            seen.add(name)
        for image in list(images or []):
            name = image.split("/")[-1] or image[:40]
            if name in seen:
                continue
            merged.append({"name": name, "kind": "image"})
            seen.add(name)
        state.uploaded_files = merged[-MAX_FILES:]

        await self.store.save_session(state)
        return state
