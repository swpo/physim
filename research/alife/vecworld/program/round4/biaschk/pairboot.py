"""Paired trajectory bootstrap of (local law - global closure) G ceilings, seed means (checker of study `bias`).
usage: python -I -B pairboot.py OUT_DIR RESULT_JSON   (OUT_DIR = jobs/r4-bias-003/out from origin/gpu-jobs)
Both configs are certified on the same 64 trajectories, so the bootstrap resamples trajectories jointly."""
import json
import sys, numpy as np
O = sys.argv[1]
FAMG = ["mean", "persistence", "ar1", "ridge_p1", "ridge_p2", "ridge_p4", "ridge_p8", "knn"]
def items(phi):
    E, OR, IJ = {}, [], []
    for k, h in enumerate("AB"):
        d = np.load(f"{O}/items/{phi}__cert{h}.npz"); nm = [str(n) for n in d["names"]]
        for i, n in enumerate(nm):
            E.setdefault(n, []).append(d["err"][i].astype(float))
        OR.append(d["orac"].astype(float)); IJ.append(d["item_j"] + 32 * k)
    return {n: np.concatenate(v) for n, v in E.items()}, np.concatenate(OR), np.concatenate(IJ)
def ceil(E, Orc, idx):
    V0 = E["mean"][idx].mean(0); Vu = Orc[idx].mean(0)
    Vb = np.min(np.stack([E[n][idx].mean(0) for n in FAMG if n in E]), 0)
    return (V0 - Vb) / (V0 - Vu)
rng = np.random.default_rng(1)
RES = {}
for a, b in [(f"{e}{h}_local_c1", f"{e}{h}_clos_c1") for e in "NL" for h in (0, 4, 8, 16)] + [("N0_pib_c1", "hand_mass_x"), ("N0_clos_c1", "hand_mass_x")]:
    D = {p: [items(p[:-2])] * 2 if p.endswith("_x") else [items(f"{p}_s{s}") for s in (0, 1)] for p in (a, b)}
    ij = D[a][0][2]
    assert all((D[p][s][2] == ij).all() for p in (a, b) for s in (0, 1))
    uj = np.unique(ij)
    f = lambda idx: np.mean([ceil(*D[a][s][:2], idx) for s in (0, 1)], 0) - np.mean([ceil(*D[b][s][:2], idx) for s in (0, 1)], 0)
    full = f(np.arange(len(ij)))
    bs = np.array([f(np.concatenate([np.flatnonzero(ij == u) for u in rng.choice(uj, uj.size)])) for _ in range(400)])
    RES[f"{a} - {b.replace('_x', '')}"] = {"diff": np.round(full, 4).tolist(), "paired_boot_se": np.round(bs.std(0), 4).tolist(),
                           "z": np.round(full / bs.std(0), 1).tolist(), "n_boot": 400, "unit": "trajectory (64)"}
    print(a, "-", b, "diff", np.round(full, 4).tolist(), "paired boot SE", np.round(bs.std(0), 4).tolist(), "z", np.round(full / bs.std(0), 1).tolist())
json.dump(RES, open(sys.argv[2], "w"), indent=1)
