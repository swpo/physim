"""Compare later spatial responses in the two prepared laboratories."""

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
    source = Path(source)
    fig, axes = plt.subplots(2, 3, figsize=(12, 8), sharex=True, sharey=True)
    for row, name in enumerate(("bf", "xv")):
        root = source / name
        apparatus = json.loads((root / "preparation/apparatus.json").read_text())
        center = np.array(apparatus["devices"][0]["parameters"]["center"])
        y_grid, x_grid = np.arange(-40, 41) * 0.5, np.arange(-40, 49) * 0.5
        ys = (np.arange(-40, 41) + int(center[0] / 0.5)) % 256
        xs = (np.arange(-40, 49) + int(center[1] / 0.5)) % 256
        arms = [("sham", "No source"), ("act_strong", "Activator pulse")]
        arms.append(("trail_high", "Trail pulse") if name == "bf" else ("partner_pulse", "Partner pulse"))
        for col, (arm, label) in enumerate(arms):
            with np.load(root / "science" / arm / "fields.npz", allow_pickle=False) as data:
                fields, times = data["F"], data["t"]
            final = fields[np.argmin(abs(times - 50))]
            axis = axes[row, col]
            im = axis.imshow(
                final[0][np.ix_(ys, xs)], extent=(-20.25, 24.25, 20.25, -20.25), vmin=-0.8, vmax=1.5, cmap="viridis"
            )
            axis.contour(
                x_grid,
                y_grid,
                fields[0, 0][np.ix_(ys, xs)],
                levels=[0.5],
                colors="#bbbbbb",
                linestyles="--",
                linewidths=1.1,
            )
            if name == "xv":
                axis.contour(x_grid, y_grid, final[1][np.ix_(ys, xs)], levels=[0.5], colors="white", linewidths=1.2)
            emitter = np.array(apparatus["emitter_yx"]) - center
            axis.plot(emitter[1], emitter[0], "+", color="#ff7777", ms=9, mew=1.5)
            axis.set_title(f"{name.upper()} · {label}", fontsize=12)
            if col == 0:
                axis.set_ylabel("Relative y")
            if row == 1:
                axis.set_xlabel("Relative x")
    fig.suptitle("The same starting fields lead to different futures after a five-tu pulse", fontsize=15)
    fig.subplots_adjust(left=0.07, right=0.89, top=0.9, bottom=0.13, hspace=0.25)
    fig.colorbar(im, cax=fig.add_axes([0.92, 0.2, 0.017, 0.6]), label="Activator 0 at 50 tu, native units")
    fig.text(
        0.5,
        0.035,
        "Dashed gray: initial activator core.  White: XV partner at 50 tu.  Red cross: fixed source.\n"
        "One representative fresh realization per program; each starts from its world's identical preparation.",
        ha="center",
        fontsize=10,
    )
    fig.savefig(output, dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    plot(args.source, args.output)
