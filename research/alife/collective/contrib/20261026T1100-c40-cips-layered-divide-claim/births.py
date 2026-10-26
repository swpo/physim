"""Strips of the births at the deepest generation (from the labkit pack's frames.npz and metrics.json).
usage: python births.py pack/seed0 out.png"""
import sys, json, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
pk, out = sys.argv[1], sys.argv[2]
m = json.load(open(pk + "/metrics.json")); M = np.load(pk + "/frames.npz")["matter"]
dtf = m["steps_per_frame"] * m["dt"]
gen = {}
ev = sorted(m["persistent_splits"], key=lambda e: e["frame"])
for e in ev:
    g = gen.get(e["parent"], 0) + 1
    for c in e["children"]: gen[c] = g
for e in ev: e["gen"] = gen[e["children"][0]]
G = max(e["gen"] for e in ev)
deep = [e for e in ev if e["gen"] == G]
H, W = M.shape[1:]
rows = []
for e in deep:
    k = e["frame"]; kb = max(k - 8, 0)
    # parent = component at frame kb that overlaps 2 components at frame k+2
    la, na = ndimage.label(M[kb] > 0.5); lb, nb = ndimage.label(M[min(k + 2, len(M) - 1)] > 0.5)
    best = None
    for i in range(1, na + 1):
        ov = set(np.unique(lb[la == i])) - {0}
        if len(ov) >= 2: best = i; break
    if best is None: continue
    cy, cx = ndimage.center_of_mass(la == best)
    rows.append((e, int(cy), int(cx), kb))
ks = [-8, -4, -2, 0, 2, 6, 12]
fig, ax = plt.subplots(max(len(rows), 1), len(ks), figsize=(1.6 * len(ks), 1.7 * max(len(rows), 1)), squeeze=False)
for r, (e, cy, cx, kb) in enumerate(rows):
    for j, dk in enumerate(ks):
        k = min(max(e["frame"] + dk, 0), len(M) - 1)
        im = np.roll(np.roll(M[k], H // 2 - cy, 0), W // 2 - cx, 1)[H // 2 - 28:H // 2 + 28, W // 2 - 28:W // 2 + 28]
        ax[r, j].imshow(im, cmap="magma", vmin=0, vmax=1); ax[r, j].axis("off")
        ax[r, j].set_title(f"t={k*dtf:.0f}" + (f" gen{e['gen']} parent {e['parent']}" if j == 0 else ""), fontsize=6)
fig.suptitle(f"{pk}: every birth at the deepest generation ({G}), 56x56 px crops centred on the parent", fontsize=7)
fig.tight_layout(); fig.savefig(out, dpi=80)
print(G, len(deep), len(rows))
