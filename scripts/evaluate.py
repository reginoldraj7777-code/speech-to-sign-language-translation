"""Evaluate authored retrieval regressions; not an independent gesture-accuracy study."""

import argparse
import csv
import hashlib
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.pipeline import Lexicon


def evaluate(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    fixture = ROOT / "tests/fixtures/retrieval_cases.json"
    cases = json.loads(fixture.read_text())
    lexicon = Lexicon()
    rows = []
    for index, case in enumerate(cases):
        started = time.perf_counter()
        result = lexicon.translate(case["text"], case["language"])
        elapsed = (time.perf_counter() - started) * 1000
        baseline = lexicon.translate(
            case["text"], case["language"], normalization=False
        )
        predicted = [entry["gloss"] for entry in result]
        rows.append(
            {
                "case": index,
                "language": case["language"],
                "text": case["text"],
                "expected": json.dumps(case["expected_glosses"]),
                "predicted": json.dumps(predicted),
                "exact_match": predicted == case["expected_glosses"],
                "retrieval_ms": elapsed,
                "baseline_unknown": sum(
                    entry["status"] == "unmapped" for entry in baseline
                ),
                "baseline_units": len(baseline),
                "normalized_unknown": sum(
                    entry["status"] == "unmapped" for entry in result
                ),
                "normalized_units": len(result),
            }
        )
    with (output / "retrieval_cases.csv").open("w") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    baseline = sum(row["baseline_unknown"] for row in rows) / sum(
        row["baseline_units"] for row in rows
    )
    normalized = sum(row["normalized_unknown"] for row in rows) / sum(
        row["normalized_units"] for row in rows
    )
    metrics = {
        "generated_utc": datetime.now(UTC).isoformat(),
        "source_sha256": hashlib.sha256(
            (ROOT / "src/pipeline.py").read_bytes()
        ).hexdigest(),
        "fixture_sha256": hashlib.sha256(fixture.read_bytes()).hexdigest(),
        "inventory": lexicon.inventory(),
        "cases": len(rows),
        "cases_per_language": {
            language: sum(row["language"] == language for row in rows)
            for language in ["en", "ta", "de"]
        },
        "exact_sequence_match_rate": sum(row["exact_match"] for row in rows)
        / len(rows),
        "baseline_unknown_unit_rate": baseline,
        "normalized_unknown_unit_rate": normalized,
        "relative_unknown_unit_rate_reduction": 1 - normalized / baseline
        if baseline
        else 0,
        "median_retrieval_ms": sorted(row["retrieval_ms"] for row in rows)[
            len(rows) // 2
        ],
        "scope": "24 authored regression cases, not an independent accuracy dataset. Normalization and phrase grouping change the retrieval-unit denominator. No gesture alignment or end-to-end latency is measured.",
    }
    (output / "retrieval_metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    print(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="evidence")
    evaluate(parser.parse_args().output)
