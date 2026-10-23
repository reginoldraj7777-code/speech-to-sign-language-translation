# Prototype model card

**Version:** October 2026 implementation extension. **Purpose:** demonstrate modular transcription, inspectable concept retrieval and asset governance. **Audience:** technical reviewers and research collaborators. It is not a validated interpretation service or a replacement for a qualified interpreter.

**Models:** faster-whisper CPU inference (tiny by default; selectable base/small). No custom training or fine-tuning. First use downloads upstream weights. FFmpeg converts audio to mono 16 kHz. The real benchmark is one English clip, not multilingual ASR validation.

**Retrieval:** deterministic longest phrase lookup over 36 authored concepts. Unicode normalization preserves Tamil marks. The 117 aliases are text entries, not 117 gestures. English, Tamil and German aliases are illustrative and need fluent/expert review, including polysemy and idiomatic usage. Word order is preserved from the input; sign-language grammar is not modeled.

**Known limitations:** no licensed gesture files bundled; no independent accuracy study; no signer-specific evaluation; no learned context disambiguation; no true live microphone transport. Audio inference is synchronous and may be slow on CPU. Long clips can require substantial memory; the UI limits uploaded size to 20 MB. The service has no account/authentication layer and is intended for local use.

**Data handling:** typed messages and uploaded audio are used in the local app process. Temporary audio files are removed after transcription. Models are cached locally. The user may explicitly download a JSON trace; no transcription is sent to an external ASR API by this implementation. Avoid entering sensitive audio in an untrusted hosted environment.

**Provenance:** original academic report preserved without edits. The October 2026 code was AI-assisted at the owner's request. Automated tests and real ASR smoke checks are recorded separately; no retrospective human review or publication verification is claimed.
