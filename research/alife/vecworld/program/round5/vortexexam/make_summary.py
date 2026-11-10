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
                                 "b1_proportional": r(v.get("b1_proportional"), 4),
                                 "b1_line_eps_positive": r(v.get("b1_line_eps_positive"), 4),
                                 "share_of_change_variance_explained_by_law": r([q["explained_by_law"] for q in v["per_eps"]]),
                                 "by_binned_drift": r([q["explained_by_binned_drift"] for q in v["per_eps"]]),
                                 "shape_r2": r([q["shape_r2"] for q in v["per_eps"]]),
                                 "mean_by_tick": [r(q["mean_by_tick"]) for q in v["per_eps"]],
                                 "first_tick_mean_above_half": [q["first_tick_mean_above_half"] for q in v["per_eps"]]}
                           for var, v in L["vars"].items()},
                        "N_mean_by_eps": r(L["N_mean_ticks_100_on_by_eps"], 2)},
                       src + f" {tag} (job out {tag}.npz)",
                       "x(t+16) - x(t) = b1 x(1-x) + b2 (1-2x) + e per eps, pooled over members and ticks >= 64; "
                       "b1_line: weighted straight line b1 = c0 + c1 eps over the eps values; b1_proportional: b1 = c eps; "
                       "b1_line_eps_positive: the line fitted without eps = 0 (chi2 against the member-bootstrap SEs)")
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
                      f"results/analysis1.json scan (analyse1.py; scan files of {sc.get('scan_dir')}: scan_main.npz, "
                      f"{sc.get('branch_file')})",
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
    fams = ("net", "ridge", "law", "lin2")
    S["scores"] = V({"n_truths": P["n_truths"], "n_items": P["n_items_pooled"], "primary_cells": P["primary_cells"],
                     "items_by_program_class": P.get("items_by_program_class"),
                     "L_pooled": r(P["L_pooled"], 4), "oes": r(P["oes"]), "oes_se_items": r(P["oes_se_items"]),
                     "oes_per_cell": {k: r(P["oes_per_cell"][k]) for k in names if k.split("|")[-1] in
                                      ("P0", "C", "PM", "Cded", "K", "K0", "O_noinput") or k in ("oracle",)},
                     "cells": P["cells"]},
                    src2 + "prediction.json (L_pooled, oes, oes_se_items, oes_per_cell)",
                    "L = mean fair energy score (vw.scoring.energy_fair) over items and the primary cells (level 2 = (N, s_b) "
                    "jointly, scaled, at h = 8, 16, 32 ticks); OES = (L(K) - L) / (L(K) - L(O)), equal-weight mean over the "
                    "primary cells (vw.scoring.skill_report); K = the truth's other main runs at the same tick, K0 = design "
                    "episodes at the same tick (prior climatology), O_noinput = replicates from the hidden state without "
                    "the test program")
    acc = P["acceptance"]

    def short(a):
        return None if a is None else {
            "sigma": r(a["sigma"]), "sigma_se_worlds": r((a.get("sigma_worlds") or {}).get("se")),
            "sigma_p05_p95_worlds": r([(a.get("sigma_worlds") or {}).get(q) for q in ("p05", "p95")]),
            "null_is": a["null_is"], "rho": r(a.get("rho")), "rho_se_worlds": r((a.get("rho_worlds") or {}).get("se")),
            "rho_p05_p95_worlds": r([(a.get("rho_worlds") or {}).get(q) for q in ("p05", "p95")]),
            "pass_sigma": a["pass_sigma"], "pass_rho": a.get("pass_rho"), "n_worlds": a.get("n_worlds")}
    S["acceptance"] = V({k: short(v) for k, v in acc.items()}, src2 + "prediction.json acceptance",
                        "computed by round5/agentenv/evaluator/acceptance.py (shares): sigma = (L(null) - L(C)) / (L(K) - "
                        "L(C)), null = the better of D@n and P0; rho = (L(P0) - L(S@n)) / (L(P0) - L(C)); one predictor "
                        "family per row 'family@n'; '|S2' = posterior from level-2 histories only; '|ded' = dedicated "
                        "models (C = Cded, S = Sded); SE and 5-95% range from the bootstrap clustered by truth; bars "
                        "sigma >= 0.15 and rho <= 0.7")
    S["acceptance_per_world"] = V({k: r(v.get("per_world")) for k, v in acc.items() if "|" not in k},
                                  src2 + "prediction.json acceptance[*].per_world")
    S["gaps"] = V({k: r(v) for k, v in P["gaps_oes_item_bootstrap"].items()}, src2 + "prediction.json gaps_oes_item_bootstrap",
                  "OES gaps with a paired bootstrap over items (not clustered by truth)")
    cc = P["cchg"]
    keep = [k for k in cc["reached"] if k in ("K", "K0", "anchor", "O_noinput") or k.split("|")[-1] in ("P0", "C", "PM", "Cded")
            or k.endswith("@16") or k.endswith("@4")]
    S["cchg"] = V({"hs_ticks": cc["hs"], "coords": cc["coords"],
                   "pooled": {"oracle_predictable_share": r(cc["oracle_predictable_share"]), "V_change": r(cc["V_change"], 5),
                              "Vu": r(cc["Vu"], 5), "reached": {k: r(cc["reached"][k]) for k in keep}},
                   "within_truth": {"oracle_predictable_share": r(cc["within_truth"]["oracle_predictable_share"]),
                                    "oracle_predictable_share_per_truth": r(cc["within_truth"]["oracle_predictable_share_per_truth"]),
                                    "reached": {k: r(cc["within_truth"]["reached"][k]) for k in keep}}},
                  src2 + "prediction.json cchg",
                  "share of the oracle-predictable change reached, (V_change - Ve) / (V_change - Vu), per horizon (rows) "
                  "and coordinate (N, s_b): V_change = variance of y(a + h) - y(a) about its mean, Vu = within-item "
                  "replicate variance, Ve = mean squared error of the predictive mean (64 samples); 'pooled' over all "
                  "items as in round 3 (track1/vortex128), 'within_truth' about each truth's own mean change, summed over truths")
    if P.get("oes_by_program_class"):
        bg = P["oes_by_program_class"]
        cols = [k for k in ("K0", "O_noinput", "net|P0", "net|C", "net|Cded", "ridge|P0", "ridge|C", "law|C", "lin2|C") if k in P["oes"]]
        S["by_program_class"] = V({g: {k: r(bg[g][k]) for k in cols} for g in bg}, src2 + "prediction.json oes_by_program_class",
                                  "OES per program class of the test program (a none, b blind, c aimed, d regional); "
                                  "1 - OES(O_noinput) = the share of the K-to-O skill that needs the test program")
S["review_of_job1"] = V({
    "1 GPU-backend check": "fixed: job2.py and job1.py --scan-only assert jax.default_backend() == 'gpu' unless --smoke",
    "2 output size": "fixed: every file written atomically and under 20 MB (design summaries in parts, programs sparse, level-1 "
                     "rasters of the scan scored on the pod); job 2 audits its total",
    "3 turnover at chunk starts": "fixed: vxlib.summaries takes the previous list (job 2, scan rerun); job 1's arrays keep the "
                                  "zeros and analyse1.py / select_prior.py drop those ticks from turnover statistics",
    "4 bench memory": "relabelled process_peak_bytes_so_far in results/analysis1.json (bench.json of job 1 is unchanged)",
    "5 stage sizers": "not changed in job 1 (finished); job 2 takes its sizes from presets against the measured rate and the "
                      "scan rerun from job 2's measured rate",
    "info: atomic npz": "fixed in job1.py and job2.py (temporary name, then os.replace)"},
    "origin/gpu-jobs:jobs/r5-vortexexam-002/review.md and the coordinator's relay of it")
json.dump(S, open(os.path.join(RES, "summary.json"), "w"), indent=1)
print("wrote", os.path.join(RES, "summary.json"), "keys", list(S))
