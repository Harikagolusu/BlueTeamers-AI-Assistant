import pytest
from app.persona.off_topic import OffTopicResponseBuilder


def test_supports_off_topic_intent():
    assert OffTopicResponseBuilder.supports("tell me a joke", "OFF_TOPIC")
    assert not OffTopicResponseBuilder.supports("hello", "GREETING")
    assert not OffTopicResponseBuilder.supports("explain siem", "RAG_CHAT")


def test_build_returns_scope_refusal():
    builder = OffTopicResponseBuilder()
    message = builder.build("tell me a joke", "OFF_TOPIC")
    assert "cybersecurity" in message
    assert "outside my scope" in message
