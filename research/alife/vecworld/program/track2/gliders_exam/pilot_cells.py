"""pilot_cells -- per-cell paired OES gaps (bootstrap over the 32 pooled items) from results/pilot_scores.npz."""
import json

import numpy as np

z = np.load("results/pilot_scores.npz", allow_pickle=True)["scores"].item()
ks = sorted(z)
S = {"climatology": np.concatenate([z[k]["refs"]["climatology"] for k in ks]),
     "oracle": np.concatenate([z[k]["refs"]["oracle"] for k in ks])}
for nm in z[ks[0]]["scored"]:
    S[nm] = np.concatenate([z[k]["scored"][nm] for k in ks])
cells = json.load(open("results/pilot.json"))["per_truth"]["0"]["cells"]
rng = np.random.default_rng(0)
n = S["oracle"].shape[0]
idx = rng.integers(0, n, (4000, n))


def oes(M, i):
    m = {k: v[i].mean(-2) for k, v in S.items()}
    return (m["climatology"] - m[M]) / (m["climatology"] - m["oracle"])


out = {"n_items": n, "cells": cells, "pairs": {}}
for a, b in (("plugin_true", "plugin_prior"), ("ridge_true", "ridge_prior"), ("ridge_true", "ridge_true_noact")):
    pt = oes(a, slice(None)) - oes(b, slice(None))
    bt = oes(a, idx) - oes(b, idx)
    se = bt.std(0, ddof=1)
    out["pairs"][f"{a}-{b}"] = {"gap": pt.tolist(), "se": se.tolist(), "z": (pt / se).tolist()}
    print(a, b, [f"{g:+.3f}({zz:.1f})" for g, zz in zip(pt, pt / se)])
json.dump(out, open("results/pilot_cells.json", "w"), indent=1)
