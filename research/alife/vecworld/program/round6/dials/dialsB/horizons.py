"""horizons -- the per-horizon statistics that DECLARED.md 2.4 lists, from the job's per-item scores (numpy, seconds).

    python -B horizons.py GATE_DIR [ANALYSIS_JSON]        (GATE_DIR = jobs/<job>/out/gate with s<seed>_<arm>.npz / .json)

The job's analysis.json holds, per horizon, the pooled share for every policy and the per-seed shares of five
policies; DECLARED.md 2.4 lists the median, the leave-one-seed-out range and the bootstrap per horizon as well
(the job's review noted the gap). This script computes them from the same per-item scores with the same formulas
as s0.analyse (share = sum(L(pub) - L(P)) / sum(L(pub) - L(O)), seeds as clusters, the same bootstrap generator
and draws) and checks its pooled values against analysis.json. Writes results/per_horizon.json. Nothing here
enters the verdict. PILOT values, never to be reused as an exam.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
gd = sys.argv[1]
ana = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else None
HS4 = (4, 8, 16, 32)
POLS = ("G2", "G3", "A_act", "Gstar", "G1", "G4", "H", "pub0")
seeds = sorted({int(f[1:].split("_")[0]) for f in os.listdir(gd) if f.endswith(".npz")})
D = {}
for arm in ("main", "control"):
    for s in seeds:
        z = np.load(os.path.join(gd, f"s{s}_{arm}.npz"))
        D[(arm, s)] = ({k: z[k] for k in z.files}, json.load(open(os.path.join(gd, f"s{s}_{arm}.json"))))
rb = np.random.default_rng(20261111)                     # s0.analyse's generator and draws
boots = rb.integers(0, len(seeds), size=(2000, len(seeds)))


def share(arm, view, pol, cols, drop):
    num, den = [], []
    for s in seeds:
        z, m = D[(arm, s)]
        keep = z["test_state"] != m["heaviest_test_state"] if drop else np.ones(len(z["test_state"]), bool)
        Lp, Lo, Lk = (z[f"L_{view}_{k}"][keep][:, cols].sum(1) for k in ("pub", "O", pol))
        num.append(float((Lp - Lk).sum()))
        den.append(float((Lp - Lo).sum()))
    num, den = np.array(num), np.array(den)
    loo = [float(np.delete(num, j).sum() / np.delete(den, j).sum()) for j in range(len(seeds))]
    bs = np.array([num[b].sum() / den[b].sum() for b in boots])
    return {"closed": float(num.sum() / den.sum()), "per_seed": (num / den).tolist(), "median_seed": float(np.median(num / den)),
            "leave_one_seed_out_range": [min(loo), max(loo)], "bootstrap_seeds_5_95": [float(np.quantile(bs, 0.05)), float(np.quantile(bs, 0.95))],
            "gap_sum": float(den.sum()), "gap_per_seed": den.tolist()}


out = {"PILOT_NEVER_REUSE_AS_EXAM": True, "what": "per-horizon shares of the public-to-oracle gap closed, with the statistics of DECLARED.md 2.4 "
       "(computed after the job from its per-item scores; in no verdict)", "seeds": seeds, "horizons": list(HS4), "arms": {}}
worst = 0.0
for arm in ("main", "control"):
    out["arms"][arm] = {}
    for view in ("focus", "cr"):
        out["arms"][arm][view] = {}
        for drop, name in ((False, "all_start_states"), (True, "heaviest_left_out")):
            blk = {}
            for j, h in enumerate(HS4):
                blk[str(h)] = {p: share(arm, view, p, [j], drop) for p in POLS}
                if ana is not None:
                    for p in POLS:
                        worst = max(worst, abs(blk[str(h)][p]["closed"] - ana["arms"][arm][view][name]["by_horizon"][str(h)][p]))
            out["arms"][arm][view][name] = blk
out["max_abs_difference_from_analysis_json_by_horizon"] = worst if ana is not None else None
os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "results", "per_horizon.json"), "w"), indent=1)
print("wrote results/per_horizon.json; max |difference| from analysis.json's pooled by-horizon shares:", worst if ana is not None else "not checked")
