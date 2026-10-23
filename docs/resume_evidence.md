# Résumé evidence map

| Claim | Current repository evidence | Remaining gap |
|---|---|---|
| Three languages | English, Tamil and German input paths and eight retrieval regressions each | Spoken-language input is not three validated sign languages; ASR smoke tested in English only |
| 5K+ gesture mappings | 36 authored concepts, 117 aliases, zero bundled media assets | Need licensed gesture collection, provenance and expert review; aliases never count as gestures |
| Streaming ASR | Working audio transcription and chunk iterator with timestamp offsets | UI handles completed clips, not live continuous microphone streaming |
| Context-aware retrieval | Longest phrase lookup with Unicode normalization | No learned contextual model, POS pipeline or grammar-aware sign translation |
| 2.1s median end-to-end | 5.45s median on one 11s English audio clip, three CPU runs | ASR-only; end-to-end sign playback benchmark missing |
| 88% gesture alignment | 24/24 authored text-to-gloss regression sequences match | Not independent alignment accuracy; no actual sign assets are evaluated |
| 28% OOV fallback reduction | 90.21% relative unknown-unit rate reduction on authored normalization fixtures | Changed grouping denominator and non-independent fixture; historical 28% not reproduced |
| AIDE 2024 publication | Original November 2024 academic report is preserved | Need verifiable proceedings/DOI/acceptance record; report alone is not publication proof |

The report's own gesture-mapping figure is 85%, not 88%, and it describes English/Tamil. Its evaluation is not reproducible from the original repository contents. New code is a dated extension; it does not backdate work or establish historical authorship/deployment.
