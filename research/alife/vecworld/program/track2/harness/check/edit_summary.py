"""Apply the checker's corrections to results/summary.json (headline block) and add a 'checker' block."""
import json
import sys

P = "/home/user/evalwork/vecworld/program/track2/harness/results/summary.json"
CHK = "/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/chk/"
S = json.load(open(P))
H = S["headline"]
rc = json.load(open(CHK + "recompute.json"))
rr = json.load(open(CHK + "rerun.json"))
tests = open(CHK + "vw_tests.log").read().strip().splitlines()
edits = []

# 1. GPU arithmetic: 2e5 member-ticks at 1e3-1e4 /s is 0.0056-0.056 GPU-h, not 0.06-0.6
g = H["gliders_gpu_estimate"]
g["filter_training"] = ("~200k member-ticks from posterior draws (0.006-0.06 GPU-h at 1e3-1e4 member-ticks/s) "
                        "+ ~1 GPU-h training (guess)")
g["per_run_gpu_hours"] = "1.3-3.8"
g["per_run_gpu_hours_derivation"] = "sl 0.27-2.73 + filter simulation 0.006-0.06 + training ~1.0 (guess)"
g["grid_3_worlds_x_3_budgets_plus_B3"] = "15-37"
g["grid_derivation"] = "9 B2 runs x 1.28-3.79 + 3 B3 filters x 1.006-1.056 = 14.5-37.2 GPU-h"
g["suite_truths_64_items_cpu_hours"] = [2.5, "program/track2/EXAM.md section 6.3: 64 x (16 + 16 x 64) = 66,560 "
                                        "member-ticks x 0.136 s = 2.51 h (climatology pool extra)"]
edits.append("gliders_gpu_estimate.filter_training: '0.06-0.6 GPU-h' -> '0.006-0.06 GPU-h' (factor-10 slip)")
edits.append("gliders_gpu_estimate.per_run_gpu_hours: '1.3-4' -> '1.3-3.8' (report said 1.3-4.3), derivation added")
edits.append("gliders_gpu_estimate.grid: '15-40' -> '15-37' (report said 15-45), derivation added")
edits.append("gliders_gpu_estimate.suite_truths_64_items_cpu_hours: added (report's 2.5 CPU-h was not in the summary; "
             "source EXAM 6.3)")
edits.append("sbi_cost_toy.B2_vs_B2x_note: added (within 0.01 holds for 3-world means only; per world up to 0.018)")
H["sbi_cost_toy"]["B2_vs_B2x_note"] = ("pooled B2 - B2x per world: up to 0.018 (world 2, small active: 0.928 vs 0.910); "
                                       "3-world means within 0.006 (C_budget_study.oes_alternatives_point)")

# 2. charge = KL is an algebraic identity in this toy
H["nats"]["charge_minus_closed_form_kl_note"] = (
    "identity, not a test: NatsBudget.isotropic cost and shift_kl both evaluate 1/2 sum |u_t|^2 / sigma^2; "
    "the substantive check is the Monte Carlo LLR on vw-simulated level-0 paths (mc_llr_class_d, mc_abs_z_max)")
H["nats"]["kl_obs_given_history_note"] = ("level 1, 64 ticks, Kalman covariance after the 17-frame history of "
                                           "one item (the covariance does not depend on the data)")
edits.append("nats: notes added (charge = KL is an identity; scope of the 'given history' KL)")

# 3. acceptance check 1: passes at the small passive budget under the pooled ratio
d2 = json.load(open(P.replace("summary.json", "stageD2.json")))
ch = {}
for alloc in ("n64_R16", "n128_R16", "n256_R4"):
    for mode in ("pooled", "mean"):
        c = d2[f"valid_n128/{alloc}"][mode]["chains"]["small_passive"]
        ch[f"{alloc}/{mode}"] = {k: c[k] for k in ("B1@small_passive-B0@small_passive",
                                                   "B2@small_passive-B1@small_passive",
                                                   "B3_true_theta-B2@small_passive", "oracle-B3_true_theta")}
H["acceptance_check1_world0_small_passive"] = {
    "source": "results/stageD2.json valid_n128/*/{pooled,mean}/chains/small_passive (recomputed by the checker)",
    "chains": ch,
    "verdict": ("check 1 as written (B0 < B1 < B2 < B3 < B5, every gap >= 3 paired SE) PASSES at the small passive "
                "budget under the pooled ratio at all three allocations (min z 4.5); it fails under EXAM's "
                "equal-weight mean (oracle - B3 z <= 0.96), at the large budgets (B3 - B2 z <= 1.1) and at small "
                "active (B1 < B0). It passes only because B0 (-0.78) is far below climatology while B1 is not above "
                "it (-0.07 +- 0.04).")}
edits.append("acceptance_check1_world0_small_passive: added; contradicts the report's 'cannot pass at any single budget'")

# 4. pooled ratio weights cells by their denominators
H["pooled_ratio_cell_weights_n128"] = {
    "source": "results/d2_scores.npz (checker), denominators S_clim - S_oracle per valid cell",
    "cells": [[1, 1], [1, 2], [1, 4], [1, 8], [1, 16], [2, 16]],
    "weights": rc["pooled_weight_per_valid_cell"], "weight_h_le_4": rc["pooled_weight_h<=4"],
    "weight_h16_cells": rc["pooled_weight_h16_cells"],
    "consequence": ("the pooled ratio is ~87% a level-1 h<=4 score; theta-sensitive long horizons get 3%. "
                    "World 0 n128: ctrl_prior_mean 0.826 pooled vs 0.337 equal-weight; B3 0.942 vs 0.974")}
edits.append("pooled_ratio_cell_weights_n128: added (caveat to the 'replace with pooled ratio' recommendation)")

# 5. equal-weight SE at R = 4 depends on applying n128's cells
e = H["equal_weight_mean_failure"]
e["B3_mean_oes_se_n256_R4_valid_n128_cells_note"] = (
    "uses the n128 exam's cells; the n256/R4 exam's own 3-SE rule drops the h=16 cells, and then B3's "
    f"equal-weight SE is {rc['n256_R4_own_cells_mean_se_B3']} (checker). The 10.9 is itself unstable "
    "(checker bootstrap, 4000 draws, other seed: ~20): denominators cross zero in resamples")
e["B3_mean_oes_se_n256_R4_own_cells"] = rc["n256_R4_own_cells_mean_se_B3"]
edits.append("equal_weight_mean_failure: note + own-rule SE (0.014) added to the 10.9 figure")

# 6. check 4 / theta headroom
H["theta_headroom_pooled_per_world"] = {
    "source": "results/stageC_w{0,1,2}.json report.mean_score (checker, pooled point estimates)",
    "w0": rc["pooled_w0"], "w1": rc["pooled_w1"], "w2": rc["pooled_w2"],
    "reading": ("theta is worth 0.02-0.12 pooled OES (prior-mean control vs B3). The item history closes 0-48% of "
                "that gap; the large budget closes all of it (B2 within 0.002 of B3 in every world); the small budget "
                "is in between in worlds 0 and 2 (not in world 1). Check 4's letter (B2 between B1 and B3; "
                "more budget closes part of the gap) holds; its intent (B2 near the middle) fails because the "
                "headroom is small, not because 16-tick histories identify theta")}
edits.append("theta_headroom_pooled_per_world: added (corrects the report's explanation of check 4)")

# 7. by-class numbers are equal-weight
H["aimed_items_by_class"] = {
    "source": "summary.json C_budget_study.by_class (EXAM equal-weight mean, not pooled)",
    "ctrl_ignore_actions_class_c": [x["c"]["ctrl_ignore_actions"] for x in S["C_budget_study"]["by_class"]],
    "B3_class_c": [x["c"]["B3_true_theta"] for x in S["C_budget_study"]["by_class"]]}
edits.append("aimed_items_by_class: added with source (report's -0.20..0.04 and 0.91..1.06 are equal-weight)")

# 8. untested claims
H["untested_claims"] = [
    "Lab and HistoryExam on the gliders MapWorld: no script, test or log runs them",
    "'keep at least 8 truths per item': only R = 4 and R = 16 were run",
    "filter training ~1 GPU-h: guess; GPU throughput 1e3-1e4 member-ticks/s: unmeasured"]
edits.append("untested_claims: added")

S["sources"]["D2"] = "results/stageD2.json, results/d2_scores.npz (run_d2.py)"
S["sources"]["checker"] = "check/ (recompute.py, rerun.py, edit_summary.py, outputs) and results/check.md"
edits.append("sources: D2 and checker entries added")

# 9. checker block
S["checker"] = {
    "who": "independent check, core 1",
    "vw_tests": [ln.strip() for ln in tests if "passed" in ln or "failed" in ln or ln.startswith("user")],
    "existing_vw_port_files_modified": "none (all pre-existing files predate 2026-11-07 15:35; new files only)",
    "rerun_stageA": {"max_abs_diff": rr["stageA_max_abs_diff"], "rejections_equal": rr["stageA_rejections_equal"],
                     "cpu_s": round(rr["stageA_cpu_s"], 1)},
    "rerun_world0_small_passive_end_to_end": {"reference_max_abs_diff": rr["ref_max_abs_diff"],
                                               "predictor_max_abs_diff": rr["pred_max_abs_diff"],
                                               "cpu_s": round(rr["world0_small_passive_cpu_s"], 1)},
    "independent_recompute": "scratch recompute.py (own aggregation + 4000-draw bootstrap) reproduces every "
                             "pooled/mean aggregate and gap in headline.ordering_world0_pooled and "
                             "allocation_equal_truth_cost (SEs within 0.001), and oes_B3 fair/v1 (0.9744/0.6449)",
    "figures": "none produced",
    "edits": edits}
json.dump(S, open(P, "w"), indent=1)
print("\n".join(edits))
