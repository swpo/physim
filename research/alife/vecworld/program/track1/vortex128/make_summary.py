"""make_summary -- results/summary.json from results/analysis.json and the run metadata (every number with its source).

    python make_summary.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")


def J(name):
    p = os.path.join(RES, name)
    return json.load(open(p)) if os.path.exists(p) else None


def E(value, source, note=None):
    d = {"value": value, "source": source}
    if note:
        d["note"] = note
    return d


def r(x, n=3):
    if isinstance(x, float):
        return round(x, n)
    if isinstance(x, list):
        return [r(v, n) for v in x]
    if isinstance(x, dict):
        return {k: r(v, n) for k, v in x.items()}
    return x


def main():
    A = J("analysis.json")
    S = {"study": "vortex128 (track 1, round 3): the fed-vortex world's level-2 selection signal at 128^2",
         "date": "2026-11-07", "core": "taskset -c 2, OMP/XLA single-threaded, float64 (stored float32)"}
    m = {a: J(f"main128_{a}.json") for a in ("sel", "neu")}
    S["design128"] = E({"H": 128, "seeds": m["sel"]["S"], "ensemble_seed": m["sel"]["seed"], "T_ticks": m["sel"]["t_done"],
                        "t_end": m["sel"]["t_done"] * 5.0, "arms": {"sel": "eps 0.2", "neu": "eps 0 (twin, shared keys)"},
                        "sigma_a": m["sel"]["sigma_a"], "mut_dt": m["sel"]["mut_dt"], "tracker": m["sel"]["tracker"],
                        "W1_t": A["sel128"]["W1_t"], "W2_t": A["sel128"]["W2_t"], "W3_t": A["sel128"].get("W3_t"),
                        "branch_snapshots_ticks": m["sel"]["snapshots"]},
                       "results/main128_{sel,neu}.json (run.py main ARM 6 440 2)",
                       "designer ensemble(6, seed=2): keys independent of the round-2 pilot (ensemble(1, seed 0)) and checker (ensemble(1, seed 1))")
    S["timing"] = E({k: {"cpu_s": r(v["cpu_s"], 1), "member_ticks": v["member_ticks"], "cpu_s_per_member_tick": r(v["cpu_s_per_member_tick"], 4),
                         "overflow_rows": v.get("overflow")}
                     for k, v in {**{f"main128_{a}": m[a] for a in m},
                                  **{f"{g}_{a}": J(f"{g}_{a}.json") for g in ("area64", "area64x", "box64x") for a in ("sel", "neu")
                                     if J(f"{g}_{a}.json")},
                                  **{f"branch128_{a}": J(f"branch128_{a}.json") for a in ("sel", "neu") if J(f"branch128_{a}.json")}}.items()},
                    "results/{main128,area64,area64x,box64x,branch128}_*.json (time.process_time in run.py)",
                    "overflow rows = (raw_overflow_ticks, kept_overflow_ticks, raw_peak, kept_peak) per member; main128 includes the "
                    "extension from tick 440 to 600 (resumed from the saved carry)")
    # ---------------------------------------------------------------- (a) selection at 128^2
    sel, neu = A["sel128"], A["neu128"]
    keep = ("s_b_W1", "s_b_W2", "s_b_W3", "N_W1", "N_W2", "N_W3", "s_b_W1_mean", "s_b_W2_mean", "s_b_W3_mean", "N_W1_mean",
            "N_W2_mean", "N_W3_mean", "first_t_majority_b", "frac_ticks_majority_W2", "frac_ticks_majority_W3",
            "share_b_by_t_mean", "N_by_t_mean")
    S["selection128"] = {
        "per_seed": E({"sel": r({k: sel[k] for k in keep if k in sel}), "neu": r({k: neu[k] for k in keep if k in neu})},
                      "results/analysis.json sel128, neu128 (analyse.py)",
                      "W1 = ticks [100, 300) (t 500-1495), W2 = ticks [300, 440] (t 1500-2200), W3 = ticks [441, 600] (t 2205-3000, the "
                      "extension); first majority = first tick whose "
                      "centred 9-tick running mean of s_b > 0.5 (None = never)"),
        "paired_sel_minus_neu": E(r(A["paired128"], 4), "results/analysis.json paired128",
                                  "6 seeds; p from a paired t-test, the exact sign-flip permutation test (64 patterns), the exact "
                                  "Wilcoxon signed-rank test and the sign test"),
        "paired_with_earlier_seeds": E(r(A["paired128_with_earlier_seeds"], 4), "results/analysis.json paired128_with_earlier_seeds",
                                       "adds the round-2 pilot seed (W1 and W2) and the checker's seed 1 (W1 only; it stopped at t 1500)"),
        "earlier_seeds": E(r(A["earlier_seeds128"]), "results/analysis.json earlier_seeds128 (from ../vortex_world/results/pilot_H128.npz, "
                           "../vortex_world/checker/seed128_s1.npz)"),
        "diff_s_b_by_t": E(A["diff_s_b_by_t"], "results/analysis.json diff_s_b_by_t", "mean, SE and positive count of sel - neu over the 6 seeds"),
        "mutations": E({"n_to_t2200": A["mutations128"]["n_to_t2200"], "first_t": A["mutations128"]["times_to_t2200"][0],
                        "last_t": A["mutations128"]["times_to_t2200"][-1]}, "results/analysis.json mutations128 (analyse.mutation_times)",
                       "the accumulated float64 time is 300.0000000000171 at native step 15000, so the first mutation acts at the "
                       "labelling step (t 300), not at t 350"),
    }
    # ---------------------------------------------------------------- (b) 64^2 per-area mutation
    if "area64" in A:
        b = A["area64"]
        sl = ("s_b_W1", "s_b_W2", "N_W1", "N_W2", "s_b_W1_mean", "s_b_W2_mean", "N_W2_mean", "first_t_majority_b", "frac_ticks_majority_W2")
        S["area64"] = {
            "design": E({"H": 64, "seeds": b["n_seeds"], "ensemble_seed": 0, "members": f"0-{b['n_seeds'] - 1}", "T_ticks": b["T_ticks"],
                         "mut_dt_per_area": 200.0, "mut_dt_per_box": 50.0, "mutations": b["mutations"]},
                        "results/area64_{sel,neu}.json (members 0-3), area64x_* and box64x_* (members 4-7); per-box members 0-3 from "
                        "../vortex_world/results/pilot_H64.npz",
                        "same initial conditions and keys per member at both rates (ensemble(8, seed 0) member j = the round-2 pilot's "
                        "member j for j < 4); mut_dt 200 at 64^2 = the 128^2 rate per unit area (9 vs 38/4 = 9.5 events per 64^2 of area by t 2200)"),
            "identical_until_tick": E(b["identical_until_tick_members0_3"], "results/analysis.json area64.identical_until_tick_members0_3",
                                      "level-2 rows equal to the round-2 per-box rows to tick 60; the first per-box mutation acts at t 300"),
            "neutral_N_identical": E(b["neutral_N_identical_area_vs_box"], "results/analysis.json area64.neutral_N_identical_area_vs_box",
                                     "with eps = 0 the labels are passive, so the vortex count does not depend on the mutation schedule"),
            "per_area": E(r({a: {k: b["per_area"][a][k] for k in sl if k in b["per_area"][a]} for a in ("sel", "neu")}),
                          "results/analysis.json area64.per_area", "W1 = t 500-1495, W2 = t 1500-2500"),
            "per_box": E(r({a: {k: b["per_box"][a][k] for k in sl if k in b["per_box"][a]} for a in ("sel", "neu")}),
                         "results/analysis.json area64.per_box"),
            "paired_sel_minus_neu": E(r({"per_area": b["per_area"]["paired"], "per_box": b["per_box"]["paired"],
                                         "per_area_to_t2200": b["per_area"]["paired_to_t2200"],
                                         "per_box_to_t2200": b["per_box"]["paired_to_t2200"]}, 4),
                                      "results/analysis.json area64.*.paired*"),
            "neutral_area_minus_box": E(r(b["area_minus_box_neutral"], 4), "results/analysis.json area64.area_minus_box_neutral",
                                        "paired by member (same initial conditions)"),
            "favoured_area_minus_box": E(r(b["area_minus_box_sel"], 4), "results/analysis.json area64.area_minus_box_sel"),
        }
    # ---------------------------------------------------------------- (c) closure at 128^2
    if "closure128" in A:
        cl = A["closure128"]
        keys = ("V0", "Vu", "Vu_over_V0", "V_change", "c_persistence", "c_branch_w1", "c_branch_w2", "c_branch_w4", "c_traj_w1",
                "c_traj_w2", "c_traj_w4", "c_traj_t_w2", "c_traj_slope_w2", "cchg_branch_w2", "cchg_traj_w2", "cchg_traj_slope_w2")
        S["closure128"] = {
            "design": E({"branch_points_ticks": cl["branch_points_ticks"], "R": J("branch128_sel.json")["R"],
                         "H_branch_ticks": J("branch128_sel.json")["HB"], "horizons_ticks": cl["pooled"]["horizons_ticks"] if "pooled" in cl else None,
                         "n_rows_pooled": cl.get("pooled", {}).get("n_rows"), "n_branch_points_pooled": cl.get("pooled", {}).get("n_branch_points")},
                        "results/branch128_{sel,neu}.json, results/analysis.json closure128",
                        "c = (V0 - Ve)/(V0 - Vu); OLS on the last w level-2 values, leave-one-seed-out with twins held out together; "
                        "'branch' = fitted on branch rows (the round-2 definition), 'traj' = fitted on main trajectories, 'traj_t' = "
                        "'traj' plus the tick, 'traj_slope' = 'traj' plus the 20-tick mean and 40-tick slope; cchg = (V_change - Ve)/(V_change - Vu) "
                        "with V_change = var(y(t+h) - y(t)): closure against persistence plus the mean drift; horizons in 5-time-unit "
                        "ticks; a linear predictor, so c is a lower bound"),
        }
        for name in [k for k in ("pooled", "sel", "neu") if k in cl]:
            S["closure128"][name] = E({nm: r({k: cl[name][nm][k] for k in keys}) for nm in ("N", "s_b")},
                                      f"results/analysis.json closure128.{name}")
        if "pooled" in cl:
            S["closure128"]["bootstrap_pooled_w2"] = E({"traj": cl["pooled"]["bootstrap_traj_w2"], "branch": cl["pooled"]["bootstrap_branch_w2"],
                                                        "cchg_traj": cl["pooled"]["bootstrap_cchg_traj_w2"]},
                                                       "results/analysis.json closure128.pooled.bootstrap_*",
                                                       "16th and 84th percentiles over seed resamples (draws with < 3 distinct seeds dropped)")
    if "closure64_recomputed" in A:
        c64 = A["closure64_recomputed"]
        S["closure64_recomputed"] = E({nm: r({k: c64["pooled"][nm][k] for k in ("V0", "Vu", "Vu_over_V0", "V_change", "c_persistence", "c_branch_w2",
                                                                                "c_traj_w2", "c_traj_slope_w2", "cchg_branch_w2", "cchg_traj_w2",
                                                                                "cchg_traj_slope_w2")}) for nm in ("N", "s_b")}
                                      | {"n_rows": c64["pooled"]["n_rows"], "n_branch_points": c64["pooled"]["n_branch_points"]},
                                      "results/analysis.json closure64_recomputed (analyse.closure on ../vortex_world/results/pilot_H64.npz)",
                                      "c_branch_w2 reproduces the round-2 checker's 'twins held out together' numbers exactly")
    extra = J("extra.json")
    if extra:
        S.update(extra)
    tot = sum(v["cpu_s"] for v in S["timing"]["value"].values())
    S["cpu_seconds"] = E({"runs": r(tot, 1), "total_hours_including_smoke_and_analysis_est": r((tot + 300) / 3600, 2)},
                         "sum of timing cpu_s; +300 s estimate for the smoke test, analysis and compile in this session")
    json.dump(S, open(os.path.join(RES, "summary.json"), "w"), indent=1)
    print(json.dumps(S["cpu_seconds"]))


if __name__ == "__main__":
    main()
