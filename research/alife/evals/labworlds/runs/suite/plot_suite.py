"""Lab-only figure from cached labeval ensembles: device0 centre node and global mean per port.

usage: plot_suite.py OUT_DIR FIG.png [program ...]
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

out, fig_path = Path(sys.argv[1]), Path(sys.argv[2])
suite = json.loads((out / "suite.json").read_text())
fields = suite["declaration"]["fields"]
times = np.array(suite["cases"][0]["request"]["queries"][0]["t"], float)
want = sys.argv[3:] or ["sham", "pulse_d0_" + fields[0], "probe_shift", "move_during_pulse"]
cases = [c for c in suite["cases"] if c["family"] in want]
controls = [k for k in suite["controls"] if k not in ("initial_persistence",)]
colors = dict(ignore_actions="tab:orange", wrong_probe_geometry="tab:purple", numerical_null="tab:green")
abl = [k for k in controls if k.startswith("ablate_")]
for k, c in zip(abl, ("tab:red", "tab:blue", "tab:brown")):
    colors[k] = c


def load(path):
    with np.load(path) as z:
        return [z["query0"], z["query1"], z["query2"]]


nrow, ncol = len(cases), 2 * len(fields)
fig, axes = plt.subplots(nrow, ncol, figsize=(2.6 * ncol, 2.1 * nrow), squeeze=False)
for r, c in enumerate(cases):
    cid = c["request"]["id"]
    truth = load(out / c["truth"])
    preds = {}
    for k in controls:
        p = out / "controls" / cid / f"{k}.npz"
        if k == "ignore_actions":
            p = out / "ignore_actions.npz"
        if p.exists():
            preds[k] = load(p)
    for j, f in enumerate(fields):
        for col, (qi, slot, lab) in enumerate(((0, 0, "device0 centre"), (2, 0, "global mean"))):
            ax = axes[r, 2 * j + col]
            if "independent_native" in preds:
                for m in preds["independent_native"][qi][:, :, j, slot]:
                    ax.plot(times, m, color="0.6", lw=0.6)
            for k, v in preds.items():
                if k == "independent_native":
                    continue
                ax.plot(times, v[qi][:, :, j, slot].mean(0), color=colors.get(k, "k"), lw=1.0,
                        ls="--" if k == "numerical_null" else "-", label=k if (r == 0 and j == 0 and col == 0) else None)
            for m in truth[qi][:, :, j, slot]:
                ax.plot(times, m, "k.", ms=3)
            ax.set_title(f"{c['family']}\n{lab} {f}", fontsize=7)
            ax.tick_params(labelsize=6)
fig.legend(loc="lower center", ncol=6, fontsize=7)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(fig_path, dpi=90)
print(fig_path)
