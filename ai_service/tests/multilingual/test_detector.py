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
        # Strong lexical match (score 6) -> high confidence so it overrides a
        # stored preference in the stage.
        assert conf >= 0.9

    def test_natural_conversational_teluglish(self, detector):
        # Real-world Tinglish queries must auto-detect as te+en.
        for text in [
            "siem ante enti?",
            "wazuh ela work avtundi?",
            "phishing ni ela identify cheyali?",
            "hacker ante evaru",
            "SIEM ante security operations center na?",
        ]:
            assert detector.detect(text)[0] == "te+en", text

    def test_low_score_teluglish_still_overrides_stored_preference(self, detector):
        # Queries with only a 3-point lexical match (score 3) are still clearly
        # Tinglish and must reach SWITCH_THRESHOLD (0.9) so a stored preference
        # never forces the wrong language (e.g. pure Telugu for a romanized
        # query like "soc course about emiti").
        for text in [
            "soc oka example kavali",
            "soc course about emiti",
            "soc ante",
        ]:
            code, conf = detector.detect(text)
            assert code == "te+en", text
            assert conf >= 0.9, (text, conf)

    def test_missing_conversational_words_detected(self, detector):
        # Regression: these romanized words were absent from the lexicon, so
        # natural Tinglish questions fell back to English.
        for text in [
            "log analysis ela chestaru",
            "siem ante emiti",
            "windows logs ela chudandi",
        ]:
            assert detector.detect(text)[0] == "te+en", text

    def test_removed_mixed_modes_fall_back_to_english(self, detector):
        # hi+en / ta+en / kn+en / ml+en lexicons were removed from the catalog.
        assert detector.detect("SIEM kya hai bhai")[0] == "en"
        assert detector.detect("Wazuh log pannunga")[0] == "en"
        assert detector.detect("Python yenu bekagide")[0] == "en"
        assert detector.detect("enthu vechitaangal")[0] == "en"


class TestLanguageRequestDetection:
    """Explicit "answer in <language>" requests (romanized + English)."""

    @pytest.mark.parametrize(
        "text,expected",
        [
            # Romanized per-language request phrases -> romanized mixed mode.
            ("telugu lo cheppava", "te+en"),
            ("telugu lo cheppandi", "te+en"),
            ("hindi me batao", "hi+en"),
            ("hindi me bataiye", "hi+en"),
            ("tamil la solunga", "ta+en"),
            ("kannada dalli heli", "kn+en"),
            ("marathi madhe sanga", "mr+en"),
            ("bengali te bolo", "bn+en"),
            ("gujarati ma keh", "gu+en"),
            ("punjabi vich dasso", "pa+en"),
            ("malayalam il parayu", "ml+en"),
            ("urdu me batao", "ur+en"),
            # English-language request phrases -> romanized mixed mode.
            ("Explain in Telugu", "te+en"),
            ("please answer in Hindi", "hi+en"),
            ("in Tamil please", "ta+en"),
            ("reply in kannada", "kn+en"),
            ("tell me in malayalam", "ml+en"),
            ("answer in English", "en"),
        ],
    )
    def test_explicit_language_request(self, detector, text, expected):
        code, conf = detector.detect(text)
        assert code == expected
        assert conf >= 0.9  # above SWITCH_THRESHOLD so it overrides stored pref

    @pytest.mark.parametrize(
        "text",
        [
            "What does a firewall do?",
            "SIEM kya hai bhai",
            "I speak Telugu at home",
            "learning Hindi is fun",
            "Firewall rules for tamil",
        ],
    )
    def test_plain_english_with_language_words_stays_english(self, detector, text):
        code, _ = detector.detect(text)
        assert code == "en"



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
