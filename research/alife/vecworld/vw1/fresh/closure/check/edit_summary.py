"""Checker edits to results/summary.json (original kept as check/summary_before_check.json)."""
import json, shutil, os
import numpy as np
RES = "/home/user/evalwork/vecworld/vw1/fresh/closure/results"
CHK = "/home/user/evalwork/vecworld/vw1/fresh/closure/check"
if not os.path.exists(f"{CHK}/summary_before_check.json"):
    shutil.copy(f"{RES}/summary.json", f"{CHK}/summary_before_check.json")
s = json.load(open(f"{CHK}/summary_before_check.json"))
rc = json.load(open(f"{CHK}/recompute.json"))
bc = json.load(open(f"{CHK}/baseline_choice.json"))
v0 = json.load(open(f"{CHK}/vw0_event_rate.json"))
rs = json.load(open(f"{CHK}/rerun_sim.json"))
e2e = json.load(open(f"{CHK}/e2e_analysis.json"))
cc, co = json.load(open(f"{RES}/closure_coarse.json")), json.load(open(f"{RES}/closure_objects.json"))
edits = []

# 1. estimator string: the best-of set also holds patchnet / patchnet_long / slotnet (the headline best predictors)
old = s["estimator"]
s["estimator"] = ("integrate/analyze.closure (VW-0 code, read only; MLP on; HORIZONS 1..32; folds j % 4) with extra JAX "
                  "predictors in the best-of set (closure_lib.closure_ext, checked equal to analyze.closure with the MLP off): "
                  "'rmlp' (residual MLP on 4 lags; never beat its baseline), coarse 'patchnet' (one residual MLP shared by the 64 "
                  "blocks, 5x5 neighbourhood, 3 lags, 300-epoch cap) and 'patchnet_long' (same, 1000-epoch cap, added in "
                  "finalize.py), objects 'slotnet' (one residual MLP shared by the 12 slots, 3 nearest neighbours, 4 lags); "
                  "each residual net sits on a per-horizon linear baseline (AR(1) or ridge_p2, chosen on validation). Bootstrap "
                  "SE over trajectories (400, test predictors held fixed: excludes fit-to-fit and baseline-choice variation)")
edits.append({"key": "estimator", "was": old, "now": s["estimator"],
              "why": "named only rmlp; the headline best predictors are patchnet_long/patchnet (coarse) and slotnet (objects)"})

# 2. validation gains of the new predictors, by horizon (min..max over 4 folds x 2 seeds)
for phi, c, nm in (("coarse", cc, "patchnet_info"), ("objects", co, "slotnet_info")):
    g = np.array([x for i in c[nm] for x in i["val_gain"]])
    s[phi][nm.replace("_info", "") + "_validation_gain_by_horizon"] = {"min": g.min(0).tolist(), "max": g.max(0).tolist(),
        "note": "1 - V_val(net)/V_val(linear baseline), per horizon 1..32, over 4 folds x 2 seeds (closure_<phi>.json)"}
edits.append({"key": "coarse.patchnet_validation_gain_by_horizon, objects.slotnet_validation_gain_by_horizon", "was": None,
              "now": "added", "why": "report quoted 21-27% (patchnet) and 5-12% (slotnet) as if for all horizons; those ranges hold "
                                     "for 1-8 ticks only (patchnet 3-7% at 16-32; slotnet 2-4% at 16, 0-0.6% at 32)"})

# 3. coarse learning-curve verdict at 16 ticks: the non-monotonicity is the baseline switch
lcv = s["coarse"]["learning_curve_verdict"]
old = lcv[4]
lcv[4] = ("non-monotone: at this horizon the residual net's linear baseline is AR(1) with 4 and 9 fit trajectories and "
          "ridge_p2 with 18 (chosen on validation); the 9-trajectory fit on AR(1) is better (V 0.764, ceiling 0.24) than the "
          "18-trajectory fit on ridge_p2 (V 0.864, ceiling 0.13); saturation undetermined")
edits.append({"key": "coarse.learning_curve_verdict[16 ticks]", "was": old, "now": lcv[4],
              "why": "check/baseline_choice.json: the non-monotone points (8 ticks 1/4->1/2, 16 ticks 1/2->all) coincide "
                     "exactly with the AR(1)->ridge_p2 baseline switch; 'fit-to-fit variance' is not shown"})
s["coarse"]["learning_curve_baseline_choice"] = {k: v for k, v in bc.items() if k.startswith("coarse")}
s["coarse"]["ceiling_caveat"] = ("lower bound, loosest at 8-16 ticks: on the same 144 test states the learning-curve patchnet "
                                 "fitted on 9 trajectories with an AR(1) baseline reaches c = 0.24 at 16 ticks (headline 0.136 +- "
                                 "0.012); the bootstrap SE does not include fit-to-fit or baseline-choice variation")
edits.append({"key": "coarse.ceiling_caveat, coarse.learning_curve_baseline_choice", "was": None, "now": "added",
              "why": "the 16-tick headline understates what an existing held-out fit already achieves"})

# 4. objects gap: SE of the base-continuation version (the report quoted best_all_se for it)
g = s["objects_gap_tau1"]
g["best_base_se"] = {"share_slot_ticks_with_event": rc["objects_gap_tau1"]["slotnet_base"]["share_slot_ticks_se"],
                     "share_of_error_on_event_slots": rc["objects_gap_tau1"]["slotnet_base"]["share_err_se"],
                     "note": "checker, bootstrap over trajectories (1000); check/recompute.json"}
g["ar1_base_se"] = {"share_slot_ticks_with_event": rc["objects_gap_tau1"]["ar1_base"]["share_slot_ticks_se"],
                    "share_of_error_on_event_slots": rc["objects_gap_tau1"]["ar1_base"]["share_err_se"],
                    "note": "checker, bootstrap over trajectories (1000); check/recompute.json"}
g["velocity_share_on_event_free_slots"] = {"best_base": rc["objects_gap_tau1"]["slotnet_base"]["vel_share_on_eventfree"],
                                           "ar1_base": rc["objects_gap_tau1"]["ar1_base"]["vel_share_on_eventfree"],
                                           "note": "share of the tau-1 squared error on velocity coords of event-free live slots"}
g["old_page_16pct_check"] = {"vw0_test_states_share": v0["test_states_share"], "vw0_test_states_share_se": v0["test_states_share_se"],
                             "vw0_test_states_counts": v0["test_states_counts"], "vw0_every_tick_share": v0["every_tick_share"],
                             "vw0_every_tick_counts": v0["every_tick_counts"],
                             "note": "VW-0 data read only, checker's rule; the old 16% was a +1.9 SE fluctuation of the 72 test "
                                     "states (VW-0 every-tick rate 11.5%); check/vw0_event_rate.json"}
g["headline_wording"] = ("tau = 1 objects gap: slot-ticks with a fusion/fission at t+1 are 11% of live slot-ticks and carry "
                         "53% +- 14% of the best predictor's (slotnet) squared error at the 144 test states; for AR(1) at every "
                         "tick (83,289 slot-ticks) 11.8% +- 0.1% carry 69% +- 1.2%. The 144-state AR(1) value is 57% +- 14%, "
                         "consistent with 69%.")
edits.append({"key": "objects_gap_tau1.{best_base_se, ar1_base_se, velocity_share_on_event_free_slots, old_page_16pct_check, headline_wording}",
              "was": None, "now": "added", "why": "SE of the quoted base version; the 144-state AR(1) share (57%) was missing from the "
                                                   "report's comparison; old 16% verified as sampling"})

# 5. chaos: plateau and 'reaches 1' statements
for phi in ("coarse", "objects"):
    c = rc[phi]["chaos"]
    s["chaos"][phi]["checker_long_curve"] = {"max": c["max"], "argmax_tick": c["argmax_h"], "mean_ticks_60_96": c["mean_h60_96"],
                                             "mean_ticks_60_96_se": c["mean_h60_96_se"],
                                             "frac_bootstrap_resamples_reaching_1": c["frac_boot_reaching_1"]}
s["chaos"]["checker_note"] = ("coarse: still rising, 0.98 of the unconditional spread by 90-96 ticks (6% of bootstrap resamples "
                              "reach 1). objects: 0.93 +- 0.025 averaged over 60-96 ticks, peak 0.996 at 71 ticks, 64% of resamples "
                              "reach 1: 'does not reach the natural spread within 96 ticks' is not established for objects.")
edits.append({"key": "chaos.{coarse,objects}.checker_long_curve, chaos.checker_note", "was": None, "now": "added",
              "why": "report: 'neither reaches 1.0 within 96 ticks' and 'plateaus at 0.93 +- 0.02' (no such number in the json)"})

s["checker"] = {"edits": edits,
                "verified": {
                    "vw1_only": "sim_closure.py builds RecWorld(aworld.MapWorld(specs['both'])) and calls only Designer.ensemble/"
                                "clone/rollout and aworld.chunked_rollout; analyze.py is imported for its numpy estimators and "
                                "objects_stats (it imports lenia_world/flowlenia at import time; no VW-0 simulator call)",
                    "rerun_bit_for_bit": {k: v for k, v in rs.items() if k != "world"},
                    "rerun_note": "sim_A (seed 301, J 18) re-simulated from scratch, ticks 0-50 of the base run and the first 4 ticks of "
                                  "the 90 tick-40 clones: L1 and tracker table identical to sim_A.npz (max |diff| 0)",
                    "recompute": "check/recompute.py (own code): oracle, V0, persistence, items, ceilings, old-set ceilings, z, "
                                 "selection check, chaos curve and crossings, tau-1 gap shares, objects stats all reproduce "
                                 "summary.json (differences only in bootstrap SEs, <= 0.003)",
                    "e2e_analysis": e2e,
                    "null": "sim_probe.json: same key, same rollout call -> 0 (L1 and x); fresh keys -> ~2 at 1 tick. There are no "
                            "shared-noise twin comparisons in this part: replicates are independent fresh-noise copies, so layout "
                            "rounding (base B=18,T=10 vs clones B=90,T=4) is irrelevant against the noise",
                    "caveat_shared_clone_keys": "both processes use world_seed 0 and the same branch counter, so clone r of member "
                                                "j in sim_A and sim_B get identical noise keys (vw counter-based noise); different "
                                                "states, so the effect on the bootstrap is negligible, but replicates are not "
                                                "independent across the two processes"},
                "files": {"report": f"{RES}/check.md", "scripts": f"{CHK}/", "summary_before_check": f"{CHK}/summary_before_check.json"}}
json.dump(s, open(f"{RES}/summary.json", "w"), indent=1)
print(len(edits), "edits")
