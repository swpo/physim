"""Readout traces (lab env): truth vs predictors, per case. usage: traces.py"""
import json, sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
OUT = Path(__file__).resolve().parent / "out" / "suite"
TIMES = [0, 2, 5, 8, 10, 12, 15, 20, 22, 25, 30, 35, 40, 45, 50]
FIELDS = ("e", "p", "F", "s")
suite = json.loads((OUT / "suite.json").read_text())
names = ["independent_native", "ablate_kF0", "ablate_d0", "ablate_chi0", "ablate_chis0", "wrong_probe_geometry", "numerical_null"]
cols = dict(zip(names, ["k", "r", "orange", "m", "c", "b", "g"]))


def load(p):
    z = np.load(p); return [z[f"query{i}"] for i in range(3)]


panels = [("device0", 0, 0, "device0 node 0, e"), ("device1", 0, 0, "device1 node 0, e"), ("device0", 2, 0, "device0 node 0, F"),
          ("global", 0, 1, "global var e"), ("global", 3, 0, "global mean s"), ("device1", 3, 5, "device1 node 5, s")]
for case in suite["cases"]:
    cid = case["id"]
    fig, ax = plt.subplots(1, len(panels), figsize=(3.2 * len(panels), 3))
    tr = load(OUT / "truth" / f"{cid}.npz")
    pr = {n: load(OUT / "controls" / cid / f"{n}.npz") for n in names if (OUT / "controls" / cid / f"{n}.npz").exists()}
    for a, (sensor, port, slot, title) in zip(ax, panels):
        qi = ("device0", "device1", "global").index(sensor)
        for n, p in pr.items():
            a.plot(TIMES, p[qi][:, :, port, slot].T, color=cols[n], lw=0.6, alpha=0.6)
        a.plot(TIMES, tr[qi][:, :, port, slot].T, color="k", lw=1.6, ls=":")
        a.set_title(title, fontsize=8); a.set_xlabel("tu", fontsize=7); a.tick_params(labelsize=6)
    ax[0].legend([plt.Line2D([], [], color=cols[n]) for n in pr] + [plt.Line2D([], [], color="k", ls=":", lw=1.6)],
                 list(pr) + ["truth"], fontsize=5)
    fig.suptitle(f"{cid} {'sham' if not case['actions'] else 'fuel pulse'}: 8 members per predictor, truth dotted", fontsize=8)
    fig.tight_layout(); fig.savefig(OUT.parent / f"traces_{cid}.png", dpi=75)
print("ok")
