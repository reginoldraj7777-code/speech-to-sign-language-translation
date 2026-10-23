# Register genuine sign media

The repository ships no licensed gesture collection. `data/lexicon.json` contains authored text concepts and aliases only. Input languages and sign languages are distinct: an English word is not automatically an ASL, BSL or ISL sign, and Tamil text does not define a sign-language grammar.

1. Obtain a corpus whose license permits the intended local use and redistribution, if any. Retain its license and source record. Do not upload third-party media without permission.
2. Place a local file under `data/assets/`; this directory is ignored by Git by default.
3. On the corresponding concept in `data/lexicon.json`, set `asset`, `license`, `source_url` and `sign_language`. Example structure (replace with real values):

```json
{
  "asset": "data/assets/hello.mp4",
  "license": "exact license identifier or permission reference",
  "source_url": "canonical source URL",
  "sign_language": "actual sign-language identifier"
}
```

4. Run `python scripts/validate_assets.py`. The validator confines paths, requires metadata, checks supported extension/nonempty file, and counts distinct file hashes. Different aliases or duplicate files never inflate the unique-asset count.
5. Open the app and inspect playback. Have an expert verify sign meaning, variation, sequencing and language suitability. File-presence validation is not media decoding or linguistic validation.
6. Only after registering genuine media, use `--require-assets 5000` to enforce a real minimum count. It fails on the current repository, correctly.

Supported playback containers: MP4/WebM video and GIF/PNG/JPEG images. Browser codec support varies. A still image can document a pose but does not capture motion-based signs; do not count it as validated dynamic translation without appropriate review. The authored lexicon supports a single selected media asset per concept; variants and grammar need a richer reviewed model before production use.
