"""analyse -- selection signal at 128^2 (paired across seeds), the 64^2 per-area mutation test, rough level-2 closure.

    python analyse.py            -> results/analysis.json, results/traces.png

Conventions follow ../vortex_world/analyse.py: windows W1 = ticks [100, 300) (t 500-1495) and W2 = ticks [300, end]
(t 1500-2200 at 128^2); first majority = first tick whose centred 9-tick running mean of s_b exceeds 0.5.
Closure: c(h, w) = (V0 - Ve) / (V0 - Vu) per coordinate (N, s_b); V0 = variance of y(t+h) over branch rows,
Vu = mean within-branch variance over the R fresh-noise replicates (oracle spread), Ve = mean squared error of
an OLS predictor on [1, y(t), ..., y(t-w+1)] (both coordinates), leave-one-seed-out (twins held out together
when arms are pooled). Predictor fits: 'branch' = fitted on other seeds' branch rows (as the round-2 analysis);
'traj' = fitted on other seeds' main trajectories (every tick); 'traj_t' = 'traj' plus the tick as a regressor; 'traj_slope' = 'traj' plus the mean of the last 20 ticks and the slope over the
last 40 ticks of both coordinates (a longer level-2 memory).
Horizons in ticks of 5 time units. Because V0 pools branch points across the rise of s_b (and both arms), c is
also given against the change: cchg = (V_change - Ve) / (V_change - Vu), V_change = variance of y(t+h) - y(t) over
rows (the reference 'persistence plus the mean drift'; 1 = closed, 0 = no better than that reference).
"""
import itertools
import json
import os
import sys

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
OLD = "/home/user/evalwork/vecworld/program/track1/vortex_world"
W1, W2 = (100, 300), 300
HS = (1, 2, 4, 8, 16, 32)
WS = (1, 2, 4)
NAMES = ("N", "s_b")


def load(name):
    p = os.path.join(RES, name)
    return np.load(p) if os.path.exists(p) else None


def first_major(sb):
    rm = np.convolve(sb, np.ones(9) / 9, "valid")
    i = np.flatnonzero(rm > 0.5)
    return int(i[0] + 4) if i.size else None


def paired(d):
    d = np.asarray(d, float)
    n = len(d)
    out = {"n": n, "diffs": np.round(d, 4).tolist(), "mean": float(d.mean()), "n_positive": int((d > 0).sum())}
    if n < 2:
        return out
    se = d.std(ddof=1) / np.sqrt(n)
    tt = d.mean() / se if se > 0 else np.inf
    out.update(sd=float(d.std(ddof=1)), se=float(se), t=float(tt), p_t_two_sided=float(2 * stats.t.sf(abs(tt), n - 1)))
    signs = np.array(list(itertools.product([1.0, -1.0], repeat=n)))
    m = (signs * np.abs(d)).mean(1)
    out["p_signflip_exact_two_sided"] = float(np.mean(np.abs(m) >= abs(d.mean()) - 1e-12))
    out["p_signflip_exact_one_sided"] = float(np.mean(m >= d.mean() - 1e-12))
    try:
        out["p_wilcoxon_exact_two_sided"] = float(stats.wilcoxon(d, alternative="two-sided", method="exact").pvalue)
    except Exception:
        pass
    k = int((d > 0).sum())
    out["p_sign_test_two_sided"] = float(stats.binomtest(k, int((d != 0).sum()), 0.5).pvalue)
    return out


def windows(L2, w1=W1, w2=(W2, None), w3=None, tt=5.0):
    """Per-seed window means of s_b and N (W1 [w1), W2 and W3 inclusive ranges, None = to the end), first majority."""
    sb, n = L2[..., 1].astype(float), L2[..., 0].astype(float)
    T = L2.shape[1] - 1
    out = {"t_end": T * tt, "W1_t": [w1[0] * tt, (w1[1] - 1) * tt],
           "s_b_W1": sb[:, w1[0]:w1[1]].mean(1).round(4).tolist(), "N_W1": n[:, w1[0]:w1[1]].mean(1).round(3).tolist(),
           "first_t_majority_b": [None if f is None else f * tt for f in (first_major(s) for s in sb)],
           "share_b_by_t_mean": {str(int(t * tt)): round(float(sb[:, t].mean()), 4) for t in range(0, T + 1, 25)},
           "N_by_t_mean": {str(int(t * tt)): round(float(n[:, t].mean()), 3) for t in range(0, T + 1, 25)}}
    for nm, w in (("W2", w2), ("W3", w3)):
        if w is None or T <= w[0]:
            continue
        hi = T if w[1] is None else min(w[1], T)
        out[f"{nm}_t"] = [w[0] * tt, hi * tt]
        out[f"s_b_{nm}"] = sb[:, w[0]:hi + 1].mean(1).round(4).tolist()
        out[f"N_{nm}"] = n[:, w[0]:hi + 1].mean(1).round(3).tolist()
        out[f"frac_ticks_majority_{nm}"] = (sb[:, w[0]:hi + 1] > 0.5).mean(1).round(3).tolist()
    for k in ("s_b_W1", "N_W1", "s_b_W2", "N_W2", "s_b_W3", "N_W3"):
        if k in out:
            out[k + "_mean"] = float(np.mean(out[k]))
    return out


def compare(a, b, keys=("s_b_W1", "s_b_W2", "s_b_W3", "N_W1", "N_W2", "N_W3")):
    return {k: paired(np.array(a[k]) - np.array(b[k])) for k in keys if k in a and k in b}


def mutation_times(mut_dt, n_ticks, n_sub=250, dt=0.02, lab_t=300.0):
    """Times of the mutation events in n_ticks ticks, from the accumulated float64 time as in vortex_jax."""
    per, t, out = int(round(mut_dt / dt)), 0.0, []
    for k in range(n_ticks * n_sub):
        if t > lab_t and k % per == 0:
            out.append(round(t, 6))
        t = t + dt
    return out


# ----------------------------------------------------------------------------- closure
LONG = 40                                                         # ticks of history for the 'slope' features


def design(L2, ticks, w, with_t=False):
    """Rows [1, y(t), y(t-1), ..., y(t-w+1)] for ticks, plus the tick (with_t True) or, with_t 'slope', the mean over
    the last LONG/2 ticks and the OLS slope over the last LONG ticks of both coordinates (a longer level-2 memory)."""
    cols = [np.ones(len(ticks))]
    for i in range(w):
        cols += [L2[ticks - i, 0], L2[ticks - i, 1]]
    if with_t is True:
        cols.append(ticks / 100.0)
    elif with_t == "slope":
        lag = np.arange(LONG)
        idx = ticks[:, None] - lag[None, :]
        x = -lag - (-lag).mean()
        for c in (0, 1):
            Y = L2[idx, c]
            cols.append(Y[:, :LONG // 2].mean(1))
            cols.append(((Y - Y.mean(1, keepdims=True)) * x).sum(1) / (x ** 2).sum() * 100.0)
    return np.stack(cols, 1)


def closure(arms, mains, branches, seeds=None, variants=("branch", "traj", "traj_t", "traj_slope")):
    """arms: list of arm names; mains[arm] (S, T+1, 2); branches[arm] {tb: (S, R, HB+1, 2)}."""
    S = mains[arms[0]].shape[0]
    seeds = list(range(S)) if seeds is None else [int(x) for x in seeds]
    rows = []                                                     # (arm, slot j, seed s, tb, r)
    for arm in arms:
        for tb, B in sorted(branches[arm].items()):
            for j, s in enumerate(seeds):
                for r in range(B.shape[1]):
                    rows.append((arm, j, s, tb, r))
    if not rows:
        return None
    grp = np.array([j for (_, j, _, _, _) in rows])               # twins (same slot j) held out together
    keys = sorted({(a, j, tb) for (a, j, _, tb, _) in rows})
    bid = np.array([keys.index((a, j, tb)) for (a, j, _, tb, _) in rows])
    out = {"n_rows": len(rows), "n_branch_points": int(len(keys)), "horizons_ticks": list(HS),
           "horizons_t": [5.0 * h for h in HS]}
    Xrow = {(w, wt): np.stack([design(mains[a][s].astype(float), np.array([tb]), w, wt)[0] for (a, j, s, tb, r) in rows])
            for w in WS for wt in (False, True, "slope")}
    traj = {}
    for a in arms:
        for s in set(seeds):
            Mt = mains[a][s].astype(float)
            for w in WS:
                tk = np.arange(w - 1 + 3, Mt.shape[0])
                traj[(a, s, w, False)] = (tk, design(Mt, tk, w, False))
                traj[(a, s, w, True)] = (tk, design(Mt, tk, w, True))
                tk = np.arange(max(w - 1 + 3, LONG), Mt.shape[0])
                traj[(a, s, w, "slope")] = (tk, design(Mt, tk, w, "slope"))
    for c, name in enumerate(NAMES):
        res = {"V0": [], "Vu": [], "Vu_over_V0": [], "c_persistence": [], "V_change": []}
        for v in variants:
            for w in WS:
                res[f"c_{v}_w{w}"] = []
                res[f"Ve_{v}_w{w}"] = []
                res[f"cchg_{v}_w{w}"] = []
        for h in HS:
            y = np.array([branches[a][tb][s, r, h, c] for (a, j, s, tb, r) in rows], float)
            y0 = np.array([mains[a][s, tb, c] for (a, j, s, tb, r) in rows], float)
            V0 = y.var(ddof=1)
            Vu = float(np.mean([y[bid == b].var(ddof=1) for b in np.unique(bid)]))
            res["V0"].append(float(V0))
            res["Vu"].append(Vu)
            res["Vu_over_V0"].append(Vu / V0)
            res["c_persistence"].append(float((V0 - np.mean((y - y0) ** 2)) / (V0 - Vu)))
            Vc = float((y - y0).var(ddof=1))
            res["V_change"].append(Vc)
            for w in WS:
                for v in variants:
                    wt = {"traj_t": True, "traj_slope": "slope"}.get(v, False)
                    X = Xrow[(w, wt)]
                    err = np.empty_like(y)
                    for g in np.unique(grp):
                        te = grp == g
                        if v == "branch":
                            beta = np.linalg.lstsq(X[~te], y[~te], rcond=None)[0]
                        else:
                            Xs, ys = [], []
                            for a in arms:
                                for j, s in enumerate(seeds):
                                    if j == g:
                                        continue
                                    tk, Xd = traj[(a, s, w, wt)]
                                    keep = tk + h < mains[a].shape[1]
                                    Xs.append(Xd[keep])
                                    ys.append(mains[a][s, tk[keep] + h, c].astype(float))
                            beta = np.linalg.lstsq(np.concatenate(Xs), np.concatenate(ys), rcond=None)[0]
                        err[te] = y[te] - X[te] @ beta
                    Ve = float(np.mean(err ** 2))
                    res[f"c_{v}_w{w}"].append(float((V0 - Ve) / (V0 - Vu)))
                    res[f"Ve_{v}_w{w}"].append(Ve)
                    res[f"cchg_{v}_w{w}"].append(float((Vc - Ve) / (Vc - Vu)))
        out[name] = res
    return out


def closure_boot(arms, mains, branches, n=200, seed=0, key="c_traj_w2"):
    rng = np.random.default_rng(seed)
    S = mains[arms[0]].shape[0]
    cs = []
    for _ in range(n):
        sel = rng.choice(S, S, replace=True)
        if len(np.unique(sel)) < 3:
            continue
        cl = closure(arms, mains, branches, seeds=sel, variants=(key.split('_')[1],))
        cs.append([cl[nm][key] for nm in NAMES])
    cs = np.array(cs)
    return {nm: {"p16": np.percentile(cs[:, i], 16, 0).round(3).tolist(), "p84": np.percentile(cs[:, i], 84, 0).round(3).tolist(),
                 "n_draws": int(len(cs))} for i, nm in enumerate(NAMES)} | {"key": key}


def main():
    out = {}
    M = {a: load(f"main128_{a}.npz") for a in ("sel", "neu")}
    meta = {a: json.load(open(os.path.join(RES, f"main128_{a}.json"))) for a in ("sel", "neu")
            if os.path.exists(os.path.join(RES, f"main128_{a}.json"))}
    out["meta128"] = meta
    if all(v is not None for v in M.values()):
        T = min(M["sel"]["L2"].shape[1], M["neu"]["L2"].shape[1])
        Lfull = {a: M[a]["L2"][:, :T].astype(float) for a in M}
        L2 = {a: Lfull[a][:, :441] for a in M}                          # the design horizon t <= 2200 (closure, W1, W2)
        sel, neu = windows(Lfull["sel"], w2=(300, 440), w3=(441, None)), windows(Lfull["neu"], w2=(300, 440), w3=(441, None))
        out["sel128"], out["neu128"] = sel, neu
        out["paired128"] = compare(sel, neu)
        d = Lfull["sel"][..., 1] - Lfull["neu"][..., 1]
        out["diff_s_b_by_t"] = {str(int(t * 5)): {"mean": round(float(d[:, t].mean()), 4),
                                                  "se": round(float(d[:, t].std(ddof=1) / np.sqrt(d.shape[0])), 4),
                                                  "n_pos": int((d[:, t] > 0).sum())} for t in range(0, T, 50)}
        # earlier seeds: the round-2 pilot (ensemble(1, seed 0), to t 2200) and the checker's seed 1 (to t 1500)
        P = np.load(os.path.join(OLD, "results/pilot_H128.npz"))
        C = np.load(os.path.join(OLD, "checker/seed128_s1.npz"))
        old = {"sel": [P["sel_L2"][0].astype(float), C["sel"].astype(float)],
               "neu": [P["neu_L2"][0].astype(float), C["neu"].astype(float)]}
        ow = {a: [windows(x[None], w2=(300, 440)) for x in old[a]] for a in old}
        out["earlier_seeds128"] = {a: [{k: v[k] for k in ("t_end", "s_b_W1", "s_b_W2", "N_W1", "N_W2", "first_t_majority_b") if k in v}
                                       for v in ow[a]] for a in ow}
        pooled = {}
        for k in ("s_b_W1", "N_W1", "s_b_W2", "N_W2"):
            dd = list(np.array(sel[k]) - np.array(neu[k]))
            for i in range(2):
                if k in ow["sel"][i]:
                    dd.append(ow["sel"][i][k][0] - ow["neu"][i][k][0])
            pooled[k] = paired(dd)
        out["paired128_with_earlier_seeds"] = pooled
        out["mutations128"] = {"times_to_t2200": mutation_times(50.0, 440), "n_to_t2200": len(mutation_times(50.0, 440))}
        # closure
        BR = {a: load(f"branch128_{a}.npz") for a in ("sel", "neu")}
        if all(v is not None for v in BR.values()):
            br = {a: {int(k[1:]): BR[a][k].astype(float) for k in BR[a].files} for a in BR}
            arms_ok = [a for a in ("sel", "neu") if br[a]]
            cl = {a: closure([a], L2, br) for a in arms_ok}
            if len(arms_ok) == 2 and set(br["sel"]) == set(br["neu"]):
                cl["pooled"] = closure(["sel", "neu"], L2, br)
                cl["pooled"]["bootstrap_traj_w2"] = closure_boot(["sel", "neu"], L2, br)
                cl["pooled"]["bootstrap_branch_w2"] = closure_boot(["sel", "neu"], L2, br, key="c_branch_w2")
                cl["pooled"]["bootstrap_cchg_traj_w2"] = closure_boot(["sel", "neu"], L2, br, key="cchg_traj_w2")
            cl["branch_points_ticks"] = {a: sorted(br[a]) for a in arms_ok}
            out["closure128"] = cl
    # the round-2 64^2 closure recomputed with the same code (branch variant = checker's twins-held-out-together numbers)
    P64 = np.load(os.path.join(OLD, "results/pilot_H64.npz"))
    m64 = {a: P64[f"{a}_L2"].astype(float) for a in ("sel", "neu")}
    b64 = {a: {int(t): P64[f"{a}_branch_L2"][i].astype(float) for i, t in enumerate(P64[f"{a}_branch_t"])} for a in ("sel", "neu")}
    out["closure64_recomputed"] = {"pooled": closure(["sel", "neu"], m64, b64), "branch_points_ticks": sorted(b64["sel"]),
                                   "note": "../vortex_world/results/pilot_H64.npz: 4 seeds x 2 arms, branch points every 25 ticks from 75, R = 3"}
    # (b) 64^2: per-area mutation (mut_dt 200) vs per-box (mut_dt 50), same initial conditions and keys per member.
    # Members 0-3: area64_* vs the round-2 pilot_H64 rows; members 4-7 (if run): area64x_* vs box64x_*.
    A = {a: load(f"area64_{a}.npz") for a in ("sel", "neu")}
    if all(v is not None for v in A.values()):
        P64 = np.load(os.path.join(OLD, "results/pilot_H64.npz"))
        area = {a: A[a]["L2"][:, :501].astype(float) for a in A}
        box = {a: P64[f"{a}_L2"][:4, :501].astype(float) for a in ("sel", "neu")}
        b = {"identical_until_tick_members0_3": {a: int(np.argmax(np.any(np.abs(area[a] - box[a]) > 0, -1).any(0))) - 1 for a in area}}
        X = {a: load(f"area64x_{a}.npz") for a in ("sel", "neu")}
        Bx = {a: load(f"box64x_{a}.npz") for a in ("sel", "neu")}
        extra = all(v is not None and v["L2"].shape[1] >= 501 for v in list(X.values()) + list(Bx.values()))
        if extra:
            area = {a: np.concatenate([area[a], X[a]["L2"][:, :501].astype(float)]) for a in area}
            box = {a: np.concatenate([box[a], Bx[a]["L2"][:, :501].astype(float)]) for a in box}
        b["n_seeds"] = int(area["sel"].shape[0])
        b["T_ticks"] = int(area["sel"].shape[1] - 1)
        for name, D in (("per_area", area), ("per_box", box)):
            ws = {a: windows(D[a], w2=(300, 500)) for a in D}
            ws128 = {a: windows(D[a], w2=(300, 440)) for a in D}       # the 128^2 windows (t <= 2200)
            b[name] = {"sel": ws["sel"], "neu": ws["neu"], "paired": compare(ws["sel"], ws["neu"]),
                       "paired_to_t2200": compare(ws128["sel"], ws128["neu"])}
        b["area_minus_box_neutral"] = compare(b["per_area"]["neu"], b["per_box"]["neu"])
        b["area_minus_box_sel"] = compare(b["per_area"]["sel"], b["per_box"]["sel"])
        b["neutral_N_identical_area_vs_box"] = bool(np.array_equal(area["neu"][..., 0], box["neu"][..., 0]))
        mb, ma = mutation_times(50.0, 500), mutation_times(200.0, 500)
        b["mutations"] = {"per_box_mut_dt50": {"n_to_t2500": len(mb), "first_t": mb[0], "last_t": mb[-1]},
                          "per_area_mut_dt200": {"n_to_t2500": len(ma), "times": ma},
                          "per_area_n_to_t2200": len(mutation_times(200.0, 440)),
                          "128_mut_dt50_n_to_t2200": len(mutation_times(50.0, 440))}
        out["area64"] = b
    json.dump(out, open(os.path.join(RES, "analysis.json"), "w"), indent=1)
    plot(out, M, A)
    return out


def plot(out, M, A):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return
    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    if all(v is not None for v in M.values()):
        for a, col in (("sel", "C3"), ("neu", "C0")):
            L2 = M[a]["L2"]
            t = np.arange(L2.shape[1]) * 5
            for s in range(L2.shape[0]):
                ax[0].plot(t, L2[s, :, 1], col, lw=0.7, alpha=0.6, label=a if s == 0 else None)
                ax[1].plot(t, L2[s, :, 0], col, lw=0.7, alpha=0.6, label=a if s == 0 else None)
        ax[0].set_title("128^2: share of kind b (6 seeds)")
        ax[1].set_title("128^2: vortex count N")
        ax[0].axhline(0.5, color="k", lw=0.5)
        ax[0].legend()
    if all(v is not None for v in A.values()):
        P64 = np.load(os.path.join(OLD, "results/pilot_H64.npz"))
        for a, col in (("sel", "C3"), ("neu", "C0")):
            L2 = A[a]["L2"]
            t = np.arange(L2.shape[1]) * 5
            ax[2].plot(t, L2[..., 1].mean(0), col, lw=1.5, label=f"{a} per-area (mut_dt 200)")
            ax[2].plot(t, P64[f"{a}_L2"][:, :L2.shape[1], 1].mean(0), col, lw=1, ls="--", label=f"{a} per-box (mut_dt 50)")
        ax[2].set_title("64^2: mean s_b over seeds 0-3")
        ax[2].axhline(0.5, color="k", lw=0.5)
        ax[2].legend(fontsize=7)
    for x in ax:
        x.set_xlabel("t")
    fig.tight_layout()
    fig.savefig(os.path.join(RES, "traces.png"), dpi=80)


if __name__ == "__main__":
    o = main()
    for k in ("paired128", "paired128_with_earlier_seeds"):
        if k in o:
            for kk, v in o[k].items():
                print(k, kk, {x: (round(y, 4) if isinstance(y, float) else y) for x, y in v.items() if x != "diffs"})
