"""viability_stats -- (a) viability of the wind world at sigma_w in (0, 0.05, 0.1) and the oracle cost of the wind.

usage: python -B viability_stats.py   -> results/viability.json
Inputs: results/raw/viab.npz (6 members per sigma_w, seed 9002), actuation/results/viability.npz (3 members,
seed 9001, same design; pooled -> 9), results/raw/free_b*.npz (16 set-F trajectories at 0.05, ticks 0..236),
results/raw/oracle.npz (12 states x 3 sigma_w x 6 shared keys x 16 ticks).
Statistics: actuation/viability.traj_stats. Native band: 2.5-97.5% of means of n trajectories resampled from
the 36 wind-free closure trajectories (same window). Paired test vs sigma_w = 0 over members (shared keys).
"""
import glob
import json
import math

import numpy as np

import wr
import viability as AV            # actuation/viability.py (definitions only)

WD = wr.WD
K, NF = WD.K_SLOTS, WD.NF
FRESH = "/home/user/evalwork/vecworld/vw1/fresh/closure/results"


def native(T):
    nat = []
    for tg in "AB":
        c = np.load(f"{FRESH}/sim_{tg}.npz")
        Y, TAB = c["Y"].astype(float), c["TAB"].astype(float)
        for j in range(len(Y)):
            tb = TAB[j, :T + 1, :K * 5].reshape(T + 1, K, 5)
            nat.append(AV.traj_stats(Y[j, :T + 1, WD.NC:], tb, TAB[j, :T + 1, K * 5:]))
    return nat


def band(nat, n, keys, seed=1):
    rng = np.random.default_rng(seed)
    out = {}
    for k in keys:
        v = np.array([s[k] for s in nat])
        means = v[rng.integers(0, len(v), (10000, n))].mean(1)
        out[k] = [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]
    return out


def stats_of(y, tab_extra, glob_):
    return [AV.traj_stats(y[b][:, WD.NC:].astype(float), tab_extra[b].astype(float), glob_[b].astype(float))
            for b in range(len(y))]


def main():
    out = {"sources": {}}
    z = np.load(f"{wr.RAW}/viab.npz")
    a = np.load(f"{wr.ACT}/results/viability.npz")
    out["sources"] = {"new": f"{wr.RAW}/viab.npz", "actuation": f"{wr.ACT}/results/viability.npz",
                      "native": f"{FRESH}/sim_A.npz, sim_B.npz (36 wind-free trajectories)"}
    T = wr.V_T
    nat = native(T)
    keys = [k for k in nat[0] if k != "n_tracks"]
    out["native_mean_36"] = {k: float(np.mean([s[k] for s in nat])) for k in keys}
    sd = WD.closure_sd()
    rows = {}
    for sw in wr.V_SIGMAS:
        i_new = np.flatnonzero(np.isclose(z["sigmas"], sw))
        i_old = np.flatnonzero(np.isclose(a["sigmas"], sw))
        new = stats_of(z["y"][i_new], z["tab"][i_new], z["TAB"][i_new][..., K * 5:])
        old = stats_of(a["y"][i_old], a["tab"][i_old][..., NF:], a["glob"][i_old])
        yc = z["y"][i_new][:, 1:, :WD.NC].reshape(-1, WD.NC).astype(float)
        yo = z["y"][i_new][:, 1:, WD.NC:].reshape(-1, WD.NO).astype(float)
        rows[sw] = {"new": new, "old": old,
                    "coarse_sd_ratio": float((yc.std(0)[sd["coarse"][1]] / sd["coarse"][0][sd["coarse"][1]]).mean()),
                    "objects_sd_ratio": float((yo.std(0)[sd["objects"][1]] / sd["objects"][0][sd["objects"][1]]).mean()),
                    "mass_drift_max_abs": float(np.abs(z["mass1"][i_new] - z["mass0"][i_new]).max())}
    out["per_sigma"] = {}
    for label, pick, n in (("new6", lambda r: r["new"], 6), ("pooled9", lambda r: r["new"] + r["old"], 9)):
        bd = band(nat, n, keys)
        res = {"native_band": bd}
        # false-alarm rate of the band part of the rule on native data: n of the 36 native trajectories
        # (without replacement) -> share of draws with at least one statistic outside its band
        rng = np.random.default_rng(3)
        V = np.array([[s[k] for k in keys] for s in nat])
        lo, hi = np.array([bd[k][0] for k in keys]), np.array([bd[k][1] for k in keys])
        fa = [bool(((m < lo) | (m > hi)).any()) for m in (V[rng.choice(len(V), n, replace=False)].mean(0)
                                                         for _ in range(4000))]
        res["band_rule_false_alarm_native"] = float(np.mean(fa))
        for sw in wr.V_SIGMAS:
            S = pick(rows[sw])
            S0 = pick(rows[0.0])
            r = {}
            for k in keys:
                v = np.array([s[k] for s in S])
                d = v - np.array([s[k] for s in S0])
                se = d.std(ddof=1) / math.sqrt(len(d)) if len(d) > 1 else float("nan")
                r[k] = {"mean": float(v.mean()), "in_band": bool(bd[k][0] <= v.mean() <= bd[k][1]),
                        "paired_diff": float(d.mean()), "paired_se": float(se),
                        "paired_z": float(d.mean() / se) if se > 0 else (0.0 if d.mean() == 0 else float("inf"))}
            r["out_of_band"] = [k for k in keys if not r[k]["in_band"]]
            r["paired_abs_z_gt_3"] = [k for k in keys if abs(r[k]["paired_z"]) > 3]
            r["passes"] = not r["out_of_band"] and not r["paired_abs_z_gt_3"]
            res[str(sw)] = r
        out["per_sigma"][label] = res
    for sw in wr.V_SIGMAS:
        out["per_sigma"]["new6"][str(sw)].update({k: rows[sw][k] for k in ("coarse_sd_ratio", "objects_sd_ratio",
                                                                             "mass_drift_max_abs")})
    out["member_ticks_new"] = int(len(z["sigmas"]) * (T + WD.BURN_TICKS))
    out["seconds_new"] = z["seconds"].tolist()

    # set F trajectories as 16 extra members at 0.05 (window 0..236)
    fs = sorted(glob.glob(f"{wr.RAW}/free_b*.npz"))
    if fs:
        TF = wr.F_T
        natF = native(TF)
        Y = np.concatenate([np.load(f)["Y"] for f in fs])
        TAB = np.concatenate([np.load(f)["TAB"] for f in fs])
        SF = [AV.traj_stats(Y[j, :, WD.NC:].astype(float), TAB[j, :, :K * 5].reshape(TF + 1, K, 5).astype(float),
                            TAB[j, :, K * 5:].astype(float)) for j in range(len(Y))]
        bF = band(natF, len(SF), keys)
        rF = {k: {"mean": float(np.mean([s[k] for s in SF])), "band": bF[k],
                  "in_band": bool(bF[k][0] <= np.mean([s[k] for s in SF]) <= bF[k][1])} for k in keys}
        rF["out_of_band"] = [k for k in keys if not rF[k]["in_band"]]
        out["set_F_16_members_sigma0.05_window236"] = rF

    # oracle cost of the wind: paired branches from the same states with shared keys
    o = np.load(f"{wr.RAW}/oracle.npz")
    yo = o["y"].astype(float)                                   # (nsig, nS, R, TB+1, 336)
    fresh = {v: json.load(open(f"{FRESH}/closure_{v}.json")) for v in ("coarse", "objects")}
    oc = {}
    for v, sl in (("coarse", slice(0, WD.NC)), ("objects", slice(WD.NC, None))):
        s_, eff = sd[v]
        Z = yo[..., sl][..., eff] / s_[eff]
        Vor = Z.var(2, ddof=1).mean(-1)[:, :, np.array(wr.HORIZONS)]       # (nsig, nS, nH)
        Vb = np.array(fresh[v]["best_level1"][:len(wr.HORIZONS)])
        Vu = np.array(fresh[v]["V_oracle"][:len(wr.HORIZONS)])
        r = {"V_best_fresh": Vb, "V_oracle_fresh_144": Vu, "n_states": int(Z.shape[1]), "replicates": int(Z.shape[2])}
        for a_, sw in enumerate(wr.V_SIGMAS):
            dv = Vor[a_] - Vor[0]
            r[str(sw)] = {"V_oracle": Vor[a_].mean(0), "V_oracle_se": Vor[a_].std(0, ddof=1) / math.sqrt(Z.shape[1]),
                          "dV": dv.mean(0), "dV_se": dv.std(0, ddof=1) / math.sqrt(Z.shape[1]),
                          "dV_over_Vbest": dv.mean(0) / Vb, "dV_over_Vbest_se": dv.std(0, ddof=1) / math.sqrt(Z.shape[1]) / Vb}
        oc[v] = r
    out["oracle_cost"] = oc
    out["oracle_cost"]["seconds"] = o["seconds"].tolist()
    out["oracle_cost"]["actuation_extrapolated_dV_over_Vbest_coarse_h1_2_4_8"] = {
        "0.05": [0.029, 0.021, 0.015, 0.011], "0.1": [0.137, 0.084, 0.051, 0.036],
        "source": f"{wr.ACT}/results/summary.json headline.dV_over_Vbest_by_sigma_coarse"}
    # decision (declared rule)
    p05 = out["per_sigma"]["pooled9"]["0.05"]["passes"]
    p10 = out["per_sigma"]["pooled9"]["0.1"]["passes"]
    dv10 = max(float(np.max(oc[v]["0.1"]["dV_over_Vbest"])) for v in ("coarse", "objects"))
    out["decision"] = {"pooled9_passes_0.05": p05, "pooled9_passes_0.1": p10,
                       "max_dV_over_Vbest_0.1": dv10,
                       "sigma_w": 0.1 if (p10 and dv10 <= 0.10) else (0.05 if p05 else None),
                       "rule": "declaration.json a_viability.decision"}
    json.dump(_js(out), open(f"{wr.RES}/viability.json", "w"), indent=1)
    print(json.dumps(_js(out["decision"])))
    for lab in ("new6", "pooled9"):
        for sw in wr.V_SIGMAS:
            r = out["per_sigma"][lab][str(sw)]
            print(lab, sw, "out of band", r["out_of_band"], "|z|>3", r["paired_abs_z_gt_3"])
    for v in ("coarse", "objects"):
        for sw in wr.V_SIGMAS[1:]:
            print(v, sw, "dV/Vbest", np.round(oc[v][str(sw)]["dV_over_Vbest"], 3).tolist(),
                  "+-", np.round(oc[v][str(sw)]["dV_over_Vbest_se"], 3).tolist())


def _js(o):
    if isinstance(o, dict):
        return {str(k): _js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_js(v) for v in o]
    if isinstance(o, np.ndarray):
        return _js(o.tolist())
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, float) and not math.isfinite(o):
        return None
    return o


if __name__ == "__main__":
    main()
