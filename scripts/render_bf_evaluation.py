"""Replot recorded BF sensor evidence; never run a simulation.

Capture the selected raw readings once with --capture-from, then render from the
small checked-in snapshot. The recorded study uses the fixed-source apparatus.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/physim-bf-figures-mpl")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs_source/data/bf-evaluation.npz"
META = DATA.with_suffix(".json")
OUT = ROOT / "docs/assets/evaluation"
ARMS = ("sham", "trail_low", "trail_mid", "trail_high")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def capture(source):
    arrays, sources = {}, []

    def record(path):
        sources.append(dict(path=str(path.relative_to(ROOT)), sha256=digest(path)))

    apparatus_path = source / "preparation/apparatus.json"
    apparatus = json.loads(apparatus_path.read_text())
    assert apparatus.get("protocol", "fixed-source-v1") == "fixed-source-v1"
    port = apparatus["port_permutation"].index(0)
    record(apparatus_path)
    for arm in ARMS:
        path = source / "science" / arm / "observations.npz"
        receipt_path = path.with_name("receipt.json")
        receipt = json.loads(receipt_path.read_text())
        assert digest(path) == receipt["observations_sha256"]
        with np.load(path, allow_pickle=False) as data:
            request = json.loads(str(data["request"]))
            assert request == receipt["request"]
            expected_actions = (
                []
                if arm == "sham"
                else [
                    dict(
                        t=0,
                        kind="inject",
                        port=2,
                        amp={"trail_low": 0.002, "trail_mid": 0.01, "trail_high": 0.05}[arm],
                        dur=5,
                    )
                ]
            )
            assert request["actions"] == expected_actions
            arrays[arm] = data["query0"][:, :, port, :]
            assert arrays[arm].shape == (3, 15, 13) and np.isfinite(arrays[arm]).all()
            times = np.array(request["queries"][0]["t"])
            if "times" in arrays:
                np.testing.assert_array_equal(times, arrays["times"])
            arrays["times"] = times
        record(path)
        record(receipt_path)
    causal_path = source / "causal/readings.npz"
    result_path = source / "causal/result.json"
    result = json.loads(result_path.read_text())
    arrays["causal_times"] = np.array(result["queries"][0]["t"])
    with np.load(causal_path, allow_pickle=False) as data:
        for key in data.files:
            arrays[key] = data[key][:, :, port, :]
    for label in ("coupled", "feedback_removed"):
        effect = np.sqrt(np.mean((arrays[label + "_pulse"] - arrays[label + "_sham"]) ** 2, axis=-1))
        np.testing.assert_array_equal(effect[:, -1], result[label + "_effect_rms"])
    record(causal_path)
    record(result_path)
    np.savez_compressed(DATA, **arrays)
    META.write_text(
        json.dumps(
            dict(
                study="BF preparation study, 13–14 September 2026",
                apparatus="fixed-source-v1; source six units from the probe center",
                data_sha256=digest(DATA),
                sources=sources,
                selected_data="Exact activator readings (public port 1), all 13 device-0 slots, all three repetitions.",
                ordinary_contrast="Per-repetition RMS over slots versus the independent no-pulse ensemble mean.",
                noise_comparison="Mean RMS over the three distinct no-pulse member pairs; pairs share members.",
                mechanism_effect="Per-repetition pulse-minus-sham RMS with paired future noise, at time 50.",
            ),
            indent=2,
        )
        + "\n"
    )


def save(fig, name):
    path = OUT / (name + ".svg")
    fig.savefig(path, metadata={"Date": None}, facecolor="white")
    path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n")
    fig.savefig(Path("/tmp") / (name + ".png"), dpi=130)
    plt.close(fig)


def render(mobile=False):
    assert digest(DATA) == json.loads(META.read_text())["data_sha256"]
    OUT.mkdir(parents=True, exist_ok=True)
    suffix = "-mobile" if mobile else ""
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 12,
            "text.color": "#17242f",
            "axes.labelcolor": "#17242f",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "svg.fonttype": "path",
            "svg.hashsalt": "physim-bf-evaluation",
        }
    )
    with np.load(DATA, allow_pickle=False) as data:
        t, sham = data["times"], data["sham"]
        assert sham.shape == (3, 15, 13) and t[-1] == 50
        fig, ax = plt.subplots(figsize=(4.6, 4.5) if mobile else (8.2, 4.2))
        fig.subplots_adjust(left=0.19 if mobile else 0.11, right=0.97, bottom=0.16, top=0.76)
        ax.axvspan(0, 5, color="#e8ecef", zorder=0)
        ax.text(2.5, 1.44, "Pulse", ha="center", fontsize=10, rotation=90 if mobile else 0)
        for arm, amp, color, marker in (
            ("trail_low", 0.002, "#126e64", "o"),
            ("trail_mid", 0.01, "#075dad", "s"),
            ("trail_high", 0.05, "#b9510a", "^"),
        ):
            contrast = np.sqrt(np.mean((data[arm] - sham.mean(axis=0)) ** 2, axis=-1))
            ax.plot(t, contrast.mean(axis=0), label=f"Amplitude {amp:g}", color=color, marker=marker, ms=3.5, lw=1.8)
            ax.fill_between(t, contrast.min(axis=0), contrast.max(axis=0), color=color, alpha=0.16)
            print(f"{arm}: final sensor contrast {contrast[:, -1].mean():.12g}")
        noise = np.array([np.sqrt(np.mean((sham[i] - sham[j]) ** 2, axis=-1)) for i, j in ((0, 1), (0, 2), (1, 2))])
        ax.plot(t, noise.mean(axis=0), "--", color="#303940", lw=1.7, label="No-pulse difference")
        print(f"No-pulse pairwise difference: {noise[:, -1].mean():.12g}")
        ax.set(xlabel="Time after preparation", ylabel="Activator contrast (RMS)", xlim=(0, 50), ylim=(0, 1.6))
        ax.set_xticks([0, 10, 20, 30, 40, 50])
        ax.grid(axis="y", color="#e4e8ec", lw=0.7)
        ax.set_axisbelow(True)
        fig.legend(
            loc="upper center", ncol=2, frameon=False, fontsize=10 if mobile else 11, bbox_to_anchor=(0.53, 0.98)
        )
        save(fig, "bf-sensor-response" + suffix)

        fig, ax = plt.subplots(figsize=(4.6, 4.1) if mobile else (8.2, 3.5))
        fig.subplots_adjust(left=0.19 if mobile else 0.11, right=0.97, bottom=0.20, top=0.90)
        for i, (label, color) in enumerate((("coupled", "#126e64"), ("feedback_removed", "#68737e"))):
            effect = np.sqrt(np.mean((data[label + "_pulse"][:, -1] - data[label + "_sham"][:, -1]) ** 2, axis=-1))
            ax.bar(i, effect.mean(), width=0.52, color=color, alpha=0.30, edgecolor=color, linewidth=1.3)
            ax.scatter(i + np.array([-0.07, 0, 0.07]), effect, s=30, color=color, zorder=3, clip_on=False)
            label_text = f"{effect.mean():.3f}" if i == 0 else "0 in all three repeats"
            ax.text(i, effect.mean() + 0.065, label_text, ha="center", fontsize=11)
        ax.set(
            xticks=[0, 1],
            xticklabels=["Original\nfeedback", "Feedback term\nremoved"],
            ylabel="Pulse effect at time 50 (RMS)",
            ylim=(0, 1.5),
            xlim=(-0.55, 1.55),
        )
        ax.grid(axis="y", color="#e4e8ec", lw=0.7)
        ax.set_axisbelow(True)
        save(fig, "bf-feedback-control" + suffix)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture-from", type=Path)
    args = parser.parse_args()
    if args.capture_from:
        capture(args.capture_from.resolve())
    render()
    render(mobile=True)
