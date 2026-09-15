"""Render full-field and trajectory evidence without hiding dense activators."""

import argparse
import json
import math
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/physim-phenomenology-mpl")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from blobkit import metrics_v1


def render_rotors(sources, output):
    """Compare prepared-pair rotation with the otherwise identical control."""
    sources = [Path(source) for source in sources if (Path(source) / "rotation.json").exists()]
    if not sources:
        return
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.7))
    for source in sources:
        row = json.loads((source / "rotation.json").read_text())
        t, angle = np.array(row["t"]), np.array(row["angle_unwrapped"])
        label = f"{'Coupled' if row['coupled'] else 'Cross-drive removed'}, seed {row['seed']}"
        style = {} if row["coupled"] else dict(color="#777777", linestyle="--")
        axes[0].plot(t, (angle - angle[0]) / (2 * np.pi), label=label, **style)
        axes[1].plot(t, row["separation"], label=label, **style)
    axes[0].set(xlabel="Time (tu)", ylabel="Turns since initialization", title="Pair orientation")
    axes[1].set(xlabel="Time (tu)", ylabel="Separation (simulation units)", title="Pair separation")
    for ax in axes:
        ax.axvspan(1500, 2500, color="#555555", alpha=0.07)
        ax.set_xlim(0, 2500)
        ax.legend(fontsize=8)
    fig.suptitle("xv: sustained rotation depends on cross-coupling")
    fig.text(
        0.5,
        0.025,
        "Same initial fields, no kick · shaded interval: angular-velocity fit · all fields retained",
        ha="center",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 0.94))
    fig.savefig(output / "xv_rotation_control.png", dpi=140)
    plt.close(fig)


def render_memory(source, output):
    path = source / "responses/samples.npz"
    if not path.exists():
        return
    with np.load(path, allow_pickle=False) as data:
        samples, times, arms = data["samples"], data["times"], data["arms"].tolist()
    if "erase_trail" not in arms:
        return
    with np.load(source / "final_state.npz", allow_pickle=False) as data:
        initial = data["F"]
    with np.load(source / "responses/final_fields.npz", allow_pickle=False) as data:
        fields = data["F"]
    erase = arms.index("erase_trail")
    iy, ix = np.unravel_index(np.argmax(initial[0]), initial[0].shape)
    ys, xs = (np.arange(-40, 41) + iy) % 256, (np.arange(-40, 41) + ix) % 256
    fig, axes = plt.subplots(1, 4, figsize=(15, 4.2))
    for ax, field, title in zip(
        axes[:2],
        [fields[0, 0], fields[erase, 0]],
        ["Trail retained: activator at t=50", "Initial trail erased: activator at t=50"],
    ):
        im = ax.imshow(field[np.ix_(ys, xs)], extent=(-20, 20, 20, -20), vmin=-0.75, vmax=1.5, cmap="viridis")
        fig.colorbar(im, ax=ax, shrink=0.7)
        ax.set_title(title, fontsize=9)
        ax.set(xlabel="Relative x", ylabel="Relative y")
    delta = (fields[erase, 0] - fields[0, 0])[np.ix_(ys, xs)]
    limit = float(np.abs(delta).max())
    im = axes[2].imshow(delta, extent=(-20, 20, 20, -20), vmin=-limit, vmax=limit, cmap="RdBu_r")
    fig.colorbar(im, ax=axes[2], shrink=0.7)
    axes[2].set(title="Activator difference, paired noise", xlabel="Relative x", ylabel="Relative y")
    effect = np.sqrt(np.mean((samples[erase, :, :, 0] - samples[0, :, :, 0]) ** 2, axis=-1))
    noise = np.array(
        [
            np.sqrt(np.mean((samples[0, i, :, 0] - samples[0, j, :, 0]) ** 2, axis=-1))
            for i, j in [(0, 1), (0, 2), (1, 2)]
        ]
    )
    for data, label, color in [
        (effect, "Erase-trail effect", "#007e87"),
        (noise, "Independent-noise difference", "#777777"),
    ]:
        axes[3].plot(times, data.mean(axis=0), label=label, color=color)
        axes[3].fill_between(times, data.min(axis=0), data.max(axis=0), color=color, alpha=0.2)
    axes[3].set(
        title="Native activator readings", xlabel="Time after reset (tu)", ylabel="RMS difference across 13 probe nodes"
    )
    axes[3].legend(fontsize=8)
    fig.suptitle("bf: changing only the initial trail changes future activator dynamics", fontsize=13)
    fig.text(
        0.5,
        0.02,
        f"{source.name} · same activator at t=0 · 3 future noise seeds · privileged causal diagnostic",
        ha="center",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.07, 1, 0.90))
    fig.savefig(output / f"{source.name}_memory.png", dpi=130)
    plt.close(fig)


def render(source, output):
    source, output = Path(source), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    with np.load(source / "fields.npz", allow_pickle=False) as data:
        fields, times = data["F"], data["t"]
    g = json.loads((source / "genome.json").read_text())
    record = json.loads((source / "record.json").read_text())
    na, nf = len(g["acts"]), fields.shape[1]
    fig, axes = plt.subplots(math.ceil(nf / 4), 4, figsize=(12, 3.2 * math.ceil(nf / 4)), squeeze=False)
    for i, ax in enumerate(axes.flat):
        if i >= nf:
            ax.set_visible(False)
            continue
        baseline = g["acts"][i]["u0"] if i < na else 0
        lo, hi = min(float(fields[:, i].min()), baseline), max(float(fields[:, i].max()), baseline)
        im = ax.imshow(fields[-1, i], extent=(0, 128, 128, 0), cmap="viridis", vmin=lo, vmax=hi)
        label = f"activator {i}" if i < na else f"channel {i - na} (tau={g['chans'][i - na]['tau']:.3g})"
        ax.set_title(f"{label}\nspatial SD {fields[-1, i].std():.3g}", fontsize=9)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        fig.colorbar(im, ax=ax, shrink=0.75)
    fig.suptitle(
        f"{source.name}: ALL fields at t={times[-1]:g}\nEach field's scale spans its whole recorded run.", fontsize=12
    )
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(output / f"{source.name}_fields.png", dpi=120)
    plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))
    for i in range(na):
        thr = g["acts"][i]["u0"] + 0.45 * (np.sqrt(g["acts"][i]["lam"]) - g["acts"][i]["u0"])
        axes[0].plot(times, (fields[:, i] > thr).mean(axis=(-1, -2)), label=f"act {i}")
        axes[1].plot(record["ct"], [r["n"] for r in record["orgs"][str(i)]], label=f"act {i}")
    record["blobs"] = {int(i): value for i, value in record["blobs"].items()}
    for track in metrics_v1.build_tracks(record):
        idx = np.array(track["ks"])
        select = np.array(record["t"])[idx] >= times[-1] - 250
        positions = np.array(track["yx"])[select] % 128
        if len(positions) < 2:
            continue
        positions[np.r_[False, np.any(np.abs(np.diff(positions, axis=0)) > 64, axis=1)]] = np.nan
        axes[2].plot(positions[:, 1], positions[:, 0], lw=0.7, alpha=0.7, color=plt.get_cmap("tab10")(track["act"]))
    axes[0].set(
        title="Activator occupancy (dense backgrounds included)",
        xlabel="Time (tu)",
        ylabel="Fraction of domain",
        ylim=(0, 1.03),
    )
    axes[1].set(title="Organism-level connected components", xlabel="Time (tu)", ylabel="Count")
    axes[2].set(
        title="Tracked centroids: final 250 tu", xlabel="x", ylabel="y", xlim=(0, 128), ylim=(128, 0), aspect="equal"
    )
    axes[0].legend(fontsize=8)
    axes[1].legend(fontsize=8)
    fig.suptitle(f"{source.name}: fields, organisms and motion are separate measurements")
    fig.tight_layout()
    fig.savefig(output / f"{source.name}_dynamics.png", dpi=120)
    plt.close(fig)
    render_memory(source, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    for source in args.sources:
        render(source, args.output)
    render_rotors(args.sources, args.output)
