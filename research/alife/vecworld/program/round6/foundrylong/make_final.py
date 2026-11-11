"""make_final -- study foundrylong: results/summary.json from the committed analyses (every number with its source).

    python -B make_final.py

Reads results/analysis_stage1.json, results/analysis_stage2.json (if present), results/cpu_float64.json,
results/cpu_float32.json, results/w_*.json. PILOT ONLY: public pilot worlds; never an exam.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "results")


def J(name):
    p = os.path.join(R, name)
    return json.load(open(p)) if os.path.exists(p) else None


def r3(x):
    return None if x is None else round(float(x), 3)


def bnd(q, keys=("value", "se", "p10", "p90")):
    return {k: r3(q[k]) for k in keys if k in q}


def main():
    s1, s2 = J("analysis_stage1.json"), J("analysis_stage2.json")
    c64, c32 = J("cpu_float64.json"), J("cpu_float32.json")
    out = dict(PILOT_NEVER_REUSE_AS_EXAM=True, study="foundrylong", round=6,
               declared="DECLARED.md (commit 2ab6e7bb, before any request); deviations and addenda 1-3 in DEVIATIONS.md",
               jobs={"r6-foundrylong-001": dict(stage=1, billed_usd=4.92, run_hours=r3(s1["job_info"]["hours"]),
                                                source="origin/gpu-jobs:jobs/r6-foundrylong-001/status.json (billed), out/full/info.json"),
                     "r6-foundrylong-002": dict(stage=2, billed_usd=0.10, outcome="stopped by its own presmoke speed guard (compilation counted); addendum 4",
                                                source="origin/gpu-jobs:jobs/r6-foundrylong-002/status.json"),
                     "r6-foundrylong-003": dict(stage=2, billed_usd=3.92, run_hours=1.88, w_steps_chosen_by_speed_guard=143,
                                                source="origin/gpu-jobs:jobs/r6-foundrylong-003/status.json (billed), out/full/info.json, out/progress.txt")},
               gpu_total_usd=round(4.92 + 0.10 + 3.92, 2))
    # ---------------------------------------------------------------- stage 1
    S1 = s1["S1"]
    src1 = "results/analysis_stage1.json (make_summary.py on origin/gpu-jobs:jobs/r6-foundrylong-001/out/full/scores.npz)"
    st1 = dict(source=src1, n_worlds=s1["n_worlds"], p0_worlds=s1["p0_worlds"], c_episodes=s1["c_episodes"])
    st1["S1"] = dict(criterion="sigma(16 ticks, 32 Lab episodes): SURVIVES if p10 >= 0.15 with all worlds and each left out; CLOSED if p90 < 0.15 likewise",
                     verdict=S1["verdict"], point=r3(S1["point"]), p10_all=r3(S1["lower_bound_all"]), p90_all=r3(S1["upper_bound_all"]),
                     p10_min_leave_one_out=r3(S1["lower_bound_min_over_leave_one_out"]), p90_max_leave_one_out=r3(S1["upper_bound_max_over_leave_one_out"]),
                     point_range_leave_one_out=[r3(x) for x in S1["point_range_leave_one_out"]], median_world=r3(S1["median_world"]),
                     null=S1["null_all"], C=S1["C_all"], incomplete=S1["incomplete"], stage2_runs=S1["stage2_runs"])
    a = S1["S1a"]
    st1["S1a"] = dict(reading=a["reading"], gain_last_step_prior_worlds=bnd(a["gain_last_step_prior_worlds"]),
                      gain_double_schedule_seed0=r3(a["gain_double_schedule_seed0"]), gain_reference_last_data_step=bnd(a["gain_reference_last_data_step"]),
                      lower_bound_after_one_more_step_of_the_null=r3(a["lower_bound_after_one_more_step_of_the_null"]),
                      upper_bound_after_one_more_step_of_C=r3(a["upper_bound_after_one_more_step_of_C"]))
    st1["sigma_by_cell"] = {k: dict(point=r3(v["point"]), p10=r3(v["lower_bound_all"]), p90=r3(v["upper_bound_all"]),
                                    p10_min_loo=r3(v["lower_bound_min_over_leave_one_out"]), verdict_by_S1_rule=v["verdict"], null=v["null_all"])
                            for k, v in s1["sigma"].items()}
    st1["skill"] = {b: {h: r3(v["value"]) for h, v in hv.items()} for b, hv in s1["skill"].items()}
    st1["S3_prior_worlds"] = {h: dict(s0={w: r3(x["value"]) for w, x in v["s0"].items()},
                                      steps=[dict(frm=s["frm"], to=s["to"], fall=r3(s["fall_of_s0"]["value"]), se=r3(s["fall_of_s0"]["se"]),
                                                  reading=s["fall_of_s0"]["reading"]) for s in v["steps"]],
                                      doubled_schedule_fall=r3(v.get("double_schedule_seed0_fall_of_s0"))) for h, v in s1["S3"].items()}
    st1["S4_reference_data"] = {h: dict(skill={n: r3(x) for n, x in v["skill"].items()},
                                        steps=[dict(frm=s["frm"], to=s["to"], gain=r3(s["gain_of_skill"]["value"]), se=r3(s["gain_of_skill"]["se"])) for s in v["steps"]],
                                        verdict=v["verdict"]) for h, v in s1["S4"].items()}
    st1["S5_actions"] = {h: dict(program=bnd(v["program"], ("value", "p05", "p95")), regional=r3(v["d"]["value"]), aimed=r3(v["c"]["value"]),
                                 blind=r3(v["b"]["value"]), verdict=v["verdict"]) for h, v in s1["S5"].items()}
    st1["S2_training_rule"] = {f: dict(nets=v["nets"], steps=v["schedule_steps"], trained_by_horizon=v["trained_by_horizon"],
                                       late_gain_max=v.get("late_gain_max_by_horizon"), chosen_rates=v.get("chosen_rate_counts_by_horizon"))
                               for f, v in s1["S2"].items()}
    out["stage1"] = st1
    # ---------------------------------------------------------------- stage 2
    if s2:
        src2 = "results/analysis_stage2.json (make_summary2.py on origin/gpu-jobs:jobs/r6-foundrylong-002/out/full/scores.npz)"
        inc = (s2.get("completeness") or {}).get("incomplete", ["completeness not computed"])
        st2 = dict(source=src2, readable=not inc, incomplete=inc, w_steps=(s2.get("completeness") or {}).get("w_steps"),
                   verdict=s2["verdict"] if not inc else dict(stage2="incomplete: T1-T6 are values without verdicts", criteria_values=s2["verdict"]["criteria"]),
                   picks=s2["picks"])
        st2["T1_sigma_G"] = {h: dict(point=r3(v["point"]), p10=r3(v["lower_bound_all"]), p90=r3(v["upper_bound_all"]),
                                     p10_min_loo=r3(v["lower_bound_min_over_leave_one_out"]), p90_max_loo=r3(v["upper_bound_max_over_leave_one_out"]),
                                     G=v["all"]["G"], verdict=v["verdict"]) for h, v in s2["T1"].items()}
        st2["T2_generic_share"] = dict(verdict=s2["T2"]["verdict"], G=s2["T2"]["G"], rho=bnd(s2["T2"]["rho_G"]),
                                       P0_minus_C=s2["T2"]["P0_minus_C"])
        st2["T3_recovery"] = {h: dict(G=v["G"], W=v["W"], recovery=bnd(v["recovery"]), W_beats_G_t=r3(v["W_beats_G"]["t"]),
                                      W_beats_G_mean=r3(v["W_beats_G"]["mean"]), worlds_W_better=v["W_beats_G"]["worlds_positive"], holds=v["holds"])
                              for h, v in s2["T3"].items() if isinstance(v, dict) and "G" in v}
        st2["T3_leave_one_out_16"] = [dict(left_out=r["left_out"], recovery=r3(r["recovery_value"]), holds=r["holds"]) for r in s2["T3"]["16"]["leave_one_out"]]
        st2["T4_experiments"] = {h: dict(W=[v["W_mix"], v["W_designed"]], G=[v["G_mix"], v["G_designed"]],
                                         gain_W=dict(mean=r3(v["gain_W"]["mean"]), se=r3(v["gain_W"]["se"]), t=r3(v["gain_W"]["t"])),
                                         gain_G=dict(mean=r3(v["gain_G"]["mean"]), se=r3(v["gain_G"]["se"]), t=r3(v["gain_G"]["t"])),
                                         difference=dict(mean=r3(v["difference"]["mean"]), se=r3(v["difference"]["se"])),
                                         same_policy={b: dict(mean=r3(x["mean"]), se=r3(x["se"])) for b, x in v["same_policy"].items()}, holds=v["holds"])
                                 for h, v in s2["T4"].items()}
        st2["T5_actions"] = {h: dict(program=bnd(v["program"], ("value", "p05", "p95")), verdict=v["verdict"]) for h, v in s2["T5"].items()}
        st2["T6"] = s2["T6"]
        st2["skill"] = {b: {h: r3(v["value"]) for h, v in hv.items()} for b, hv in s2["skill"].items()}
        st2["W_pipeline"] = s2.get("W_pipeline")
        st2["W_fits"] = s2.get("W_fits")
        st2["job_info"] = s2.get("job_info")
        # readings declared in DECLARED.md section 3 and addendum 5 (not criteria)
        k = st2["skill"]
        c4096_truth = s1["skill"]["C4096"]["16"]["value"]
        st2["readings_16_ticks"] = dict(
            W_true_minus_C=s2["W_pipeline"]["16"]["Wtrue_minus_C"],
            W_true_skill=k["Wtrue"]["16"], C_skill=k["C16384"]["16"], W_fit_skill=k["Wm"]["16"], W_prior_skill=k["Wprior"]["16"],
            W_fit_share_of_way_from_prior_to_true_weights=r3((k["Wm"]["16"] - k["Wprior"]["16"]) / (k["Wtrue"]["16"] - k["Wprior"]["16"])),
            W_plus_skill=k["Wpm"]["16"], C4096_at_true_weights_stage1=r3(c4096_truth),
            note=("W_true_minus_C is L(C) - L(W(true)) per world (negative: C better). W(true) below C means the predictor's state inference, not the law, is the first limit (DECLARED section 3); "
                  "W+ trains the 4,096-episode C recipe at the fitted weights, so its ceiling is C(4,096) at the truth (addendum 5)"))
        out["stage2"] = st2
    # ---------------------------------------------------------------- W on CPU (before the stage-2 job)
    wt = {}
    for f, what in (("w_cpu_seed2027-46.json", "W predictor at the true / perturbed / another world's weights (test 1)"),
                    ("w_fit1tick_seed2027-46.json", "fit with the one-tick loss (superseded)"),
                    ("w_fitk16_seed2027-46.json", "fit with the 16-tick loss from a 30% neighbour (scalars moved too)"),
                    ("w_fitk16_other_seed2027-46.json", "fit with the 16-tick loss from another screened world")):
        d = J(f)
        if d:
            wt[f] = dict(what=what, skill=d.get("skill"), fits={k: dict(skill_after=v.get("skill_after"), loss_before=r3(v.get("loss_before")),
                                                                         loss_after=r3(v.get("loss_after")))
                                                                for k, v in (d.get("fit") or {}).items()},
                         fit_loss_truth=r3(d.get("fit_loss_truth")), source=f"results/{f}")
    out["W_cpu_tests"] = wt
    # ---------------------------------------------------------------- the exam profile (CPU, 2 cores)
    ep = 348
    r64 = max(v["member_ticks_per_s"] for v in c64["speed"].values())
    r32 = max(v["member_ticks_per_s"] for v in c32["speed"].values())
    gpu = 45613056 / 1094.65                                      # stage 1, 'sim C g0' (info.json)
    prof = dict(source="results/cpu_float64.json, results/cpu_float32.json (cpu_part.py, 2 pinned cores of a SHARED 4-core box: lower bounds); "
                       "GPU rate from origin/gpu-jobs:jobs/r6-foundrylong-001/out/full/info.json",
                member_ticks_per_s=dict(float64=r3(r64), float32=r3(r32), float64_by_batch={b: r3(v["member_ticks_per_s"]) for b, v in c64["speed"].items()},
                                        float32_by_batch={b: r3(v["member_ticks_per_s"]) for b, v in c32["speed"].items()}, gpu_A100_float64=round(gpu)),
                seconds_per_full_episode_348_ticks=dict(float64=r3(ep / r64), float32=r3(ep / r32)),
                full_episodes_per_hour_2_cores=dict(float64=round(3600 * r64 / ep), float32=round(3600 * r32 / ep)),
                net_ms_per_step_2_cores=dict(batch64=r3(c64["nets"]["ms_per_step_one_net_batch64"]), batch256=r3(c64["nets"]["ms_per_step_one_net_batch256"])),
                bundle=c64["bundle"])
    mt = dict(P0_prior_simulation=1000 * 64 * ep, screen_15040_draws=49271040, C16384_one_world=16384 * ep, C4096_one_world=4096 * ep,
              lab_32_episodes=32 * ep, oracle_futures_96x12x32=96 * 12 * 32)
    prof["reference_rows_member_ticks"] = mt
    prof["reference_rows_hours_on_2_cores_float64"] = {k: r3(v / r64 / 3600) for k, v in mt.items()}
    prof["reference_rows_hours_on_A100"] = {k: r3(v / gpu / 3600) for k, v in mt.items()}
    prof["training_hours_on_2_cores"] = dict(P0_40000_steps_batch256_one_seed=r3(40000 * c64["nets"]["ms_per_step_one_net_batch256"] / 3.6e6),
                                             C16384_16000_steps_batch128_one_world=r3(16000 * 0.5 * (c64["nets"]["ms_per_step_one_net_batch64"] + c64["nets"]["ms_per_step_one_net_batch256"]) / 3.6e6),
                                             FT_cv_one_world_seed_6000_steps_batch64=r3(6000 * c64["nets"]["ms_per_step_one_net_batch64"] / 3.6e6))
    prof["W_fit_on_2_cores"] = dict(seconds_per_step_16tick_loss_4ep_2members_2anchors=[11.8, 14.8],
                                    source="w_cpu.py logs of the two 16-tick fits (steps 10 to 40: 355 s / 30 steps; steps 10 to 60: 740 s / 50 steps), quoted in PROGRESS.md",
                                    minutes_200_steps=[round(200 * 11.8 / 60), round(200 * 14.8 / 60)])
    out["exam_profile"] = prof
    with open(os.path.join(R, "summary.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("wrote results/summary.json")


if __name__ == "__main__":
    main()
