"""make_summary -- results/summary.json from the result files of this study (every number with its source).

usage: python -B make_summary.py
"""
import glob
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
RAW = os.path.join(RES, "raw")
FRESH = "/home/user/evalwork/vecworld/vw1/fresh/closure/results"
r4 = lambda v: None if v is None else (np.round(np.asarray(v, float), 4).tolist() if np.ndim(v) else round(float(v), 4))


def J(p):
    return json.load(open(p))


def closure_block(fn):
    d = J(fn)
    b = {"source": fn, "J": d["data"]["J"], "T": d["data"]["T"], "test_ticks": d["data"]["test_ticks"],
         "n_items": d["n_test_states"], "replicates": d["replicates"], "mlp": d["data"]["mlp"],
         "ceiling": r4(d["ceiling"]), "ceiling_se": r4(d["ceiling_se"]), "V_best": r4(d["best_level1"]),
         "best_name": d["best_name"], "V_oracle": r4(d["V_oracle"]), "V0": r4(d["V0_mean_predictor"]),
         "common_scale_V_oracle": r4(d["common_scale"]["V_oracle"]),
         "common_scale_V_oracle_se": r4(d["common_scale"]["V_oracle_se"]),
         "common_scale_V_best": r4(d["common_scale"]["V_best"]),
         "copy_check_max_abs_diff": d["copy_check_max_abs_diff"], "seconds": round(d["seconds"], 1)}
    return b, d


def main():
    S = {"what": "Track 2 wind recertification of the gliders world at sigma_w = 0.05: viability at sigma_w 0 / 0.05 / 0.1, "
                 "closure ceilings (coarse, objects; h = 1, 2, 4, 8, 16) in the wind world, free and under the exam "
                 "program mix, and the loss of an input-blind level-1 predictor on program-mix items",
         "declaration": os.path.join(RES, "declaration.json"),
         "code": {k: os.path.join(HERE, k) for k in ("wr.py", "sim.py", "feats.py", "closure_run.py",
                                                     "viability_stats.py", "make_summary.py", "declare.py",
                                                     "run_sims.sh", "run_analysis.sh", "interpretation.json")}}
    # ---------------------------------------------------------------- (a) viability
    v = J(os.path.join(RES, "viability.json"))
    S["viability"] = {"source": os.path.join(RES, "viability.json"), "decision": v["decision"],
                      "new6": {sw: {"out_of_band": v["per_sigma"]["new6"][sw]["out_of_band"],
                                    "paired_abs_z_gt_3": v["per_sigma"]["new6"][sw]["paired_abs_z_gt_3"],
                                    "passes": v["per_sigma"]["new6"][sw]["passes"]} for sw in ("0.0", "0.05", "0.1")},
                      "pooled9": {sw: {"out_of_band": v["per_sigma"]["pooled9"][sw]["out_of_band"],
                                       "paired_abs_z_gt_3": v["per_sigma"]["pooled9"][sw]["paired_abs_z_gt_3"],
                                       "passes": v["per_sigma"]["pooled9"][sw]["passes"]} for sw in ("0.0", "0.05", "0.1")},
                      "speed_p90": {lab: {sw: {k: r4(v["per_sigma"][lab][sw]["speed_p90"][k]) for k in
                                               ("mean", "paired_diff", "paired_se", "paired_z")}
                                          for sw in ("0.0", "0.05", "0.1")} | {"band": r4(v["per_sigma"][lab]["native_band"]["speed_p90"])}
                                    for lab in ("new6", "pooled9")},
                      "oracle_cost": {view: {sw: {"dV_over_Vbest": r4(v["oracle_cost"][view][sw]["dV_over_Vbest"]),
                                                  "dV_over_Vbest_se": r4(v["oracle_cost"][view][sw]["dV_over_Vbest_se"]),
                                                  "V_oracle": r4(v["oracle_cost"][view][sw]["V_oracle"])}
                                             for sw in ("0.0", "0.05", "0.1")} | {"V_best_fresh": r4(v["oracle_cost"][view]["V_best_fresh"])}
                                      for view in ("coarse", "objects")},
                      "set_F_16_members": {"out_of_band": v.get("set_F_16_members_sigma0.05_window236", {}).get("out_of_band")}}
    # ---------------------------------------------------------------- (b) closure
    C = {}
    for view in ("coarse", "objects"):
        C[view] = {}
        for tag in ("F", "M", "F_jax", "M_jax", "P"):
            sfx = "_jax" if tag.endswith("_jax") else ""
            fn = os.path.join(RES, f"closure_{tag[0]}_{view}{sfx}.json")
            if os.path.exists(fn):
                C[view][tag], _ = closure_block(fn)
        fr = J(f"{FRESH}/closure_{view}.json")
        C[view]["fresh_headline_36traj"] = {"source": f"{FRESH}/closure_{view}.json", "ceiling": r4(fr["ceiling"][:5]),
                                            "ceiling_se": r4(fr["ceiling_se"][:5]), "V_best": r4(fr["best_level1"][:5]),
                                            "V_oracle": r4(fr["V_oracle"][:5])}
        for a, b in (("F", "M"), ("F_jax", "M_jax")):
            if a in C[view] and b in C[view]:
                d = np.array(C[view][a]["ceiling"]) - np.array(C[view][b]["ceiling"])
                se = np.hypot(C[view][a]["ceiling_se"], C[view][b]["ceiling_se"])
                C[view][f"{a}_minus_{b}"] = {"ceiling_diff": r4(d), "se": r4(se), "z": r4(d / se)}
    S["closure"] = C
    # ---------------------------------------------------------------- exam effect
    E = {}
    for view in ("coarse", "objects"):
        fn = os.path.join(RES, f"closure_P_{view}.json")
        if not os.path.exists(fn):
            continue
        d = J(fn)
        ee = d["exam_effect"]
        bv = ee["best_vs_best"]
        E[view] = {"source": fn, "aware_names": d["aware_names"], "best_all": ee["best_all"], "best_blind": ee["best_blind"],
                   "V_best_all": r4(ee["V_best_all"]), "V_best_blind": r4(ee["V_best_blind"]),
                   "by_class_ceiling": {k: {"n": c["n"], "ceiling_all": r4(c["ceiling_all"]), "ceiling_blind": r4(c["ceiling_blind"]),
                                            "V_oracle": r4(c["V_oracle"]), "V_best_all": r4(c["V_best_all"])}
                                        for k, c in ee["by_class"].items()},
                   "loss": {k: {"n": c["n_items"], "loss_over_Vbest": r4(c["loss_over_Vbest"]),
                                "loss_se_over_Vbest": r4(np.array(c["loss_se"]) / np.array(ee["V_best_all"])),
                                **{f"z_n{n}_R{R}": r4(c[f"z_n{n}_R{R}"]) for n in (16, 32, 64, 128) for R in (1, 6, 16)},
                                **{f"mde80_over_Vbest_n{n}_R{R}": r4(c[f"mde80_over_Vbest_n{n}_R{R}"]) for n in (32, 64, 128) for R in (1, 16)}}
                            for k, c in bv.items()},
                   "fixed_pairs": {k: {kl: {"n": v_[kl]["n_items"], "loss_over_Vbest": r4(v_[kl]["loss_over_Vbest"]),
                                            "loss_se_over_Vbest": r4(np.array(v_[kl]["loss_se"]) / np.array(ee["V_best_all"])),
                                            **{f"z_n{n}_R16": r4(v_[kl][f"z_n{n}_R16"]) for n in (32, 64, 128)}}
                                       for kl in v_} for k, v_ in ee["fixed_pairs"].items()},
                   "twin_effect": {k: {kk: (r4(vv) if not isinstance(vv, int) else vv) for kk, vv in t.items()}
                                   for k, t in d["twin_effect"].items() if k != "ideal_loss_detectability"},
                   "ideal_loss_detectability": {k: {kk: (r4(vv) if not isinstance(vv, int) else vv) for kk, vv in t.items()}
                                                for k, t in d["twin_effect"]["ideal_loss_detectability"].items()},
                   "ar1_refit_check_max_abs_err_diff": d.get("ar1_rep_check_max_abs_V_diff"),
                   "items_meta": d["items_meta"]}
    S["exam_effect"] = E
    # ---------------------------------------------------------------- CPU
    cpu = {}
    for f in sorted(glob.glob(os.path.join(RAW, "*.npz"))):
        if "closure_" in f:
            continue
        z = np.load(f)
        if "seconds" in z:
            cpu[os.path.basename(f)] = float(np.sum(z["seconds"]))
    an = {}
    for f in sorted(glob.glob(os.path.join(RES, "closure_*.json"))):
        an[os.path.basename(f)] = round(J(f)["seconds"], 1)
    overhead = {"smoke_test": 40.6, "pipeline_tests_and_diagnostics_user_cpu": 290.0,
                "superseded_P_runs_dense_inputs_only": 215.0 + 137.4, "P_runs_crashed_at_logging_after_compute": 225.3 + 149.5,
                "viability_stats_runs": 12.0,
                "source": "logs in results/raw (an_*.log, sim_*.log) and the shell 'time' of the tests; superseded / crashed "
                          "runs are timings printed before their outputs were overwritten"}
    S["cpu_seconds"] = {"simulation_by_file": {k: round(v, 1) for k, v in cpu.items()},
                        "simulation_total": round(sum(cpu.values()), 1), "analysis_by_file": an,
                        "analysis_total": round(sum(an.values()), 1), "overhead": overhead,
                        "grand_total": round(sum(cpu.values()) + sum(an.values()) + sum(v for v in overhead.values()
                                                                                        if isinstance(v, float)), 1),
                        "core": 0}
    # throughput (seconds per member-tick) from the per-call timings
    tp = {}
    vz = np.load(os.path.join(RAW, "viab.npz"))
    tp["viab_init_burn"] = float(vz["seconds"][0]) / (18 * 50)
    tp["viab_run_contended_by_tests"] = float(vz["seconds"][1]) / (18 * 250)
    oz = np.load(os.path.join(RAW, "oracle.npz"))
    tp["oracle_branches"] = [float(s) / (12 * 6 * 16) for s in oz["seconds"]]
    fb, fr = [], []
    for f in sorted(glob.glob(os.path.join(RAW, "free_b*.npz"))):
        s = np.load(f)["seconds"]
        fb.append(float(s[1]) / (4 * 236))
        fr.append(float(s[2]) / (4 * 4 * 5 * 16))
    tp["free_base"], tp["free_branch"] = fb, fr
    pb, pr = [], []
    for f in sorted(glob.glob(os.path.join(RAW, "prog_b*.npz"))):
        s = np.load(f)["seconds"]
        m = J(f.replace(".npz", ".json"))
        ntw = sum(1 for it in m["items"] if it["klass"] != "none")
        pb.append(float(s[1]) / (4 * 200))
        pr.append(float(s[2]) / ((6 * 4 * 5 + ntw * 3) * 16))
    tp["prog_base"], tp["prog_branch"] = pb, pr
    S["throughput_s_per_member_tick"] = {k: r4(v) for k, v in tp.items()}
    mt = {"viability": 18 * 300, "oracle_branches": 3 * 12 * 6 * 16, "set_F": 16 * 286 + 16 * 4 * 5 * 16,
          "set_P": 16 * 250 + sum((6 * 4 * 5 + sum(1 for it in J(f)["items"] if it["klass"] != "none") * 3) * 16
                                  for f in sorted(glob.glob(os.path.join(RAW, "prog_b*.json")))), "smoke": 50 + 8 + 12}
    mt["total"] = sum(mt.values())
    S["member_ticks"] = mt
    INTERP = os.path.join(HERE, "interpretation.json")
    if os.path.exists(INTERP):
        S.update(J(INTERP))
    json.dump(S, open(os.path.join(RES, "summary.json"), "w"), indent=1)
    print("wrote", os.path.join(RES, "summary.json"))


if __name__ == "__main__":
    main()
