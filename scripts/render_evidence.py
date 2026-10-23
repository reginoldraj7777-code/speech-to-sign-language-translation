"""Show measured retrieval regressions, ASR smoke timings and actual asset inventory."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

p = Path(__file__).resolve().parents[1] / "evidence"
m = json.loads((p / "retrieval_metrics.json").read_text())
a = json.loads((p / "asr_smoke.json").read_text())
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titleweight": "bold",
    }
)
fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor="#f7fafc")
fig.suptitle(
    "Speech to Sign • An inspectable research prototype",
    fontsize=18,
    fontweight="bold",
    x=0.06,
    ha="left",
)
axes[0].bar(
    ["English", "Tamil", "German"],
    [m["cases_per_language"][key] for key in ["en", "ta", "de"]],
    color="#087f8c",
)
axes[0].set(
    title="24 authored retrieval regressions",
    ylabel="Cases with expected concept sequence",
    ylim=(0, 10),
)
axes[1].bar(
    ["Run 1", "Run 2", "Run 3"],
    [r["processing_seconds"] for r in a["runs"]],
    color="#087f8c",
)
axes[1].set(
    title="Real CPU transcription smoke check", ylabel="Processing time (seconds)"
)
axes[1].axhline(
    a["median_processing_seconds"],
    color="#e07726",
    label=f"Median {a['median_processing_seconds']:.2f}s",
)
axes[1].legend(frameon=False)
axes[2].axis("off")
axes[2].text(
    0.04,
    0.78,
    str(m["inventory"]["concepts"]),
    fontsize=48,
    color="#123945",
    fontweight="bold",
)
axes[2].text(0.04, 0.62, "authored concepts", fontsize=16)
axes[2].text(
    0.04,
    0.36,
    str(m["inventory"]["distinct_usable_assets"]),
    fontsize=48,
    color="#e07726",
    fontweight="bold",
)
axes[2].text(0.04, 0.20, "licensed sign assets bundled", fontsize=16)
fig.text(
    0.06,
    0.025,
    "Authored regression success is not gesture accuracy. ASR: one 11-second English clip; model load excluded. Sign playback awaits licensed assets.",
    fontsize=10,
    color="#475569",
)
fig.tight_layout(rect=(0.03, 0.08, 1, 0.92), w_pad=3)
fig.savefig(p / "evaluation.png", dpi=150)
