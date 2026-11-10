"""prove -- the scripted end-to-end proof through verifiers: fresh hidden worlds, every reference policy through
the agent's route (scripted harness in the agent's box, host-side laboratory, stock isolated grader, per-item
predictor runs in the verifier box), the reference table and the acceptance shares.

For each of --worlds fresh hidden instances (tools/make_instances.py; they live in --store only):
  S, D, P0, PM, null   agentenv's agents/reference_agent.py, run in the agent's box by the physim2-script harness
  C                    needs the true parameters: built on the worker (same script, --no-submit --theta), then
                       installed and submitted from the agent's box by agents/install_prebuilt.py
Every rollout is graded by the reward of physim2_env (one item at a time in the verifier box); the per-item
scores stay in the store and evaluator.grader.table (agentenv, unchanged) computes the table from them.
The output JSON holds no hidden value: no theta, no secret, no item; only scores, counters, commitments.

usage: python tools/prove.py --store DIR --scratch DIR --worlds 4 --out results/proof_ring.json
"""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import vfrun  # noqa: E402
from physim2_env._paths import agentenv_root, use_agentenv  # noqa: E402

POLICIES = ["S", "D", "P0", "PM", "C", "null"]
LABELS = {"K": "long-run average of the hidden world (climatology pool)", "D": "ridge fitted to the real episodes the budget allows",
          "P0": "ridge trained on simulations at prior draws", "PM": "ridge trained on simulations at the prior mean",
          "S": "scripted inference, then ridge trained on simulations at posterior draws (the reference agent)",
          "C": "ridge trained on simulations at the true parameters", "O": "oracle: replicate futures from the hidden state (leave one out)",
          "null": "null agent: prior-predictive long-run law, no history, no program"}


def prebuild_C(store, iid, sizes, seed):
    """The designer's ceiling, built on the trusted worker: agentenv's reference_agent.py, policy C, no laboratory."""
    out = os.path.join(store, iid, "work", "reference_C")
    if os.path.exists(os.path.join(out, "predict.py")):
        return out
    os.makedirs(out, exist_ok=True)
    theta = json.load(open(os.path.join(store, iid, "hidden", "instance.json")))["theta"]
    ae = agentenv_root()
    cmd = [sys.executable, "-B", os.path.join(ae, "agents", "reference_agent.py"), "--policy", "C", "--sizes", json.dumps(sizes),
           "--seed", str(seed), "--theta", ",".join(repr(float(v)) for v in theta), "--no-submit", "--out", out]
    tmp = os.path.join(store, iid, "work", "reference_C_cwd")
    os.makedirs(tmp, exist_ok=True)
    env = vfrun.child_env({"PYTHONPATH": ae})
    r = subprocess.run(["nice", "-n", "10"] + cmd, cwd=tmp, env=env, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError("building C failed: " + r.stderr[-500:])
    shutil.copy(os.path.join(ROOT, "agents", "install_prebuilt.py"), os.path.join(out, "install_prebuilt.py"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--world", default="ring")
    ap.add_argument("--config", default="smoke_ring")
    ap.add_argument("--worlds", type=int, default=4)
    ap.add_argument("--prefix", default="proof-ring")
    ap.add_argument("--sizes", default='{"n_lab": 8, "n_design": 256, "k_design": 2, "n_train": 512}')
    ap.add_argument("--policies", default=",".join(POLICIES))
    ap.add_argument("--cpu", type=float, default=2)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    sizes, pols = json.loads(a.sizes), a.policies.split(",")
    t0, c0 = time.time(), time.process_time()
    ids = [f"{a.prefix}-w{w}" for w in range(a.worlds)]
    idx = os.path.join(a.store, "index.json")
    have = {r["instance_id"] for r in json.load(open(idx))} if os.path.exists(idx) else set()
    if not set(ids) <= have:
        subprocess.run([sys.executable, "-B", os.path.join(HERE, "make_instances.py"), "--store", a.store, "--world", a.world,
                        "--config", a.config, "--n", str(a.worlds), "--prefix", a.prefix], check=True, env=vfrun.child_env())
    index = {r["instance_id"]: r for r in json.load(open(idx))}
    out_dir, notes = os.path.join(a.scratch, "runs"), os.path.join(a.scratch, "notes")
    state_f = os.path.join(a.scratch, "prove_state.json")
    state = json.load(open(state_f)) if os.path.exists(state_f) else {"runs": {}}
    ae_agents = os.path.join(agentenv_root(), "agents")
    for pol in pols:
        if pol in state["runs"]:
            continue
        if pol == "C":
            for w, iid in enumerate(ids):
                prebuild_C(a.store, iid, sizes, w)
            harness = {"agent_dir": os.path.join(a.store, "{instance_id}", "work", "reference_C"), "script": "install_prebuilt.py",
                       "label": "C", "collect": ["agent_log_prebuilt.json"], "collect_dir": notes}
        else:
            harness = {"agent_dir": ae_agents, "script": "reference_agent.py", "label": pol,
                       "args": ["--policy", pol, "--sizes", json.dumps(sizes), "--seed", "{idx}"],
                       "collect": [f"agent_log_{pol}.json"] + (["posterior_draws_u.npy"] if pol == "S" else []), "collect_dir": notes}
        r = vfrun.run_eval(f"proof-{pol.lower()}", store=a.store, out_dir=out_dir, harness=harness, instances=ids, cpu=a.cpu)
        rolls = [vfrun.rollout(ep) for ep in r["episodes"]]
        if len(rolls) != len(ids):
            raise SystemExit(f"policy {pol}: {len(rolls)} episodes for {len(ids)} instances\n{r['log_tail']}")
        state["runs"][pol] = {"rollouts": rolls, "wall_s": r["wall_s"], "host_cpu_s": r["host_cpu_s"], "returncode": r["returncode"]}
        json.dump(state, open(state_f, "w"))
        print(f"{pol}: {[round(x['reward_skill_vs_O'], 3) for x in rolls]} ({time.time() - t0:.0f}s)", flush=True)

    use_agentenv()
    from evaluator import grader as GR
    from evaluator import instance as INST
    W = INST.world_module(a.world)
    per_world, hiddens = [], []
    for w, iid in enumerate(ids):
        hidden = os.path.join(a.store, iid, "hidden")
        hiddens.append(hidden)
        rec = {"instance_id": iid, "secret_commitment": index[iid]["secret_commitment"], "rollouts": {}}
        for pol in pols:
            x = next(r for r in state["runs"][pol]["rollouts"] if r["instance_id"] == iid)
            g = os.path.join(hidden, "grades")
            if x["graded"]:                                  # name the per-item scores of this rollout after its policy
                shutil.copy(os.path.join(g, f"{x['trace_id']}.npz"), os.path.join(g, f"{pol}.npz"))
            else:                                            # a rollout without a reward is K (memo hole 3)
                ex = INST.FrozenExam(hidden)
                np.savez_compressed(os.path.join(g, f"{pol}.npz"), es=ex.references()["K"], failed=np.ones(ex.n, bool), cpu=np.zeros(ex.n))
            lg_f = os.path.join(notes, x["trace_id"], f"agent_log_{pol}.json")
            lg = json.load(open(lg_f)) if os.path.exists(lg_f) else {}
            post = lg.get("posterior")
            gr = x["grade"]
            rec["rollouts"][pol] = {
                "trace_id": x["trace_id"], "graded": x["graded"], "ok": x["ok"], "script_exit_code": x["script_exit_code"],
                "submission": x["submission"], "submitted_before_finalization": (x["lab"] or {}).get("submitted"),
                "lab_ticks_used": (x["lab"] or {}).get("ticks_used"), "lab_total_nats": (x["lab"] or {}).get("total_nats"),
                "lab_requests": (x["lab"] or {}).get("requests"), "lab_infrastructure_errors": (x["lab"] or {}).get("infrastructure_errors"),
                "lab_episodes": lg.get("lab_episodes"), "member_ticks_simulated": lg.get("member_ticks_simulated"),
                "train_episodes": lg.get("train_episodes"), "agent_cpu_s": lg.get("cpu_s"),
                "posterior_sd_over_prior_sd": None if post is None else post["sd_over_prior_sd"],
                "reward_skill_vs_O": x["reward_skill_vs_O"], "wall_s": x["wall_s"], "cpu_s": x["cpu_s"],
                "grade": {k: gr.get(k) for k in ("n_items", "n_failed", "cpu_s_mean", "cpu_s_max", "layers", "items_with_leftovers",
                                                 "cleanup_between_items", "seconds")}}
        if "S" in pols:                                      # how close was the scripted inference (no theta is written)
            x = next(r for r in state["runs"]["S"]["rollouts"] if r["instance_id"] == iid)
            f = os.path.join(notes, x["trace_id"], "posterior_draws_u.npy")
            if os.path.exists(f):
                theta = np.array(json.load(open(os.path.join(hidden, "instance.json")))["theta"])
                u_true = (theta - (W.PRIOR_LO + W.PRIOR_HI) / 2) / ((W.PRIOR_HI - W.PRIOR_LO) / 2)
                rec["S_abs_error_over_prior_sd"] = (np.abs(np.load(f).mean(0) - u_true) * np.sqrt(3)).tolist()
        rec["table"] = GR.table(hidden, pols, n_boot=500)
        per_world.append(rec)
    rolls = [r for p in pols for r in state["runs"][p]["rollouts"]]
    out = {"world": a.world, "config": json.load(open(os.path.join(agentenv_root(), "configs", f"{a.config}.json"))),
           "sizes": sizes, "n_worlds": a.worlds, "policy_labels": LABELS, "PILOT_NEVER_REUSE_AS_EXAM": True,
           "hidden_values_in_this_file": "none (theta, secrets and items stay in the worker's store, which is deleted)",
           "route": "vf-eval physim2-env --env.id isolated-verifier, docker runtime, physim2-script harness, --no-push",
           "platform": {"machine": platform.machine(), "python": platform.python_version(), "cpu_count": os.cpu_count(),
                        "backend": "cpu", "verifiers": __import__("verifiers").__version__, "box_cpus": a.cpu,
                        "docker": subprocess.run(["docker", "version", "--format", "{{.Server.Version}}"], capture_output=True, text=True).stdout.strip()},
           "pooled": GR.table(hiddens, pols, labels=LABELS), "per_world": per_world,
           "rollout_cost": {
               "n_rollouts": len(rolls),
               "wall_s_per_rollout_mean": float(np.mean([r["wall_s"]["total"] for r in rolls])),
               "wall_s_per_rollout_max": float(np.max([r["wall_s"]["total"] for r in rolls])),
               "agent_box_cpu_s_mean": float(np.mean([r["cpu_s"]["agent_box"] or 0 for r in rolls])),
               "verifier_box_cpu_s_mean": float(np.mean([r["cpu_s"]["verifier_box"] or 0 for r in rolls])),
               "vf_eval_host_cpu_s_per_rollout": float(sum(state["runs"][p]["host_cpu_s"] for p in pols) / len(rolls)),
               "vf_eval_wall_s_per_policy": {p: state["runs"][p]["wall_s"] for p in pols},
               "note": "wall = boot + setup + agent + finalize of the solver trace plus the verifier phase (setup, restore, staging, "
                       "reward); box CPU = the cgroup counter of each container; host CPU = vf-eval and its children (laboratory "
                       "process, docker CLI), shared by the rollouts of one invocation"},
           "all_graded": all(r["graded"] for r in rolls), "all_ok": all(r["ok"] for r in rolls),
           "n_failed_items_total": int(sum((r["grade"].get("n_failed") or 0) for r in rolls)),
           "wall_s": time.time() - t0, "driver_cpu_s": time.process_time() - c0}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    p = out["pooled"]
    print(json.dumps({k: round(v["vs_C"], 4) for k, v in p["policies"].items() if v["vs_C"] is not None}))
    if "acceptance" in p:
        print(json.dumps({k: p["acceptance"].get(k) for k in ("sigma", "null_is", "rho", "sigma_worlds", "rho_worlds")}))


if __name__ == "__main__":
    main()
