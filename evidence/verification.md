# Verification record — 2026-10-20

- `python -m pytest -q`: five tests passed (normalization, authored examples, asset provenance, chunk protocol, Streamlit render/language switch).
- `python scripts/evaluate.py`: 24/24 authored sequence regressions; eight cases per language.
- `python scripts/validate_assets.py`: reports 36 concepts, 117 aliases and zero sign assets.
- Actual tiny-model CPU ASR: three successful transcriptions of the 11s JFK fixture; median 5.4471s. Results and hashes in asr_smoke.json.
- Chart rendered from committed metrics and inspected.

Asset checks are structural only. No gesture playback can be verified without real assets; no end-to-end or independent alignment benchmark is claimed.
