"""analyse -- level-1 cells, growth and division; a rough level-2 closure; the dt and noise checks.

    python analyse.py

Inputs: results/pilot_{arm}.npz and .json (pilot.py). Window: ticks 100..600 (t 1000..6000, after formation)
unless stated. Level 2 is recomputed for every arm from the saved level-1 series with the declared transducer
(membrane_world.level2_from_level1); for arm main the recomputation is checked against the level 2 recorded
online. Writes results/analysis.json.

Level 1 (arm main). From the per-slot features (present, mass) and the tracker's per-slot (event, uid):
  * events: births, deaths, fusions and fissions per cell per 100 t (cumulative counters / sum of N dt);
  * fission products (new uid, event 2) are assigned to the nearest continuing slot with event 2 at the same tick
    (the parent); their fate (ticks until the uid leaves its slot) by mass. Products >= M_DIV = 50 px are daughters
    (a division); smaller ones are shed fragments (shedding). Mass balance m_parent(t-1) vs m_parent(t) +
    m_products(t), and daughter share;
  * cell cycles: from a cell's creation by a division (or its own previous division as parent) to its next division
    as parent, with no fusion on it in between (shedding does not end a cycle): duration, mass at start and just
    before division, growth factor;
  * hazards per tick binned by mass: division, shedding, death, fusion (absorbed);
  * growth: mean mass change per tick of continuing, event-free cells binned by mass.
Level 2 closure (arm main, branches; vw.certificates.closure's definitions with the oracle from branches): for
horizon h and a window of w past level-2 values,
    V0(h) variance of y(t+h) over all branch rows; Vu(h) mean within-branch variance over the R fresh-noise
    replicates (oracle spread); Ve(h, w) MSE of an OLS predictor of y(t+h) from [1, y(t), ..., y(t-w+1)] (all three
    coordinates), leave-one-seed-out; c(h, w) = (V0 - Ve) / (V0 - Vu); persistence y(t+h) = y(t) for reference.
    Bootstrap over seeds (200 draws) for w = 2: 16th-84th percentiles.
dt check: per seed (paired twins, same keys) time averages over the window of N, mean size, size quantiles,
event rates and phi-mass; differences dt025 - main and dt1 - main with 95% t-intervals, against the seed-to-seed
SD; the same for the noise arms (det, sa003, sa03) against main. Twin divergence: first tick at which N differs
between paired twins, against the first horizon at which N differs among fresh-noise replicates.
"""
import json
import os

import _paths
import numpy as np
from scipy import stats

import membrane_world as MW

R = _paths.RESULTS
ARMS = ("main", "dt025", "dt1", "det", "sa003", "sa03")
W0, W1 = 100, 600
NF = 12
D, M = {}, {}
for a in ARMS:
    p = os.path.join(R, f"pilot_{a}.npz")
    if os.path.exists(p):
        D[a] = np.load(p)
        M[a] = json.load(open(os.path.join(R, f"pilot_{a}.json")))
TT = M["main"]["tick_time"]
K = M["main"]["K"]
G_NAMES = ("next_uid", "births", "deaths", "fusions", "fissions")
M_DIV = MW.M_DIV
# level 2 recomputed from the saved level-1 series with the declared transducer (membrane_world.phi_population):
# every arm gets the current definition; for arm main it must equal the level 2 recorded online.
L2R = {a: MW.level2_from_level1(D[a]["L1"], K, TT) for a in D}
# (the other arms ran before the level-2 rule changed and recorded the earlier rule: tracker fissions, 20-tick window)
L2_CHECK = {"main": float(np.abs(L2R["main"] - D["main"]["L2"]).max())}


def unpack(a):
    L1 = D[a]["L1"].astype(np.float64)
    S, T1, _ = L1.shape
    tab = L1[..., :K * NF].reshape(S, T1, K, NF)
    pres = tab[..., 0] > 0.5
    mass = np.where(pres, tab[..., 1], 0.0)
    H = M[a]["H"]
    cx = (np.arctan2(tab[..., 4], tab[..., 3]) * H / (2 * np.pi)) % H
    cy = (np.arctan2(tab[..., 6], tab[..., 5]) * H / (2 * np.pi)) % H
    glob = L1[..., K * NF:]
    ev = D[a]["ev"]
    return dict(pres=pres, mass=mass, frac=tab[..., 2], cx=cx, cy=cy, glob=glob, ev=ev[..., 0], uid=ev[..., 1],
                L2=L2R[a], H=H)


def per_seed_stats(a, w0=W0, w1=W1):
    u = unpack(a)
    pres, mass, glob = u["pres"], u["mass"], u["glob"]
    N = pres.sum(-1)
    out = {}
    sl = slice(w0, w1)
    out["N"] = N[:, sl].mean(1)
    out["mean_size"] = (mass[:, sl].sum(-1) / np.maximum(N[:, sl], 1)).mean(1)
    out["phi_mass"] = mass[:, sl].sum(-1).mean(1)
    out["mean_K"] = (np.where(pres, u["frac"] * mass, 0)[:, sl].sum(-1) / np.maximum(mass[:, sl].sum(-1), 1e-9)).mean(1)
    cell_time = N[:, w0:w1].sum(1) * TT
    for gi, g in enumerate(G_NAMES[1:], 1):
        out[f"{g}_per_cell_per_100t"] = 100 * (glob[:, w1, gi] - glob[:, w0, gi]) / cell_time
    newc = pres[:, 1:] & ~pres[:, :-1]
    big = newc & (mass[:, 1:] >= M_DIV)
    out["divisions_ge50_per_cell_per_100t"] = 100 * big[:, w0:w1].sum((1, 2)) / cell_time
    q = {p: [] for p in (10, 50, 90)}
    for s in range(pres.shape[0]):
        m = mass[s, sl][pres[s, sl]]
        for p in q:
            q[p].append(np.percentile(m, p))
    for p in q:
        out[f"size_p{p}"] = np.array(q[p])
    out["L2_rate"] = u["L2"][:, sl, 2].mean(1)
    return out


def paired(a, b, w0=W0, w1=W1):
    """b - a per seed (common seeds), for every statistic."""
    A, B = per_seed_stats(a, w0, w1), per_seed_stats(b, w0, w1)
    n = min(len(A["N"]), len(B["N"]))
    res = {}
    for k in A:
        d = B[k][:n] - A[k][:n]
        se = d.std(ddof=1) / np.sqrt(n)
        tq = stats.t.ppf(0.975, n - 1)
        res[k] = {"mean_" + a: float(A[k][:n].mean()), "mean_" + b: float(B[k][:n].mean()), "diff": float(d.mean()),
                  "ci95": [float(d.mean() - tq * se), float(d.mean() + tq * se)],
                  "diff_rel_pct": float(100 * d.mean() / A[k][:n].mean()) if A[k][:n].mean() != 0 else None,
                  "seed_sd_" + a: float(A[k][:n].std(ddof=1)), "diff_over_seed_sd": float(d.mean() / A[k][:n].std(ddof=1)),
                  "p_paired_t": float(stats.ttest_1samp(d, 0).pvalue) if se > 0 else None, "n": int(n)}
    return res


def _life(pres, uid, s, t, k, T1):
    """Ticks a new cell (slot k, first present at tick t) keeps its slot and uid, and the slot's event when it ends."""
    u0, n = uid[s, t, k], 0
    while t + n < T1 and pres[s, t + n, k] and uid[s, t + n, k] == u0:
        n += 1
    return n, (None if t + n >= T1 else None)


def level1(a="main"):
    u = unpack(a)
    pres, mass, ev, uid, cx, cy, H = u["pres"], u["mass"], u["ev"], u["uid"], u["cx"], u["cy"], u["H"]
    S, T1, _ = pres.shape
    divs, cycles, prods_all, births = [], [], [], []
    haz = {"mass": [], "div": [], "shed": [], "death": [], "fused": []}
    growth = {"mass": [], "dm": []}
    n_prod_unassigned = 0
    for s in range(S):
        last_div = {}          # uid -> (tick, mass) at its creation by a division or its last division as parent
        fused_since = set()
        for t in range(1, T1):
            new = [k for k in range(K) if pres[s, t, k] and not pres[s, t - 1, k]]
            prods = [k for k in new if ev[s, t, k] == 2]
            parents = [k for k in range(K) if pres[s, t, k] and pres[s, t - 1, k] and ev[s, t, k] == 2]
            for k in range(K):
                if pres[s, t, k] and pres[s, t - 1, k] and ev[s, t, k] == 3:
                    fused_since.add(int(uid[s, t, k]))
            for k in new:
                if ev[s, t, k] == 1 and t >= W0:
                    births.append((mass[s, t, k], _life(pres, uid, s, t, k, T1)[0]))
            assign = {}
            for k in prods:
                if not parents:
                    n_prod_unassigned += 1
                    continue
                d = [np.hypot((cy[s, t, k] - cy[s, t, p] + H / 2) % H - H / 2, (cx[s, t, k] - cx[s, t, p] + H / 2) % H - H / 2)
                     for p in parents]
                assign.setdefault(parents[int(np.argmin(d))], []).append(k)
            divided = set()
            for p, ks in assign.items():
                mp0, mp1 = mass[s, t - 1, p], mass[s, t, p]
                for k in ks:
                    life = _life(pres, uid, s, t, k, T1)[0]
                    if t >= W0:
                        prods_all.append((mass[s, t, k], life, T1 - t))
                big = [k for k in ks if mass[s, t, k] >= M_DIV]
                if not big:
                    continue
                divided.add(p)
                mk = sum(mass[s, t, k] for k in big)
                divs.append({"seed": s, "tick": t, "m_before": mp0, "m_parent_after": mp1, "m_products": mk,
                             "m_all_products": sum(mass[s, t, k] for k in ks), "n_products": len(big)})
                up = int(uid[s, t, p])
                if up in last_div and up not in fused_since and t >= W0:
                    t0, m0 = last_div[up]
                    cycles.append({"dur_ticks": t - t0, "m_start": m0, "m_end": mp0})
                last_div[up] = (t, mp1)
                fused_since.discard(up)
                for k in big:
                    last_div[int(uid[s, t, k])] = (t, mass[s, t, k])
            # hazards and growth from t-1 -> t (cells present at t-1, window only)
            if W0 <= t - 1 < W1:
                for k in range(K):
                    if not pres[s, t - 1, k]:
                        continue
                    m0 = mass[s, t - 1, k]
                    cont = pres[s, t, k] and uid[s, t, k] == uid[s, t - 1, k]
                    haz["mass"].append(m0)
                    haz["div"].append(bool(cont and k in divided))
                    haz["shed"].append(bool(cont and k in assign and k not in divided))
                    haz["death"].append(bool(not pres[s, t, k] and ev[s, t, k] == -2))
                    haz["fused"].append(bool(not pres[s, t, k] and ev[s, t, k] == -1))
                    if cont and ev[s, t, k] == 0:
                        growth["mass"].append(m0)
                        growth["dm"].append(mass[s, t, k] - m0)
    dv = {k: np.array([d[k] for d in divs], float) for k in ("m_before", "m_parent_after", "m_products", "m_all_products",
                                                              "n_products", "tick")}
    win = dv["tick"] >= W0
    bal = (dv["m_parent_after"] + dv["m_all_products"]) / dv["m_before"]
    share = dv["m_products"] / (dv["m_parent_after"] + dv["m_products"])
    cy_ = {k: np.array([c[k] for c in cycles], float) for k in ("dur_ticks", "m_start", "m_end")}
    edges = np.array([12, 50, 100, 150, 200, 300, 400, 600, 1e9])
    hm = np.array(haz["mass"])

    def binned(x, m):
        return [float(x[(m >= lo) & (m < hi)].mean()) if ((m >= lo) & (m < hi)).any() else None for lo, hi in zip(edges[:-1], edges[1:])]
    hz = {nm: binned(np.array(haz[nm], float), hm) for nm in ("div", "shed", "death", "fused")}
    hz["n"] = [int(((hm >= lo) & (hm < hi)).sum()) for lo, hi in zip(edges[:-1], edges[1:])]
    hz["mass_edges"] = edges[:-1].tolist() + ["inf"]
    gm, gd = np.array(growth["mass"]), np.array(growth["dm"])
    gr = {"mean_dm_per_tick": binned(gd, gm), "mean_rel_growth_per_100t": binned(100 / TT * gd / gm, gm),
          "n": [int(((gm >= lo) & (gm < hi)).sum()) for lo, hi in zip(edges[:-1], edges[1:])], "mass_edges": hz["mass_edges"]}
    P = np.array(prods_all, float)                     # (mass, life ticks, ticks left in run)
    fate = {}
    for lo, hi in ((12, 25), (25, 50), (50, 100), (100, 200), (200, 1e9)):
        m = (P[:, 0] >= lo) & (P[:, 0] < hi)
        ok = m & (P[:, 2] >= 20)                      # products with >= 20 ticks of run left
        fate[f"[{lo},{hi if hi < 1e9 else 'inf'})"] = {"n": int(m.sum()), "median_life_ticks": float(np.median(P[m, 1])) if m.any() else None,
                                                      "frac_alive_20_ticks": float((P[ok, 1] >= 20).mean()) if ok.any() else None}
    B = np.array(births, float)
    N = pres.sum(-1)
    out = {
        "N_mean_window": float(N[:, W0:W1].mean()), "N_range_window": [int(N[:, W0:W1].min()), int(N[:, W0:W1].max())],
        "N_by_t_mean": {str(int(t * TT)): float(N[:, t].mean()) for t in range(0, T1, 50)},
        "mean_size_by_t_mean": {str(int(t * TT)): float((mass[:, t].sum(-1) / np.maximum(N[:, t], 1)).mean()) for t in range(0, T1, 50)},
        "fission_products_in_window": int(len(P)), "fission_products_lt50_frac": float((P[:, 0] < M_DIV).mean()),
        "fission_product_fate_by_mass": fate, "fission_products_unassigned": int(n_prod_unassigned),
        "births_in_window": int(len(B)), "birth_mass_median": float(np.median(B[:, 0])) if len(B) else None,
        "birth_median_life_ticks": float(np.median(B[:, 1])) if len(B) else None,
        "divisions_ge50_total": int(len(divs)), "divisions_ge50_in_window": int(win.sum()),
        "division_products_per_division": {str(int(v)): int((dv["n_products"][win] == v).sum()) for v in np.unique(dv["n_products"][win])},
        "division_mass_balance_median": float(np.median(bal[win])), "division_mass_balance_iqr": np.percentile(bal[win], [25, 75]).tolist(),
        "daughter_share_median": float(np.median(share[win])), "daughter_share_iqr": np.percentile(share[win], [25, 75]).tolist(),
        "parent_mass_before_division_median": float(np.median(dv["m_before"][win])),
        "parent_mass_before_division_iqr": np.percentile(dv["m_before"][win], [25, 75]).tolist(),
        "cycles_n": int(len(cycles)),
        "cycle_duration_t_median": float(np.median(cy_["dur_ticks"]) * TT) if cycles else None,
        "cycle_duration_t_iqr": (np.percentile(cy_["dur_ticks"], [25, 75]) * TT).tolist() if cycles else None,
        "cycle_mass_start_median": float(np.median(cy_["m_start"])) if cycles else None,
        "cycle_mass_end_median": float(np.median(cy_["m_end"])) if cycles else None,
        "cycle_growth_factor_median": float(np.median(cy_["m_end"] / cy_["m_start"])) if cycles else None,
        "cycle_growth_factor_iqr": np.percentile(cy_["m_end"] / cy_["m_start"], [25, 75]).tolist() if cycles else None,
        "corr_mass_start_end": float(np.corrcoef(cy_["m_start"], cy_["m_end"])[0, 1]) if len(cycles) > 2 else None,
        "hazard_per_tick_by_mass": hz, "growth_by_mass": gr,
        "rates_per_cell_per_100t": {k: float(v.mean()) for k, v in per_seed_stats(a).items() if k.endswith("per_100t")},
    }
    return out


# ----------------------------------------------------------------------------- level-2 closure
HS = (1, 2, 4, 8, 16, 32)
WS = (1, 2, 4)
NAMES = ("N", "mean_size", "div_rate")


def rows(seeds=None):
    L2 = L2R["main"]
    BR = D["main"]["branch_L2"].astype(float)         # (P, S, R, HB+1, 3)
    tb = D["main"]["branch_t"]
    P, S, Rr = BR.shape[:3]
    seeds = range(S) if seeds is None else seeds
    X, Y, G, B = [], [], [], []
    bid = 0
    for p in range(P):
        for j, s in enumerate(seeds):
            past = np.concatenate([L2[s, tb[p] - i] for i in range(max(WS))])
            for r in range(Rr):
                X.append(past)
                Y.append(BR[p, s, r, list(HS)])
                G.append(j)
                B.append(bid)
            bid += 1
    return np.array(X), np.array(Y), np.array(G), np.array(B)


def closure(X, Y, G, B):
    out = {}
    nc = len(NAMES)
    for c, name in enumerate(NAMES):
        res = {"V0": [], "Vu": [], "Ve": {w: [] for w in WS}, "Vpersist": []}
        for hi, h in enumerate(HS):
            y = Y[:, hi, c]
            res["V0"].append(float(y.var(ddof=1)))
            res["Vu"].append(float(np.mean([y[B == b].var(ddof=1) for b in np.unique(B)])))
            res["Vpersist"].append(float(np.mean((y - X[:, c]) ** 2)))
            for w in WS:
                Xw = np.concatenate([np.ones((len(y), 1)), X[:, :nc * w]], 1)
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


def boot(n=200, seed=0):
    rng = np.random.default_rng(seed)
    S = D["main"]["L2"].shape[0]
    cs = []
    for _ in range(n):
        sel = rng.choice(S, S, replace=True)
        if len(np.unique(sel)) < 2:
            continue
        cl = closure(*rows(sel))
        cs.append([[cl[nm]["ceiling"][2][i] for i in range(len(HS))] for nm in NAMES])
    cs = np.array(cs)
    return {nm: {"p16": np.percentile(cs[:, c], 16, 0).tolist(), "p84": np.percentile(cs[:, c], 84, 0).tolist()}
            for c, nm in enumerate(NAMES)}


def divergence():
    """First tick at which N differs between paired twins (arm vs main) and among fresh-noise replicates."""
    out = {}
    Nm = D["main"]["L2"][..., 0]
    for a in ARMS[1:]:
        if a not in D:
            continue
        Na = D[a]["L2"][..., 0]
        n = min(len(Nm), len(Na))
        first = []
        for s in range(n):
            i = np.flatnonzero(Na[s] != Nm[s])
            first.append(int(i[0]) if i.size else None)
        f = [x for x in first if x is not None]
        out[f"{a}_vs_main_first_tick_N_differs"] = {"per_seed": first, "median_t": float(np.median(f) * TT) if f else None}
    BR = D["main"]["branch_L2"][..., 0]                    # (P, S, R, HB+1)
    fr = []
    for p in range(BR.shape[0]):
        for s in range(BR.shape[1]):
            spread = BR[p, s].max(0) != BR[p, s].min(0)
            i = np.flatnonzero(spread)
            fr.append(int(i[0]) if i.size else BR.shape[-1])
    fr = np.array(fr)
    out["fresh_noise_replicates_first_h_N_differs"] = {"median_t": float(np.median(fr) * TT),
                                                       "iqr_t": (np.percentile(fr, [25, 75]) * TT).tolist(),
                                                       "frac_never_within_32_ticks": float((fr == BR.shape[-1]).mean())}
    return out


def main():
    out = {"window_ticks": [W0, W1], "tick_time": TT, "arms_present": list(D)}
    out["level1_main"] = level1("main")
    if "branch_L2" in D["main"].files:
        X, Y, G, B = rows()
        cl = closure(X, Y, G, B)
        cl["n_branch_points"] = int(len(np.unique(B)))
        cl["n_rows"] = int(len(B))
        cl["horizons_ticks"] = list(HS)
        cl["bootstrap_w2"] = boot()
        out["closure_L2_main"] = cl
    out["dt_check"] = {f"{a}_minus_main": paired("main", a) for a in ("dt025", "dt1") if a in D}
    out["dt_check_formation"] = {f"{a}_minus_main": {k: v for k, v in paired("main", a, 0, W0).items() if k in ("N", "mean_size", "phi_mass")}
                                 for a in ("dt025", "dt1") if a in D}
    out["noise_check"] = {f"{a}_minus_main": paired("main", a) for a in ("det", "sa003", "sa03") if a in D}
    out["divergence"] = divergence()
    out["per_arm_means"] = {a: {k: float(v.mean()) for k, v in per_seed_stats(a).items()} for a in D}
    out["level2_recomputed_from_level1_max_abs_diff_vs_recorded"] = L2_CHECK
    out["cpu"] = {a: {k: M[a][k] for k in ("cpu_s_total", "cpu_s_branches", "member_ticks_main", "member_ticks_branches",
                                            "cpu_s_per_member_tick_main", "cpu_s_per_member_tick_branches")} for a in M}
    out["tracker_overflow_ticks_max"] = {a: int(np.max(np.asarray(M[a]["tracker_overflow_per_member"])[:, :2])) for a in M}
    json.dump(out, open(os.path.join(R, "analysis.json"), "w"), indent=1)
    l1 = out["level1_main"]
    print(json.dumps({k: v for k, v in l1.items() if not k.endswith("_by_t")}, indent=1))
    if "closure_L2_main" in out:
        for nm in NAMES:
            v = out["closure_L2_main"][nm]
            print(nm, "c(w=2)", np.round(v["ceiling"][2], 3).tolist(), "persist", np.round(v["ceiling_persistence"], 3).tolist(),
                  "Vu/V0", np.round(v["oracle_share_of_V0"], 3).tolist())
    for grp in ("dt_check", "noise_check"):
        for k, v in out[grp].items():
            print(grp, k, {s: (round(x["diff_rel_pct"], 1) if x["diff_rel_pct"] is not None else None, round(x["diff_over_seed_sd"], 2),
                               round(x["p_paired_t"], 3) if x["p_paired_t"] is not None else None) for s, x in v.items()})
    print(json.dumps(out["divergence"], indent=1))


if __name__ == "__main__":
    main()
