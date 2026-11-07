"""analyse -- selection signal and rough level-2 closure numbers from pilot.py output.

    python analyse.py H [window_start_tick]

Selection: s_b(t) (share of kind-b vortices) per seed and arm; mean over ticks >= window_start (default
300 = t 1500) per seed; first tick at which the 9-tick running mean of s_b exceeds 0.5; vortex count N.

Closure (vw.certificates.closure's definitions, with the oracle replaced by the pilot's branches):
for horizon h and a level-2 window of w past values,
    V0(h)   variance of y(t+h) over all branch rows (branch points x seeds x replicates)
    Vu(h)   mean within-branch variance of y(t+h) over the R fresh-noise replicates (oracle spread)
    Ve(h,w) mean squared error of an OLS predictor of y(t+h) from [1, y(t), ..., y(t-w+1)] (both
            coordinates), fitted leave-one-seed-out (a seed's whole trajectory is held out)
    c(h,w)  = (V0 - Ve) / (V0 - Vu)                     the closure ceiling (1: level 2 is closed)
per coordinate (N, s_b) and per arm (sel, neu) and pooled; persistence y(t+h) = y(t) as a reference.
Uncertainty: seeds resampled with replacement (200 bootstrap draws), 16th-84th percentile.
Writes results/analysis_H{H}.json.
"""
import json
import os
import sys

import _paths
import numpy as np

H = int(sys.argv[1])
WIN = int(sys.argv[2]) if len(sys.argv) > 2 else 300
MID = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (100, 300)      # ticks: the rise
D = np.load(os.path.join(_paths.RESULTS, f"pilot_H{H}.npz"))
META = json.load(open(os.path.join(_paths.RESULTS, f"pilot_H{H}.json")))
TT = META["tick_time"]
HS = [h for h in (1, 2, 4, 8, 16, 32) if h <= META["H_branch"]]
WS = (1, 2, 4)
NAMES = ("N", "s_b")


def selection(arm):
    L2 = D[f"{arm}_L2"].astype(float)                     # (seeds, T+1, 2)
    sb, n = L2[..., 1], L2[..., 0]
    k = np.ones(9) / 9
    first = []
    for s in range(sb.shape[0]):
        rm = np.convolve(sb[s], k, "valid")
        i = np.flatnonzero(rm > 0.5)
        first.append(int(i[0] + 4) if i.size else None)
    late = sb[:, WIN:].mean(1)
    mid = sb[:, MID[0]:MID[1]].mean(1)
    return {"mid_share_b_per_seed": mid.round(3).tolist(), "mid_share_b_mean": float(mid.mean()), "mid_window_t": [MID[0] * TT, MID[1] * TT],
            "mid_count_mean": float(n[:, MID[0]:MID[1]].mean()), "late_count_per_seed": n[:, WIN:].mean(1).round(2).tolist(),
            "late_share_b_per_seed": late.round(3).tolist(), "late_share_b_mean": float(late.mean()),
            "late_window_t": [WIN * TT, (sb.shape[1] - 1) * TT],
            "first_t_majority_b": [None if f is None else f * TT for f in first],
            "count_mean_late": float(n[:, WIN:].mean()), "count_range_late": [float(n[:, WIN:].min()), float(n[:, WIN:].max())],
            "share_b_by_t": {str(int(t * TT)): float(sb[:, t].mean()) for t in range(0, sb.shape[1], 25)},
            "count_by_t": {str(int(t * TT)): float(n[:, t].mean()) for t in range(0, sb.shape[1], 25)}}


def rows(arms, seeds_sel=None):
    """Branch rows: X (n, 2*max(WS)) past window, Y (n, len(HS), 2) futures, g (n,) seed group, b (n,) branch id."""
    X, Y, G, B = [], [], [], []
    bid = 0
    for ai, arm in enumerate(arms):
        L2 = D[f"{arm}_L2"].astype(float)
        BR = D[f"{arm}_branch_L2"].astype(float)          # (P, seeds, R, HB+1, 2)
        tb = D[f"{arm}_branch_t"]
        P, S, R = BR.shape[:3]
        seeds = range(S) if seeds_sel is None else seeds_sel[ai]
        for p in range(P):
            for j, s in enumerate(seeds):
                past = np.concatenate([L2[s, tb[p] - i] for i in range(max(WS))])
                for r in range(R):
                    X.append(past)
                    Y.append(BR[p, s, r, HS])
                    G.append(ai * 1000 + j)
                    B.append(bid)
                bid += 1
    return np.array(X), np.array(Y), np.array(G), np.array(B)


def closure(X, Y, G, B):
    out = {}
    for c, name in enumerate(NAMES):
        res = {"V0": [], "Vu": [], "Ve": {w: [] for w in WS}, "Vpersist": []}
        for hi, h in enumerate(HS):
            y = Y[:, hi, c]
            res["V0"].append(float(y.var(ddof=1)))
            vu = [y[B == b].var(ddof=1) for b in np.unique(B)]
            res["Vu"].append(float(np.mean(vu)))
            res["Vpersist"].append(float(np.mean((y - X[:, c]) ** 2)))
            for w in WS:
                Xw = np.concatenate([np.ones((len(y), 1)), X[:, :2 * w]], 1)
                err = np.empty_like(y)
                for g in np.unique(G):
                    tr, te = G != g, G == g
                    beta = np.linalg.lstsq(Xw[tr], y[tr], rcond=None)[0]
                    err[te] = y[te] - Xw[te] @ beta
                res["Ve"][w].append(float(np.mean(err ** 2)))
        V0, Vu = np.array(res["V0"]), np.array(res["Vu"])
        res["ceiling"] = {w: ((V0 - np.array(res["Ve"][w])) / (V0 - Vu)).tolist() for w in WS}
        res["ceiling_persistence"] = ((V0 - np.array(res["Vpersist"])) / (V0 - Vu)).tolist()
        res["oracle_share_of_V0"] = (Vu / V0).tolist()
        out[name] = res
    return out


def boot(arms, n=200, seed=0):
    rng = np.random.default_rng(seed)
    S = D[f"{arms[0]}_L2"].shape[0]
    cs = []
    for _ in range(n):
        sel = [rng.choice(S, S, replace=True) for _ in arms]
        if any(len(np.unique(s_)) < 2 for s_ in sel):
            continue
        X, Y, G, B = rows(arms, sel)
        cl = closure(X, Y, G, B)
        cs.append([[cl[nm]["ceiling"][2][i] for i in range(len(HS))] for nm in NAMES])
    cs = np.array(cs)
    return {nm: {"p16": np.percentile(cs[:, c], 16, 0).tolist(), "p84": np.percentile(cs[:, c], 84, 0).tolist()}
            for c, nm in enumerate(NAMES)}


def main():
    arms = [a for a in ("sel", "neu") if f"{a}_branch_L2" in D.files]
    out = {"H": H, "horizons_ticks": HS, "horizons_t": [h * TT for h in HS], "windows": list(WS),
           "selection": {a: selection(a) for a in ("sel", "neu", "sel0") if f"{a}_L2" in D.files}}
    if "sel" in out["selection"] and "neu" in out["selection"]:
        d = np.array(out["selection"]["sel"]["late_share_b_per_seed"]) - np.array(out["selection"]["neu"]["late_share_b_per_seed"])
        out["selection"]["sel_minus_neu_per_seed"] = d.round(3).tolist()
        dm = np.array(out["selection"]["sel"]["mid_share_b_per_seed"]) - np.array(out["selection"]["neu"]["mid_share_b_per_seed"])
        out["selection"]["sel_minus_neu_mid_per_seed"] = dm.round(3).tolist()
    clo = {}
    for name, a in ([(x, [x]) for x in arms] + ([("pooled", arms)] if len(arms) > 1 else [])) if arms else []:
        X, Y, G, B = rows(a)
        clo[name] = closure(X, Y, G, B)
        clo[name]["n_branch_points"] = int(len(np.unique(B)))
        clo[name]["n_rows"] = int(len(B))
        clo[name]["bootstrap_w2"] = boot(a)
    if clo:
        out["closure"] = clo
    json.dump(out, open(os.path.join(_paths.RESULTS, f"analysis_H{H}.json"), "w"), indent=1)
    print(json.dumps(out["selection"], indent=1))
    for k, v in clo.items():
        for nm in NAMES:
            print(k, nm, "c(w=2)", np.round(v[nm]["ceiling"][2], 3).tolist(), "persist", np.round(v[nm]["ceiling_persistence"], 3).tolist(),
                  "Vu/V0", np.round(v[nm]["oracle_share_of_V0"], 3).tolist())


if __name__ == "__main__":
    main()
