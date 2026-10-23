# Evaluation protocol

## Retrieval regression

The committed fixture contains 24 authored examples, eight each in English, Tamil and German. It deliberately covers punctuation, case, multiword aliases, unknown words and Tamil combining marks. Expected output includes unknowns as null. Exact sequence match is 100%; because the examples and lexicon were authored together, this only establishes regression behavior, not generalization or gesture accuracy.

Baseline uses case-sensitive whitespace splitting against the same alias index; improved retrieval applies Unicode NFKC, case folding, punctuation cleanup and longest-phrase matching. Baseline unknown-unit rate = 68.0851%; normalized rate = 6.6667%. Relative reduction = 1 − normalized rate / baseline rate. The denominator is returned retrieval units, which changes with phrase grouping. This is not the résumé's independently measured 28% OOV reduction. Raw counts per case are included so readers can recompute or choose another denominator.

## Actual ASR smoke check

The public faster-whisper test fixture `tests/data/jfk.flac` was downloaded from its GitHub repository. SHA256: `63a4b1e4c1dc655ac70961ffbf518acd249df237e5a0152faae9a4a836949715`. It contains 11 seconds of English speech. CPU tiny model, int8, beam size five, VAD enabled; three repeated runs with model initialization excluded. Processing includes FFmpeg decoding and consuming the transcription generator. All three transcripts and durations are committed. Median: 5.4471s. No Tamil/German speech evaluation or word-error-rate study is claimed.

## What is not measured

No sign-language alignment accuracy, semantic adequacy, signer comprehension, natural grammar or complete speech-to-video latency. Chunk timestamps are tested with a fake recognizer solely to isolate the streaming protocol; these tests are not speech-quality evidence. Streamlit AppTest verifies render and language switching without requiring model downloads.

## Next independent evaluation

Register an appropriately licensed corpus with actual distinct media, linguistic labels and train/dev/test separation by signer and utterance. Freeze the lexicon and processing code before evaluating held-out spoken and signed utterances. Have qualified sign-language reviewers score alignment and comprehension. Measure audio arrival through final visible gesture under fixed hardware, clip lengths and warmup rules. Report error cases, uncertainty, denominators and all exclusions.
