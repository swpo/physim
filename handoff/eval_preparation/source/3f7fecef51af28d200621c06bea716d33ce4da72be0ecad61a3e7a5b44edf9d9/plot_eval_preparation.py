"""Scientific figures for prepared-world experiments and evaluation checks."""

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/physim-phenomenology-mpl")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def plot(source, output):
    source, output = Path(source), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    origin = json.loads((source / "preparation/origin.json").read_text())
    name = origin["world"]
    apparatus = json.loads((source / "preparation/apparatus.json").read_text())
    center = np.array(apparatus["devices"][0]["parameters"]["center"])
    ys, xs = [(np.arange(-40, 41) + int(v / 0.5)) % 256 for v in center]
    selected = ["sham", "act_strong", "trail_high"] if name == "bf" else ["sham", "act_strong", "partner_pulse"]
    labels = ["No source", "Activator pulse", "Trail-channel pulse" if name == "bf" else "Partner pulse"]
    fig, axes = plt.subplots(3, 3, figsize=(10, 9.5), sharex=True, sharey=True)
    for row, (arm, label) in enumerate(zip(selected, labels)):
        with np.load(source / "science" / arm / "fields.npz", allow_pickle=False) as data:
            times, fields = data["t"], data["F"]
        for col, t in enumerate([0, 10, 50]):
            field = fields[np.argmin(abs(times - t)), 0][np.ix_(ys, xs)]
            im = axes[row, col].imshow(field, vmin=-0.8, vmax=1.5, cmap="viridis", extent=(-20, 20, 20, -20))
            axes[row, col].set_title(f"{label} · t={t}", fontsize=10)
            if row == 2:
                axes[row, col].set_xlabel("Relative x")
            if col == 0:
                axes[row, col].set_ylabel("Relative y")
    fig.suptitle(f"{name}: ordinary interventions change later activator fields", fontsize=14)
    fig.subplots_adjust(left=0.07, right=0.88, bottom=0.06, top=0.93, hspace=0.25)
    fig.colorbar(im, cax=fig.add_axes([0.91, 0.15, 0.02, 0.65]), label="Activator 0, native units")
    fig.savefig(output / f"{name}_fields.png", dpi=140)
    plt.close(fig)

    with np.load(source / "science/sham/observations.npz", allow_pickle=False) as data:
        sham = data["query0"]
        request = json.loads(str(data["request"]))
    t = np.array(request["queries"][0]["t"])
    act_port = apparatus["port_permutation"].index(0)
    arms = (
        ["act_weak", "act_strong", "trail_low", "trail_mid", "trail_high"]
        if name == "bf"
        else ["act_weak", "act_strong", "partner_pulse", "act_delayed"]
    )
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.7))
    for arm in arms:
        with np.load(source / "science" / arm / "observations.npz", allow_pickle=False) as data:
            values = data["query0"]
        contrast = np.sqrt(np.mean((values[:, :, act_port] - sham[:, :, act_port].mean(axis=0)) ** 2, axis=-1))
        line = axes[0].plot(t, contrast.mean(0), label=arm.replace("_", " "))[0]
        axes[0].fill_between(t, contrast.min(0), contrast.max(0), color=line.get_color(), alpha=0.15)
    noise = np.array(
        [
            np.sqrt(np.mean((sham[i, :, act_port] - sham[j, :, act_port]) ** 2, axis=-1))
            for i, j in [(0, 1), (0, 2), (1, 2)]
        ]
    )
    axes[0].plot(t, noise.mean(0), color="black", linestyle="--", label="Independent sham difference")
    axes[0].set(
        xlabel="Time (tu)",
        ylabel="Activator RMS contrast across 13 nodes",
        title="Effects visible through native sensors",
    )
    axes[0].legend(fontsize=8)
    if name == "bf":
        causal = json.loads((source / "causal/result.json").read_text())
        for i, key in enumerate(["coupled_effect_rms", "feedback_removed_effect_rms"]):
            values = causal[key]
            axes[1].bar(i, np.mean(values), width=0.5, color=["#007e87", "#777777"][i])
            axes[1].scatter(np.linspace(i - 0.07, i + 0.07, 3), values, color="black", s=16)
        axes[1].set(
            xticks=[0, 1],
            xticklabels=["Original feedback", "Bilinear term removed"],
            ylabel="Paired trail-pulse effect at 50 tu",
            title="Mechanism control: response disappears",
        )
    else:
        with np.load(source / "science/sham/fields.npz", allow_pickle=False) as data:
            fields, times = data["F"], data["t"]
        from blobkit import genome

        centers = []
        for field in fields:
            coords = []
            for a in [0, 1]:
                support = field[a] > 0.5
                ys0, xs0 = np.where(support)
                coords.append(np.array([ys0.mean(), xs0.mean()]) * 0.5)
            centers.append(coords)
        centers = np.array(centers)
        for a in [0, 1]:
            positions = genome.min_image(centers[:, a] - center, 128)
            axes[1].plot(positions[:, 1], positions[:, 0], "o-", ms=3, label=f"Activator {a}")
        axes[1].set(xlabel="Relative x", ylabel="Relative y", title="Unforced pair motion over 50 tu", aspect="equal")
        axes[1].legend()
    fig.suptitle(f"{name}: repeatable observations and a physical explanation", fontsize=14)
    fig.text(
        0.5,
        0.015,
        "Three independent native realizations per ordinary program; bands show observed ranges, not confidence intervals.",
        ha="center",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.05, 1, 0.94))
    fig.savefig(output / f"{name}_mechanism.png", dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plot(args.source, args.output)
