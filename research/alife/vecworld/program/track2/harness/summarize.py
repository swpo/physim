"""summarize -- assemble results/summary.json from the stage files (every claimed number + source)."""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results")


def load(n):
    p = os.path.join(OUT, n)
    return json.load(open(p)) if os.path.exists(p) else None


def r(x, k=4):
    return None if x is None else round(float(x), k)


A, B, D = load("stageA.json"), load("stageB.json"), load("stageD.json")
C = [c for c in (load(f"stageC_w{w}.json") for w in range(3)) if c]
S = {"sources": {"A": "results/stageA.json", "B": "results/stageB.json", "C": "results/stageC_w{0,1,2}.json",
                 "D": "results/stageD.json", "code": ["run_toy.py", "toy.py", "summarize.py"],
                 "library": ["vw1/vw/secret.py", "vw1/vw/nats.py", "vw1/vw/scoring.py", "vw1/vw/harness.py",
                             "vw1/vw/tests/test_harness.py"]}}

if A:
    S["A_nats_vs_kl"] = {
        "source": "results/stageA.json", "theta_world0": A["theta"],
        "programs": {k: {"charge_nats": r(v["charge_nats"]), "closed_form_level0_kl": r(v["closed_form_level0_kl"]),
                         "charge_minus_kl": v["charge_minus_kl"], "mc_llr_nats": r(v["mc_llr"]["mc_nats"], 3),
                         "mc_llr_se": r(v["mc_llr"]["mc_se"], 3), "mc_z": r(v["mc_llr"]["z"], 2),
                         "mc_z_under_P0": r(v["mc_llr_under_P0"]["z"], 2),
                         "kl_obs_level1_stationary": r(v["kl_obs_level1_stationary"], 3),
                         "kl_obs_level1_given_history": r(v["kl_obs_level1_given_history"], 3),
                         "kl_obs_level2_given_history": r(v["kl_obs_level2_given_history"], 3),
                         "efficiency_level1_given_history": r(v["efficiency_level1_given_history"], 3),
                         "max_mean_shift_sd": r(v["max_mean_shift_sd_level1_given_history"], 3),
                         "sqrt_2C": r(v["sqrt_2C"], 3)} for k, v in A["programs"].items()},
        "rejections": A["rejections"], "cpu_s": r(A["cpu_s"], 1)}

if B:
    S["B_estimators"] = {"source": "results/stageB.json", "n_items": B["n_items"], "R": B["R"],
                         "truth_law_check": B["truth_law_check"],
                         "exam": {k: {kk: r(vv) for kk, vv in v.items()} for k, v in B["exam_estimates"].items()},
                         "redraws_400": {k: {kk: r(vv, 5) for kk, vv in v.items()} for k, v in B["redraw_estimates"].items()},
                         "oes_B3": {k: (r(v) if isinstance(v, float) else v) for k, v in B["oes_B3"].items()},
                         "cpu_s": r(B["cpu_s"], 1)}

if C:
    budgets = ["zero", "small_passive", "small_active", "large_passive", "large_active"]
    tab = {}
    names = set()
    for c in C:
        names |= set(c["report"]["aggregate"])
    for nm in sorted(names):
        vals = [c["report"]["aggregate"].get(nm) for c in C]
        ses = [c["report"]["se"].get(nm) for c in C]
        tab[nm] = {"per_world": [r(v, 3) for v in vals], "se_per_world": [r(v, 3) for v in ses],
                   "mean": r(np.mean([v for v in vals if v is not None]), 3)}
    S["C_budget_study"] = {
        "source": "results/stageC_w*.json", "thetas": [c["theta"] for c in C],
        "valid_cells_per_world": [[cc for cc, ok in zip(c["report"]["cells"], c["report"]["valid"]) if ok] for c in C],
        "oes_aggregate": tab,
        "by_class": [{k: {kk: r(vv, 3) for kk, vv in v.items() if kk in ("B3_true_theta", "ctrl_ignore_actions",
                                                                         "ctrl_prior_mean", "B2@small_passive",
                                                                         "B1@large_passive", "B1@large_active",
                                                                         "B2@large_passive")}
                      for k, v in c["report"]["by_group"].items()} for c in C],
        "posteriors": [{b: {k: c["budgets"][b][k] for k in ("B2_post", "B2x_post", "B2s_post") if k in c["budgets"][b]}
                        for b in c["budgets"]} for c in C],
        "B1_choice": [{b: c["budgets"][b]["B1"] for b in c["budgets"]} for c in C],
        "sbi_cost": [{b: {k: c["budgets"][b].get(k) for k in ("B2_cpu_s", "B2_member_ticks", "B2x_cpu_s",
                                                               "B2s_cpu_s", "B2s_member_ticks")}
                      for b in c["budgets"]} for c in C],
        "gaps_n128": [c["gaps_n128"] for c in C],
        "vs_aggregate": [{k: r(v, 3) for k, v in c["report_vs"]["aggregate"].items()} for c in C],
        "cpu_s": [r(c["cpu_s"], 1) for c in C]}

def pooled_from_report(rep, k):
    """Pooled and floored aggregates from a stage C report's per-cell mean scores (point estimates)."""
    ms, v = rep["mean_score"], np.array(rep["valid"])
    clim, orc, x = (np.array(ms[n]) for n in ("climatology", "oracle", k))
    pooled = (clim - x)[v].sum() / (clim - orc)[v].sum()
    floor0 = np.maximum((clim - x) / (clim - orc), 0)[v].mean()
    h8 = np.array([c[0] == 1 and c[1] <= 8 for c in rep["cells"]])
    mean_h8 = ((clim - x) / (clim - orc))[h8].mean()
    return pooled, floor0, mean_h8


if C:
    alt = {}
    for nm in sorted(names):
        vals = [pooled_from_report(c["report"], nm) for c in C if nm in c["report"]["mean_score"]]
        alt[nm] = {"pooled_per_world": [r(v[0], 3) for v in vals], "pooled_mean": r(np.mean([v[0] for v in vals]), 3),
                   "floor0_per_world": [r(v[1], 3) for v in vals], "floor0_mean": r(np.mean([v[1] for v in vals]), 3),
                   "level1_h8_mean_per_world": [r(v[2], 3) for v in vals],
                   "level1_h8_mean": r(np.mean([v[2] for v in vals]), 3)}
    S["C_budget_study"]["oes_alternatives_point"] = alt
    S["C_budget_study"]["note"] = ("oes_aggregate = EXAM 4.4 equal-weight mean over valid cells (bootstrap SE per world); "
                                   "oes_alternatives_point = pooled ratio, per-cell floor at 0 and level-1 h<=8 mean, "
                                   "recomputed from per-cell mean scores (no SE; SEs for world 0 in D2)")

D2 = load("stageD2.json")
if D2:
    keep = {}
    for k, v in D2.items():
        if "/" in k:
            keep[k] = {m: {"aggregate": {kk: v[m]["aggregate"][kk] for kk in v[m]["aggregate"]
                                          if kk in ("B0@large_passive", "B0@small_passive", "B1@small_passive",
                                                    "B1@large_passive", "B1@large_active", "B2@zero",
                                                    "B2@small_passive", "B2@large_passive", "B3_true_theta",
                                                    "ctrl_prior_mean", "ctrl_ignore_actions")},
                           "se": {kk: v[m]["se"][kk] for kk in v[m]["se"]
                                  if kk in ("B1@small_passive", "B1@large_passive", "B2@small_passive",
                                            "B2@large_passive", "B3_true_theta")},
                           "chains": v[m]["chains"]} for m in v}
    S["D2_aggregation_and_allocation_world0"] = {
        "source": "results/stageD2.json (per-item scores: results/d2_scores.npz)", "cells": D2["cells"],
        "cell_sets": D2["cell_sets"], "valid_by_own_rule": D2["valid_by_own_rule"],
        "v1_convention_valid_n128": D2["v1_convention_valid_n128"], **keep}

if D:
    S["D_item_counts"] = {"source": "results/stageD.json (own-rule cells per exam; superseded by D2)", **D}

cpu = sum(x for x in [A and A["cpu_s"], B and B["cpu_s"], D and D["cpu_s"]] if x) + sum(c["cpu_s"] for c in C)
cpu += 425.6   # D2 (results/log_D2.txt: 'D2 cpu 425.578')
S["cpu_s_total_runs"] = r(cpu, 1)
json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=1)
print(json.dumps({k: (v if k != "C_budget_study" else v["oes_aggregate"]) for k, v in S.items()
                  if k in ("C_budget_study", "cpu_s_total_runs")}, indent=1))


# ----------------------------------------------------------------------------- headline numbers (as claimed in REPORT.md)
def gap(setname, alloc, mode, budget, key):
    return D2[f"{setname}/{alloc}"][mode]["chains"][budget][key]


H = {}
if A and B and C and D2:
    P = A["programs"]
    H["nats"] = {"source": "results/stageA.json",
                 "charge_minus_closed_form_kl": {k: v["charge_minus_kl"] for k, v in P.items()},
                 "mc_llr_class_d": [r(P["d"]["mc_llr"]["mc_nats"], 3), r(P["d"]["mc_llr"]["mc_se"], 3), 8.0],
                 "mc_abs_z_max": r(max(abs(v["mc_llr"]["z"]) for v in P.values()), 2),
                 "kl_obs_given_history_range": [r(min(v["kl_obs_level1_given_history"] for v in P.values()), 3),
                                                r(max(v["kl_obs_level1_given_history"] for v in P.values()), 3)],
                 "efficiency_range": [r(min(v["efficiency_level1_given_history"] for v in P.values()), 3),
                                      r(max(v["efficiency_level1_given_history"] for v in P.values()), 3)],
                 "max_mean_shift_sd_vs_sqrt2C": [r(P["c"]["max_mean_shift_sd_level1_given_history"], 3), 4.0]}
    RB = B["redraw_estimates"]
    H["fair_vs_v1"] = {"source": "results/stageB.json",
                       "redraw_bias": {k: [r(v["bias"], 5), r(v["se"], 5), r(v["rel_bias"], 4), v["theory_v1_bias"]]
                                       for k, v in RB.items()},
                       "exam_fair_abs_z_max": r(max(abs(v["z"]) for k, v in B["exam_estimates"].items() if "fair" in k), 2),
                       "oes_B3_exact": r(B["oes_B3"]["exact"]), "oes_B3_fair_R16": r(B["oes_B3"]["fair_R16"]),
                       "oes_B3_fair_R16_se": r(B["oes_B3"]["fair_R16_se"]), "oes_B3_v1_R16": r(B["oes_B3"]["v1_R16"]),
                       "denominator_exact_per_cell": [r(x) for x in B["oes_B3"]["denominator_exact"]],
                       "denominator_v1_R16_per_cell": [r(x) for x in B["oes_B3"]["denominator_v1_R16"]]}
    w0 = C[0]["report"]
    H["equal_weight_mean_failure"] = {"source": "results/stageC_w0.json, results/stageD2.json",
                                      "B1@small_passive_mean_oes": r(w0["aggregate"]["B1@small_passive"], 3),
                                      "B1@small_passive_cell_1_16": r(w0["oes"]["B1@small_passive"][4], 2),
                                      "B3_mean_oes_se_n256_R4_valid_n128_cells":
                                          D2["valid_n128/n256_R4"]["mean"]["se"]["B3_true_theta"]}
    H["ordering_world0_pooled"] = {
        "source": "results/stageD2.json (valid_n128 cells, pooled)",
        "n128_R16_large_passive": {k: gap("valid_n128", "n128_R16", "pooled", "large_passive", k)
                                   for k in ("B1@large_passive-climatology", "B2@large_passive-B1@large_passive",
                                             "oracle-B2@large_passive", "B3_true_theta-B2@large_passive")},
        "n64_R16_large_passive": {k: gap("valid_n128", "n64_R16", "pooled", "large_passive", k)
                                  for k in ("B1@large_passive-climatology", "B2@large_passive-B1@large_passive",
                                            "oracle-B2@large_passive")},
        "n128_R16_small_passive": {k: gap("valid_n128", "n128_R16", "pooled", "small_passive", k)
                                   for k in ("B3_true_theta-B2@small_passive", "B1@small_passive-climatology",
                                             "oracle-B3_true_theta")},
        "aggregates_n128": {k: [D2["valid_n128/n128_R16"]["pooled"]["aggregate"][k],
                                D2["valid_n128/n128_R16"]["pooled"]["se"].get(k)]
                            for k in ("B1@large_passive", "B2@large_passive", "B3_true_theta")}}
    alt = S["C_budget_study"]["oes_alternatives_point"]
    H["budget_pooled_mean_of_3_worlds"] = {"source": "summary.json C_budget_study.oes_alternatives_point",
                                           **{k: alt[k]["pooled_mean"] for k in alt}}
    H["allocation_equal_truth_cost"] = {
        "source": "results/stageD2.json (valid_n128 cells, pooled)",
        "se_B2-B1_large_passive": {a: r(gap("valid_n128", a, "pooled", "large_passive", "B2@large_passive-B1@large_passive")["se"], 4)
                                   for a in ("n64_R16", "n128_R16", "n256_R4")},
        "se_oracle-B3": {a: r(gap("valid_n128", a, "pooled", "large_passive", "oracle-B3_true_theta")["se"], 4)
                         for a in ("n64_R16", "n128_R16", "n256_R4")},
        "own_rule_valid_cells": D2["valid_by_own_rule"]}
    sb = S["C_budget_study"]["sbi_cost"]
    H["sbi_cost_toy"] = {"source": "results/stageC_w*.json budgets.*",
                         "B2_member_ticks_large": sb[0]["large_passive"]["B2_member_ticks"],
                         "B2s_member_ticks_large": sb[0]["large_passive"]["B2s_member_ticks"],
                         "B2_cpu_s_large_range": [r(min(s[b]["B2_cpu_s"] for s in sb for b in ("large_passive", "large_active")), 1),
                                                  r(max(s[b]["B2_cpu_s"] for s in sb for b in ("large_passive", "large_active")), 1)],
                         "B2_ess_range": [r(min(c["budgets"][b]["B2_post"]["ess"] for c in C for b in c["budgets"]), 1),
                                          r(max(c["budgets"][b]["B2_post"]["ess"] for c in C for b in c["budgets"]), 1)],
                         "B2x_ess_range": [r(min(c["budgets"][b]["B2x_post"]["ess"] for c in C for b in c["budgets"]), 1),
                                           r(max(c["budgets"][b]["B2x_post"]["ess"] for c in C for b in c["budgets"]), 1)],
                         "B2_abs_z_vs_truth_max": r(max(abs(z) for c in C for b in c["budgets"]
                                                        for z in c["budgets"][b]["B2_post"]["z"]), 2)}
    H["gliders_gpu_estimate"] = {
        "inputs": {"cpu_s_per_member_tick": [0.136, "vw1/fresh/closure/results/summary.json data.s_per_member_tick"],
                   "gpu_member_ticks_per_s": ["1e3-1e4, UNMEASURED", "program/track1/DESIGN.md section 4 (FLOP estimate)"],
                   "sl_design": "1024 theta (4 rounds x 256) x 16 datasets x 4 episodes x (100 ticks + 50 burn-in), as B2s here",
                   "closure_training_member_ticks": [47160, "vw1/fresh/closure/results/summary.json data.member_ticks_simulated"]},
        "sl_member_ticks": 1024 * 16 * 4 * 150,
        "sl_cpu_hours": r(1024 * 16 * 4 * 150 * 0.136 / 3600, 0),
        "sl_gpu_hours": [r(1024 * 16 * 4 * 150 / 1e4 / 3600, 2), r(1024 * 16 * 4 * 150 / 1e3 / 3600, 2)],
        "filter_training": "~200k member-ticks from posterior draws (0.06-0.6 GPU-h) + ~1 GPU-h training (guess)",
        "per_run_gpu_hours": "1.3-4", "grid_3_worlds_x_3_budgets_plus_B3": "15-40"}
    H["cpu"] = {"runs_s": S["cpu_s_total_runs"], "first_stage_B_run_s": 103.8,
                "vw_suite_baseline_s": 409, "vw_suite_final_s": 412, "other_s": 60,
                "total_min": r((S["cpu_s_total_runs"] + 103.8 + 409 + 412 + 60) / 60, 1),
                "note": "all on core 1, float64; see results/log_*.txt and results/vw_tests.log"}
    H["tests"] = {"vw_suite_before": "94 passed", "vw_suite_after": "105 passed (results/vw_tests.log)",
                  "new": "vw/tests/test_harness.py, 11 tests"}
    H["example_api_cpu_s"] = 7.4
S["headline"] = H
json.dump(S, open(os.path.join(OUT, "summary.json"), "w"), indent=1)
