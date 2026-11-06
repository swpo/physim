"""Render calibration/calibration.png from calibration/results.json (matplotlib only).
Closed forms are lines; estimates are markers with +-1 SE bars, in the same series colour."""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))
W = {w["world"]: w for w in R["worlds"]}
COL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
MRK = ["o", "s", "^", "D"]
INK, MUTED, GRID = "#1f1f1e", "#6b6a63", "#e4e3de"

plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.titlesize": 9.5, "axes.titleweight": "bold",
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.color": GRID, "grid.linewidth": 0.6, "figure.facecolor": "#fcfcfb",
                     "axes.facecolor": "#fcfcfb", "legend.frameon": False, "legend.fontsize": 8})
H = np.array(R["horizons"])
P = list(R["pasts"])
fig, ax = plt.subplots(2, 3, figsize=(9.6, 6.0), dpi=100)


def label_end(a, x, y, text, color):
    a.annotate(text, (x, y), xytext=(4, 0), textcoords="offset points", va="center", fontsize=8, color=INK)


def gap_panel(a, world, title):
    c = W[world]["closure"]
    for i, p in enumerate([1, 2, 16]):
        j = P.index(p)
        cf = np.array(c["cf"]["gap_nats"])[:, j]
        est = np.array(c["est"]["gap_nats"])[:, j]
        se = np.array(c["se"]["gap_nats"])[:, j]
        a.plot(H, cf, color=COL[i], lw=2)
        a.errorbar(H, est, yerr=se, fmt=MRK[i], ms=6, color=COL[i], mec="#fcfcfb", mew=1, capsize=0, lw=1.2,
                   label=f"past p={p}")
    a.set_xscale("log", base=2)
    a.set_xticks(H, [str(h) for h in H])
    a.set_xlabel("horizon tau (ticks)")
    a.set_ylabel("closure gap (nats)")
    a.set_title(title, loc="left")
    a.legend(loc="upper right")


gap_panel(ax[0, 0], "ring", "a  ring: closure gap vs horizon")
gap_panel(ax[0, 1], "random", "b  random: closure gap vs horizon")

# c: leak spectra
a = ax[0, 2]
for i, (world, p) in enumerate([("ring", "p1"), ("ring", "pmax"), ("random", "p1"), ("random", "pmax")]):
    lk = W[world]["leak"]
    cf, est = np.array(lk["cf"][f"mu_{p}"]), np.array(lk["est"][f"mu_{p}"])
    x = np.arange(1, cf.size + 1)
    a.plot(x, cf, color=COL[i], lw=2)
    a.plot(x, est, MRK[i], ms=5, color=COL[i], mec="#fcfcfb", mew=0.8,
           label=f"{world}, p={'1' if p == 'p1' else '16'}")
a.axhline(0.5, color=MUTED, lw=0.8, ls="--")
a.text(24, 0.52, "leak threshold 1/2", ha="right", fontsize=7.5, color=MUTED)
a.set_yscale("log")
a.set_xlabel("level-0 direction (sorted)")
a.set_ylabel("posterior / prior variance mu")
a.set_title("c  leak spectrum (h0 given level-1 past)", loc="left")
a.legend(loc="lower right")

# d: input response singular values (times amplitude b)
a = ax[1, 0]
for i, world in enumerate(["ring", "random", "concat(ring,random)", "stack(ring)"]):
    ic = W[world]["input_capacity"]
    b = 1.0 if world != "random" else 0.5
    cf, est = b * np.array(ic["cf"]["singular_values"]), b * np.array(ic["est"]["singular_values"])
    x = np.arange(1, cf.size + 1)
    a.plot(x, cf, color=COL[i], lw=2)
    a.plot(x, est, MRK[i], ms=4.5, color=COL[i], mec="#fcfcfb", mew=0.6, label=world)
a.axhline(1.0, color=MUTED, lw=0.8, ls="--")
a.text(39, 1.15, "visible: b s >= 1", ha="right", fontsize=7.5, color=MUTED)
a.set_yscale("log")
a.set_ylim(1e-4, 30)
a.set_xlabel("input direction (sorted)")
a.set_ylabel("b x whitened singular value")
a.set_title("d  input visibility at level 1 (L=8, p=8)", loc="left")
a.legend(loc="lower right")

# e: composition, gap at p=16
a = ax[1, 1]
j = P.index(16)
for i, world in enumerate(["ring", "refine(ring,eta=0.0)", "refine(ring,eta=0.3)", "stack(ring)"]):
    c = W[world]["closure"]
    cf = np.array(c["cf"]["gap_nats"])[:, j]
    est, se = np.array(c["est"]["gap_nats"])[:, j], np.array(c["se"]["gap_nats"])[:, j]
    a.plot(H, cf, color=COL[i], lw=2 if i != 1 else 3.5, alpha=1 if i != 1 else 0.45)
    a.errorbar(H * (1.06 if i == 1 else 1), est, yerr=se, fmt=MRK[i], ms=5.5, color=COL[i], mec="#fcfcfb",
               mew=0.8, capsize=0, lw=1.1,
               label={"ring": "ring (level 0, n=24)", "refine(ring,eta=0.0)": "lumpable level -1 (n=48)",
                      "refine(ring,eta=0.3)": "leaky level -1 (eta=0.3)", "stack(ring)": "stack: level 2"}[world])
a.set_xscale("log", base=2)
a.set_xticks(H, [str(h) for h in H])
a.set_xlabel("horizon tau (ticks)")
a.set_ylabel("closure gap at p=16 (nats)")
a.set_title("e  composition: gap of the composed world", loc="left")
a.legend(loc="upper right")

# f: exam
a = ax[1, 2]
e = [x for x in R["exam"] if x["world"] == "ring"][0]
q = np.array(e["queries"])
a.plot(q, e["mse_persistence"], MRK[3], color=COL[3], ms=6, mec="#fcfcfb", label="persistence baseline")
a.plot(q, e["cf_kalman"], color=COL[0], lw=2)
a.errorbar(q, e["mse_kalman"], yerr=e["mse_kalman_se"], fmt=MRK[0], color=COL[0], ms=6, mec="#fcfcfb",
           capsize=0, label="Kalman = level-1 ceiling")
a.plot(q, e["cf_oracle"], color=COL[1], lw=2)
a.plot(q * 1.06, e["oracle"], MRK[1], color=COL[1], ms=5.5, mec="#fcfcfb", label="oracle (h0 known)")
a.set_xscale("log", base=2)
a.set_xticks(q, [str(x) for x in q])
a.set_xlabel("query horizon (ticks after prefix)")
a.set_ylabel("expected squared error")
a.set_title("f  exam harness, ring (400 items)", loc="left")
a.legend(loc="upper left")

fig.suptitle("VW-0 certificate estimators vs closed forms on linear-Gaussian worlds "
             "(lines: closed form; markers: estimate +- 1 SE)", fontsize=10, color=INK, x=0.01, ha="left")
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(os.path.join(HERE, "calibration.png"), facecolor=fig.get_facecolor())
print("wrote", os.path.join(HERE, "calibration.png"))
