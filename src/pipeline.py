"""Speech transcription and multilingual gloss retrieval with explicit asset provenance."""

import hashlib
import json
import subprocess
import time
import unicodedata
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = {"en": "English", "ta": "Tamil", "de": "German"}


def normalize(text):
    text = unicodedata.normalize("NFKC", text).casefold().replace("’", "'")
    return " ".join(
        "".join(
            c
            if unicodedata.category(c)[0] in "LMN" or c.isspace() or c in "-'"
            else " "
            for c in text
        ).split()
    )


class Lexicon:
    def __init__(self, path=None, root=ROOT):
        self.root = Path(root).resolve()
        self.entries = json.loads(
            Path(path or self.root / "data/lexicon.json").read_text()
        )
        self.index = {language: {} for language in LANGUAGES}
        seen = set()
        for entry in self.entries:
            if entry["id"] in seen:
                raise ValueError("Duplicate concept ID")
            seen.add(entry["id"])
            for language, aliases in entry["aliases"].items():
                if language not in LANGUAGES:
                    raise ValueError("Unsupported language in lexicon")
                for alias in aliases:
                    key = tuple(normalize(alias).split())
                    if not key or (
                        key in self.index[language]
                        and self.index[language][key]["id"] != entry["id"]
                    ):
                        raise ValueError("Empty or ambiguous alias")
                    self.index[language][key] = entry

    def usable_asset(self, entry):
        if not entry.get("asset"):
            return None, "No licensed sign asset registered"
        path = (self.root / entry["asset"]).resolve()
        if not path.is_relative_to(self.root / "data/assets"):
            return None, "Asset path must stay under data/assets"
        if not all(
            entry.get(key) for key in ["license", "source_url", "sign_language"]
        ):
            return None, "Missing license, source or sign-language metadata"
        if (
            path.suffix.lower()
            not in {".mp4", ".webm", ".gif", ".png", ".jpg", ".jpeg"}
            or not path.is_file()
            or path.stat().st_size == 0
        ):
            return None, "Missing, empty or unsupported media file"
        return path, "Registered media; linguistic correctness requires expert review"

    def inventory(self):
        usable = [self.usable_asset(entry)[0] for entry in self.entries]
        return {
            "concepts": len(self.entries),
            "aliases": {language: len(index) for language, index in self.index.items()},
            "mapping_entries_with_assets": sum(path is not None for path in usable),
            "distinct_usable_assets": len(
                {
                    hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in usable
                    if path
                }
            ),
            "scope": "File and metadata checks, not expert linguistic validation.",
        }

    def translate(self, text, language="en", normalization=True):
        if language not in LANGUAGES:
            raise ValueError("Unsupported input language")
        tokens = (normalize(text) if normalization else text).split()
        index = self.index[language]
        maximum = max((len(key) for key in index), default=1)
        result, position = [], 0
        while position < len(tokens):
            match, size = None, 1
            for length in range(min(maximum, len(tokens) - position), 0, -1):
                match = index.get(tuple(tokens[position : position + length]))
                if match:
                    size = length
                    break
            phrase = " ".join(tokens[position : position + size])
            if match:
                path, reason = self.usable_asset(match)
                result.append(
                    {
                        "source": phrase,
                        "gloss": match["gloss"],
                        "concept_id": match["id"],
                        "status": "media" if path else "gloss_only",
                        "asset": str(path) if path else None,
                        "reason": reason,
                    }
                )
            else:
                result.append(
                    {
                        "source": phrase,
                        "gloss": None,
                        "concept_id": None,
                        "status": "unmapped",
                        "asset": None,
                        "reason": "No matching concept; requires clarification",
                    }
                )
            position += size
        return result


class SpeechRecognizer:
    def __init__(self, model="tiny"):
        from faster_whisper import WhisperModel

        self.model_name = model
        self.model = WhisperModel(model, device="cpu", compute_type="int8")

    def transcribe(self, audio, language="en"):
        if language not in LANGUAGES:
            raise ValueError("Unsupported input language")
        started = time.perf_counter()
        if isinstance(audio, (str, Path)):
            decoded = subprocess.run(
                [
                    "ffmpeg",
                    "-nostdin",
                    "-v",
                    "error",
                    "-i",
                    str(audio),
                    "-f",
                    "f32le",
                    "-ac",
                    "1",
                    "-ar",
                    "16000",
                    "pipe:1",
                ],
                capture_output=True,
                check=True,
                timeout=120,
            )
            samples = np.frombuffer(decoded.stdout, dtype=np.float32).copy()
        else:
            samples = np.asarray(audio, dtype=np.float32)
        if samples.ndim != 1 or not len(samples) or not np.isfinite(samples).all():
            raise ValueError("Audio must be nonempty finite mono samples at 16 kHz")
        segments, _ = self.model.transcribe(
            samples, language=language, beam_size=5, vad_filter=True
        )
        segments = [
            {"start": float(s.start), "end": float(s.end), "text": s.text.strip()}
            for s in segments
        ]
        return {
            "text": " ".join(s["text"] for s in segments),
            "segments": segments,
            "language": language,
            "model": self.model_name,
            "processing_seconds": time.perf_counter() - started,
            "audio_seconds": len(samples) / 16000,
        }

    def stream_chunks(self, chunks, language="en", sample_rate=16000):
        """Chunk-by-chunk protocol, not native streaming ASR or a live microphone transport."""
        if sample_rate != 16000:
            raise ValueError("Resample to 16 kHz mono before streaming")
        offset = 0.0
        for index, chunk in enumerate(chunks):
            chunk = np.asarray(chunk, dtype=np.float32)
            if chunk.ndim != 1 or not len(chunk) or not np.isfinite(chunk).all():
                raise ValueError("Invalid audio chunk")
            result = self.transcribe(chunk, language)
            for segment in result["segments"]:
                segment["start"] += offset
                segment["end"] += offset
            yield {**result, "chunk_index": index, "audio_offset_seconds": offset}
            offset += len(chunk) / sample_rate
