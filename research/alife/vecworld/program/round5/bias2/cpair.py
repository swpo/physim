"""cpair -- paired trajectory bootstrap of closure-ceiling differences between two Phi (study `bias2`; local, numpy).

usage: python -B cpair.py ITEMS_DIR OUT_JSON A=B [A=B ...]
ITEMS_DIR holds the per-item errors written by ccert.py (origin/gpu-jobs:jobs/<job>/out/<world>/items/*.npz:
names, err (predictor, item, horizon), orac (item, horizon), item_j). A and B are Phi stems without the seed and
half suffixes: a config name (both seeds s0, s1 are averaged) or `hand_<design>`. Both sides are certified on the
same test states and fresh-noise branches of the same trajectories, so the trajectories (2 x J_CERT, both
certification halves) are resampled jointly: 400 resamples, the same indices for both sides.
For each pair: ceiling_G of A and of B (family G = lphi.FAM_G, best predictor per horizon chosen inside every
resample), the difference A - B, its bootstrap SE and z, per horizon (1, 2, 4, 8, 16).
This is round 4's checker's test (round4/biaschk/pairboot.py) applied to every comparison the report words as
"more / less closed than".
"""
import json
import os
import sys

import numpy as np

FAM_G = ["mean", "persistence", "ar1", "ridge_p1", "ridge_p2", "ridge_p4", "ridge_p8", "knn"]
HZ = [1, 2, 4, 8, 16]


def load(items_dir, stem):
    """One Phi (one seed or a hand design): errors pooled over the two certification halves."""
    out = []
    off = 0
    for half in ("A", "B"):
        d = np.load(os.path.join(items_dir, f"{stem}__cert{half}.npz"))
        names = [str(n) for n in d["names"]]
        err = {n: d["err"][i].astype(np.float64) for i, n in enumerate(names)}
        ij = d["item_j"].astype(int)
        out.append((err, d["orac"].astype(np.float64), ij + off))
        off += int(ij.max()) + 1
    names = [n for n in FAM_G if all(n in o[0] for o in out)]
    return ({n: np.concatenate([o[0][n] for o in out]) for n in names}, np.concatenate([o[1] for o in out]),
            np.concatenate([o[2] for o in out]))


def phis(items_dir, name):
    if name.startswith("hand_"):
        return [load(items_dir, name)]
    return [load(items_dir, f"{name}_s{s}") for s in (0, 1) if os.path.exists(os.path.join(items_dir, f"{name}_s{s}__certA.npz"))]


def ceiling(P, idx):
    err, orac, _ = P
    V0 = err["mean"][idx].mean(0)
    Vu = orac[idx].mean(0)
    Vb = np.stack([err[n][idx].mean(0) for n in err]).min(0)
    return (V0 - Vb) / (V0 - Vu)


def mean_ceiling(Ps, idx):
    return np.mean([ceiling(P, idx) for P in Ps], 0)


def pair(items_dir, a, b, n_boot=400, seed=0):
    PA, PB = phis(items_dir, a), phis(items_dir, b)
    ij = PA[0][2]
    for P in PA + PB:
        assert np.array_equal(P[2], ij), "the two sides are not certified on the same items"
    uj = np.unique(ij)
    rng = np.random.default_rng(seed)
    full = np.arange(len(ij))
    ca, cb = mean_ceiling(PA, full), mean_ceiling(PB, full)
    where = {u: np.flatnonzero(ij == u) for u in uj}
    D = []
    for _ in range(n_boot):
        idx = np.concatenate([where[u] for u in rng.choice(uj, uj.size, replace=True)])
        D.append(mean_ceiling(PA, idx) - mean_ceiling(PB, idx))
    se = np.std(D, 0)
    return {"A": a, "B": b, "n_seeds": [len(PA), len(PB)], "n_trajectories": int(uj.size), "n_items": int(len(ij)),
            "horizons": HZ, "ceiling_A": ca.tolist(), "ceiling_B": cb.tolist(), "diff": (ca - cb).tolist(),
            "se": se.tolist(), "z": ((ca - cb) / np.maximum(se, 1e-12)).tolist()}


if __name__ == "__main__":
    items_dir, out_path = sys.argv[1], sys.argv[2]
    res = {}
    for arg in sys.argv[3:]:
        a, b = arg.split("=")
        try:
            r = pair(items_dir, a, b)
        except (FileNotFoundError, AssertionError) as exc:
            print(f"{a} vs {b}: skipped ({exc})")
            continue
        res[f"{a}__minus__{b}"] = r
        print(f"{a} - {b}: diff {np.round(r['diff'], 3).tolist()} z {np.round(r['z'], 1).tolist()}")
    json.dump(res, open(out_path, "w"), indent=1)
