import json
from pathlib import Path

import numpy as np
import pytest
from streamlit.testing.v1 import AppTest

from src.pipeline import ROOT, Lexicon, SpeechRecognizer, normalize


def test_normalization_and_phrase_retrieval():
    lexicon = Lexicon()
    assert normalize("  HELLO,  world! ") == "hello world"
    assert normalize("தண்ணீர்") == "தண்ணீர்"
    assert [x["gloss"] for x in lexicon.translate("THANK YOU!")] == ["THANK-YOU"]
    assert lexicon.translate("unknown")[0]["status"] == "unmapped"
    assert lexicon.translate("") == []
    with pytest.raises(ValueError):
        lexicon.translate("hello", "xx")


def test_authored_regression_cases():
    lexicon = Lexicon()
    cases = json.loads((ROOT / "tests/fixtures/retrieval_cases.json").read_text())
    for case in cases:
        assert [
            x["gloss"] for x in lexicon.translate(case["text"], case["language"])
        ] == case["expected_glosses"]
    assert lexicon.inventory()["concepts"] == 36
    assert lexicon.inventory()["distinct_usable_assets"] == 0


def test_asset_provenance_and_deduplication(tmp_path):
    entry = {
        "id": "hello",
        "gloss": "HELLO",
        "aliases": {"en": ["hello"]},
        "asset": "data/assets/hello.mp4",
        "license": "test-only",
        "source_url": "https://example.org/test-fixture",
        "sign_language": "TEST",
    }
    (tmp_path / "data/assets").mkdir(parents=True)
    path = tmp_path / "lexicon.json"
    path.write_text(json.dumps([entry]))
    lexicon = Lexicon(path, root=tmp_path)
    assert lexicon.usable_asset(entry)[0] is None
    # File validator only; this fake byte fixture is never presented as a playable gesture.
    (tmp_path / entry["asset"]).write_bytes(b"test-only-file-presence-fixture")
    assert lexicon.usable_asset(entry)[0] is not None
    assert lexicon.translate("hello")[0]["status"] == "media"
    assert lexicon.usable_asset({**entry, "asset": "../escape.mp4"})[0] is None
    assert lexicon.usable_asset({**entry, "license": None})[0] is None
    assert lexicon.usable_asset({**entry, "asset": None})[0] is None
    duplicate = {**entry, "id": "second", "aliases": {"en": ["second"]}}
    path.write_text(json.dumps([entry, duplicate]))
    assert Lexicon(path, root=tmp_path).inventory()["distinct_usable_assets"] == 1
    path.write_text(json.dumps([entry, entry]))
    with pytest.raises(ValueError):
        Lexicon(path, root=tmp_path)
    for aliases in [{"en": [""]}, {"xx": ["hello"]}]:
        path.write_text(json.dumps([{**entry, "aliases": aliases}]))
        with pytest.raises(ValueError):
            Lexicon(path, root=tmp_path)


def test_chunk_timestamps_and_validation():
    class FakeRecognizer(SpeechRecognizer):
        def __init__(self):
            pass

        def transcribe(self, audio, language="en"):
            return {
                "text": "hello",
                "segments": [{"start": 0.0, "end": 0.2, "text": "hello"}],
            }

    recognizer = FakeRecognizer()
    results = list(recognizer.stream_chunks([np.zeros(16000), np.zeros(8000)]))
    assert results[1]["audio_offset_seconds"] == 1
    assert results[1]["segments"][0]["start"] == 1
    for chunk in [[], [[0]], [np.nan]]:
        with pytest.raises(ValueError):
            list(recognizer.stream_chunks([chunk]))
    with pytest.raises(ValueError):
        list(recognizer.stream_chunks([np.zeros(10)], sample_rate=8000))


def test_interface_renders_and_switches_language():
    app = AppTest.from_file(str(ROOT / "src/app.py")).run(timeout=20)
    assert not app.exception
    assert app.title[0].value == "Make a message easier to follow."
    app.selectbox[0].select("de").run(timeout=20)
    assert not app.exception
    assert "Hallo" in app.text_area[0].value
