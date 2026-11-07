"""run_d2 -- world 0 per-item scores for every baseline on two exams of equal-or-larger truth cost,
saved for post-hoc aggregation (results/d2_scores.npz), then the comparison of aggregation rules and
item allocations on FIXED cells (results/stageD2.json).

Exams: (n = 128, R = 16) [the stage C exam; its first 64 items give n = 64, R = 16] and
(n = 256, R = 4) [truth cost 1024 replicate futures, equal to n = 64, R = 16].
Predictors are rebuilt with the same secrets and seeds as stage C (deterministic).
Aggregations: 'mean' (EXAM 4.4: equal-weight mean of per-cell OES), 'floor0' (mean of max(OES_c, 0)),
'pooled' (sum_c (S_clim - S) / sum_c (S_clim - S_oracle)).
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_toy as RT  # noqa: E402
import toy as T  # noqa: E402
from vw.harness import Lab  # noqa: E402
from vw.scoring import cells_ok, paired_gap, skill_report  # noqa: E402

W = 0
NPZ = os.path.join(RT.OUT, "d2_scores.npz")


def build(sim):
    th = RT.theta(W)
    P = {"B3_true_theta": T.filter_predictor(th),
         "ctrl_prior_mean": T.filter_predictor(T.PRIOR_MEAN, reweight=False),
         "ctrl_ignore_actions": T.filter_predictor(th, ignore_actions=True)}
    rng0 = np.random.default_rng([W, 1])
    prior_draws = np.stack([T.draw_theta(rng0) for _ in range(RT.J_POST)])
    P["B2@zero"] = T.filter_predictor(prior_draws)
    P["B0@zero"] = T.prior_climatology(seed=W)
    for bname, (E, L, active) in RT.BUDGETS.items():
        if E == 0:
            continue
        lab = Lab(T.world(th), RT.SEC.child("agent", W, bname),
                  nats=T.nats_budget(total=T.EPISODE_CAP * E if active else 0.0), max_ticks=E * (L + 1))
        eps = T.collect(lab, E, L, active, seed=W * 100 + len(bname))
        rng = np.random.default_rng([W, len(bname), 2])
        THs, lws, _ = T.pmc(T.synthetic_loglik(sim, eps, n_rep=RT.NREP_SL, seed=W * 10 + len(bname)), rng,
                            M=RT.M_PMC, rounds=RT.ROUNDS)
        THx, lwx, _ = T.pmc(T.exact_loglik(eps), np.random.default_rng([W, len(bname), 3]), M=RT.M_PMC,
                            rounds=RT.ROUNDS)
        P[f"B0@{bname}"] = T.climatology_from_data(eps)
        P[f"B1@{bname}"] = T.fit_arx(eps)
        P[f"B2@{bname}"] = T.filter_predictor(T.posterior_draws(THs, lws, RT.J_POST, rng))
        P[f"B2x@{bname}"] = T.filter_predictor(T.posterior_draws(THx, lwx, RT.J_POST, rng))
        print("built", bname, flush=True)
    return P


def score_all():
    sim = T.Simulator()
    P = build(sim)
    out = {}
    for tag, (n, R, name) in {"n128R16": (128, 16, "exam"), "n256R4": (256, 4, "exam-R4")}.items():
        ex = RT.make_exam(W, n=n, R=R, name=name)
        refs = ex.references()
        out[f"{tag}/climatology"] = refs["climatology"]["es"]
        out[f"{tag}/oracle"] = refs["oracle"]["es"]
        out[f"{tag}/climatology_v1"] = refs["climatology"]["es_v1"]
        out[f"{tag}/oracle_v1"] = refs["oracle"]["es_v1"]
        out[f"{tag}/classes"] = ex.classes
        for k, f in P.items():
            sc = ex.score(ex.collect(f, 64, 0))
            out[f"{tag}/{k}"] = sc["es"]
            out[f"{tag}/{k}/v1"] = sc["es_v1"]
        print("scored", tag, flush=True)
    np.savez_compressed(NPZ, **out)


def analyse():
    Z = np.load(NPZ, allow_pickle=False)
    cells = [(l, t) for l in sorted(T.QUERIES) for t in T.QUERIES[l]]
    preds = sorted({k.split("/")[1] for k in Z.files if k.startswith("n128R16/") and not k.endswith("/v1")
                    and k.split("/")[1] not in ("classes", "climatology_v1", "oracle_v1")})
    v128 = cells_ok(Z["n128R16/climatology"], Z["n128R16/oracle"])
    sets = {"valid_n128": v128, "level1_h<=8": np.array([l == 1 and t <= 8 for l, t in cells])}
    res = {"cells": cells, "cell_sets": {k: v.tolist() for k, v in sets.items()},
           "valid_by_own_rule": {"n128R16": v128.tolist(),
                                 "n256R4": cells_ok(Z["n256R4/climatology"], Z["n256R4/oracle"]).tolist(),
                                 "n64R16": cells_ok(Z["n128R16/climatology"][:64], Z["n128R16/oracle"][:64]).tolist()}}
    for setname, valid in sets.items():
        for alloc, (tag, n) in {"n64_R16": ("n128R16", 64), "n128_R16": ("n128R16", 128),
                                "n256_R4": ("n256R4", 256)}.items():
            S = {k: Z[f"{tag}/{k}"][:n] for k in preds}
            rep = skill_report(S, cells=cells, valid=valid, groups=Z[f"{tag}/classes"][:n], n_boot=2000)
            entry = {}
            for mode in ("", "floor0", "pooled"):
                sfx = f"_{mode}" if mode else ""
                agg = rep["aggregate" + sfx]
                se = rep["se" + sfx]
                m = mode or "mean"
                entry[m] = {"aggregate": {k: round(agg[k], 4) for k in preds}, "se": {k: round(se[k], 4) for k in preds}}
                chains = {}
                for b in ("small_passive", "small_active", "large_passive", "large_active"):
                    ks = ["climatology", f"B0@{b}", f"B1@{b}", f"B2@{b}", "B3_true_theta", "oracle"]
                    g = {f"{c}-{a}": paired_gap(rep, c, a, mode) for a, c in zip(ks[:-1], ks[1:])}
                    g[f"oracle-B2@{b}"] = paired_gap(rep, "oracle", f"B2@{b}", mode)
                    g[f"B2@{b}-climatology"] = paired_gap(rep, f"B2@{b}", "climatology", mode)
                    g[f"B1@{b}-climatology"] = paired_gap(rep, f"B1@{b}", "climatology", mode)
                    chains[b] = {kk: {"gap": round(v["gap"], 4), "se": round(v["se"], 4), "z": round(v["z"], 2)}
                                 for kk, v in g.items()}
                entry[m]["chains"] = chains
            res[f"{setname}/{alloc}"] = entry
    # v1 conventions on the same fixed cells (n = 128, R = 16 and n = 256, R = 4)
    v1 = {}
    for tag, n in (("n128R16", 128), ("n256R4", 256)):
        S = {k: Z[f"{tag}/{k}/v1"] for k in preds if k not in ("climatology", "oracle")}
        S["climatology"], S["oracle"] = Z[f"{tag}/climatology_v1"], Z[f"{tag}/oracle_v1"]
        rep = skill_report(S, cells=cells, valid=sets["valid_n128"], n_boot=200)
        den = (S["climatology"].mean(0) - S["oracle"].mean(0))
        v1[tag] = {"aggregate": {k: round(rep["aggregate"][k], 4) for k in preds},
                   "denominator_per_cell": den.tolist()}
    res["v1_convention_valid_n128"] = v1
    json.dump(res, open(os.path.join(RT.OUT, "stageD2.json"), "w"), indent=1)


if __name__ == "__main__":
    import time
    t0 = time.process_time()
    if not os.path.exists(NPZ):
        score_all()
    analyse()
    print("D2 cpu", time.process_time() - t0)
