"""Independent recomputation of the headline numbers from the saved npz files (not importing analyse.py)."""
import json, sys
import numpy as np
from scipy import stats

R = "/home/user/evalwork/vecworld/program/track1/vortex_world/results/"
D = np.load(R + "pilot_H64.npz")
E = np.load(R + "pilot_H128.npz")
out = {}

# level 2 from level 1 (consistency with the stacked Phi): K slots x 12 features, present = f0 > .5, kind b = f2 > .5
def kinds(L1, K):
    T = L1.reshape(L1.shape[:-1] + (K, 12)).astype(float)
    p = T[..., 0] > 0.5
    n = p.sum(-1)
    nb = (p & (T[..., 2] > 0.5)).sum(-1)
    return np.stack([n, nb / np.maximum(n, 1)], -1)

for nm, F, K in (("64", D, 24), ("128", E, 56)):
    for arm in ("sel", "neu", "sel0"):
        if f"{arm}_L1" in F.files:
            out[f"L2_from_L1_maxdiff_{nm}_{arm}"] = float(np.abs(kinds(F[f"{arm}_L1"], K) - F[f"{arm}_L2"]).max())

def win(F, arm, a, b=None):
    L = F[f"{arm}_L2"].astype(float)
    return L[:, a:b, 1].mean(1), L[:, a:b, 0].mean(1)

for nm, F, late_end in (("64", D, None), ("128", E, None)):
    for arm in ("sel", "neu", "sel0"):
        if f"{arm}_L2" not in F.files:
            continue
        mid_s, mid_n = win(F, arm, 100, 300)
        late_s, late_n = win(F, arm, 300)
        sb = F[f"{arm}_L2"][..., 1].astype(float)
        first = []
        for s in range(sb.shape[0]):
            rm = np.convolve(sb[s], np.ones(9) / 9, "valid")
            i = np.flatnonzero(rm > 0.5)
            first.append(float((i[0] + 4) * 5) if i.size else None)
        out[f"{nm}_{arm}"] = {"mid_sb": mid_s.round(3).tolist(), "mid_sb_mean": round(mid_s.mean(), 3),
                              "late_sb": late_s.round(3).tolist(), "late_sb_mean": round(late_s.mean(), 3),
                              "late_N_mean": round(late_n.mean(), 3), "mid_N_mean": round(mid_n.mean(), 3), "first_t_majority": first}
dm = np.array(out["64_sel"]["mid_sb"]) - np.array(out["64_neu"]["mid_sb"])
dl = np.array(out["64_sel"]["late_sb"]) - np.array(out["64_neu"]["late_sb"])
out["64_paired_mid"] = {"diffs": dm.round(3).tolist(), "mean": round(dm.mean(), 3),
                        "t": round(float(stats.ttest_1samp(dm, 0).statistic), 2),
                        "p_two_sided": round(float(stats.ttest_1samp(dm, 0).pvalue), 3),
                        "sign_test_p_one_sided": 1 / 16}
out["64_paired_late"] = {"diffs": dl.round(3).tolist(), "mean": round(dl.mean(), 3),
                         "p_two_sided": round(float(stats.ttest_1samp(dl, 0).pvalue), 3)}
dN = np.array([win(D, "sel", 300)[1] - win(D, "neu", 300)[1]])[0]
out["64_paired_late_N"] = {"diffs": dN.round(2).tolist(), "p_two_sided": round(float(stats.ttest_1samp(dN, 0).pvalue), 3)}

# closure, pooled sel + neu, w = 2, leave-one-(arm, seed)-out OLS
HS = [1, 2, 4, 8, 16, 32]
def rows(arms):
    X, Y, G, B = [], [], [], []
    b = 0
    for ai, arm in enumerate(arms):
        L2 = D[f"{arm}_L2"].astype(float); BR = D[f"{arm}_branch_L2"].astype(float); tb = D[f"{arm}_branch_t"]
        for p in range(BR.shape[0]):
            for s in range(BR.shape[1]):
                past = np.concatenate([L2[s, tb[p]], L2[s, tb[p] - 1]])
                for r in range(BR.shape[2]):
                    X.append(past); Y.append(BR[p, s, r, HS]); G.append(ai * 10 + s); B.append(b)
                b += 1
    return np.array(X), np.array(Y), np.array(G), np.array(B)

def ceil(X, Y, G, B, group_by_seed_only=False):
    res = {}
    Xw = np.concatenate([np.ones((len(X), 1)), X], 1)
    GG = G % 10 if group_by_seed_only else G
    for c, nm in enumerate(("N", "s_b")):
        cs, cp, vu0 = [], [], []
        for hi in range(len(HS)):
            y = Y[:, hi, c]
            V0 = y.var(ddof=1)
            Vu = np.mean([y[B == b].var(ddof=1) for b in np.unique(B)])
            err = np.empty_like(y)
            for g in np.unique(GG):
                tr, te = GG != g, GG == g
                beta = np.linalg.lstsq(Xw[tr], y[tr], rcond=None)[0]
                err[te] = y[te] - Xw[te] @ beta
            cs.append(round((V0 - np.mean(err ** 2)) / (V0 - Vu), 3))
            cp.append(round((V0 - np.mean((y - X[:, c]) ** 2)) / (V0 - Vu), 3))
            vu0.append(round(Vu / V0, 3))
        res[nm] = {"c_w2": cs, "c_persist": cp, "Vu_over_V0": vu0}
    return res

X, Y, G, B = rows(("sel", "neu"))
out["closure_pooled"] = ceil(X, Y, G, B)
out["closure_pooled_twins_held_out_together"] = ceil(X, Y, G, B, group_by_seed_only=True)
out["closure_n_branch_points"] = int(len(np.unique(B)))
# share of branch rows where s_b is exactly constant over the 32-tick branch (granularity check)
BR = np.concatenate([D["sel_branch_L2"], D["neu_branch_L2"]], 0)
out["s_b_levels_64"] = int(len(np.unique(np.round(D["sel_L2"][..., 1], 4))))
print(json.dumps(out, indent=1))
json.dump(out, open(__file__.replace("recompute.py", "recompute.json"), "w"), indent=1)
