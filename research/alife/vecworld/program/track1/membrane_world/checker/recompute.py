"""Checker: recompute headline numbers from saved outputs, independently of analyse.py where practical."""
import json, sys
import numpy as np
from scipy import stats
R = "/home/user/evalwork/vecworld/program/track1/membrane_world/results"
OUT = {}
NF, K, TT, W0, W1 = 12, 48, 10.0, 100, 600
D = {a: np.load(f"{R}/pilot_{a}.npz") for a in ("main", "dt025", "dt1", "det", "sa003", "sa03")}

def unpack(a):
    L1 = D[a]["L1"].astype(np.float64)
    tab = L1[..., :K * NF].reshape(L1.shape[0], L1.shape[1], K, NF)
    pres = tab[..., 0] > 0.5
    return pres, np.where(pres, tab[..., 1], 0.0), L1[..., K * NF:], tab

# --- level 1 basics (main)
pres, mass, glob, tab = unpack("main")
N = pres.sum(-1)
sl = slice(W0, W1)
ms = mass[:, sl].sum(-1) / np.maximum(N[:, sl], 1)
newc = pres[:, 1:] & ~pres[:, :-1]
big = newc & (mass[:, 1:] >= 50)
ev = D["main"]["ev"][..., 0][:, 1:]
bw = big[:, W0 - 1:W1 - 1]  # transitions t-1 -> t for t in [W0, W1)
evw = ev[:, W0 - 1:W1 - 1]
cell_time = N[:, W0:W1].sum(1) * TT
OUT["L1"] = {"N_mean": float(N[:, sl].mean()), "N_min_max": [int(N[:, sl].min()), int(N[:, sl].max())],
             "mean_size": float(ms.mean()),
             "div_ge50_per_cell_per_100t_seedmean": float((100 * big[:, W0:W1].sum((1, 2)) / cell_time).mean()),
             "new_slots_ge50_in_window_by_event": {str(e): int((bw & (evw == e)).sum()) for e in np.unique(evw[bw])},
             "new_slots_lt50_by_event": {str(e): int(((newc[:, W0 - 1:W1 - 1] & ~bw) & (evw == e)).sum()) for e in (1, 2)}}

# --- closure (main), independent + extra predictors
L2 = D["main"]["L2"].astype(np.float64)
BR = D["main"]["branch_L2"].astype(np.float64)  # (P,S,R,HB+1,3)
tb = D["main"]["branch_t"]
P, S, Rr = BR.shape[:3]
HS = (1, 2, 4, 8, 16, 32)
edges = [12, 50, 100, 150, 200, 300, 400, 600, 1e9]

def l1feat(s, t):
    m = mass[s, t][pres[s, t]]
    return np.array([((m >= lo) & (m < hi)).sum() for lo, hi in zip(edges[:-1], edges[1:])] + [m.sum(), m.max() if m.size else 0, (m ** 2).sum() / 1e3])

newbig = np.concatenate([np.zeros((S, 1, ), bool).reshape(S, 1) if False else np.zeros((S, 1)), big.sum(-1)], 1)  # (S, T) divisions at tick t

rows = []
for p in range(P):
    for s in range(S):
        t = tb[p]
        y0, y1 = L2[s, t], L2[s, t - 1]
        f1 = l1feat(s, t)
        # divisions in the level-2 window that leave it by t+h: ticks t-49 .. t-50+h
        dout = [newbig[s, t - 49:t - 49 + h].sum() if h <= 50 else np.nan for h in HS]
        for r in range(Rr):
            rows.append((s, p * S + s, y0, y1, f1, dout, BR[p, s, r, list(HS)]))
G = np.array([r[0] for r in rows]); B = np.array([r[1] for r in rows])
Y0 = np.array([r[2] for r in rows]); Y1 = np.array([r[3] for r in rows]); F1 = np.array([r[4] for r in rows])
DO = np.array([r[5] for r in rows]); Y = np.array([r[6] for r in rows])

def loso(X, y):
    X = np.concatenate([np.ones((len(y), 1)), X], 1)
    err = np.empty_like(y)
    for g in np.unique(G):
        tr, te = G != g, G == g
        mu, sd = X[tr].mean(0), X[tr].std(0); sd[sd == 0] = 1; mu[0] = 0; sd[0] = 1
        Xt, Xe = (X[tr] - mu) / sd, (X[te] - mu) / sd
        lam = 1e-6 * len(Xt)
        beta = np.linalg.solve(Xt.T @ Xt + lam * np.eye(X.shape[1]), Xt.T @ y[tr])
        err[te] = y[te] - Xe @ beta
    return float(np.mean(err ** 2))

def quad(Z):
    i, j = np.triu_indices(Z.shape[1])
    return np.concatenate([Z, Z[:, i] * Z[:, j]], 1)

names = ("N", "mean_size", "div_rate")
cl = {}
for c, nm in enumerate(names):
    res = {k: [] for k in ("lin_w2", "quad_w2", "lin_w2_plus_L1", "quad_w2_plus_L1", "lin_w2_plus_window_exit", "lin_w2_plus_L1_plus_exit", "oracle_share")}
    for hi, h in enumerate(HS):
        y = Y[:, hi, c]
        V0 = y.var(ddof=1)
        Vu = np.mean([y[B == b].var(ddof=1) for b in np.unique(B)])
        base = np.concatenate([Y0, Y1], 1)
        cands = {"lin_w2": base, "quad_w2": np.concatenate([quad(Y0), Y1], 1),
                 "lin_w2_plus_L1": np.concatenate([base, F1], 1),
                 "quad_w2_plus_L1": np.concatenate([quad(np.concatenate([Y0, F1[:, :8]], 1)), Y1, F1[:, 8:]], 1),
                 "lin_w2_plus_window_exit": np.concatenate([base, DO[:, [hi]]], 1),
                 "lin_w2_plus_L1_plus_exit": np.concatenate([base, F1, DO[:, [hi]]], 1)}
        for k, X in cands.items():
            res[k].append(round((V0 - loso(X, y)) / (V0 - Vu), 4))
        res["oracle_share"].append(round(Vu / V0, 4))
    cl[nm] = res
OUT["closure_check"] = cl

# --- dt / noise checks: all statistics, multiple-comparison view
def per_seed(a):
    pres, mass, glob, tab = unpack(a)
    N = pres.sum(-1); out = {}
    out["N"] = N[:, sl].mean(1)
    out["mean_size"] = (mass[:, sl].sum(-1) / np.maximum(N[:, sl], 1)).mean(1)
    out["phi_mass"] = mass[:, sl].sum(-1).mean(1)
    ct = N[:, W0:W1].sum(1) * TT
    for gi, g in enumerate(("births", "deaths", "fusions", "fissions"), 1):
        out[g] = 100 * (glob[:, W1, gi] - glob[:, W0, gi]) / ct
    nc = pres[:, 1:] & ~pres[:, :-1]
    out["div_ge50"] = 100 * (nc & (mass[:, 1:] >= 50))[:, W0:W1].sum((1, 2)) / ct
    for q in (10, 50, 90):
        out[f"size_p{q}"] = np.array([np.percentile(mass[s, sl][pres[s, sl]], q) for s in range(N.shape[0])])
    return out

PS = {a: per_seed(a) for a in D}
def comp(a, b):
    A, Bb = PS[a], PS[b]; res = {}
    for k in A:
        d = Bb[k] - A[k]
        if d.std() == 0:
            continue
        p = stats.ttest_1samp(d, 0).pvalue
        res[k] = {"rel_pct": round(100 * d.mean() / A[k].mean(), 2), "over_sd": round(d.mean() / A[k].std(ddof=1), 3), "p": round(float(p), 4)}
    ps = sorted((v["p"], k) for k, v in res.items()); m = len(ps)
    for i, (p, k) in enumerate(ps):
        res[k]["p_holm"] = round(min(1.0, max((m - j) * ps[j][0] for j in range(i + 1))), 4)
    return res
OUT["paired"] = {f"{b}-{a}": comp(a, b) for a, b in (("main", "dt025"), ("main", "dt1"), ("dt025", "dt1"), ("dt025", "main"),
                                                      ("main", "det"), ("main", "sa003"), ("det", "sa003"), ("main", "sa03"))}
OUT["dt025_max_abs_over_sd"] = max(abs(v["over_sd"]) for v in OUT["paired"]["dt025-main"].values())

# --- probe ratio
pl = json.load(open(f"{R}/probe_input_long.json")); an = json.load(open(f"{R}/analysis.json"))
Ve = an["closure_L2_main"]["mean_size"]["Ve"]["2"]  # h = 1,2,4,8,16,32
pr = {}
for arm in ("feed", "starve"):
    for h, hc in (("10", 3), ("20", 4), ("30", 5)):
        dm = pl["arms"][arm]["paired_L2_diff_mean"][h][1]; se = pl["arms"][arm]["paired_L2_diff_se"][h][1]
        pr[f"{arm}_h{h}_vs_closure_h{HS[hc]}"] = round((dm ** 2 - se ** 2) / Ve[hc], 3)
        pr[f"{arm}_h{h}_diff_over_oracle_sd"] = round(dm / pl["oracle_sd_L2"][h][1], 3)
    pr[f"{arm}_h10_vs_closure_h8_raw"] = round(pl["arms"][arm]["paired_L2_diff_mean"]["10"][1] ** 2 / Ve[3], 3)
pr["nats_feed_starve_mean"] = [float(np.mean(pl["arms"]["feed"]["nats_per_member"])), float(np.mean(pl["arms"]["starve"]["nats_per_member"]))]
d0 = np.array(pl["arms"]["none"]["target_divisions_within_H"]) > 0
for arm in ("feed", "starve"):
    d1 = np.array(pl["arms"][arm]["target_divisions_within_H"]) > 0
    b, c = int((d0 & ~d1).sum()), int((~d0 & d1).sum())
    pr[f"mcnemar_{arm}_vs_none_discordant"] = [b, c, float(stats.binomtest(min(b, c), b + c, 0.5).pvalue) if b + c else 1.0]
OUT["probe"] = pr
ps = json.load(open(f"{R}/probe_input.json"))
OUT["probe5_nats_feed_starve"] = [float(np.mean(ps["arms"]["feed"]["nats_per_member"])), float(np.mean(ps["arms"]["starve"]["nats_per_member"]))]
OUT["cpu_pilot_sum_s"] = sum(json.load(open(f"{R}/pilot_{a}.json"))["cpu_s_total"] for a in D)
json.dump(OUT, open("/home/user/evalwork/vecworld/program/track1/membrane_world/checker/recompute.json", "w"), indent=1)
print(json.dumps(OUT, indent=1))
