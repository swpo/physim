"""make_summary -- results/summary.json from the result files of this study (every number with its source).

Sources: results/proof_ring.json, results/proof_gliders.json (prove.py), results/probe_ring.json (check_probe.py),
results/acceptance_gliders_round4.json (acceptance_round4.py), results/cost.json (cost_model.py).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")


def load(name):
    f = os.path.join(RES, name)
    return json.load(open(f)) if os.path.exists(f) else None


def proof_block(name, note):
    p = load(name)
    if p is None:
        return None
    t = p["pooled"]
    acc = t.get("acceptance", {})
    pol = {k: {"L": round(v["L"], 4), "skill_vs_C": None if v["vs_C"] is None else round(v["vs_C"], 4),
               "skill_vs_O": None if v["vs_O"] is None else round(v["vs_O"], 4)} for k, v in t["policies"].items()}
    ro = [w["rollouts"] for w in p["per_world"]]
    pols = list(ro[0])

    def tot(key, pl):
        xs = [r[pl][key] for r in ro if r[pl].get(key) is not None]
        return sum(xs) if xs else None
    return {
        "source": f"results/{name}", "note": note, "world": p["world"], "n_worlds": p["n_worlds"], "n_items": t["n_items"],
        "config": p["config"], "sizes": p["sizes"], "platform": p["platform"], "wall_s": round(p["wall_s"], 1),
        "policies": {"value": pol, "source": f"results/{name} [pooled.policies]",
                     "definition": "L = item mean of the fair energy score summed over the declared cells; "
                                   "skill_vs_C = (L(K) - L) / (L(K) - L(C)); skill_vs_O likewise with the oracle"},
        "oes_mean": {"value": {k: round(v["mean"], 4) for k, v in t["oes"].items()},
                     "se": {k: round(v["se"], 4) for k, v in t["oes"].items()}, "source": f"results/{name} [pooled.oes]"},
        "acceptance": {"value": {k: acc.get(k) for k in ("sigma", "null_is", "rho", "sigma_items", "rho_items", "sigma_worlds",
                                                         "rho_worlds", "pass_sigma", "pass_rho", "per_world")},
                       "source": f"results/{name} [pooled.acceptance]"},
        "wall_s_note": ("this file's wall_s is the second invocation (the S rerun); the first took 1117.7 s "
                        "(results/gliders_S_insample_failure.json)") if p["world"] == "gliders" else None,
        "per_policy_totals": {pl: {"lab_ticks_used": tot("lab_ticks_used", pl), "lab_episodes": tot("lab_episodes", pl),
                                   "member_ticks_simulated": tot("member_ticks_simulated", pl),
                                   "agent_cpu_s": None if tot("agent_cpu_s", pl) is None else round(tot("agent_cpu_s", pl), 1),
                                   "failed_items": sum(r[pl]["grade"]["n_failed"] for r in ro if r[pl]["grade"]),
                                   "predictor_cpu_s_per_item_max": max(r[pl]["grade"]["cpu_s_max"] for r in ro if r[pl]["grade"]),
                                   "submitted_by_agent": all(r[pl]["submitted_before_finalization"] for r in ro)}
                              for pl in pols},
        "S_inference": {"posterior_sd_over_prior_sd": [w["rollouts"]["S"]["posterior_sd_over_prior_sd"] for w in p["per_world"] if "S" in w["rollouts"]],
                        "abs_error_over_prior_sd": [w.get("S_abs_error_over_prior_sd") for w in p["per_world"]],
                        "source": f"results/{name} [per_world[*].rollouts.S.posterior_sd_over_prior_sd, per_world[*].S_abs_error_over_prior_sd]"},
        "isolation_layers": {"agent": ro[0][pols[0]]["agent"]["layers"], "predictor": ro[0][pols[0]]["grade"]["layers"],
                             "source": f"results/{name} [per_world[0].rollouts.{pols[0]}]"},
        "secret_commitments": [w["secret_commitment"] for w in p["per_world"]],
    }


def main():
    r4 = load("acceptance_gliders_round4.json")
    cost = load("cost.json")
    probe = load("probe_ring.json")
    g4 = {}
    for fam, d in r4["families"].items():
        g4[fam] = {N: {"sigma": round(v["pooled"]["sigma"], 4), "sigma_se_worlds": round(v["pooled"]["sigma_worlds"]["se"], 4),
                       "null_is": v["pooled"]["null_is"], "rho": round(v["pooled"]["rho"], 3),
                       "rho_se_worlds": round(v["pooled"]["rho_worlds"]["se"], 3),
                       "sigma_oes_mean": round(v["oes_mean"]["sigma"], 4), "rho_oes_mean": round(v["oes_mean"]["rho"], 3)}
                   for N, v in d["by_budget_episodes"].items()}
    out = {
        "study": "round 5, study agentenv (track 2): the PhySim-v2 exam as an agent-facing environment, proved end to end "
                 "with scripted agents; no GPU, no model calls",
        "folder": "research/alife/vecworld/program/round5/agentenv",
        "PILOT_NEVER_REUSE_AS_EXAM": True,
        "hidden_values": "none in git: every instance's theta and secret were drawn at run time in a scratch directory and deleted; "
                         "results hold scores, counters and commitment hashes",
        "gpu": {"jobs": [], "gpu_hours": 0.0, "billed_usd": 0.0, "cap_usd": 0.0, "source": "no request file was submitted"},
        "proof_ring": proof_block("proof_ring.json", "the cheap mechanics world at statistical size; its sigma and rho describe the toy, not an exam candidate"),
        "proof_gliders": proof_block("proof_gliders.json", "SMOKE SIZE (8 items, 12 training episodes per policy): proves the gliders adapter, "
                                     "bundle and interface end to end on CPU; its scores, sigma and rho are noise and decide nothing"),
        "probe": None if probe is None else {"value": {k: probe[k] for k in ("n_checks", "n_passed", "failed", "skipped_no_capability")},
                                             "checks": probe["checks"], "source": "results/probe_ring.json"},
        "acceptance_gliders_full_size": {
            "value": g4, "bars": r4["bars"], "n_items": r4["n_items"], "n_worlds": r4["n_worlds"],
            "source": "results/acceptance_gliders_round4.json [families.<family>.by_budget_episodes.<N>], recomputed with "
                      "evaluator/acceptance.py from program/round4/sbi/results/job/scores.npz (GPU job r4-sbi-002)",
            "note": "sigma, rho: pooled-L definition (ROADMAP section 1) with world-clustered bootstrap SE; *_oes_mean: the "
                    "arithmetic of roadmap/checks/roadmap_envelope.py, reproduced"},
        "gliders_S_insample_failure": {"value": load("gliders_S_insample_failure.json"),
                                       "source": "results/gliders_S_insample_failure.json"},
        "bundles": {"value": load("bundles.json"), "source": "results/bundles.json"},
        "final_collection_test": {"value": load("final_collection_test.json"), "source": "results/final_collection_test.json"},
        "tcp_transport_test": {"value": load("tcp_test.json"), "source": "results/tcp_test.json (tests_tcp.py)"},
        "cost": {"value": cost, "source": "results/cost.json (cost_model.py)"},
    }
    json.dump(out, open(os.path.join(RES, "summary.json"), "w"), indent=1)
    print("summary written:", [k for k, v in out.items() if v is None])


if __name__ == "__main__":
    main()
