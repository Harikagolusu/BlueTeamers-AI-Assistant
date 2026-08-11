"""Tests for the rule-based language detector (Sprint 7 — Feature 1)."""
import pytest

from app.multilingual.detector import LanguageDetector


@pytest.fixture()
def detector() -> LanguageDetector:
    return LanguageDetector()


class TestScriptDetection:
    def test_telugu_script(self, detector):
        assert detector.detect("SIEM అంటే ఏంటి")[0] == "te"

    def test_telugu_full_sentence(self, detector):
        assert detector.detect("తెలుగులో SIEM గురించి చెప్పండి")[0] == "te"

    def test_hindi_script(self, detector):
        assert detector.detect("SIEM क्या है?")[0] == "hi"

    def test_tamil_script(self, detector):
        assert detector.detect("SIEM பற்றி சொல்லுங்க")[0] == "ta"

    def test_kannada_script(self, detector):
        assert detector.detect("SIEM ಬಗ್ಗೆ ಹೇಳಿ")[0] == "kn"

    def test_malayalam_script(self, detector):
        assert detector.detect("SIEM കുറിച്ച് പറയൂ")[0] == "ml"

    def test_bengali_script(self, detector):
        assert detector.detect("SIEM কী?")[0] == "bn"

    def test_gujarati_script(self, detector):
        assert detector.detect("SIEM શું છે?")[0] == "gu"

    def test_punjabi_script(self, detector):
        assert detector.detect("SIEM ਕੀ ਹੈ?")[0] == "pa"

    def test_marathi_script_vs_hindi(self, detector):
        # Marathi function words disambiguate from Hindi.
        assert detector.detect("SIEM म्हणजे काय आहे?")[0] == "mr"

    def test_hindi_default_devanagari(self, detector):
        assert detector.detect("SIEM क्या होता है")[0] == "hi"

    def test_urdu_script(self, detector):
        assert detector.detect("SIEM کیا ہے؟")[0] == "ur"


class TestRomanizedDetection:
    def test_teluglish(self, detector):
        code, conf = detector.detect("SIEM ante enti")
        assert code == "te+en"
        assert conf == pytest.approx(0.65)

    def test_removed_mixed_modes_fall_back_to_english(self, detector):
        # hi+en / ta+en / kn+en / ml+en lexicons were removed from the catalog.
        assert detector.detect("SIEM kya hai bhai")[0] == "en"
        assert detector.detect("Wazuh log pannunga")[0] == "en"
        assert detector.detect("Python yenu bekagide")[0] == "en"
        assert detector.detect("enthu vechitaangal")[0] == "en"


class TestEnglishFallback:
    def test_plain_english(self, detector):
        code, conf = detector.detect("Explain firewall for me")
        assert code == "en"
        assert conf >= 0.8

    def test_empty_text(self, detector):
        code, conf = detector.detect("")
        assert code == "en"

    def test_whitespace_text(self, detector):
        assert detector.detect("   ")[0] == "en"

    def test_technical_english_stays_english(self, detector):
        # "ante"/"enti" alone should not trigger Teluglish on English text.
        assert detector.detect("What does a firewall do?")[0] == "en"
