"""analyse1 -- analysis of GPU job 1 (throughput, effective law, headroom scan) -> results/analysis1.json.

    python -B analyse1.py JOB1_OUT_DIR [SCAN_DIR]     (SCAN_DIR: a --scan-only rerun, default JOB1_OUT_DIR)

Index convention of job 1's arrays: S[..., i, :] is the level-1 summary of the state after i + 1 ticks.

Law (replicator check). For each eps: the change of a share x (the level-2 share s_b, and the mass-weighted
label share fb_mass of the vortex list) over h ticks is regressed on the replicator-mutator terms,
    x(t + h) - x(t) = b1 x (1 - x) + b2 (1 - 2 x) + e,
pooled over members and states from tick 64 on (h = 16 ticks = 80 time units; one row per member and tick).
Reported: b1, b2 per eps with member-bootstrap SE; the straight line b1 = c0 + c1 eps (R^2 over the eps values,
c0 / (c1 x 0.2) = the part of the rate at eps 0.2 that is not selection); 'shape' = R^2 between the fitted drift
and the binned mean change E[dx | x] (10 bins), i.e. whether the drift has the replicator-mutator form; and
'explained' = share of var(dx) explained by the law, by the binned drift and by the oracle bound
1 - within-(eps, tick) spread is not available here (no branches), so only the first two.
Scan (one-at-a-time, paired keys). Per setting: viability, paired shifts of trajectory statistics against the
null setting, and the theta-plug-in deficit (headroom, EXAM 4.5) at level 2 (h = 8, 16, 32) and on the level-1
block raster (h = 1, 2, 4, 8): mean over branch states of ES_fair(controls under theta_0, truths) - ES_loo(truths),
divided by D_h = S_clim - S_oracle of the null setting (climatology = the truths of the other members at the same
anchor and horizon).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vxlib as VX  # noqa: E402

import numpy as np  # noqa: E402

from vw.scoring import energy_fair, energy_loo  # noqa: E402

D = sys.argv[1]
SCAN_D = sys.argv[2] if len(sys.argv) > 2 else D                 # the scan may come from a second run (job 2, scan/)
RES = os.path.join(HERE, "results")
os.makedirs(RES, exist_ok=True)
IX = {n: i for i, n in enumerate(VX.S1_NAMES)}
out = {"source_dir": os.path.basename(os.path.normpath(D))}


def J(name):
    p = os.path.join(D, name)
    return json.load(open(p)) if os.path.exists(p) else None


info = J("info.json")
out["info"] = {k: info.get(k) for k in ("backend", "devices", "versions", "H_exam", "H_rule", "bmax", "rate", "hours",
                                         "failed")}
bench = J("bench.json")
# memory: bench.json's per-row figure is the process-wide running peak up to that row, not the row's own peak
# (the Mac's review, point 4), so it is named accordingly here
out["bench"] = [{k: r.get(k) for k in ("H", "B", "track", "member_ticks_per_s", "native_steps_per_s", "first_call_s",
                                       "tracker_update_s_per_member", "host_level12_s_per_member_tick", "K", "error")}
                | {"process_peak_bytes_so_far": (r.get("memory") or {}).get("peak_bytes_in_use")} for r in bench["rows"]]


# ----------------------------------------------------------------------------- law
def law_fit(x, h=16, t0=63):
    """x (J, T) -> b (2,), rows."""
    a = x[:, t0:-h].ravel()
    d = (x[:, t0 + h:] - x[:, t0:-h]).ravel()
    A = np.stack([a * (1 - a), 1 - 2 * a], 1)
    b = np.linalg.lstsq(A, d, rcond=None)[0]
    return b, a, d, A


def law_block(tag):
    p = os.path.join(D, f"{tag}.npz")
    if not os.path.exists(p):
        return None
    Z = np.load(p)
    S, eps = Z["S"].astype(float), Z["eps"]
    nE, Jm, T, _ = S.shape
    rng = np.random.default_rng(0)
    res = {"eps": eps.tolist(), "J": int(Jm), "T": int(T), "H": J(f"{tag}.json")["H"],
           "member_ticks_per_s": J(f"{tag}.json")["member_ticks_per_s"], "vars": {}}
    for var in ("s_b", "fb_mass"):
        X = S[..., IX[var]]
        rows = []
        for e in range(nE):
            b, a, d, A = law_fit(X[e])
            bb = []
            for _ in range(200):
                k = rng.integers(0, Jm, Jm)
                bb.append(law_fit(X[e][k])[0])
            bb = np.array(bb)
            fit = A @ b
            bins = np.clip((a * 10).astype(int), 0, 9)
            bm = np.array([d[bins == q].mean() if (bins == q).sum() > 20 else np.nan for q in range(10)])
            fm = np.array([fit[bins == q].mean() if (bins == q).sum() > 20 else np.nan for q in range(10)])
            cnt = np.array([(bins == q).sum() for q in range(10)])
            okb = np.isfinite(bm)
            w = cnt[okb] / cnt[okb].sum()
            mu = (w * bm[okb]).sum()
            shape_r2 = 1 - (w * (bm[okb] - fm[okb]) ** 2).sum() / max((w * (bm[okb] - mu) ** 2).sum(), 1e-12)
            rows.append({"eps": float(eps[e]), "b1": float(b[0]), "b2": float(b[1]), "b1_se": float(bb[:, 0].std()),
                         "b2_se": float(bb[:, 1].std()), "rate_per_time_unit": float(b[0] / (16 * VX.TICK_TIME)),
                         "explained_by_law": float(1 - ((d - fit) ** 2).mean() / d.var()),
                         "explained_by_binned_drift": float(1 - ((d - bm[bins]) ** 2)[np.isfinite(bm[bins])].mean() / d.var()),
                         "shape_r2": float(shape_r2), "binned_drift": np.round(bm, 4).tolist(),
                         "law_drift_in_bins": np.round(fm, 4).tolist(), "bin_counts": cnt.tolist(),
                         "mean_by_tick": {str(t): float(X[e][:, t - 1].mean()) for t in (100, 150, 200, 250, 300, 350, 400, 440)
                                          if t <= T},
                         "first_tick_mean_above_half": int(np.argmax(X[e].mean(0) > 0.5)) + 1
                         if (X[e].mean(0) > 0.5).any() else None})
        b1 = np.array([r["b1"] for r in rows])
        se = np.maximum(np.array([r["b1_se"] for r in rows]), 1e-6)
        A = np.stack([np.ones(nE), eps], 1)
        W = 1 / se ** 2
        c = np.linalg.solve((A * W[:, None]).T @ A, (A * W[:, None]).T @ b1) if nE > 2 else np.array([b1[0], 0.0])
        pred = A @ c
        r2 = 1 - ((b1 - pred) ** 2).sum() / max(((b1 - b1.mean()) ** 2).sum(), 1e-12)
        chi2 = float((((b1 - pred) / se) ** 2).sum())
        # strict proportionality b1 = c eps (no intercept), and the same line fitted without eps = 0
        c_prop = float((W * eps * b1).sum() / max((W * eps * eps).sum(), 1e-12))
        chi2_prop = float((((b1 - c_prop * eps) / se) ** 2).sum())
        pos = eps > 0
        cp = np.linalg.solve((A[pos] * W[pos, None]).T @ A[pos], (A[pos] * W[pos, None]).T @ b1[pos]) if pos.sum() > 2 \
            else np.array([np.nan, np.nan])
        chi2_pos = float((((b1[pos] - A[pos] @ cp) / se[pos]) ** 2).sum()) if pos.sum() > 2 else None
        res["vars"][var] = {"per_eps": rows, "b1_line": {"c0": float(c[0]), "c1": float(c[1]), "r2": float(r2),
                                                           "chi2": chi2, "dof": int(nE - 2),
                                                           "c0_over_c1_times_0p2": float(c[0] / (c[1] * 0.2)) if c[1] else None},
                            "b1_proportional": {"c": c_prop, "chi2": chi2_prop, "dof": int(nE - 1)},
                            "b1_line_eps_positive": {"c0": float(cp[0]), "c1": float(cp[1]), "chi2": chi2_pos,
                                                     "dof": int(pos.sum() - 2), "zero_crossing_eps": float(-cp[0] / cp[1])
                                                     if np.isfinite(cp[1]) and cp[1] else None},
                            "b2_mean": float(np.mean([r["b2"] for r in rows])),
                            "b2_range": [float(min(r["b2"] for r in rows)), float(max(r["b2"] for r in rows))]}
    N = S[..., IX["N"]]
    res["N_mean_ticks_100_on_by_eps"] = N[:, :, 99:].mean((1, 2)).tolist()
    res["N_sd_over_members_and_ticks"] = float(N[:, :, 99:].std())
    res["s_b_sd_ticks_100_on_by_eps"] = S[..., IX["s_b"]][:, :, 99:].std((1, 2)).tolist()
    return res


out["law"] = law_block("law")
out["law128"] = law_block("law128")

# ----------------------------------------------------------------------------- scan
if os.path.exists(os.path.join(SCAN_D, "scan_main.npz")):
    Z = np.load(os.path.join(SCAN_D, "scan_main.npz"))
    S, names = Z["S"].astype(float), [str(s) for s in Z["settings"]]
    nS, Jm, T, _ = S.shape
    sc = json.load(open(os.path.join(SCAN_D, "scan.json")))
    Hx = sc["H"]
    Kslots = VX.Runner.__init__.__defaults__ and VX.VW.slots_for(VX.VJ.Config(H=Hx, W=Hx))["K"]
    Nn = S[..., IX["N"]]
    viab = {}
    for i, nm in enumerate(names):
        ok = Z["finite"][i] & (Z["overflow"][i][:, :2].sum(1) == 0) & (Nn[i][:, 19:].min(1) >= 3) & (Nn[i][:, 19:].max(1) <= Kslots - 1)
        viab[nm] = {"viable_members": int(ok.sum()), "of": int(Jm), "N_min": float(Nn[i][:, 19:].min()),
                    "N_max": float(Nn[i].max()), "N_mean": float(Nn[i][:, 99:].mean()),
                    "all_finite": bool(Z["finite"][i].all()), "overflow_ticks": Z["overflow"][i][:, :2].sum(0).tolist()}
    stats = {"N": ("N", 99, T), "s_b_early": ("s_b", 99, 249), "s_b_late": ("s_b", 249, T), "fb_mass_late": ("fb_mass", 249, T),
             "log_mass_mean": ("log_mass_mean", 99, T), "speed": ("speed_mean", 99, T), "rg": ("rg_mean", 99, T),
             "turnover": ("turnover", 99, T), "N_pre": ("N", 19, 59)}
    shift = {}
    # job 1 computed the summaries per 40-tick chunk, so 'turnover' is 0 at the first tick of every chunk (array
    # index i with i % 40 == 0): those ticks are dropped from the turnover statistic (the Mac's review, point 3)
    for i, nm in enumerate(names):
        shift[nm] = {}
        for st, (v, a, b) in stats.items():
            tt = np.arange(a, b)
            tt = tt[tt % 40 != 0] if v == "turnover" else tt
            x = S[i][:, tt, IX[v]].mean(1)
            x0 = S[0][:, tt, IX[v]].mean(1)
            d = x - x0
            se = d.std(ddof=1) / np.sqrt(Jm) if Jm > 1 else np.nan
            shift[nm][st] = {"mean": float(x.mean()), "diff": float(d.mean()), "z_paired": float(d.mean() / se) if se > 0 else 0.0}
    scan = {"scan_dir": os.path.basename(os.path.normpath(SCAN_D)), "H": Hx, "J": int(Jm), "T": int(T), "settings": names,
            "box": sc["box"], "viability": viab, "shift": shift,
            "anchors": sc["anchors"], "R": sc["R"], "Mc": sc["Mc"]}
    pb = os.path.join(SCAN_D, "scan_branch.npz")
    if not os.path.exists(pb):                                       # the first run's file cut down on the runner Mac
        pb = os.path.join(SCAN_D, "scan_branch_small.npz")           # (L2 in full, level-1 rasters at 4 horizons)
    if os.path.exists(pb):
        B = np.load(pb)
        scan["branch_file"] = os.path.basename(pb)
        L2 = B["L2"].astype(float)                                   # (nS, J, nA, R + Mc, HB, 2)
        R, Mc = int(B["R"]), int(B["Mc"])
        nA = L2.shape[2]
        done = [a for a in range(nA) if np.abs(L2[:, :, a]).sum() > 0]
        sc2 = np.array([Nn[0][:, 99:].std(), max(S[0][:, 99:, IX["s_b"]].std(), 0.05)])
        hs2, hs1 = [8, 16, 32], [int(h) for h in B["hs1"]]

        def deficits(Yall, hs, scale):
            """Yall (nS, J, nA, R + Mc, HB, d): per setting and h: mean over states of ES(controls, truths) - ES_loo."""
            de, orc, cl = np.zeros((nS, len(hs))), np.zeros((nS, len(hs))), np.zeros((nS, len(hs)))
            for k, h in enumerate(hs):
                Yh = Yall[:, :, done][:, :, :, :, h - 1] / scale        # (nS, J, nA', R + Mc, d)
                tr, ct = Yh[:, :, :, :R], Yh[:, :, :, R:]
                es_c = energy_fair(ct, tr)                               # (nS, J, nA')
                es_o = energy_loo(tr)
                de[:, k] = (es_c - es_o).mean((1, 2))
                orc[:, k] = es_o.mean((1, 2))
                for i in range(nS):                                      # climatology: the other members' truths
                    v = []
                    for j in range(Jm):
                        oth = [q for q in range(Jm) if q != j]
                        for a in range(len(done)):
                            v.append(energy_fair(tr[i, oth, a].reshape(-1, tr.shape[-1]), tr[i, j, a]))
                    cl[i, k] = np.mean(v)
            return de, orc, cl
        d2, o2, c2 = deficits(L2, hs2, sc2)
        # level-1 raster: scored in the job (es_c1, es_o1, es_k1: (nS, J, nA, n_h)), or here from the rasters
        if "es_c1" in B.files:
            E1 = {k: B[k] for k in ("es_c1", "es_o1", "es_k1")}
        else:
            R1h = B["R1h"].astype(float)                             # (nS, J, nA, R + Mc, n_h, G2)
            E1 = {k: np.full(R1h.shape[:3] + (len(hs1),), np.nan) for k in ("es_c1", "es_o1", "es_k1")}
            sc1 = None
            for a in done:
                if sc1 is None:
                    g = R1h.shape[-1] // 2
                    sc1 = np.r_[np.full(g, max(R1h[0, :, a, :R, :, :g].std(), 1e-6)),
                                np.full(g, max(R1h[0, :, a, :R, :, g:].std(), 1e-6))]
                for k in range(len(hs1)):
                    E1["es_c1"][:, :, a, k], E1["es_o1"][:, :, a, k], E1["es_k1"][:, :, a, k], _ = \
                        VX.raster_scores(R1h[:, :, a, :, k], R, sc1)
        d1 = (E1["es_c1"] - E1["es_o1"])[:, :, done].mean((1, 2))
        o1 = E1["es_o1"][:, :, done].mean((1, 2))
        c1 = E1["es_k1"][:, :, done].mean((1, 2))
        D2, D1 = c2[0] - o2[0], c1[0] - o1[0]
        scan["branch"] = {"anchors_done": [sc["anchors"][a] for a in done], "scales_level2": sc2.tolist(),
                          "null_D_h_level2": dict(zip(map(str, hs2), D2.tolist())),
                          "null_D_h_level1_raster": dict(zip(map(str, hs1), D1.tolist())),
                          "null_oracle_level2": o2[0].tolist(), "null_clim_level2": c2[0].tolist(),
                          "null_oracle_level1": o1[0].tolist(), "null_clim_level1": c1[0].tolist()}
        head = {}
        for i, nm in enumerate(names):
            head[nm] = {"L2": dict(zip(map(str, hs2), (d2[i] / D2).tolist())), "L2_mean": float((d2[i] / D2).mean()),
                        "L1": dict(zip(map(str, hs1), (d1[i] / D1).tolist())), "L1_mean": float((d1[i] / D1).mean()),
                        "L2_own_D": float(np.mean(d2[i] / np.maximum(c2[i] - o2[i], 1e-9)))}
        scan["headroom"] = head
        table = {}
        for p in sc["box"]:
            lo, hi = f"{p}@lo", f"{p}@hi"
            if lo in head:
                table[p] = {"box": sc["box"][p],
                            "viable_both": bool(viab[lo]["viable_members"] == Jm and viab[hi]["viable_members"] == Jm),
                            "L2_lo": head[lo]["L2_mean"], "L2_hi": head[hi]["L2_mean"],
                            "L2_min_edge": min(head[lo]["L2_mean"], head[hi]["L2_mean"]),
                            "L2_mean_edges": (head[lo]["L2_mean"] + head[hi]["L2_mean"]) / 2,
                            "L1_lo": head[lo]["L1_mean"], "L1_hi": head[hi]["L1_mean"],
                            "L1_mean_edges": (head[lo]["L1_mean"] + head[hi]["L1_mean"]) / 2,
                            "z_s_b_late": [shift[lo]["s_b_late"]["z_paired"], shift[hi]["s_b_late"]["z_paired"]],
                            "z_N": [shift[lo]["N"]["z_paired"], shift[hi]["N"]["z_paired"]],
                            "max_abs_z": [max(abs(v["z_paired"]) for v in shift[lo].values()),
                                          max(abs(v["z_paired"]) for v in shift[hi].values())]}
        scan["table"] = table
        scan["null_floor"] = head["null"]
    out["scan"] = scan



def clean(o):
    """NaN and infinities -> null (strict JSON)."""
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, float) and not np.isfinite(o):
        return None
    return o


json.dump(clean(out), open(os.path.join(RES, "analysis1.json"), "w"), indent=1, allow_nan=False)
print("bench:")
for r in out["bench"]:
    print("  ", r)
for tag in ("law", "law128"):
    if out.get(tag):
        print(tag, "H", out[tag]["H"], "J", out[tag]["J"])
        for var, v in out[tag]["vars"].items():
            print("  ", var, "b1 line", {k: (round(x, 4) if isinstance(x, float) else x) for k, x in v["b1_line"].items()},
                  "b2", round(v["b2_mean"], 4))
            for r in v["per_eps"]:
                print("     eps", r["eps"], "b1", round(r["b1"], 4), "+-", round(r["b1_se"], 4), "b2", round(r["b2"], 4),
                      "law R2", round(r["explained_by_law"], 3), "binned", round(r["explained_by_binned_drift"], 3),
                      "shape", round(r["shape_r2"], 3), "mean@", r["mean_by_tick"])
if "scan" in out and "table" in out["scan"]:
    print("scan null floor", out["scan"]["null_floor"])
    for p, t in sorted(out["scan"]["table"].items(), key=lambda kv: -kv[1]["L2_min_edge"]):
        print(f"  {p:7s} viable {t['viable_both']!s:5s} L2 lo {t['L2_lo']:+.3f} hi {t['L2_hi']:+.3f} | L1 lo {t['L1_lo']:+.3f} "
              f"hi {t['L1_hi']:+.3f} | z s_b late {np.round(t['z_s_b_late'], 1).tolist()} z N {np.round(t['z_N'], 1).tolist()} "
              f"max|z| {np.round(t['max_abs_z'], 1).tolist()}")
    print("viability:", {k: (v["viable_members"], round(v["N_mean"], 1), v["N_min"], v["N_max"]) for k, v in out["scan"]["viability"].items()})
