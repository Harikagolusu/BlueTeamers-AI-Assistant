"""Tests for the language prompt blocks (Sprint 7 — Features 2, 3, 4)."""
import pytest

from app.multilingual.languages import catalog_options, is_concrete_code
from app.multilingual.prompts import build_language_block
from app.multilingual.terminology import PRESERVED_TERMS, preserved_terms_text


class TestLanguageBlock:
    def test_english_returns_no_block(self):
        assert build_language_block("en") == ""

    def test_unknown_code_returns_no_block(self):
        assert build_language_block("xx") == ""
        assert build_language_block("") == ""

    def test_pure_mode_mentions_language_and_script(self):
        block = build_language_block("te")
        assert "Telugu" in block
        assert "[Response Language]" in block

    def test_mixed_mode_mentions_mix_name(self):
        block = build_language_block("te+en")
        assert "Tinglish" in block
        assert "Telugu" in block

    def test_mixed_mode_enforces_natural_conversational_skeleton(self):
        block = build_language_block("te+en")
        # The reply must follow Telugu grammar/word order, not English with
        # sprinkles of Telugu.
        assert "natural conversational Tinglish" in block
        assert "grammar and word order" in block
        assert "NOT like an English answer" in block
        # It must show the Telugu function words and keep tech terms in English.
        assert "ante" in block
        assert "cheyali" in block
        assert "SIEM" in block

    def test_all_language_mixed_modes_build_blocks(self):
        for code in ["hi+en", "ta+en", "kn+en", "ml+en", "bn+en", "mr+en", "gu+en", "pa+en", "or+en", "ur+en"]:
            block = build_language_block(code)
            assert "[Response Language]" in block
            assert "grammar and word order" in block
            assert "casually types in English letters" in block

    def test_mixed_modes_are_concrete(self):
        assert is_concrete_code("te+en")
        assert is_concrete_code("hi+en")
        assert is_concrete_code("ta+en")

    def test_manual_source_is_unambiguous(self):
        block = build_language_block("ta", source="manual")
        assert "Reply" in block
        assert "ONLY" in block
        # Manual selection must not tell the model to follow the typed language.
        assert "Always match " not in block

    def test_detected_source_keeps_match_instruction(self):
        block = build_language_block("ta", source="detected")
        assert "match the language" in block

    def test_terms_preserved_in_english(self):
        block = build_language_block("te")
        assert "SIEM" in block
        assert "MITRE" in block
        assert "cybersecurity" in block.lower() or "SIEM" in block

    def test_never_translate_artefacts(self):
        block = build_language_block("te")
        assert "never translate" in block.lower() or "Never translate" in block


class TestTerminology:
    def test_terms_list_nonempty(self):
        assert len(PRESERVED_TERMS) > 20

    def test_joined_text_includes_core_terms(self):
        text = preserved_terms_text()
        assert "SIEM" in text
        assert "SOC" in text
        assert "MITRE ATT&CK" in text

    def test_catalog_options_include_auto_and_concrete(self):
        codes = [code for code, _ in catalog_options()]
        assert "auto" in codes
        assert "en" in codes
        assert "te" in codes
        assert "te+en" in codes

    def test_concrete_code_predicate(self):
        assert is_concrete_code("te")
        assert is_concrete_code("te+en")
        assert not is_concrete_code("auto")
        assert not is_concrete_code("xx")