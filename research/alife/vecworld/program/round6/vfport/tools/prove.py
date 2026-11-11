"""prove -- the scripted end-to-end proof through verifiers: fresh hidden worlds, every reference policy through
the agent's route (scripted harness in the agent's box, host-side laboratory, stock isolated grader, per-item
predictor runs in the verifier box), the reference table and the acceptance shares.

For each of --worlds fresh hidden instances (tools/make_instances.py; they live in --store only), or for the ONE
existing instance --instance of an exam profile (--profile: the reference table of a rollout):
  null                 the baseline every box starts with, left untouched (agents/keep_baseline.py); what a failed
                       item of any predictor is scored with
  S, D, P0, PM         agentenv's agents/reference_agent.py, run in the agent's box by the physim2-script harness
  C                    needs the true parameters: built on the worker by tools/build_reference.py (the same script,
                       --no-submit; the parameters go from a file of mode 0600 in the store into that process's
                       memory, never onto a command line), then installed and submitted from the agent's box by
                       agents/install_prebuilt.py
Every rollout is graded by the reward of physim2_env (one item at a time in the verifier box); the per-item
scores stay in the store and evaluator.grader.table (agentenv, unchanged) computes the table from them.
The output JSON holds no hidden value: no theta, no secret, no item; only scores, counters, commitments.
Next to it, <out minus .json>_items.npz holds the per-item, per-cell scores of every policy and of K and O for
every world, so that the table can be recomputed without the store (tools/recompute_table.py).

Grading mode: the reference policies are the evaluator's own, so the table is graded with all items of a rollout
in ONE verifier box (--isolation shared, 0.6 s per item). The default of the taskset, one fresh box per item, is
exercised on --box-check policies of the first world: the same frozen submission must get the same per-item
scores in both modes.

Every box of a reference policy gets the caps a model's box gets (ruling E8): the task asks for the profile's
CPUs and memory, and --memory lowers the memory when the rollout it stands beside ran with less.

usage: VF_RUN_ID=<label> python tools/prove.py --store DIR --scratch DIR --worlds 4 --disk-floor-gib 8 --out results/proof_ring.json
       VF_RUN_ID=<label> python tools/prove.py --store DIR --scratch DIR --profile ring --instance pilot-x --disk-floor-gib 8 --out FILE
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

vfrun.require_clean_environment()                          # before the package is imported: see vfrun.ENV_REFUSE
from physim2_env._paths import agentenv_root, config_path, use_agentenv  # noqa: E402
from physim2_env import profiles as PROFILES  # noqa: E402

POLICIES = ["S", "D", "P0", "PM", "C", "null"]
LABELS = {"K": "long-run average of the hidden world (climatology pool)", "D": "ridge fitted to the real episodes the budget allows",
          "P0": "ridge trained on simulations at prior draws", "PM": "ridge trained on simulations at the prior mean",
          "S": "scripted inference, then ridge trained on simulations at posterior draws (the reference agent)",
          "C": "ridge trained on simulations at the true parameters", "O": "oracle: replicate futures from the hidden state (leave one out)",
          "null": "null policy: the baseline every box starts with (prior-predictive long-run law, no history, no program); "
                  "also the forecast a failed item is scored with"}


def prebuild_C(store, iid, sizes, seed):
    """The designer's ceiling, built on the trusted worker: agentenv's reference_agent.py, policy C, no laboratory."""
    out = os.path.join(store, iid, "work", "reference_C")
    if os.path.exists(os.path.join(out, "predict.py")):
        return out
    os.makedirs(out, exist_ok=True)
    ae = agentenv_root()
    # The hidden parameters go to the builder through a file of mode 0600 beside (never inside) the folder that
    # is later copied into the agent's box, and from there into the builder's memory: not onto a command line,
    # which every `ps` on this machine shows (finding m1). The file stays in the store and goes with it.
    theta_file = os.path.join(store, iid, "work", "reference_C.theta.json")
    if not os.path.lexists(theta_file):
        theta = json.load(open(os.path.join(store, iid, "hidden", "instance.json")))["theta"]
        fd = os.open(theta_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "w") as f:
            json.dump({"theta": [float(v) for v in theta]}, f)
        del theta
    cmd = [sys.executable, "-B", os.path.join(HERE, "build_reference.py"), "--theta-file", theta_file,
           "--script", os.path.join(ae, "agents", "reference_agent.py"), "--",
           "--policy", "C", "--sizes", json.dumps(sizes), "--seed", str(seed), "--no-submit", "--out", out]
    tmp = os.path.join(store, iid, "work", "reference_C_cwd")
    os.makedirs(tmp, exist_ok=True)
    r = vfrun.run_helper(cmd, cwd=tmp, env=vfrun.child_env({"PYTHONPATH": ae}), capture=True)
    if r.returncode:
        raise RuntimeError("building C failed: " + r.stderr[-500:])
    shutil.copy(os.path.join(ROOT, "agents", "install_prebuilt.py"), os.path.join(out, "install_prebuilt.py"))
    return out


def cross_check(store, iid, world, config_name, name="C"):
    """The same frozen submission through round 5's own grader (evaluator.grader.grade: one process per item in
    agentenv's local sandbox, on the worker) and through the verifiers route: are the per-item scores equal?"""
    use_agentenv()
    import tempfile
    from evaluator import build_workspace as BW
    from evaluator import grader as GR
    from physim2_env.bundle import load_config
    hidden = os.path.join(store, iid, "hidden")
    sub = os.path.join(store, iid, "work", "reference_C")
    with tempfile.TemporaryDirectory(prefix="physim2-xcheck-") as tmp:
        os.chmod(tmp, 0o755)
        BW.build(world, load_config(config_name), tmp)
        g = GR.grade(hidden, sub, os.path.join(tmp, "public"), f"{name}_agentenv", log=lambda *_: None)
    a_ = np.load(os.path.join(hidden, "grades", f"{name}_agentenv.npz"))
    b_ = np.load(os.path.join(hidden, "grades", f"{name}.npz"))
    d = np.abs(a_["es"] - b_["es"])
    return {"policy": name, "n_items": int(len(d)), "n_failed_agentenv": int(g["n_failed"]), "n_failed_route": int(b_["failed"].sum()),
            "max_abs_difference": float(d.max()), "identical": bool(np.array_equal(a_["es"], b_["es"])),
            "agentenv_layers": g.get("layers"), "agentenv_cpu_s_mean": g.get("cpu_s_mean")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--profile", default=None, help="an exam profile (physim2_env/profiles.py): its world, exam config, reference "
                                                    "policies and sizes; with --instance")
    ap.add_argument("--instance", default=None, help="with --profile: the ONE existing instance to build the reference table on")
    ap.add_argument("--world", default="ring")
    ap.add_argument("--config", default="smoke_ring")
    ap.add_argument("--worlds", type=int, default=4)
    ap.add_argument("--prefix", default="proof-ring")
    ap.add_argument("--sizes", default='{"n_lab": 8, "n_design": 256, "k_design": 2, "n_train": 512}')
    ap.add_argument("--policies", default=None)
    ap.add_argument("--cpu", type=float, default=None, help="CPUs of every box (default: what the task asks for, the profile's)")
    ap.add_argument("--memory", type=float, default=None,
                    help="memory of every box in GB, to LOWER the profile's cap as a rollout did (ruling E8); default: the profile's")
    ap.add_argument("--isolation", default="shared", choices=["shared", "box"])
    ap.add_argument("--box-check", default=None, help="policies re-run on the first world with one box per item ('' = none)")
    ap.add_argument("--cross-check", action="store_true",
                    help="also grade C through round 5's own grader, which runs the evaluator's reference predictor in agentenv's local "
                         "sandbox ON THIS MACHINE (it changes modes and removes its own temporary folders there): only inside a "
                         "throwaway container; off by default since round 4")
    ap.add_argument("--no-cross-check", action="store_true", help="accepted and ignored: the cross-check is off unless --cross-check is given")
    ap.add_argument("--disk-floor-gib", type=float, default=vfrun.DISK_FLOOR_GIB,
                    help="the disk watchdog: no run starts, and a run is stopped, when the file system of the home folder has less free space")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    vfrun.DISK_FLOOR_GIB = a.disk_floor_gib
    vfrun.run_label()
    vfrun.require_disk(vfrun.disk_floor_bytes(), "the tool")
    idx = os.path.join(a.store, "index.json")
    have = {r["instance_id"] for r in json.load(open(idx))} if os.path.exists(idx) else set()
    if a.profile is not None:                                # the reference table of ONE existing instance of a profile
        prof = PROFILES.get(a.profile)
        if not a.instance or a.instance not in have:
            raise SystemExit("refused: --profile needs --instance ID, an instance that tools/make_instances.py --profile made in this store")
        a.world, a.config, a.worlds = prof["world"], prof["config_name"], 1
        a.sizes = json.dumps(prof["reference_sizes"])
        a.policies = a.policies or ",".join(prof["reference_policies"])
        a.box_check = "" if a.box_check is None else a.box_check
        ids = [a.instance]
    else:
        if a.instance:
            raise SystemExit("refused: --instance goes with --profile")
        ids = [f"{a.prefix}-w{w}" for w in range(a.worlds)]
    a.policies = a.policies or ",".join(POLICIES)
    a.box_check = "C,D" if a.box_check is None else a.box_check
    limits = {} if a.memory is None else {"box_memory_gb": a.memory}
    sizes, pols = json.loads(a.sizes), a.policies.split(",")
    t0, c0 = time.time(), time.process_time()
    if not set(ids) <= have:
        r = vfrun.run_helper([sys.executable, "-B", os.path.join(HERE, "make_instances.py"), "--store", a.store, "--world", a.world,
                              "--config", a.config, "--n", str(a.worlds), "--prefix", a.prefix])
        if r.returncode:
            raise SystemExit(f"make_instances.py ended with status {r.returncode}")
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
        elif pol == "null":                                  # the box's own baseline, untouched and not submitted
            harness = {"agent_dir": os.path.join(ROOT, "agents"), "script": "keep_baseline.py", "label": "null",
                       "collect": ["agent_log_null.json"], "collect_dir": notes}
        else:
            harness = {"agent_dir": ae_agents, "script": "reference_agent.py", "label": pol,
                       "args": ["--policy", pol, "--sizes", json.dumps(sizes), "--seed", "{idx}"],
                       "collect": [f"agent_log_{pol}.json"] + (["posterior_draws_u.npy"] if pol == "S" else []), "collect_dir": notes,
                       "collect_tree": "submission" if pol in a.box_check.split(",") else ""}
        r = vfrun.run_eval(f"proof-{pol.lower()}", store=a.store, out_dir=out_dir, harness=harness, instances=ids, cpu=a.cpu,
                           task={"item_isolation": a.isolation, "limits": limits})
        rolls = [vfrun.rollout(ep) for ep in r["episodes"]]
        if len(rolls) != len(ids):
            raise SystemExit(f"policy {pol}: {len(rolls)} episodes for {len(ids)} instances\n{r['log_tail']}")
        state["runs"][pol] = {"rollouts": rolls, "wall_s": r["wall_s"], "host_cpu_s": r["host_cpu_s"], "returncode": r["returncode"]}
        json.dump(state, open(state_f, "w"))
        print(f"{pol}: {[round(x['reward_skill_vs_O'], 3) for x in rolls]} ({time.time() - t0:.0f}s)", flush=True)
    # ---- the taskset's default, one fresh box per item, on the first world: same submission, same scores? ----
    state.setdefault("box", {})
    for pol in [p for p in a.box_check.split(",") if p and p in pols and a.isolation == "shared"]:
        if pol in state["box"]:
            continue
        if pol == "C":
            harness = {"agent_dir": os.path.join(a.store, "{instance_id}", "work", "reference_C"), "script": "install_prebuilt.py", "label": "C-box"}
        else:                                                # the SAME frozen files as the shared-mode rollout, re-installed
            x = next(r for r in state["runs"][pol]["rollouts"] if r["instance_id"] == ids[0])
            src, dst = os.path.join(notes, x["trace_id"], "submission_copy"), os.path.join(a.store, ids[0], "work", f"reference_{pol}")
            if not os.path.isdir(src):
                continue
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst)
            shutil.copy(os.path.join(ROOT, "agents", "install_prebuilt.py"), os.path.join(dst, "install_prebuilt.py"))
            harness = {"agent_dir": dst, "script": "install_prebuilt.py", "label": f"{pol}-box"}
        r = vfrun.run_eval(f"proof-{pol.lower()}-box", store=a.store, out_dir=out_dir, harness=harness, instances=ids[:1], cpu=a.cpu,
                           task={"item_isolation": "box", "item_boxes_parallel": 2 if pol == "D" else 1, "limits": limits})
        if len(r["episodes"]) != 1:
            raise SystemExit(f"box check {pol}: no episode\n{r['log_tail']}")
        state["box"][pol] = {"rollout": vfrun.rollout(r["episodes"][0]), "wall_s": r["wall_s"], "host_cpu_s": r["host_cpu_s"]}
        json.dump(state, open(state_f, "w"))
        print(f"{pol} (one box per item, world 0): {state['box'][pol]['rollout']['reward_skill_vs_O']:.3f} ({time.time() - t0:.0f}s)", flush=True)

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
            else:                                            # a rollout without a reward: every item as the null policy (ruling E3)
                from physim2_env import grading as GRADING
                ex = INST.FrozenExam(hidden)
                fb = GRADING.fallback(hidden, a.world, a.config)
                np.savez_compressed(os.path.join(g, f"{pol}.npz"), es=fb["es"], failed=np.ones(ex.n, bool), cpu=np.zeros(ex.n))
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
                "ended": (x.get("info") or {}).get("ended"), "limits": (x.get("info") or {}).get("limits"),
                "box_caps": (x.get("info") or {}).get("box_caps"),
                "grade": {k: gr.get(k) for k in ("n_items", "n_failed", "fallback", "cpu_s_mean", "cpu_s_max", "layers", "items_with_leftovers",
                                                 "cleanup_between_items", "seconds", "isolation", "validation", "item_boxes",
                                                 "item_box_wall_s_mean", "infrastructure_failed_items")}}
        if "S" in pols:                                      # how close was the scripted inference (no theta is written)
            x = next(r for r in state["runs"]["S"]["rollouts"] if r["instance_id"] == iid)
            f = os.path.join(notes, x["trace_id"], "posterior_draws_u.npy")
            if os.path.exists(f):
                theta = np.array(json.load(open(os.path.join(hidden, "instance.json")))["theta"])
                u_true = (theta - (W.PRIOR_LO + W.PRIOR_HI) / 2) / ((W.PRIOR_HI - W.PRIOR_LO) / 2)
                rec["S_abs_error_over_prior_sd"] = (np.abs(np.load(f).mean(0) - u_true) * np.sqrt(3)).tolist()
        rec["table"] = GR.table(hidden, pols, n_boot=500)
        if "C" in pols and a.cross_check:
            try:
                rec["same_submission_through_round5_grader"] = cross_check(a.store, iid, a.world, a.config)
            except Exception as e:
                rec["same_submission_through_round5_grader"] = {"error": f"{type(e).__name__}: {str(e)[:200]}"}
        per_world.append(rec)
    # ---- per-item scores, for anyone who wants to recompute the table without the store ----
    items = {"policies": np.array(pols), "instance_ids": np.array(ids)}
    for k in ("K", "O"):
        items[k] = np.stack([INST.FrozenExam(h).references()[k] for h in hiddens])
    for pol in pols:
        z = [np.load(os.path.join(h, "grades", f"{pol}.npz")) for h in hiddens]
        items[f"es_{pol}"], items[f"failed_{pol}"] = np.stack([x["es"] for x in z]), np.stack([x["failed"] for x in z])
    items_f = os.path.splitext(os.path.abspath(a.out))[0] + "_items.npz"
    os.makedirs(os.path.dirname(items_f), exist_ok=True)
    np.savez_compressed(items_f, **items)
    # ---- one box per item against one box for all items: identical per-item scores for the same frozen files ----
    box = {}
    for pol, b in state.get("box", {}).items():
        x = b["rollout"]
        g = os.path.join(hiddens[0], "grades")
        if not x["graded"]:
            box[pol] = {"graded": False, "errors": x["errors"]}
            continue
        zb, zs = np.load(os.path.join(g, f"{x['trace_id']}.npz")), np.load(os.path.join(g, f"{pol}.npz"))
        xs = next(r for r in state["runs"][pol]["rollouts"] if r["instance_id"] == ids[0])
        box[pol] = {"graded": True, "trace_id": x["trace_id"], "n_failed": int(zb["failed"].sum()), "identical_per_item_scores": bool(np.array_equal(zb["es"], zs["es"])),
                    "max_abs_difference": float(np.abs(zb["es"] - zs["es"]).max()), "reward_box": x["reward_skill_vs_O"], "reward_shared": xs["reward_skill_vs_O"],
                    "same_frozen_files": (x["submission"] or {}).get("sha256") == (xs["submission"] or {}).get("sha256"),
                    "grade": {k: x["grade"].get(k) for k in ("isolation", "item_boxes", "item_boxes_parallel", "item_box_wall_s_mean", "item_boxes_cpu_s", "infrastructure_failed_items",
                                                              "seconds", "layers", "validation")},
                    "wall_s": x["wall_s"], "cpu_s": x["cpu_s"], "vf_eval_wall_s": b["wall_s"], "vf_eval_host_cpu_s": b["host_cpu_s"],
                    "shared_grade_seconds": xs["grade"].get("seconds")}
    # ---- red team 8, after ruling E3: a failed item is scored as the NULL policy, which every agent holds
    #      anyway (it is the baseline in its box). What is "crash where I would lose to the null policy" worth? ----
    crash = {p: None for p in ("D", "S", "P0") if p in pols and "null" in pols}  # filled below, once the valid cells are known
    rolls = [r for p in pols for r in state["runs"][p]["rollouts"]]
    out = {"world": a.world, "config_name": a.config, "config": json.load(open(config_path(a.config))), "profile": a.profile,
           "instance_ids": ids, "box_memory_gb_requested": a.memory,
           "sizes": sizes, "n_worlds": a.worlds, "policy_labels": LABELS, "PILOT_NEVER_REUSE_AS_EXAM": True,
           "hidden_values_in_this_file": "none (theta, secrets and items stay in the worker's store, which is deleted)",
           "route": "vf-eval physim2-env --env.id isolated-verifier, docker runtime, physim2-script harness, --no-push",
           "platform": {"machine": platform.machine(), "python": platform.python_version(), "cpu_count": os.cpu_count(),
                        "backend": "cpu", "verifiers": __import__("verifiers").__version__, "box_cpus": a.cpu,
                        "docker": subprocess.run(["docker", "version", "--format", "{{.Server.Version}}"], capture_output=True, text=True,
                                                 timeout=60, env=vfrun.child_env()).stdout.strip()},
           "grading_mode": {"table": f"item_isolation = {a.isolation}", "taskset_default": "item_isolation = box (one fresh box per item)"},
           "one_box_per_item_check_world_0": box, "per_item_scores_file": os.path.basename(items_f),
           "pooled": GR.table(hiddens, pols, labels=LABELS), "per_world": per_world,
           "rollout_cost": {
               "n_rollouts": len(rolls),
               "wall_s_per_rollout_mean": float(np.mean([r["wall_s"]["total"] for r in rolls])),
               "wall_s_per_rollout_max": float(np.max([r["wall_s"]["total"] for r in rolls])),
               "agent_box_cpu_s_unverified_mean": float(np.mean([r["cpu_s"]["agent_box_unverified"] or 0 for r in rolls])),
               "verifier_box_cpu_s_mean": float(np.mean([r["cpu_s"]["verifier_box"] or 0 for r in rolls])),
               "vf_eval_host_cpu_s_per_rollout": float(sum(state["runs"][p]["host_cpu_s"] for p in pols) / len(rolls)),
               "vf_eval_wall_s_per_policy": {p: state["runs"][p]["wall_s"] for p in pols},
               "note": "wall = boot + setup + agent + finalize of the solver trace plus the verifier phase (setup, restore, staging, "
                       "reward); box CPU = the cgroup counter of each container (the agent box's is read inside a box where the agent is root: "
                       "unverified); host CPU = vf-eval and its children (laboratory "
                       "process, docker CLI), shared by the rollouts of one invocation"},
           "all_graded": all(r["graded"] for r in rolls), "all_ok": all(r["ok"] for r in rolls),
           "n_failed_items_total": int(sum((r["grade"].get("n_failed") or 0) for r in rolls)),
           "wall_s": state.get("wall_s_before", 0.0) + time.time() - t0, "invocations": state.get("invocations", 0) + 1,
           "driver_cpu_s": time.process_time() - c0}
    state["wall_s_before"], state["invocations"] = out["wall_s"], out["invocations"]   # this tool is resumable: wall time adds up
    json.dump(state, open(state_f, "w"))
    valid = np.array(out["pooled"]["valid_cells"], bool)
    Kf, Of = items["K"].reshape(-1, len(valid))[:, valid].sum(1), items["O"].reshape(-1, len(valid))[:, valid].sum(1)
    Nf = items["es_null"].reshape(-1, len(valid))[:, valid].sum(1) if "null" in pols else None
    for pol in crash:
        e = items[f"es_{pol}"].reshape(-1, len(valid))[:, valid].sum(1)
        worse = e > Nf
        sk = lambda v: float((Kf.mean() - v.mean()) / (Kf.mean() - Of.mean()))  # noqa: E731
        crash[pol] = {"items": int(len(e)), "items_scored_worse_than_null": int(worse.sum()), "skill_vs_O": sk(e),
                      "skill_vs_O_had_exactly_those_items_failed": sk(np.where(worse, Nf, e))}
    out["failed_item_is_null_counterfactual"] = dict(crash, note="what a predictor would gain if it could fail exactly the items on which it "
                                                                 "scores worse than the null policy; it holds that policy itself (the baseline "
                                                                 "in its box), so nothing here is a gift of the grader")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    p = out["pooled"]
    print(json.dumps({k: round(v["vs_C"], 4) for k, v in p["policies"].items() if v["vs_C"] is not None}))
    if "acceptance" in p:
        print(json.dumps({k: p["acceptance"].get(k) for k in ("sigma", "null_is", "rho", "sigma_worlds", "rho_worlds")}))


if __name__ == "__main__":
    main()
