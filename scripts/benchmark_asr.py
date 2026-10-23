"""Actual CPU transcription smoke benchmark; excludes first model initialization."""

import argparse
import hashlib
import json
import platform
import statistics
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.pipeline import SpeechRecognizer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio", type=Path)
    parser.add_argument("--model", default="tiny")
    parser.add_argument("--language", default="en", choices=["en", "ta", "de"])
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--output", type=Path, default=Path("evidence/asr_smoke.json"))
    args = parser.parse_args()
    if args.runs < 1:
        parser.error("--runs must be positive")
    recognizer = SpeechRecognizer(args.model)
    results = [
        recognizer.transcribe(args.audio, args.language) for _ in range(args.runs)
    ]
    payload = {
        "generated_utc": datetime.now(UTC).isoformat(),
        "audio_sha256": hashlib.sha256(args.audio.read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(
            (ROOT / "src/pipeline.py").read_bytes()
        ).hexdigest(),
        "model": args.model,
        "language": args.language,
        "device": "cpu",
        "compute_type": "int8",
        "runs": results,
        "median_processing_seconds": statistics.median(
            result["processing_seconds"] for result in results
        ),
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "scope": "Single-clip repeated ASR smoke check. Includes audio decoding and inference, excludes model load, user recording and sign playback. Not end-to-end or multilingual accuracy.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
