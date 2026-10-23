"""Audit asset paths, required metadata and distinct file hashes."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.pipeline import Lexicon

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-assets", type=int, default=0)
    args = parser.parse_args()
    lexicon = Lexicon()
    report = {
        "inventory": lexicon.inventory(),
        "entries": [
            {"id": entry["id"], "status": lexicon.usable_asset(entry)[1]}
            for entry in lexicon.entries
        ],
    }
    print(json.dumps(report, indent=2))
    if report["inventory"]["distinct_usable_assets"] < args.require_assets:
        raise SystemExit("Required distinct asset count not met")
