"""Tests for adaptive signal extraction (Sprint 4 features 1, 3, 4)."""
from app.adaptive.signals import extract_signals


def test_eli5_query_sets_beginner_override():
    s = extract_signals("Can you explain like I'm 5 what a SOC is?")
    assert s.beginner_override is True


def test_explicit_beginner_override():
    s = extract_signals("Explain like I'm a beginner, what is Wazuh?")
    assert s.beginner_override is True


def test_expert_override():
    s = extract_signals("Give me the expert explanation of Sigma rule optimization")
    assert s.expert_override is True


def test_expert_vocab_detection():
    s = extract_signals("How does beaconing work for lateral movement detection?")
    assert s.expert_vocab >= 2


def test_practical_and_question():
    s = extract_signals("Can you walk me through writing a Sigma rule example?")
    assert s.practical >= 1
    assert s.question >= 1


def test_struggle_signal():
    s = extract_signals("I don't understand, this is confusing, can you rephrase?")
    assert s.struggle >= 1


def test_reinforce_from_recent_context():
    s = extract_signals("What next?", ["That makes sense, thanks!"])
    assert s.reinforce >= 1


def test_reinforce_not_from_same_turn():
    s = extract_signals("That makes sense, thanks!")
    assert s.reinforce >= 1
