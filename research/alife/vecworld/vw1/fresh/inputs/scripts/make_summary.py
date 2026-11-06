"""results/summary.json: every number the page states for the inputs section, with sizes, seeds,
SE or counts and the source file. Reads visibility.json, steer.json, sensitivity.json, states.json."""
import json
import os

import common as CM
import numpy as np

V = json.load(open(f"{CM.RES}/visibility.json"))
St = json.load(open(f"{CM.RES}/steer.json"))["summary"]
Se = json.load(open(f"{CM.RES}/sensitivity.json"))
S0 = json.load(open(f"{CM.RES}/states.json"))
TA = ["1", "2", "4", "8", "16", "32"]
src = lambda f: f"/home/user/evalwork/vecworld/vw1/fresh/inputs/results/{f}"  # noqa: E731


def pick(d, keys=TA):
    return {k: d[k] for k in keys}


blind = {}
for v in ("objects", "coarse"):
    for c in ("rand_x1", "rand_x8", "body_x1", "body_x8same", "k32_x1", "empty_x1"):
        r = V[v][c]
        blind[f"{v}/{c}"] = {"median_over_states": pick(r["mean_shift_snr_median"]),
                             "median_se_bootstrap": pick(r["mean_shift_snr_median_se"]),
                             "worst_state": pick(r["mean_shift_snr_worst_state"]),
                             "n_states_ge_1": pick(r["n_states_mean_shift_snr_ge_1"]),
                             "twin_snr_median": pick(r["twin_snr_median"])}
default_conds = ["rand_x1", "rand_x8", "body_x1", "body_x8same", "empty_x1"]
mx = max(V[v][c]["mean_shift_snr_median"][t] for v in ("objects", "coarse") for c in default_conds for t in TA)
mx_blind = max(V[v][c]["mean_shift_snr_median"][t] for v in ("objects", "coarse") for c in ("rand_x1", "rand_x8") for t in TA)
worst = max(((V[v][c]["mean_shift_snr_worst_state"][t], v, c, t) for v in ("objects", "coarse") for c in default_conds
             for t in TA))
n_ge1 = {f"{v}/{c}": {t: V[v][c]["n_states_mean_shift_snr_ge_1"][t] for t in TA} for v in ("objects", "coarse")
         for c in default_conds}
ps = Se["per_state"]
sens = {}
for s, r in ps.items():
    sens[s] = {
        "deposit_share_cells_for_90pct_of_sum_s": {N: r[f"N{N}"]["deposit"]["shares"]["s"]["share_cells_for_90pct"] for N in (1, 2, 4)},
        "deposit_share_cells_for_90pct_of_sum_s2": {N: r[f"N{N}"]["deposit"]["shares"]["s2"]["share_cells_for_90pct"] for N in (1, 2, 4)},
        "deposit_s2_share_in_footprint": {N: r[f"N{N}"]["deposit"]["shares"]["s2"]["share_of_total_in_footprint"] for N in (1, 2, 4)},
        "deposit_top90_s2_cells_within_4px_of_footprint": {N: r[f"N{N}"]["deposit"]["shares"]["s2"]["frac_of_those_within_4px_of_footprint"] for N in (1, 2, 4)},
        "move_share_cells_for_90pct_of_sum_s": {N: r[f"N{N}"]["move_eff_b0.5"]["shares"]["s"]["share_cells_for_90pct"] for N in (1, 2, 4)},
        "footprint_frac_A_sum_gt_1e-3": r["footprint_frac_A_sum_gt_1e-3"],
        "deposit_max_over_floor": {N: r[f"N{N}"]["deposit"]["max"] / r[f"N{N}"]["deposit"]["direct_block_mean_floor"] for N in (1, 2, 4)},
        "deposit_max_per_unit_SD": {N: r[f"N{N}"]["deposit"]["max"] for N in (1, 2, 4)},
        "linear_snr_deposit_b0.5_max_cell": {N: r[f"N{N}"]["linear_snr_deposit_b0.5_max_cell"] for N in (1, 2, 4)},
        "linear_snr_move_b0.5_max_cell": {N: r[f"N{N}"]["linear_snr_move_b0.5_max_cell"] for N in (1, 2, 4)},
        "fd_rel_err_median_best_eps": {f"N{N}_{k}": min(r["validation"][f"N{N}_{k}_eps{e:g}"]["rel_err_median"] for e in Se["eps"])
                                       for N in Se["validation_horizons"] for k in ("deposit", "move")},
        "fd_rel_err_median_by_eps": {f"N{N}_{k}_eps{e:g}": r["validation"][f"N{N}_{k}_eps{e:g}"]["rel_err_median"]
                                     for N in Se["validation_horizons"] for k in ("deposit", "move") for e in Se["eps"]},
        "deposit_excess_share_cells_for_90pct": {N: r[f"N{N}"]["deposit"]["shares_excess_over_direct_floor"]["s"]["share_cells_for_90pct"] for N in (1, 2, 4)},
        "deposit_excess_top90_within_4px_of_footprint": {N: r[f"N{N}"]["deposit"]["shares_excess_over_direct_floor"]["s"]["frac_of_those_within_4px_of_footprint"] for N in (1, 2, 4)},
        "deposit_s2_n_cells_for_90pct": {N: r[f"N{N}"]["deposit"]["shares"]["s2"]["n_cells_for_90pct"] for N in (1, 2, 4)},
        "deposit_floor_per_unit_SD": {N: r[f"N{N}"]["deposit"]["direct_block_mean_floor"] for N in (1, 2, 4)},
        "deposit_median_footprint_per_unit_SD": {N: r[f"N{N}"]["deposit"]["median_footprint"] for N in (1, 2, 4)},
        "amplitude_0.5": r["amplitude_0.5"], "oracle_Vu": r["oracle_Vu"],
        "ad_norm_median": r["ad_norm_median"], "fd_null_check_max_abs": r["fd_null_check_max_abs"],
        "jvp_vs_vjp_N4_max_rel": r["jvp_vs_vjp_N4_max_rel"],
    }
summary = {
    "world": "VW-1 A_gliders: aworld.build()['both'|'coarse'], MapWorld, world_seed 0; FlowLenia JAX float64, stride 20, "
             "Phi_coarse 192 + Phi_objects 144 (VW-0 tracker as opaque VW-1 CoarseGrain); InputPort Admissible(k=8, [-1,1], total 4, zero sum)",
    "test_states": {"n": S0["N"], "designer_ensemble_seed": S0["seed"], "ticks_after_burn_in": S0["ticks_after_burn_in"],
                    "source": src("states.json")},
    "a_blind_visibility": {
        "metric": "squared shift of the level-1 conditional mean / oracle variance (unbiased, R noise keys, each vs its identical-noise twin)",
        "n_states": V["n_states"], "R_noise_keys": V["R_noise_keys"], "noise_keys": "member_keys(make_key(4242, s), R)",
        "program_rng": "default_rng([2026, 11, 6, s])",
        "null_check_max_abs": [V["null_check_max_abs_level0"], V["null_check_max_abs_level1"]],
        "max_median_over_default_conditions_and_horizons": mx, "max_median_blind_random": mx_blind,
        "worst_state_default": {"value": worst[0], "view": worst[1], "condition": worst[2], "tau": worst[3]},
        "n_states_ge_1_default": n_ge1, "by_condition": blind, "admissible_default": V["admissible_default"],
        "moved_matter_per_program": V["moved_matter_per_program"],
        "random_admissible_commands": V["random_admissible_commands"], "matter_footprint": V["matter_footprint"],
        "source": src("visibility.json")},
    "d_late_differences": {
        "condition": "empty_x1: 4 sources -0.5 / 4 sinks +0.5 on cells with A_sum < 1e-4, >= 8 px from tracked bodies, one tick",
        "moved_matter": V["moved_matter_per_program"]["empty_x1"],
        "first_tick_twin_snr_ge_1": {v: {k: V[v]["empty_x1"]["first_tick_twin_snr_ge_1"][k] for k in ("median", "p25", "p75", "n_never_by_32")}
                                     for v in ("objects", "coarse")},
        "twin_snr_median": {v: pick(V[v]["empty_x1"]["twin_snr_median"]) for v in ("objects", "coarse")},
        "rand_x1_first_tick_twin_snr_ge_1": {v: {k: V[v]["rand_x1"]["first_tick_twin_snr_ge_1"][k] for k in ("median", "p25", "p75", "n_never_by_32")}
                                             for v in ("objects", "coarse")},
        "n_states": V["n_states"], "source": src("visibility.json")},
    "b_steering": {k: St[k] for k in ("all", "flank", "lead", "flank+", "flank-", "lead+", "lead-", "n_targets", "n_runs_total",
                                      "n_runs_dropped_identity_lost_within_7_ticks", "all_commands_admissible",
                                      "moved_per_steered_tick_median", "null_check_max_abs_x", "null_check_max_abs_table",
                                      "ticks", "members", "video_run")},
    "c_sensitivity": {"states": Se["states"], "eps": Se["eps"], "n_eff_outputs": Se["n_eff_outputs"],
                      "per_state": sens, "source": src("sensitivity.json")},
}
summary["b_steering"]["noise_key"] = "member_keys(make_key(5151, 1), n_targets), one key per target block"
summary["b_steering"]["source"] = src("steer.json")
summary["media"] = {f: os.path.getsize(f"{CM.MEDIA}/{f}") for f in sorted(os.listdir(CM.MEDIA))}
json.dump(summary, open(f"{CM.RES}/summary.json", "w"), indent=1)
print(json.dumps(summary, indent=1)[:6000])

# CPU accounting (core 2 only; one heavy process at a time), parsed from the run logs
import re  # noqa: E402
vis_tot = sum(float(m) for m in re.findall(r"state 7 .*\(total (\d+)s\)|state 31 .*\(total (\d+)s\)",
                                           open(f"{CM.RES}/visibility.log").read()) for m in m if m)
summary["cpu_seconds"] = {"states": S0["seconds"], "visibility_32_states": vis_tot,
                          "visibility_lost_to_a_killed_job": 190.0,
                          "steering_sim_x2_identical_reruns": 2 * St["sim_seconds"],
                          "sensitivity_3_states": Se["seconds_total"],
                          "note": "plus about 6 min of timing probes, tests, analysis and rendering"}
summary["cpu_seconds"]["total_hours_approx"] = round((sum(v for v in summary["cpu_seconds"].values()
                                                          if isinstance(v, float)) + 360) / 3600, 2)
json.dump(summary, open(f"{CM.RES}/summary.json", "w"), indent=1)
print(summary["cpu_seconds"])
