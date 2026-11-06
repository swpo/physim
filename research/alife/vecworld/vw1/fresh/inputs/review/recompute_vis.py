"""Checker: independent recomputation of the (a)/(d) headline numbers from results/vis/state_*.npz."""
import glob
import json

import numpy as np

R0 = "/home/user/evalwork/vecworld/vw1/fresh/inputs/results"
files = sorted(glob.glob(f"{R0}/vis/state_*.npz"))
D = [dict(np.load(f)) for f in files]
names = [str(n) for n in D[0]["names"]]
conds = [str(c) for c in D[0]["conds"]]
assert all([str(n) for n in d["names"]] == names for d in D)
R = 6
print("n states", len(D), "B", len(names), "names[:8]", names[:8], "null", max(float(d["null_x"]) for d in D),
      max(float(d["null_y"]) for d in D))
print("adm", D[0]["adm"], [bool(d["adm"].tolist() == D[0]["adm"].tolist()) for d in D].count(True))
Y = np.stack([d["Y"].astype(np.float64) for d in D])          # (S, B, 33, 336)
print("Y shape", Y.shape)
tw = [names.index(f"twin_{r}") for r in range(R)]
# independent check of the null: null member vs twin_0 in the level-1 record
nl = names.index("null")
print("null vs twin_0 L1 max |diff|", np.abs(Y[:, nl] - Y[:, tw[0]]).max())
sd = Y[:, tw].reshape(-1, 336).std(0)
views = {"coarse": np.arange(0, 192), "objects": np.arange(192, 336)}
TAUS = [1, 2, 4, 8, 16, 32]
out = {}
for v, ix in views.items():
    s_ = sd[ix]
    keep = ix[s_ > 1e-6 * s_.max()]
    Z = Y[..., keep] / sd[keep]
    T = Z[:, tw]                                   # (S, R, 33, q)
    Vu = T.var(1, ddof=1).mean(-1)                 # (S, 33)
    out[v] = {"n_keep": int(keep.size)}
    for c in conds:
        ci = [names.index(f"{c}_{r}") for r in range(R)]
        Dl = Z[:, ci] - T                          # (S, R, 33, q)
        m = Dl.mean(1)
        vm = Dl.var(1, ddof=1) / R
        snr = (m ** 2 - vm).mean(-1) / Vu         # (S, 33)
        tsnr = (Dl ** 2).mean(-1).mean(1) / Vu
        cross = np.array([next((t for t in range(1, 33) if tsnr[i, t] >= 1), 99) for i in range(len(D))])
        out[v][c] = {"median": {t: float(np.median(snr[:, t])) for t in TAUS},
                     "worst": {t: float(snr[:, t].max()) for t in TAUS},
                     "n_ge1": {t: int((snr[:, t] >= 1).sum()) for t in TAUS},
                     "cross_median": float(np.median(cross)), "n_cross_by_32": int((cross <= 32).sum()),
                     "twin_snr_median_32": float(np.median(tsnr[:, 32]))}
blind = ["rand_x1", "rand_x8"]
deflt = ["rand_x1", "rand_x8", "body_x1", "body_x8same", "empty_x1"]
mxb = max((out[v][c]["median"][t], v, c, t) for v in views for c in blind for t in TAUS)
wb = max((out[v][c]["worst"][t], v, c, t) for v in views for c in blind for t in TAUS)
nb = max(out[v][c]["n_ge1"][t] for v in views for c in blind for t in TAUS)
mxd = max((out[v][c]["median"][t], v, c, t) for v in views for c in deflt for t in TAUS)
wd = max((out[v][c]["worst"][t], v, c, t) for v in views for c in deflt for t in TAUS)
nd = {(v, c, t): out[v][c]["n_ge1"][t] for v in views for c in deflt for t in TAUS if out[v][c]["n_ge1"][t] > 0}
print("blind max median", mxb, "blind worst", wb, "blind n>=1 max", nb)
print("default max median", mxd, "default worst", wd)
print("default n>=1 entries", nd)
print("k32", {v: (out[v]["k32_x1"]["median"][1], out[v]["k32_x1"]["n_ge1"][1]) for v in views})
for v in views:
    print(v, "empty_x1 cross median", out[v]["empty_x1"]["cross_median"], "n by 32", out[v]["empty_x1"]["n_cross_by_32"],
          "twin snr med @32", out[v]["empty_x1"]["twin_snr_median_32"])
    print(v, "rand_x1 cross median", out[v]["rand_x1"]["cross_median"], "n by 32", out[v]["rand_x1"]["n_cross_by_32"])
    print(v, "body_x1 cross median", out[v]["body_x1"]["cross_median"], "n by 32", out[v]["body_x1"]["n_cross_by_32"])
# moved matter
for c in conds:
    ci = [names.index(f"{c}_{r}") for r in range(R)]
    a = np.array([d["moved"][ci].sum(1) for d in D])
    print("moved", c, "median", np.median(a), "mean", a.mean())
rm = np.concatenate([d["rand_moved"] for d in D])
print("random admissible: n", rm.size, "mean", rm.mean(), "se", rm.std(ddof=1) / np.sqrt(rm.size), "median", np.median(rm),
      "frac empty", np.concatenate([d["rand_empty_frac"] for d in D]).mean(),
      "frac body", np.concatenate([d["rand_body_frac"] for d in D]).mean())
# per-state worst blind states
for v in views:
    for c in blind:
        print(v, c, "worst by tau", {t: round(out[v][c]["worst"][t], 3) for t in TAUS})
json.dump(out, open("/home/user/evalwork/vecworld/vw1/fresh/inputs/review/recompute_vis.json", "w"), indent=1)
