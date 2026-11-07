"""analyze -- effect sizes of the probe (results/probe/state_*.npz) -> results/probe_effects.json

Per state s, condition c (with its twin: twin_w for WA/WR, twin_0 for KA, twin_q for WA50q), view v
(coarse 192 / objects 144 standardised coordinates, closure-study SDs) and horizon h:
  d_r      = z_c,r(h) - z_twin,r(h)       (shared noise key r, r = 1..R)
  shift2   = (||mean_r d_r||^2 - sum_r ||d_r - mean||^2 / (R (R-1))) / q     unbiased squared shift of
             the state-conditioned level-1 mean, per coordinate = the expected extra MSE of a predictor
             that ignores the inputs (given the level-0 state; a level-1 history can only shrink it, by
             Jensen)
  paired2  = mean_r ||d_r||^2 / q          (common-random-number difference: what replay would show)
  ratio    = shift2 / V_best(v, h)          V_best: the best level-1 predictor's error variance
             (fresh/closure/results/summary.json)
Aggregates over the states: mean (the exam-average loss of ignore-actions, in units of V_best), its SE
over states, median, share of states >= 0.1; per nat = mean ratio / C. n = 64 detectability: mean /
(SD over states / 8). Oracle variance per twin world: sum_r ||z_r - mean||^2 / ((R-1) q).
Target displacement: the target's uid in both members, min-image centroid difference projected on n.
"""
import glob
import json

import numpy as np

import wind as WD

HS = [1, 2, 4, 8, 16]
SUMMARY = json.load(open("/home/user/evalwork/vecworld/vw1/fresh/closure/results/summary.json"))
VB = {v: np.array(SUMMARY[v]["V_best"][:5]) for v in ("coarse", "objects")}
VO_CL = {v: np.array(SUMMARY[v]["V_oracle"][:5]) for v in ("coarse", "objects")}
SL = {"coarse": slice(0, WD.NC), "objects": slice(WD.NC, WD.NC + WD.NO)}
TWIN = lambda c: "twin_q" if c == "WA50q" else ("twin_0" if c.startswith("KA") else "twin_w")


def per_state(fn, sd):
    z = np.load(fn)
    cond = [str(c) for c in z["cond"]]
    ci, ri = z["ci"], z["ri"]
    R = int(ri.max()) + 1
    idx = {c: np.array([np.flatnonzero((ci == i) & (ri == r))[0] for r in range(R)]) for i, c in enumerate(cond)}
    Z = {}
    for v, sl in SL.items():
        s_, eff = sd[v]
        Z[v] = z["y"][..., sl][..., eff].astype(float) / s_[eff]
    out = {"cond": cond, "budget": dict(zip(cond, z["budget"].tolist())), "target": int(z["target"]),
           "speed": float(z["speed"]), "eff": {}, "vor": {}, "lat": {}, "lost": {}, "moved": {}}
    for c in cond:
        if c.startswith("twin"):
            for v in SL:
                Y = Z[v][idx[c]][:, HS]                                   # (R, nH, q)
                out["vor"].setdefault(c, {})[v] = (((Y - Y.mean(0)) ** 2).sum((0, 2)) / ((R - 1) * Y.shape[2])).tolist()
            continue
        tw = TWIN(c)
        for v in SL:
            D = Z[v][idx[c]][:, HS] - Z[v][idx[tw]][:, HS]                # (R, nH, q)
            q = D.shape[2]
            m = D.mean(0)
            s2 = ((m ** 2).sum(1) - ((D - m) ** 2).sum((0, 2)) / (R * (R - 1))) / q
            p2 = (D ** 2).sum(2).mean(0) / q
            out["eff"].setdefault(c, {})[v] = {"shift2": s2.tolist(), "paired2": p2.tolist()}
        # target displacement along n (px) and target loss
        tab = z["tab"]
        tuid = tab[idx[tw][0], 0, out["target"], WD.NF + 4]
        n0 = z["n0"]
        lat, lost = np.full((R, len(HS)), np.nan), np.zeros((R, len(HS)))
        for r in range(R):
            for k, h in enumerate(HS):
                pos = []
                for b in (idx[c][r], idx[tw][r]):
                    T = tab[b, h]
                    sl_ = np.flatnonzero((T[:, 0] > 0.5) & (T[:, WD.NF + 4] == tuid))
                    pos.append(T[sl_[0], WD.NF:WD.NF + 2] if sl_.size else None)
                if pos[0] is None or pos[1] is None:
                    lost[r, k] = 1.0
                    continue
                dd = WD.mi(pos[0] - pos[1], 128.0)
                lat[r, k] = dd @ n0
        out["lat"][c] = lat.tolist()
        out["lost"][c] = lost.mean(0).tolist()
        if c.startswith("KA"):
            out["moved"][c] = float(z["moved"][idx[c]].sum(1).mean())
    return out


def fit_loglog(C, r):
    """least squares log r = a log C + b over the positive points; None if < 2 points."""
    C, r = np.asarray(C, float), np.asarray(r, float)
    ok = r > 0
    if ok.sum() < 2:
        return None
    a, b = np.polyfit(np.log(C[ok]), np.log(r[ok]), 1)
    return float(a), float(b)


def main():
    sd = WD.closure_sd()
    files = sorted(glob.glob(f"{WD.RES}/probe/state_*.npz"))
    S = [per_state(f, sd) for f in files]
    z0 = np.load(files[0])
    sig = float(z0["sigma_main"])
    conds = [c for c in S[0]["cond"] if not c.startswith("twin")]
    res = {"n_states": len(S), "sigma_w": sig, "horizons": HS, "V_best": {v: VB[v].tolist() for v in VB},
           "replicates_R": int(z0["ri"].max()) + 1, "conditions": {}, "oracle_variance": {}}
    for c in conds:
        st_ = [s for s in S if c in s["eff"]]
        row = {"n_states": len(st_), "budget_mean": float(np.mean([s["budget"][c] for s in st_]))}
        for v in SL:
            s2 = np.array([s["eff"][c][v]["shift2"] for s in st_])          # (n, nH)
            p2 = np.array([s["eff"][c][v]["paired2"] for s in st_])
            rat = s2 / VB[v]
            n = len(st_)
            row[v] = {"ratio_mean": rat.mean(0).tolist(), "ratio_se": (rat.std(0, ddof=1) / np.sqrt(n)).tolist(),
                      "ratio_median": np.median(rat, 0).tolist(), "share_states_ge_0.1": (rat >= 0.1).mean(0).tolist(),
                      "ratio_per_budget_unit": (rat.mean(0) / row["budget_mean"]).tolist(),
                      "paired_ratio_mean": (p2 / VB[v]).mean(0).tolist(),
                      "n64_mean_over_se": (rat.mean(0) / (rat.std(0, ddof=1) / 8.0)).tolist()}
        lat = np.array([s["lat"][c] for s in st_], float)                    # (n, R, nH)
        row["target_lateral_px_mean"] = np.nanmean(lat, (0, 1)).tolist()
        row["target_lateral_px_se"] = (np.nanstd(np.nanmean(lat, 1), 0, ddof=1) / np.sqrt(len(st_))).tolist()
        row["target_lost_share"] = np.mean([s["lost"][c] for s in st_], 0).tolist()
        if c.startswith("KA"):
            row["kick_matter_moved_mean"] = float(np.mean([s["moved"][c] for s in st_]))
        res["conditions"][c] = row
    for tw in ("twin_w", "twin_0", "twin_q"):
        st_ = [s for s in S if tw in s["vor"]]
        if not st_:
            continue
        res["oracle_variance"][tw] = {v: {"mean": np.mean([s["vor"][tw][v] for s in st_], 0).tolist(),
                                          "se": (np.std([s["vor"][tw][v] for s in st_], 0, ddof=1) / np.sqrt(len(st_))).tolist(),
                                          "n_states": len(st_)} for v in SL}
    # wind vs port oracle variance, paired over states
    comp = {}
    for v in SL:
        a = np.array([s["vor"]["twin_w"][v] for s in S])
        b = np.array([s["vor"]["twin_0"][v] for s in S])
        dlt = a - b
        comp[v] = {"wind_minus_port_mean": dlt.mean(0).tolist(), "se": (dlt.std(0, ddof=1) / np.sqrt(len(S))).tolist(),
                   "ratio_wind_over_port": (a.mean(0) / b.mean(0)).tolist(),
                   "increase_over_V_best": (dlt.mean(0) / VB[v]).tolist(),
                   "closure_V_oracle": VO_CL[v].tolist()}
    res["oracle_variance"]["wind_vs_port"] = comp
    # scaling check: same physical push at sigma_w/4 background
    st_ = [s for s in S if "WA50q" in s["eff"]]
    if st_:
        chk = {}
        for v in SL:
            a = np.array([s["eff"]["WA50"][v]["shift2"] for s in st_])
            b = np.array([s["eff"]["WA50q"][v]["shift2"] for s in st_])
            chk[v] = {"WA50_mean_shift2": a.mean(0).tolist(), "WA50q_mean_shift2": b.mean(0).tolist(),
                      "ratio_q_over_main": (b.mean(0) / a.mean(0)).tolist(),
                      "diff_se": ((b - a).std(0, ddof=1) / np.sqrt(len(st_))).tolist()}
        res["scaling_check_same_push_quarter_background"] = {"n_states": len(st_), **chk}
    # budget scale where ignore-inputs loses 0.1 V_best, kick equivalents
    fits = {}
    for fam in ("WA", "WR"):
        Cs = [res["conditions"][f"{fam}{C:g}"]["budget_mean"] for C in (2.0, 12.5, 50.0)]
        for v in SL:
            for k, h in enumerate(HS):
                r = [res["conditions"][f"{fam}{C:g}"][v]["ratio_mean"][k] for C in (2.0, 12.5, 50.0)]
                f = fit_loglog(Cs, r)
                key = f"{fam}/{v}/h{h}"
                if f is None:
                    fits[key] = None
                    continue
                a, b = f
                Cstar = float(np.exp((np.log(0.1) - b) / a)) if a > 0 else None
                fits[key] = {"slope": a, "intercept": b, "C_for_0.1_Vbest_nats": Cstar,
                             "C_for_0.1_Vbest_at_sigma_0.05": None if Cstar is None else Cstar * (sig / 0.05) ** 2}
                if fam == "WA":
                    for kc in ("KA4", "KA16", "KA64"):
                        rk = res["conditions"][kc][v]["ratio_mean"][k]
                        fits[key][f"{kc}_equivalent_wind_nats"] = (float(np.exp((np.log(rk) - b) / a))
                                                                   if (rk > 0 and a > 0) else None)
    res["loglog_fits"] = fits
    # the wind's own noise: wind-induced oracle variance dV(sigma) (twin_w - twin_0), its sigma^2 scaling
    # (twin_q at sigma/4 on the check states), and the wind world's predictive variance, approximated
    # from below by V_best + dV (the best level-1 predictor cannot predict the extra noise)
    dV = {v: np.maximum(np.array(comp[v]["wind_minus_port_mean"]), 0.0) for v in SL}
    stq = [s for s in S if "twin_q" in s["vor"]]
    if stq:
        sc = {}
        for v in SL:
            a = np.array([s["vor"]["twin_w"][v] for s in stq]) - np.array([s["vor"]["twin_0"][v] for s in stq])
            b = np.array([s["vor"]["twin_q"][v] for s in stq]) - np.array([s["vor"]["twin_0"][v] for s in stq])
            sc[v] = {"dV_main": a.mean(0).tolist(), "dV_quarter": b.mean(0).tolist(),
                     "ratio_quarter_over_main": (b.mean(0) / a.mean(0)).tolist(), "expected_if_sigma2": 1 / 16}
        res["oracle_variance"]["sigma2_scaling_check"] = {"n_states": len(stq), **sc}
    # sigma-free efficiency: mean shift per nat in units of the wind-induced variance (both ~ sigma^2)
    eff_inv = {}
    for c in conds:
        if c[:2] in ("WA", "WR") and c != "WA50q":
            Cn = res["conditions"][c]["budget_mean"]
            eff_inv[c] = {v: (np.array(res["conditions"][c][v]["ratio_mean"]) * VB[v] / np.where(dV[v] > 0, dV[v], np.nan)
                              / Cn).tolist() for v in SL}
            for v in SL:
                Vw = VB[v] + dV[v]
                res["conditions"][c][v]["ratio_vs_wind_world_Vbest_approx"] = (
                    np.array(res["conditions"][c][v]["ratio_mean"]) * VB[v] / Vw).tolist()
    res["shift_per_nat_over_wind_dV"] = eff_inv
    # budget scale C*(sigma') for 0.1 of the wind world's V_best, from the log-log fits (effect depends on
    # the physical push only: C at sigma' acts like C (sigma'/sigma)^2 at sigma) and dV(sigma') below
    # dV(sigma'): power law through the measured dV(sigma) (40 states) and dV(sigma/4) (= dV(sigma) times the
    # check states' ratio); exponent p = log(dV(sigma)/dV(sigma/4)) / log 4 (2 if not measurable)
    pw = {}
    for v in SL:
        if stq:
            rq = np.array(res["oracle_variance"]["sigma2_scaling_check"][v]["ratio_quarter_over_main"])
            pw[v] = np.where(rq > 0, np.log(1 / np.maximum(rq, 1e-12)) / np.log(4.0), 2.0)
        else:
            pw[v] = np.full(len(HS), 2.0)
    res["oracle_variance"]["dV_power_law_exponent"] = {v: pw[v].tolist() for v in SL}

    def dV_at(v, k, sp):
        return float(dV[v][k] * (sp / sig) ** pw[v][k])

    scan = {}
    for sp in (0.05, 0.1, 0.2, 0.4):
        row = {}
        for fam in ("WA", "WR"):
            for v in SL:
                for k, h in enumerate(HS):
                    f = fits.get(f"{fam}/{v}/h{h}")
                    Vw = VB[v][k] + dV_at(v, k, sp)
                    if f is None or f["slope"] <= 0:
                        row[f"{fam}/{v}/h{h}"] = None
                        continue
                    a, b = f["slope"], f["intercept"]
                    Ceq = float(np.exp((np.log(0.1 * Vw / VB[v][k]) - b) / a))     # nats at sigma (main)
                    row[f"{fam}/{v}/h{h}"] = {"C_nats": Ceq * (sig / sp) ** 2,
                                              "dV_over_Vbest": float(dV_at(v, k, sp) / VB[v][k])}
        scan[str(sp)] = row
    res["budget_scan_vs_wind_world_Vbest"] = scan
    json.dump(res, open(f"{WD.RES}/probe_effects.json", "w"), indent=1)
    for c in conds:
        r = res["conditions"][c]
        print(f"{c:7s} budget {r['budget_mean']:7.2f}  coarse ratio",
              " ".join(f"{x:8.4f}" for x in r["coarse"]["ratio_mean"]), " | objects",
              " ".join(f"{x:8.4f}" for x in r["objects"]["ratio_mean"]), " | lat px",
              " ".join(f"{x:5.2f}" for x in r["target_lateral_px_mean"]), flush=True)
    print(json.dumps(res["oracle_variance"]["wind_vs_port"]), flush=True)


if __name__ == "__main__":
    main()
