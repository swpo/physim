"""make_summary -- results/summary.json from the study's outputs (every number with its source), plus the
cost model of a full pilot and of the SBI baseline in member-ticks and CPU-hours.

Cost model (member-ticks, one hidden world = one truth theta; burn-in 50, prefix P = 16):
  starts        n (50 + P)
  L1 truths     n R H1                  (H1 = 16)
  L2 extension  n R2 (H2 - H1)          (level-2 cells to H2 = 64; R2 = R, or 4 as CRITIQUE 5 suggests)
  climatology   n_clim (50 + H2)        (n_clim = 256, EXAM 4.2)
  plug-in diag  n m H1                  (prior-mean plug-in from the true x_P, m = 16; optional)
  B3 training   N_b3 per truth          (true-theta level-1 predictor; 47,160 = the closure study's data)
  prior-mean control training: N_b3 once.
SBI baseline (B2): amortised NPE on summaries: N_sim draws x (50 + T_sim) member-ticks, shared by all
truths; or a per-truth synthetic likelihood (EXAM 6.3: 1,000 draws x 4 members x 100 ticks per world);
then a B1/B3-class predictor trained on posterior draws per truth.
CPU-hours at the measured 0.13-0.16 s per member-tick (this study: results/check_gworld.json, scan.json).
"""
import json
import os

import gworld as GW

RES = GW.RES
S_LO, S_HI = 0.13, 0.16


def cpu_h(mt):
    return [round(mt * S_LO / 3600, 2), round(mt * S_HI / 3600, 2)]


def exam_cost(n, R=16, H1=16, H2=64, R2=16, n_clim=256, m=16, P=16, burn=50, truths=16, N_b3=47160, plugin=True):
    per = {"starts": n * (burn + P), "L1_truths": n * R * H1, "L2_extension": n * R2 * (H2 - H1),
           "climatology": n_clim * (burn + H2), "plugin_diag": n * m * H1 if plugin else 0}
    per_truth = sum(per.values())
    tot = per_truth * truths
    return {"n_items": n, "R": R, "R2": R2, "truths": truths, "per_truth_parts": per, "per_truth": per_truth,
            "suite_member_ticks": tot, "suite_cpu_h": cpu_h(tot),
            "B3_training_member_ticks": N_b3 * (truths + 1), "B3_training_cpu_h": cpu_h(N_b3 * (truths + 1)),
            "total_with_B3_cpu_h": cpu_h(tot + N_b3 * (truths + 1))}


def sbi_cost(truths=16):
    out = {}
    for N in (1000, 4000, 10000):
        mt = N * (50 + 100)
        out[f"npe_amortised_{N}_sims_150_ticks"] = {"member_ticks": mt, "cpu_h": cpu_h(mt)}
    sl = 1000 * 4 * 100 * truths
    out["synthetic_likelihood_per_truth_EXAM"] = {"member_ticks": sl, "cpu_h": cpu_h(sl),
                                                   "note": "1,000 draws x 4 members x 100 ticks per truth (EXAM 6.3), x 16 truths"}
    post_small = 8 * 4 * 110 * truths
    post_big = 47160 * truths
    out["posterior_predictor_training"] = {"ridge_class_8draws_x4x110": {"member_ticks": post_small, "cpu_h": cpu_h(post_small)},
                                           "patchnet_class_47k_per_truth": {"member_ticks": post_big, "cpu_h": cpu_h(post_big)}}
    out["agent_real_world_ticks"] = {"member_ticks": 10000 * truths, "cpu_h": cpu_h(10000 * truths),
                                     "note": "T_max = 10,000 real ticks per agent run (EXAM 5), one run per truth"}
    return out


CPU = {"note": "wall seconds of single-threaded runs on core 1 (one heavy process at a time)",
       "check_gworld_s": 25, "refs_closure_s": 41, "scan_s": 2865, "viab_joint_full_box_s": 385,
       "viab_joint_shrunk_box_s": 388, "pilot_smoke_s": 200, "pilot_s": 3274, "ridge_size_s": 520,
       "small_tests_s": 90, "member_ticks": {"scan": 19344, "viab_joint": 5100, "pilot": 21926, "pilot_smoke": 792,
                                             "check": 42, "ridge_size": 3520}}


def headline(o):
    h = {}
    if "select" in o:
        t = o["select"]["table"]
        h["a_headroom_min_edge_L1_h2_4_8"] = {p: round(v["headroom_min_edge"], 3) for p, v in
                                              sorted(t.items(), key=lambda kv: -kv[1]["headroom_min_edge"])}
        h["a_null_noise_floor"] = o["select"]["null_noise_floor"]
        h["a_chosen"] = o["select"]["prior"]["names"]
        h["a_source"] = os.path.join(RES, "select.json")
    if "pilot" in o and "pooled" in o["pilot"]:
        r = o["pilot"]["pooled"]["report"]
        h["b_pooled_oes"] = {k: [round(r["aggregate"][k], 3), round(r["se"][k], 3)] for k in r["aggregate"]}
        h["b_pooled_gaps"] = {k: {kk: round(vv, 3) for kk, vv in v.items()} for k, v in o["pilot"]["pooled"]["gaps"].items()}
        h["b_per_truth_plugin_gap"] = {i: [round(t["gaps"]["plugin_true-plugin_prior"]["gap"], 3),
                                           round(t["gaps"]["plugin_true-plugin_prior"]["z"], 1)]
                                       for i, t in o["pilot"]["per_truth"].items()}
        h["b_per_truth_ridge_gap"] = {i: [round(t["gaps"]["ridge_true-ridge_prior"]["gap"], 3),
                                          round(t["gaps"]["ridge_true-ridge_prior"]["z"], 1)]
                                      for i, t in o["pilot"]["per_truth"].items()}
        h["b_source"] = os.path.join(RES, "pilot.json")
        h["b_pooled_oes_per_cell"] = {"cells": r["cells"], **{k: [round(x, 3) for x in r["oes"][k]] for k in r["oes"]}}
        h["b_pooled_oes_by_program_class"] = {g: {k: round(v, 3) for k, v in x.items()} for g, x in r["by_group"].items()}
    if "pilot_cells" in o:
        h["b_per_cell_gaps"] = {k: {"gap": [round(x, 3) for x in v["gap"]], "z": [round(x, 1) for x in v["z"]]}
                                for k, v in o["pilot_cells"]["pairs"].items()}
        h["b_per_cell_source"] = os.path.join(RES, "pilot_cells.json")
    if "ridge_size" in o:
        rs = o["ridge_size"]
        h["b_ridge_size"] = {"truth_index": rs["truth_index"], "cells": rs["cells"],
                             **{f"oes_gap_prior_minus_true_{n}_members": [round(x, 3) for x in g["oes_gap"]]
                                for n, g in rs["gap_prior_minus_true"].items()},
                             **{f"z_{n}_members": [round(x, 1) for x in g["z"]] for n, g in rs["gap_prior_minus_true"].items()},
                             "source": os.path.join(RES, "ridge_size.json")}
    for k in ("viab_joint_full_box", "viab_joint_shrunk_box"):
        if k in o:
            pts = o[k]["points"]
            h[f"a_{k}"] = {"lo": o[k]["lo"], "hi": o[k]["hi"], "corners_viable": sum(p["viable"] for p in pts[:16]),
                           "corners": 16, "centre_viable": pts[16]["viable"], "source": o[k]["source"]}
    if "pilot" in o:
        td = o["pilot"].get("truth_draws", {})
        h["b_truth_draws"] = {"candidates": td.get("n_candidates"), "viable": td.get("n_viable"),
                              "truths": o["pilot"]["truths"], "names": o["pilot"]["hidden"]}
    c = CPU
    tot = sum(v for k, v in c.items() if k.endswith("_s") and v)
    h["cpu_seconds_total"] = tot
    h["member_ticks_total"] = sum(c["member_ticks"].values())
    return h


def load(name):
    f = os.path.join(RES, name)
    return json.load(open(f)) if os.path.exists(f) else None


def main():
    out = {"what": "track 2 gliders_exam: (a) headroom scan of hidden global parameters of the gliders wind world; "
                   "(b) the vw exam harness wired to that world with 4 hidden parameters, small scale",
           "code": {k: os.path.join(GW.HERE, k) for k in ("gworld.py", "check_gworld.py", "refs_closure.py", "scan.py",
                                                         "select_prior.py", "viab_joint.py", "pilot.py", "make_summary.py")},
           "cpu": "core 1 (taskset -c 1), OMP_NUM_THREADS=1, single-threaded XLA, float64 simulation, float32 records"}
    for k, f in (("check_gworld", "check_gworld.json"), ("refs_closure", "refs_closure.json"),
                 ("select", "select.json"), ("prior_full_box", "prior_full.json"), ("prior", "prior.json"),
                 ("viab_joint_full_box", "viab_joint_full.json"), ("viab_joint_shrunk_box", "viab_joint.json"),
                 ("pilot", "pilot.json"), ("pilot_cells", "pilot_cells.json"), ("ridge_size", "ridge_size.json")):
        d = load(f)
        if d is not None:
            d["source"] = os.path.join(RES, f)
            out[k] = d
    scan = load("scan.json")
    if scan is not None:
        out["scan"] = {"source": os.path.join(RES, "scan.json"), "prior_boxes": scan["prior_boxes"],
                       "design": "3 members x (50 burn-in + 30 ticks); 6 branch states (3 class a, 3 class d 300 nats); "
                                 "R = 4 truths (theta) + m = 4 controls (theta_0) per state, H = 8",
                       "member_ticks": sum(r["member_ticks"] for r in scan["settings"].values()),
                       "seconds": sum(r["seconds"] for r in scan["settings"].values()),
                       "settings": {k: {kk: r[kk] for kk in ("theta", "finite", "count_min", "count_max", "count_mean",
                                                            "speed_mean", "A_sum_max_end", "deficit", "seconds",
                                                            "member_ticks")} for k, r in scan["settings"].items()}}
        for r in out["scan"]["settings"].values():
            for v in r["deficit"].values():
                v.pop("per_state", None)
    if "pilot" in out:
        sm = load("pilot_smoke.json")
        out["pilot_smoke_test"] = {"source": os.path.join(RES, "pilot_smoke.json"), "ran_end_to_end": sm is not None and "pooled" in sm,
                                   "member_ticks": None if sm is None else sm.get("member_ticks_total_this_run"),
                                   "note": "tiny sizes (4 items, R = 3, P = 3, h <= 2) to test the code path; numbers not used"}
    out["cpu_accounting"] = CPU
    out["headline"] = headline(out)
    out["cost_model"] = {"doc": __doc__.split("Cost model")[1].strip(), "s_per_member_tick": [S_LO, S_HI],
                         "full_pilot": [exam_cost(64), exam_cost(128), exam_cost(64, R2=4), exam_cost(128, R2=4),
                                        exam_cost(256, R=4, R2=4)],
                         "sbi_baseline": sbi_cost()}
    json.dump(out, open(os.path.join(RES, "summary.json"), "w"), indent=1, default=float)
    print("wrote", os.path.join(RES, "summary.json"))


if __name__ == "__main__":
    main()
