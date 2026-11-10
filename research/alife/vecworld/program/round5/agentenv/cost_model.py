"""cost_model -- what a rollout costs, per world and envelope (arithmetic; no simulation).

Inputs (each with its source in the output): CPU seconds per member-tick (gliders: EXAM.md 0.136, the task's
0.15, and this study's measurement inside the agent sandbox; membrane: track1/membrane_world timing; ring: this
study), episode shapes, round 4's simulation counts (program/round4/sbi/results/summary.json), v1 token costs
(evals/labworlds/rollout_kit/README.md), and the GPU rate of round 4's bench.
usage: python cost_model.py -> results/cost.json
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.abspath(os.path.join(HERE, "..", ".."))


def main():
    sbi = json.load(open(os.path.join(PROG, "round4", "sbi", "results", "summary.json")))
    mem = json.load(open(os.path.join(PROG, "track1", "membrane_world", "results", "summary.json")))
    proof = {}
    for w in ("ring", "gliders"):
        f = os.path.join(HERE, "results", f"proof_{w}.json")
        if os.path.exists(f):
            proof[w] = json.load(open(f))

    def measured(w, pol="P0"):
        if w not in proof:
            return None
        xs = [r["rollouts"][pol] for r in proof[w]["per_world"] if pol in r["rollouts"]]
        mt = sum(x["member_ticks_simulated"] for x in xs)
        return sum(x["agent_cpu_s"] for x in xs) / mt if mt else None

    cpu = {"gliders": {"value": 0.15, "source": "task statement of this study; EXAM.md section 5 has 0.136 (closure study)",
                       "measured_here_agent_sandbox": measured("gliders"),
                       "measured_note": "whole P0 agent process (import, compile, simulation, fit) / member-ticks, tiny run, shared CPU"},
           "membrane": {"value": mem["timing"]["world_tick_L0_L1_L2_B1_per_member_s"]["value"],
                        "source": "track1/membrane_world/results/summary.json [timing.world_tick_L0_L1_L2_B1_per_member_s]"},
           "ring": {"value": measured("ring"), "source": "this study: results/proof_ring.json, P0 agent process CPU / member-ticks"}}
    shape = {"gliders": {"burn": 50, "P": 16, "H": 16, "source": "gliders_exam/pilot.py, round4/sbi config"},
             "membrane": {"burn": 150, "P": 16, "H": 16,
                          "source": "no exam exists; burn 150 ticks = the start tick of membrane_world/probe_input.py "
                                    "[summary.json probe_input.design.t0_tick], P and H assumed as gliders"},
             "ring": {"burn": 0, "P": 16, "H": 32, "source": "physim2/world_ring.py"}}
    mt = sbi["job"]["member_ticks"]
    n_truth = sbi["config"]["n_truth"]
    ep = shape["gliders"]["burn"] + shape["gliders"]["P"] + shape["gliders"]["H"]
    recipes = {
        "P0_set_round4": {"episodes": mt["sims_prior_pred"] // ep, "member_ticks": mt["sims_prior_pred"],
                          "source": "round4/sbi summary.json [job.member_ticks.sims_prior_pred]"},
        "S_full_round4": {"episodes": (mt["design"] + mt["sims_post2"] // n_truth) // ep,
                          "member_ticks": mt["design"] + mt["sims_post2"] // n_truth,
                          "source": "round4/sbi summary.json [job.member_ticks.design + sims_post2 / n_truth] (as roadmap_envelope.py)"},
        "S_shrunk_proposed": {"episodes": 256 * 2 + 1024, "member_ticks": (256 * 2 + 1024) * ep,
                              "source": "this study's reference agent at dry-run size (design 256 x 2, training 1,024); "
                                        "NOT validated at this size on gliders"},
    }
    out = {"cpu_s_per_member_tick": cpu, "episode_shape_ticks": shape, "recipes_gliders": recipes, "envelopes": {}, "worlds": {}}
    for w in ("gliders", "membrane"):
        c = cpu[w]["value"]
        e = sum(shape[w][k] for k in ("burn", "P", "H"))
        out["worlds"][w] = {"cpu_s_per_episode": c * e, "ticks_per_episode": e}
    out["worlds"]["membrane"]["cheaper_than_gliders_per_tick"] = cpu["gliders"]["value"] / cpu["membrane"]["value"]
    out["worlds"]["membrane"]["cheaper_than_gliders_per_episode"] = (out["worlds"]["gliders"]["cpu_s_per_episode"]
                                                                    / out["worlds"]["membrane"]["cpu_s_per_episode"])
    c = cpu["gliders"]["value"]
    for name, cpus, hours in (("dry_run_4c_8h", 4, 8), ("exam_4c_24h", 4, 24)):
        budget = cpus * hours * 3600 / c
        out["envelopes"][name] = {
            "cpus": cpus, "wall_hours": hours, "core_hours": cpus * hours, "gliders_member_ticks": int(budget),
            "gliders_episodes": int(budget // ep),
            "over_P0_set": budget / recipes["P0_set_round4"]["member_ticks"],
            "over_S_full_round4": budget / recipes["S_full_round4"]["member_ticks"],
            "over_S_shrunk": budget / recipes["S_shrunk_proposed"]["member_ticks"],
            "membrane_member_ticks": int(cpus * hours * 3600 / cpu["membrane"]["value"])}
    for k, r in recipes.items():
        r["core_hours_at_0.15"] = r["member_ticks"] * c / 3600
        r["hours_on_4_cores"] = r["member_ticks"] * c / 3600 / 4
    # the evaluator's side of one gliders rollout (dry-run config)
    cfg = json.load(open(os.path.join(HERE, "configs", "dryrun_gliders.json")))
    n, R, nc, T = cfg["exam"]["n_items"], cfg["exam"]["R"], cfg["exam"]["n_clim"], cfg["lab"]["max_ticks"]
    exam_mt = n * (50 + 16) + n * R * 16 + nc * (50 + 16)
    eps = T // (cfg["lab"]["reset_cost"] + 32)
    lab_mt = T + eps * 50
    gpu_rate, gpu_usd_h = 1600.0, 1.99
    refs_per_world = recipes["P0_set_round4"]["member_ticks"] + recipes["S_shrunk_proposed"]["member_ticks"]   # C + S
    refs_shared = 2 * recipes["P0_set_round4"]["member_ticks"]                                                  # P0 + prior mean
    out["evaluator_gliders_dry_run"] = {
        "exam_member_ticks": exam_mt, "exam_core_hours": exam_mt * c / 3600,
        "lab_exam_shaped_episodes_in_budget": eps, "lab_member_ticks_incl_hidden_burn_in": lab_mt,
        "lab_cpu_minutes": lab_mt * c / 60,
        "grading_cpu_minutes_worst_case": n * cfg["predictor"]["cpu_seconds"] / 60,
        "references_member_ticks_per_world_C_and_S": refs_per_world, "references_member_ticks_shared_P0_and_PM": refs_shared,
        "references_core_hours_3_worlds_cpu": (3 * refs_per_world + refs_shared) * c / 3600,
        "references_gpu_seconds_3_worlds": (3 * refs_per_world + refs_shared) / gpu_rate,
        "references_gpu_usd_3_worlds_at_1.99_per_h_excluding_pod_startup": (3 * refs_per_world + refs_shared) / gpu_rate / 3600 * gpu_usd_h,
        "gpu_rate_source": "program/gpu/bench/README.md (1,400-1,700 member-ticks/s float64 at B >= 64 on A100/H100); "
                           "$1.99/h is r4-sbi-002's A100 40GB rate"}
    out["inference_usd_per_rollout"] = {
        "small_model_mechanics_test": "cents (Qwen3.5 9B at about $0.02 per million tokens)",
        "pilot_models": [7.60, 23.0],
        "source": "evals/labworlds/rollout_kit/README.md: the October BF case study (PhySim v1); no v2 rollout exists, so this "
                  "is an extrapolation, not a measurement"}
    out["wall_clock_per_rollout_hours"] = {
        "dry_run": {"agent_envelope": 8, "exam_build_cpu_4_cores": exam_mt * c / 3600 / 4,
                    "grading_worst_case": n * cfg["predictor"]["wall_seconds"] / 3600,
                    "total_upper_bound": 8 + exam_mt * c / 3600 / 4 + n * cfg["predictor"]["wall_seconds"] / 3600},
        "exam": {"agent_envelope": 24, "total_upper_bound": 24 + exam_mt * c / 3600 / 4 + n * cfg["predictor"]["wall_seconds"] / 3600}}
    json.dump(out, open(os.path.join(HERE, "results", "cost.json"), "w"), indent=1)
    print(json.dumps({"envelopes": out["envelopes"], "recipes": {k: round(v["hours_on_4_cores"], 2) for k, v in recipes.items()},
                      "membrane": out["worlds"]["membrane"]}, indent=1))


if __name__ == "__main__":
    main()
