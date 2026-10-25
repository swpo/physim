"""Random births at the deepest strict generation (sibling-safe fissions, lineage.py rules), from an
ecotrack run saved with save=1.  usage: python strip.py S led/run (reads run.json, run_frames.npz/json)

Each row: one fission event. Columns: the parent 2 t before, then the prey field at +0, +10, +20, +40,
+100 t, centred on the parent; each daughter lineage (all descendants) is outlined in its own colour.
"""
import json
import sys
from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage

S, run = float(sys.argv[1]), sys.argv[2]
d = json.load(open(run + ".json"))
fr = np.load(run + "_frames.npz")["prey"].astype(np.float32)
tf = {int(k): v for k, v in json.load(open(run + "_frames.json")).items()}
every = d["every"]
T = d["T"]
tr = {t[0]: dict(birth=t[1], end=t[2], born=t[3], endby=t[4], parents=t[6]) for t in d["tracks"]}
kids = defaultdict(list)
for tid, x in tr.items():
    for p in x["parents"]:
        kids[p].append(tid)


def desc(k, tmax):
    out, st = set(), [k]
    while st:
        u = st.pop()
        if u in out:
            continue
        out.add(u)
        st += [v for v in kids[u] if tr[v]["birth"] <= tmax]
    return out


safe, ev_of = [], {}
for i, (t, parent, ks, pm) in enumerate(d["events"]):
    if t > T - S:
        safe.append(None)
        continue
    D = [desc(k, t + S) for k in ks]
    alive = sum(1 for Dk in D if any(tr[u]["end"] >= t + S or tr[u]["endby"] == "alive" for u in Dk))
    co = any(D[a] & D[b] for a in range(len(D)) for b in range(a + 1, len(D)))
    safe.append((not co) and alive >= 2)
    for k in ks:
        ev_of[k] = i
gen = {}
for tid in sorted(tr, key=lambda u: (tr[u]["birth"], u)):
    x = tr[tid]
    if x["born"] == "fission":
        gen[tid] = gen.get(x["parents"][0], 0) + (1 if tid in ev_of and safe[ev_of[tid]] else 0)
    else:
        gen[tid] = 0
G = max(gen[k] for k in ev_of if safe[ev_of[k]])
if len(sys.argv) > 3:  # optional: random births at generation >= this value instead of the deepest only
    G = int(sys.argv[3])
cand = sorted({ev_of[k] for k in ev_of if safe[ev_of[k]] and gen[k] >= G})
rng = np.random.default_rng(1)
pick = sorted(rng.choice(cand, min(5, len(cand)), replace=False))
H, W = fr.shape[1:]
R = 32
offs = [-2, 0, 10, 20, 40, 100]
fig, ax = plt.subplots(len(pick), len(offs), figsize=(2 * len(offs), 2 * len(pick)))
ax = np.atleast_2d(ax)
cols = ["#ff4040", "#40a0ff", "#ffd000"]


def lab_at(fi):
    m = fr[fi]
    lab, n = ndimage.label(m > 0.35)
    for a, b in ((lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])):
        for x, y in zip(a, b):
            if x and y and x != y:
                lab[lab == y] = x
    ids = np.unique(lab)
    ids = ids[ids > 0]
    areas = ndimage.sum(np.ones_like(m), lab, ids) if len(ids) else []
    out = np.zeros_like(lab)
    j = 0
    for i, a in zip(ids, areas):
        if a >= 12:
            j += 1
            out[lab == i] = j
    return out


for r, i in enumerate(pick):
    t, parent, ks, pm = d["events"][i]
    f0 = int(round(t / every))
    pf, pj = tf[parent][-1]
    L = lab_at(pf)
    yy, xx = np.nonzero(L == pj)
    cy, cx = int(np.median(yy)), int(np.median(xx))
    for c, o in enumerate(offs):
        fi = min(max(f0 + int(round(o / every)), 0), len(fr) - 1)
        img = np.roll(np.roll(fr[fi], H // 2 - cy, 0), W // 2 - cx, 1)[H // 2 - R:H // 2 + R, W // 2 - R:W // 2 + R]
        a = ax[r, c]
        a.imshow(img, cmap="gray", vmin=0, vmax=1.2)
        Lf = np.roll(np.roll(lab_at(fi), H // 2 - cy, 0), W // 2 - cx, 1)[H // 2 - R:H // 2 + R, W // 2 - R:W // 2 + R]
        for q, k in enumerate(ks[:3]):
            Dk = desc(k, t + o)
            js = [j for u in Dk for (ff, j) in tf[u] if ff == fi]
            if js:
                a.contour(np.isin(Lf, js), [0.5], colors=cols[q], linewidths=1.2)
        a.set_title(f"ev{i} gen{G} {'+' if o >= 0 else ''}{o} t" if c else f"parent t={t - 2:.0f}", fontsize=7)
        a.axis("off")
plt.suptitle(f"{run}: random sibling-safe fissions at strict generation {'>=' if len(sys.argv) > 3 else ''}{G} ({len(cand)} events); "
             "daughter lineages outlined red/blue", fontsize=8)
plt.tight_layout()
plt.savefig(run + f"_gen{G}{'plus' if len(sys.argv) > 3 else ''}_strip.png", dpi=70)
print(G, len(cand), pick)
