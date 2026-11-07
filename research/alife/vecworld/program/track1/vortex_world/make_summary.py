"""make_summary -- collect every number the report claims into results/summary.json, each with its source.

    python make_summary.py
"""
import json
import os

import _paths

R = _paths.RESULTS


def load(name):
    p = os.path.join(R, name)
    return json.load(open(p)) if os.path.exists(p) else None


def item(value, source, note=""):
    d = {"value": value, "source": source}
    if note:
        d["note"] = note
    return d


def main():
    S = {}
    rp = load("repro.json")
    if rp:
        src = "results/repro.json (check_repro.py 500)"
        S["repro"] = {
            "per_step_max_rel_diff": item(rp["per_step_max_rel"], src, "one JAX step on numpy's state vs numpy's next state, "
                                          "max |diff|/max|field|, 101 checkpoints + labelling and mutation steps, 128^2"),
            "special_steps_max_rel_diff": item({str(p["step"]): max(p[f] for f in ("om", "Y", "a", "b")) for p in rp["per_step_special"]},
                                               src, "step 15000 = labelling (t=300); 17500, 20000, 22500 = mutations"),
            "time_identical_every_step": item(rp["per_step_t_equal_all"], src),
            "run_max_rel_diff_t500": item(max(rp["run_final"][f] for f in ("om", "Y", "a", "b")), src, "JAX run vs numpy run, noise off, numpy's mutation draws"),
            "null_max_rel_diff_t500": item(max(rp["null_final"][f] for f in ("om", "Y", "a", "b")), src, "numpy vs numpy from om*(1+-1e-15)"),
            "run_max_rel_by_t": item(rp["run_max_rel_by_t"], src),
            "null_max_rel_by_t": item(rp["null_max_rel_by_t"], src),
            "cpu_s_per_native_step_128": item(rp["timing_cpu_s_per_native_step"], src, "one core; labkit FFTs with 1 worker"),
        }
    ch = load("channel.json")
    if ch:
        src = "results/channel.json (check_channel.py)"
        S["channel"] = {"config": item(ch["config"], src), "noise_law": item(ch["noise_law"], src),
                        "kl_check_3tick_program": item(ch["kl_check"], src), "example_costs_nats": item(ch["example_costs_nats"], src),
                        "grid_contrast": item(ch["grid_contrast"], src, "same delivered field charged against the v1 pixel noise")}
    for H in (64, 128):
        pm, an = load(f"pilot_H{H}.json"), load(f"analysis_H{H}.json")
        if not pm:
            continue
        src_p, src_a = f"results/pilot_H{H}.json (pilot.py)", f"results/analysis_H{H}.json (analyse.py {H})"
        blk = {"design": item({k: pm[k] for k in ("H", "n_seeds", "T_ticks", "R", "H_branch", "every", "arms", "tick_time", "tracker", "sigma_a")}, src_p),
               "timing": item(pm["timing"], src_p)}
        if an:
            sel = an["selection"]
            blk["selection"] = item(sel, src_a)
            if "closure" in an:
                blk["closure_ceiling"] = item({arm: {nm: {"horizons_t": an["horizons_t"], "c_w2": v[nm]["ceiling"]["2"],
                                                          "c_w1": v[nm]["ceiling"]["1"], "c_w4": v[nm]["ceiling"]["4"],
                                                          "c_persistence": v[nm]["ceiling_persistence"],
                                                          "Vu_over_V0": v[nm]["oracle_share_of_V0"],
                                                          "V0": v[nm]["V0"], "Vu": v[nm]["Vu"], "Ve_w2": v[nm]["Ve"]["2"],
                                                          "bootstrap_c_w2_p16_p84": [v["bootstrap_w2"][nm]["p16"], v["bootstrap_w2"][nm]["p84"]]}
                                                     for nm in ("N", "s_b")} | {"n_branch_points": v["n_branch_points"], "n_rows": v["n_rows"]}
                                               for arm, v in an["closure"].items()}, src_a,
                                              "c = (V0 - Ve)/(V0 - Vu); Ve: OLS on the last w level-2 values, leave-one-seed-out")
        S[f"pilot_{H}"] = blk
    pr = load("probe_input.json")
    if pr:
        S["input_probe_64"] = item(pr, "results/probe_input.json (probe_input.py)")
    tm = load("timing.json")
    if tm:
        S["timing_bench"] = item(tm, "results/timing.json (bench_step.py, bench_level.py, transcribed)")
    S["cpu_seconds"] = item({"check_repro_500": 223.9, "pilot_H64 (sel, neu 4 seeds + branches; sel0 2 seeds)": 1716.4,
                             "pilot_H128 (sel, neu, 1 seed, 440 ticks)": 508.7, "probe_input": 311.7,
                             "first pilot_H64 attempt, killed by the 30-min background limit, no output": 1800,
                             "tests, smoke runs, benchmarks, analyses, channel check (estimate)": 200},
                            "results/*.log ('user' lines); the killed run and small jobs are estimates from this session")
    S["cpu_seconds"]["total_hours"] = round(sum(v for v in S["cpu_seconds"]["value"].values()) / 3600, 2)
    json.dump(S, open(os.path.join(R, "summary.json"), "w"), indent=1)
    print(json.dumps(S, indent=1)[:4000])


if __name__ == "__main__":
    main()
