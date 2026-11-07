"""make_summary -- results/summary.json: every number the report claims, each with its source file."""
import json
import os

import _paths

R = _paths.RESULTS


def J(name):
    p = os.path.join(R, name)
    return json.load(open(p)) if os.path.exists(p) else None


def V(value, source, note=None):
    d = {"value": value, "source": source}
    if note:
        d["note"] = note
    return d


def main():
    out = {"study": "membrane: phase_membrane (inventory rank 2) in the vw types",
           "folder": _paths.HERE, "cpu": "core 3 only (taskset -c 3), OMP_NUM_THREADS=1, XLA single thread, float64 "
                                          "simulation, float32 saved arrays"}
    # --- reproduction
    rep = {}
    for dt in ("0.5", "1"):
        r = J(f"repro_dt{dt}.json")
        if r is None:
            continue
        src = f"results/repro_dt{dt}.json (check_repro.py {dt} {r['T_end']:g} {r['seed']})"
        rep[f"dt{dt}"] = {
            "per_step_max_rel_diff": V(r["per_step_max_rel_diff"], src, "one JAX step on numpy's state vs numpy's next "
                                       "state, max|diff|/max|field|, every 100 time units"),
            "run_max_rel_diff_end": V(r["run_max_rel_end"], src, f"JAX run vs numpy run from numpy's initial state, noise "
                                      f"off, at t = {r['T_end']:g}"),
            "null_max_rel_diff_end": V(r["null_max_rel_end"], src, "numpy vs numpy from phi (1 +- 1e-15)"),
            "run_max_rel_by_t": V(r["run_max_rel_by_t"], src), "null_max_rel_by_t": V(r["null_max_rel_by_t"], src),
            "cells_jax_eq_numpy_every_100t": V(r["cells_jax_eq_numpy_all"], src, "phi > 0.5 component counts"),
            "cpu_s_per_native_step_128": V(r["cpu_s_per_native_step_128"], src, "one core")}
    out["repro"] = rep
    # --- cost
    t = J("timing.json")
    if t:
        out["timing"] = {k: V(v, "results/timing.json (bench.py)") for k, v in t.items()}
    # --- channel
    c = J("channel.json")
    if c:
        src = "results/channel.json (check_channel.py)"
        out["channel"] = {"config": V(c["config"], src), "noise_law": V(c["noise_law"], src),
                          "kl_check_3tick_program": V(c["kl_check"], src, "Monte Carlo LLR mean vs declared charge, 4000 paths"),
                          "delivery": V(c["delivery"], src), "grid_contrast": V(c["grid_contrast"], src),
                          "v1_S_noise_sigma_equivalent_per_bump": V(c["v1_S_noise_sigma_equivalent_per_bump"], src,
                                                                    "v1 suite's proportional S noise projected on one bump"),
                          "example_costs_nats": V(c["example_costs_nats"], src)}
    e = J("explore.json")
    if e:
        src = "results/explore.json (explore.py 2 6000)"
        out["field_ranges"] = V(e["ranges"], src, "t >= 1000, every 100 t, 2 seeds per arm; justifies the channel field")
        out["threshold_sensitivity"] = V(e["thresholds"], "results/threshold.json (explore.py)",
                                         "counts and mean mass of blur(phi,1) > thr components")
        out["component_mass_hist"] = V(e["mass_hist"], src, "picks m_min = 12")
    # --- pilot
    a = J("analysis.json")
    if a:
        src = "results/analysis.json (analyse.py on pilot_*.npz)"
        out["pilot_cpu"] = V(a["cpu"], src)
        out["level1_main"] = {k: V(v, src) for k, v in a["level1_main"].items()}
        if "closure_L2_main" in a:
            cl = a["closure_L2_main"]
            out["closure_L2_main"] = {
                nm: {"ceiling_w2": V(cl[nm]["ceiling"]["2"] if "2" in cl[nm]["ceiling"] else cl[nm]["ceiling"][2], src),
                     "ceiling_w1": V(cl[nm]["ceiling"]["1"] if "1" in cl[nm]["ceiling"] else cl[nm]["ceiling"][1], src),
                     "ceiling_persistence": V(cl[nm]["ceiling_persistence"], src),
                     "oracle_share_of_V0": V(cl[nm]["oracle_share_of_V0"], src),
                     "bootstrap_w2_p16_p84": V(cl["bootstrap_w2"][nm], src)} for nm in ("N", "mean_size", "div_rate")}
            out["closure_L2_main"]["horizons_ticks"] = V(cl["horizons_ticks"], src, "1 tick = 10 time units")
            out["closure_L2_main"]["n_branch_points"] = V(cl["n_branch_points"], src)
        out["dt_check"] = V(a["dt_check"], src, "paired twins (same keys): arm minus main, window t 1000-6000")
        out["dt_check_formation"] = V(a["dt_check_formation"], src, "window t 0-1000")
        out["noise_check"] = V(a["noise_check"], src)
        out["divergence"] = V(a["divergence"], src)
        out["per_arm_means"] = V(a["per_arm_means"], src)
        out["tracker_overflow_ticks_max"] = V(a["tracker_overflow_ticks_max"], src)
    for tag, args in (("", "12 0.05 -0.03 5 30"), ("_long", "16 0.03 -0.03 20 40 _long")):
        pr = J(f"probe_input{tag}.json")
        if pr is None:
            continue
        src = f"results/probe_input{tag}.json (probe_input.py {args})"
        arms = {}
        for arm, v in pr["arms"].items():
            e = {"nats_mean": sum(v["nats_per_member"]) / len(v["nats_per_member"]),
                 "divisions_near_target": v["target_divisions_within_H"],
                 "frac_targets_with_division": v["target_divided_frac"],
                 "target_mass_end_of_input_mean": sum(v["target_mass_at_end_of_input"]) / len(v["target_mass_at_end_of_input"])}
            if "paired_L2_diff_mean" in v:
                e["paired_L2_diff_mean_(N,size,rate)"] = v["paired_L2_diff_mean"]
                e["paired_L2_diff_se"] = v["paired_L2_diff_se"]
                e["paired_N_diff_over_oracle_sd"] = v["paired_N_diff_over_oracle_sd"]
            arms[arm] = e
        out[f"probe_input{tag}"] = V({"design": {"n_members": pr["n_members"], "t0_tick": pr["t0_tick"], "ticks_on": pr["ticks_on"],
                                                 "H": pr["H"], "amps": pr.get("amps")},
                                      "arms": arms, "oracle_sd_L2_(N,size,rate)": pr["oracle_sd_L2"]}, src,
                                     "open loop, aimed once at the largest cell at tick 150; paired twins (same keys); "
                                     "oracle sd from 4 fresh-noise replicates per member")
    d = J("dtcheck_tick.json")
    if d:
        out["dt_tick_error"] = V(d, "results/dtcheck_tick.json (dtcheck_tick.py)")
    # --- headline (each number copied from the blocks above by code)
    if a and t and c:
        cl = a["closure_L2_main"]
        l1 = a["level1_main"]
        dtc = a["dt_check"]["dt025_minus_main"]
        dt1 = a["dt_check"]["dt1_minus_main"]
        nz = a["noise_check"]
        pl = J("probe_input_long.json")
        pick = lambda d, ks: {k: {kk: d[k][kk] for kk in ("diff_rel_pct", "ci95", "diff_over_seed_sd", "p_paired_t")} for k in ks}  # noqa: E731
        out["headline"] = {
            "repro_dt0.5_per_step_max_rel": V(max(rep["dt0.5"]["per_step_max_rel_diff"]["value"].values()), "repro.dt0.5"),
            "repro_dt0.5_run_vs_null_t5000": V([rep["dt0.5"]["run_max_rel_diff_end"]["value"], rep["dt0.5"]["null_max_rel_diff_end"]["value"]], "repro.dt0.5"),
            "cpu_s_native_step_jax_vs_numpy": V([rep["dt0.5"]["cpu_s_per_native_step_128"]["value"]["jax"],
                                                 rep["dt0.5"]["cpu_s_per_native_step_128"]["value"]["numpy_source"]], "repro.dt0.5"),
            "cpu_s_member_tick_L0_L1_L2_B1": V(t["world_tick_L0_L1_L2_B1_per_member_s"], "timing", "tick = 20 native steps = 10 time units"),
            "cpu_s_member_tick_pilot_main_and_branches": V([a["cpu"]["main"]["cpu_s_per_member_tick_main"], a["cpu"]["main"]["cpu_s_per_member_tick_branches"]], "pilot_cpu"),
            "kl_check": V(c["kl_check"], "channel.kl_check_3tick_program"),
            "L1_cells_N_mean_range": V([l1["N_mean_window"], l1["N_range_window"]], "level1_main"),
            "L1_fission_products_lt50_frac": V(l1["fission_products_lt50_frac"], "level1_main"),
            "L1_divisions_ge50_per_cell_per_100t": V(l1["rates_per_cell_per_100t"]["divisions_ge50_per_cell_per_100t"], "level1_main"),
            "L1_cycle_duration_t_median_iqr_n": V([l1["cycle_duration_t_median"], l1["cycle_duration_t_iqr"], l1["cycles_n"]], "level1_main"),
            "L1_cycle_mass_start_end_median": V([l1["cycle_mass_start_median"], l1["cycle_mass_end_median"]], "level1_main"),
            "L1_division_hazard_by_mass": V(l1["hazard_per_tick_by_mass"]["div"], "level1_main", "per tick; mass bins [12,50,100,150,200,300,400,600,inf)"),
            "L1_growth_dm_per_tick_by_mass": V(l1["growth_by_mass"]["mean_dm_per_tick"], "level1_main"),
            "L1_daughter_share_median_iqr": V([l1["daughter_share_median"], l1["daughter_share_iqr"]], "level1_main"),
            "L1_division_mass_balance_median": V(l1["division_mass_balance_median"], "level1_main"),
            "L2_closure_w2": V({nm: cl[nm]["ceiling"]["2"] for nm in ("N", "mean_size", "div_rate")}, "closure_L2_main",
                               "h = 1, 2, 4, 8, 16, 32 ticks; linear predictor on 2 past level-2 vectors, leave-one-seed-out: a lower "
                               "bound; 16-84% bootstrap in closure_L2_main"),
            "L2_closure_persistence": V({nm: cl[nm]["ceiling_persistence"] for nm in ("N", "mean_size", "div_rate")}, "closure_L2_main"),
            "L2_oracle_share_of_V0": V({nm: cl[nm]["oracle_share_of_V0"] for nm in ("N", "mean_size", "div_rate")}, "closure_L2_main"),
            "dt025_minus_dt05": V(pick(dtc, ("N", "mean_size", "phi_mass", "divisions_ge50_per_cell_per_100t", "size_p10")), "dt_check"),
            "dt1_minus_dt05": V(pick(dt1, ("N", "mean_size", "divisions_ge50_per_cell_per_100t", "deaths_per_cell_per_100t")), "dt_check"),
            "dt_tick_err_over_noise_spread_h1": V({f: [d["h1"][f]["err_over_spread_dt0.5"], d["h1"][f]["err_over_spread_dt0.25"]]
                                                   for f in ("phi", "S", "cell_mass")} if d else None, "dt_tick_error", "[dt 0.5, dt 0.25]"),
            "dt_tick_err_over_noise_spread_h10": V({f: [d["h10"][f]["err_over_spread_dt0.5"], d["h10"][f]["err_over_spread_dt0.25"]]
                                                    for f in ("phi", "S", "cell_mass")} if d else None, "dt_tick_error", "[dt 0.5, dt 0.25]"),
            "noise_sigma0_minus_main": V(pick(nz["det_minus_main"], ("N", "phi_mass", "divisions_ge50_per_cell_per_100t")), "noise_check"),
            "noise_sigma0.03_minus_main": V(pick(nz["sa03_minus_main"], ("N", "mean_size", "divisions_ge50_per_cell_per_100t")), "noise_check"),
            "fresh_noise_first_N_difference_t": V(a["divergence"]["fresh_noise_replicates_first_h_N_differs"], "divergence"),
        }
        if pl:
            ar = pl["arms"]
            out["headline"]["probe_long_target_mass_end_none_feed_starve"] = V(
                [sum(ar[k]["target_mass_at_end_of_input"]) / len(ar[k]["target_mass_at_end_of_input"]) for k in ("none", "feed", "starve")],
                "probe_input_long", "20 ticks at +-0.03 on the 2-4 bumps within 8 px of the largest cell, 281 nats mean")
            out["headline"]["probe_long_divisions_near_target_none_feed_starve"] = V(
                [sum(1 for x in ar[k]["target_divisions_within_H"] if x > 0) for k in ("none", "feed", "starve")], "probe_input_long",
                "members (of 16) with >= 1 new >= 50 px cell within 25 px of the target in 40 ticks")
            out["headline"]["probe_long_L2_mean_size_diff_h20_h40"] = V(
                {k: {h: [ar[k]["paired_L2_diff_mean"][h][1], ar[k]["paired_L2_diff_se"][h][1], pl["oracle_sd_L2"][h][1]]
                     for h in ("20", "40")} for k in ("feed", "starve")}, "probe_input_long", "[diff, se, oracle sd] of mean size (px)")
            Ve = cl["mean_size"]["Ve"]["2"]                 # closure V_best (linear, w = 2) at h = 1, 2, 4, 8, 16, 32
            HSc = cl["horizons_ticks"]
            out["headline"]["probe_long_size_effect_sq_over_Vbest_approx"] = V(
                {k: {f"probe_h{hp}_vs_closure_h{hc}": (ar[k]["paired_L2_diff_mean"][str(hp)][1] ** 2
                                                       - ar[k]["paired_L2_diff_se"][str(hp)][1] ** 2) / Ve[HSc.index(hc)]
                     for hp, hc in ((20, 16), (30, 32))} for k in ("feed", "starve")},
                "probe_input_long + closure_L2_main (Ve, w = 2)",
                "unbiased squared mean shift of the level-2 mean size over the closure's best level-2 MSE; horizons "
                "mismatched (probe 20 and 30 ticks against closure 16 and 32), so approximate; EXAM's bar is about 0.1")
        pilot_s = sum(J(f"pilot_{x}.json")["cpu_s_total"] for x in ("main", "dt025", "dt1", "det", "sa003", "sa03"))
        out["headline"]["cpu_total_s"] = V({"pilot_arms_incl_main_rerun": pilot_s, "first_main_run": 599.9,
                                            "other_scripts_estimate": 900},
                                           "results/pilot_*.json cpu_s_total; first main run from its log line in results/pilot.log; "
                                           "other scripts (explore, bench, channel, repro x2, dtcheck, probes x2, analysis x3, "
                                           "tests x3, smoke test) estimated from wall time on one core",
                                           "about 0.75 CPU-hours in all")
    out["notes"] = [
        "pilot_main was run twice: the first run recorded the earlier level-2 rule (tracker fission counter, 20-tick window); "
        "the rule was changed after the first analysis showed 55% of fission products are shed fragments < 50 px; the rerun "
        "reproduced level 1 and the branch counts bit for bit (max abs diff 0) and recorded the current rule.",
        "the other arms (dt025, dt1, det, sa003, sa03) recorded the earlier level-2 rule; analyse.py recomputes level 2 for every "
        "arm from the saved level-1 series with the declared transducer (for main the recomputation matches the online record "
        "to 5e-5, float32 storage).",
        "closure ceilings are lower bounds (linear predictor); bootstrap intervals are 16th-84th percentiles over 200 seed "
        "resamples, not ranges; the division-rate coordinate is a 50-tick window, so its short-horizon closure is inflated by "
        "window overlap.",
        "tracker overflow: zero ticks over the caps in every arm (tracker_overflow_ticks_max).",
        "dt_check / noise_check: diff_rel_pct in percent of the main arm's mean; ci95 and diff in the statistic's own units "
        "(cells, px, events per cell per 100 t); paired t over 16 seeds, no multiple-comparison correction.",
        "probe_input.json (5 ticks) was regenerated after the level-2 change with the new division count (new cells >= 50 px "
        "within 25 px of the target); its first version counted tracker fission events.",
    ]
    ck = J("checker.json")
    if ck:
        out["checker"] = ck
    json.dump(out, open(os.path.join(R, "summary.json"), "w"), indent=1)
    print("wrote", os.path.join(R, "summary.json"))


if __name__ == "__main__":
    main()
