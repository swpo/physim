"""make_summary -- results/summary.json for round 5 study vortexexam: every number with its source.

    python -B make_summary.py        (reads results/analysis1.json, results/job1/*, results/job2/*, prior.json)

results/job1 and results/job2 hold the files copied from origin/gpu-jobs:jobs/<job_id>/ (status.json and the small
JSON outputs; the arrays stay on the gpu-jobs branch).
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
J1, J2 = "r5-vortexexam-002", os.environ.get("VX_JOB2", "r5-vortexexam-003")


def load(*p):
    f = os.path.join(RES, *p)
    return json.load(open(f)) if os.path.exists(f) else None


def V(value, source, note=None):
    d = {"value": value, "source": source}
    if note:
        d["note"] = note
    return d


def r(x, n=3):
    if isinstance(x, (list, tuple)):
        return [r(v, n) for v in x]
    if isinstance(x, dict):
        return {k: r(v, n) for k, v in x.items()}
    if isinstance(x, float):
        return round(x, n)
    return x


def job_cost(st):
    if st is None:
        return None
    pods = st.get("pods") or []
    hrs = None
    for k in ("pod_hours", "hours"):
        if k in st:
            hrs = st[k]
    return {"state": st.get("state"), "billed_usd": (st.get("cost") or {}).get("billed_usd"),
            "conservative_usd": (st.get("cost") or {}).get("conservative_usd"), "pod_hours": hrs,
            "gpu": [p.get("gpu") for p in pods], "provider": [p.get("provider") for p in pods],
            "rate_usd_hr": [p.get("rate_usd_hr") for p in pods], "cap_usd": st.get("cap_usd"),
            "pods": [{k: p.get(k) for k in ("created_at", "ready_at", "terminated_at", "billed_usd", "state")} for p in pods]}


S = {"study": "round 5, vortexexam (track 2): exam pilot on the fed-vortex world", "date": "2026-11-09/10",
     "PILOT_NEVER_REUSE_AS_EXAM": True}
A1 = load("analysis1.json")
st1, st2 = load("job1", "status.json"), load("job2", "status.json")
old = [load("job_r5-vortexexam-001_status.json")]
S["gpu"] = V({J1: job_cost(st1), J2: job_cost(st2),
              "r5-vortexexam-001": {"state": (old[0] or {}).get("state"), "billed_usd": ((old[0] or {}).get("cost") or {}).get("billed_usd")}},
             f"origin/gpu-jobs:jobs/<job>/status.json (copied to results/job1, results/job2)")

if A1:
    src = f"results/analysis1.json (analyse1.py on origin/gpu-jobs:jobs/{J1}/out)"
    S["platform_job1"] = V(A1["info"], src + " info")
    S["throughput"] = V(r(A1["bench"], 4), src + " bench (job out bench.json)",
                        "member-ticks per second, float64 world with the vortex tracker, jax.vmap batch B; "
                        "one tick = 250 native steps = 5 time units")
    for tag in ("law", "law128"):
        if A1.get(tag):
            L = A1[tag]
            S[tag] = V({"H": L["H"], "J_per_eps": L["J"], "T_ticks": L["T"], "eps": L["eps"],
                        "member_ticks_per_s": r(L["member_ticks_per_s"], 1),
                        **{var: {"b1_per_eps": r([q["b1"] for q in v["per_eps"]], 4),
                                 "b1_se": r([q["b1_se"] for q in v["per_eps"]], 4),
                                 "b2_per_eps": r([q["b2"] for q in v["per_eps"]], 4),
                                 "b1_line": r(v["b1_line"], 4),
                                 "share_of_change_variance_explained_by_law": r([q["explained_by_law"] for q in v["per_eps"]]),
                                 "by_binned_drift": r([q["explained_by_binned_drift"] for q in v["per_eps"]]),
                                 "shape_r2": r([q["shape_r2"] for q in v["per_eps"]]),
                                 "mean_by_tick": [r(q["mean_by_tick"]) for q in v["per_eps"]],
                                 "first_tick_mean_above_half": [q["first_tick_mean_above_half"] for q in v["per_eps"]]}
                           for var, v in L["vars"].items()},
                        "N_mean_by_eps": r(L["N_mean_ticks_100_on_by_eps"], 2)},
                       src + f" {tag} (job out {tag}.npz)",
                       "x(t+16) - x(t) = b1 x(1-x) + b2 (1-2x) + e per eps, pooled over members and ticks >= 64; "
                       "b1_line: weighted straight line b1 = c0 + c1 eps over the eps values")
    if "scan" in A1:
        sc = A1["scan"]
        S["scan"] = V({"H": sc["H"], "J": sc["J"], "T": sc["T"], "anchors": sc.get("branch", {}).get("anchors_done"),
                       "R": sc["R"], "Mc": sc["Mc"], "box": sc["box"],
                       "null_floor": r(sc.get("null_floor")),
                       "table": r(sc.get("table")),
                       "null_D_h_level2": r(sc.get("branch", {}).get("null_D_h_level2"), 4),
                       "null_D_h_level1_raster": r(sc.get("branch", {}).get("null_D_h_level1_raster"), 4),
                       "viability": {k: [v["viable_members"], v["of"], r(v["N_mean"], 1), v["N_min"], v["N_max"]]
                                     for k, v in sc["viability"].items()}},
                      src + " scan (job out scan_main.npz, scan_branch.npz)",
                      "headroom = theta-plug-in deficit / D_h of the null setting; L2 = mean over h 8, 16, 32 ticks of "
                      "level 2 (N, s_b); L1 = mean over h 1, 2, 4, 8 of the block raster of the vortex list; "
                      "viability entries: [viable members, of, mean N, min N, max N]")
PR = json.load(open(os.path.join(HERE, "prior.json"))) if os.path.exists(os.path.join(HERE, "prior.json")) else None
if PR:
    S["prior"] = V({k: PR[k] for k in ("H", "names", "lo", "hi", "T_ep", "prog_ticks", "c_prog", "hs", "viability", "const",
                                       "selection", "mutation")}, "prior.json (select_prior.py)")

P = load("job2", "prediction.json")
if P:
    src2 = f"origin/gpu-jobs:jobs/{J2}/out/"
    info, ident, truths, lab, vp = (load("job2", f) for f in ("info.json", "identification.json", "truths.json", "lab.json",
                                                              "viability_prior.json"))
    S["platform_job2"] = V({k: info.get(k) for k in ("backend", "devices", "versions", "rate", "bmax", "preset", "config",
                                                     "member_ticks", "member_ticks_total", "hours", "failed",
                                                     "secret_commitment")}, src2 + "info.json")
    S["truths"] = V({"names": truths["names"], "truths": r(truths["truths"], 4), "n_candidates": len(truths["candidates"]),
                     "n_viable": truths["n_viable"], "PILOT_NEVER_REUSE_AS_EXAM": True}, src2 + "truths.json",
                    "pilot truths are public by design; never to be reused as an exam")
    S["viability_prior"] = V(r(vp), src2 + "viability_prior.json")
    S["lab"] = V({"per_budget_truth0": lab[0]["per_budget"], "caps": lab[0]["caps"],
                  "nats_at_largest_budget_by_truth": [r(x["usage_final"]["total_nats"], 1) for x in lab]}, src2 + "lab.json")
    if ident:
        S["identification"] = V({"names": ident["names"], "prior_sd_theta": r(ident["prior_sd_theta"], 4),
                                 "state": r(ident["state"]), "coverage": r(ident["coverage"])},
                                src2 + "identification.json",
                                "L1 = summaries of level-1 histories, L2 = of (N, s_b) only; contraction = posterior sd / "
                                "prior sd per parameter, mean over truths; in90 = share of (truth, parameter) pairs inside "
                                "the central 90% interval")
    names = sorted(P["oes"])
    S["scores"] = V({"n_truths": P["n_truths"], "n_items": P["n_items_pooled"], "primary_cells": P["primary_cells"],
                     "L_pooled": r(P["L_pooled"], 4), "oes": r(P["oes"]), "oes_se_items": r(P["oes_se_items"]),
                     "oes_per_cell": {k: r(P["oes_per_cell"][k]) for k in names if k.split("|")[-1] in
                                      ("P0", "C", "PM", "Cded", "K") or k in ("oracle",)},
                     "cells": P["cells"]},
                    src2 + "prediction.json (L_pooled, oes, oes_se_items, oes_per_cell)",
                    "L = mean fair energy score over items and the primary cells (level 2 = (N, s_b) jointly, scaled, at "
                    "h = 8, 16, 32 ticks); OES = (L(K) - L) / (L(K) - L(O)), equal-weight mean over the primary cells")
    S["acceptance"] = V(r(P["acceptance"]), src2 + "prediction.json acceptance",
                        "sigma = (L(null) - L(C)) / (L(K) - L(C)), null = better of D@n and P0; rho = (L(P0) - L(S@n)) / "
                        "(L(P0) - L(C)); one predictor family per row; intervals: 16-84% over truth resamples")
    S["gaps"] = V({k: r(v) for k, v in P["gaps_oes_item_bootstrap"].items()}, src2 + "prediction.json gaps_oes_item_bootstrap",
                  "OES gaps with a paired bootstrap over items (not clustered by truth)")
    S["cchg"] = V(r(P["cchg"]), src2 + "prediction.json cchg",
                  "share of the oracle-predictable change reached: (V_change - Ve) / (V_change - Vu) per horizon and "
                  "coordinate (N, s_b); V_change = variance of y(a + h) - y(a) about its pooled mean, Vu = within-item "
                  "replicate variance, Ve = mean squared error of the predictive mean")
json.dump(S, open(os.path.join(RES, "summary.json"), "w"), indent=1)
print("wrote", os.path.join(RES, "summary.json"), "keys", list(S))
