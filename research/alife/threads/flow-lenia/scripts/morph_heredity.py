"""Do divisions preserve body composition? Run a 2-channel world, segment every frame, find clean
divisions and compare the A0 fraction of parent and daughters.

python threads/flow-lenia/scripts/morph_heredity.py WORLD OUT --steps 6000 --every 10 --seed 0
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit.world import load_world  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("world"); ap.add_argument("out")
ap.add_argument("--steps", type=int, default=6000)
ap.add_argument("--every", type=int, default=10)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--thr", type=float, default=0.15)
ap.add_argument("--live", type=int, default=10)
a = ap.parse_args()
W = load_world(a.world)
s = W.init(a.seed, tuple(W.META["size"]))
labs, fr = [], []
for t in range(a.steps + 1):
    if t:
        s = W.step(s)
    if t % a.every == 0:
        A = s["A"]
        m = A.sum(0)
        lab, n = ndimage.label(ndimage.gaussian_filter(m, 1, mode="wrap") > a.thr)
        idx = np.arange(1, n + 1)
        tot = ndimage.sum(m, lab, idx) if n else np.zeros(0)
        a0 = ndimage.sum(A[0], lab, idx) if n else np.zeros(0)
        area = ndimage.sum(np.ones_like(m), lab, idx) if n else np.zeros(0)
        labs.append(lab); fr.append({"f0": (a0 / np.maximum(tot, 1e-9)), "mass": tot, "area": area})
T = len(labs)
fwd, bwd = [], []
for f in range(T - 1):
    A_, B_ = labs[f], labs[f + 1]
    mk = (A_ > 0) & (B_ > 0)
    F, Bk = {}, {}
    for i, j in set(zip(A_[mk].tolist(), B_[mk].tolist())):
        F.setdefault(i, set()).add(j); Bk.setdefault(j, set()).add(i)
    fwd.append(F); bwd.append(Bk)


def follow(f, j):
    path = [(f, j)]
    while f < T - 1:
        nx = fwd[f].get(j, set())
        if len(nx) != 1:
            break
        k = next(iter(nx))
        if len(bwd[f].get(k, set())) != 1:
            break
        f, j = f + 1, k
        path.append((f, j))
    return path


def comp(f, j, area_min=1):
    return float(fr[f]["f0"][j - 1]) if fr[f]["area"][j - 1] >= area_min else None


rows = []
for f in range(T - 1):
    for i, ch in fwd[f].items():
        if len(ch) < 2 or any(len(bwd[f][c]) != 1 for c in ch):
            continue
        paths = [follow(f + 1, c) for c in ch]
        if not all(len(p) >= a.live for p in paths):
            continue
        # parent composition averaged over the 5 frames before, daughters over frames +5..+10
        back = [f]
        g, j = f, i
        for _ in range(5):
            if g == 0 or len(bwd[g - 1].get(j, set())) != 1:
                break
            j = next(iter(bwd[g - 1][j])); g -= 1; back.append(g)
        pc = comp(f, i)
        dc = [np.mean([comp(*p[k]) for k in range(5, min(10, len(p)))]) for p in paths]
        rows.append({"frame": f, "parent_f0": pc, "daughters_f0": [float(x) for x in dc],
                     "parent_mass": float(fr[f]["mass"][i - 1])})
Path(a.out + ".json").write_text(json.dumps(rows))
pf = np.array([r["parent_f0"] for r in rows for _ in r["daughters_f0"]])
df = np.array([d for r in rows for d in r["daughters_f0"]])
print(f"{len(rows)} clean divisions, {len(df)} daughters")
if len(df) > 2:
    print("corr(parent A0 fraction, daughter A0 fraction) = %.2f" % np.corrcoef(pf, df)[0, 1])
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.8))
    ax[0].scatter(pf, df, s=14); ax[0].plot([0, 1], [0, 1], "k:", lw=0.8)
    ax[0].set_xlabel("parent A0 fraction (orange)"); ax[0].set_ylabel("daughter A0 fraction")
    ax[0].set_title(f"{len(rows)} clean divisions, r={np.corrcoef(pf, df)[0, 1]:.2f}")
    allf = np.concatenate([x["f0"][x["area"] >= 20] for x in fr[T // 2:]])
    ax[1].hist(allf, 40); ax[1].set_xlabel("A0 fraction of bodies (2nd half of run)"); ax[1].set_title("body composition")
    fig.suptitle(Path(a.world).parent.name); fig.tight_layout(); fig.savefig(a.out + ".png", dpi=80)
