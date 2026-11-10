"""prove -- the scripted end-to-end proof: fresh hidden worlds, every reference policy through the agent's
interface, the null agent, the reference table and the acceptance shares.

For each of --worlds fresh hidden instances (secret and theta drawn at run time, kept under --scratch only):
prepare (instance, frozen exam, public bundle), then one rollout per policy (S, D, P0, PM, C, null), each with
its own laboratory budget, each graded by the same sandboxed grader. The output JSON holds no hidden value: no
theta, no secret, no item; only scores, counters and the secrets' commitment hashes.

usage: python prove.py --world ring --config configs/smoke_ring.json --worlds 4 --scratch DIR --out results/proof_ring.json
"""
import argparse
import json
import os
import platform
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import run_rollout as RR  # noqa: E402
from evaluator import grader as GR  # noqa: E402
from evaluator import sandbox  # noqa: E402

POLICIES = ["S", "D", "P0", "PM", "C", "null"]
LABELS = {"K": "long-run average of the hidden world (climatology pool)", "D": "ridge fitted to the real episodes the budget allows",
          "P0": "ridge trained on simulations at prior draws", "PM": "ridge trained on simulations at the prior mean",
          "S": "scripted inference, then ridge trained on simulations at posterior draws (the reference agent)",
          "C": "ridge trained on simulations at the true parameters", "O": "oracle: replicate futures from the hidden state (leave one out)",
          "null": "null agent: prior-predictive long-run law, no history, no program"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--world", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--worlds", type=int, default=2)
    ap.add_argument("--sizes", default="{}")
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--policies", default=",".join(POLICIES))
    ap.add_argument("--tag", default="w")
    a = ap.parse_args()
    cfg = json.load(open(a.config))
    sizes = json.loads(a.sizes)
    pols = a.policies.split(",")
    t0, c0 = time.time(), time.process_time()
    runs, per_world = [], []
    for w in range(a.worlds):
        run = os.path.join(a.scratch, f"{a.tag}{w}")
        if not os.path.exists(os.path.join(run, "prepare.json")):
            RR.prepare(a.world, cfg, run)
        prep = json.load(open(os.path.join(run, "prepare.json")))
        rec = {"secret_commitment": prep["instance"]["secret_commitment"], "exam": prep["exam"], "rollouts": {}}
        for pol in pols:
            f = os.path.join(run, f"rollout_{pol}.json")
            if not os.path.exists(f):
                theta = json.load(open(os.path.join(run, "hidden", "instance.json")))["theta"] if pol == "C" else None
                RR.rollout(run, pol, RR.scripted_cmd(pol, sizes, seed=w, theta=theta))
            r = json.load(open(f))
            lg = r.get("agent_log", {})
            post = lg.get("posterior")
            rec["rollouts"][pol] = {
                "agent": r["agent"], "submitted_before_finalization": r["submitted_before_finalization"],
                "lab_ticks_used": r["usage"]["ticks_used"], "lab_total_nats": r["usage"]["total_nats"],
                "lab_episodes": lg.get("lab_episodes"), "member_ticks_simulated": lg.get("member_ticks_simulated"),
                "train_episodes": lg.get("train_episodes"), "agent_cpu_s": lg.get("cpu_s"),
                "posterior_sd_over_prior_sd": None if post is None else post["sd_over_prior_sd"],
                "grade": {k: r["grade"][k] for k in ("n_items", "n_failed", "cpu_s_mean", "cpu_s_max", "layers")} if r["grade"] else None}
            print(f"world {w} {pol}: done ({time.time() - t0:.0f}s)", flush=True)
        if "S" in pols:                                      # how close was the scripted inference (no theta is written)
            inst = json.load(open(os.path.join(run, "hidden", "instance.json")))
            W = RR.INST.world_module(a.world)
            u_true = (np.array(inst["theta"]) - (W.PRIOR_LO + W.PRIOR_HI) / 2) / ((W.PRIOR_HI - W.PRIOR_LO) / 2)
            dr = np.load(os.path.join(run, "workspaces", "S", "posterior_draws_u.npy"))
            rec["S_abs_error_over_prior_sd"] = (np.abs(dr.mean(0) - u_true) * np.sqrt(3)).tolist()
        rec["table"] = GR.table(os.path.join(run, "hidden"), pols, n_boot=500)
        runs.append(run)
        per_world.append(rec)
    out = {"world": a.world, "config": cfg, "sizes": sizes, "n_worlds": a.worlds, "policy_labels": LABELS,
           "PILOT_NEVER_REUSE_AS_EXAM": True,
           "hidden_values_in_this_file": "none (theta, secrets and items stay in the scratch directory, which is deleted)",
           "platform": {"machine": platform.machine(), "python": platform.python_version(), "cpu_count": os.cpu_count(),
                        "backend": "cpu", "sandbox_capabilities": sandbox.caps()},
           "pooled": GR.table([os.path.join(r, "hidden") for r in runs], pols, labels=LABELS),
           "per_world": per_world, "wall_s": time.time() - t0, "driver_cpu_s": time.process_time() - c0}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    p = out["pooled"]
    print(json.dumps({k: round(v["vs_C"], 4) for k, v in p["policies"].items()}))
    print(json.dumps({k: p["acceptance"].get(k) for k in ("sigma", "null_is", "rho", "sigma_worlds", "rho_worlds")}))


if __name__ == "__main__":
    main()
