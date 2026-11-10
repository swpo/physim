"""vfrun -- drive `vf-eval` for a scripted, model-free run and read back what it saved.

One call = one vf-eval process: the stock isolated grader (`env.id = "isolated-verifier"`), the Docker runtime,
the physim2-env taskset, the physim2-script harness, no upload (`push = false`, PRIME_RUNS_MODE=disabled, and
PRIME_API_KEY removed from the child's environment), no retries, one episode at a time.
"""
from __future__ import annotations

import json
import os
import resource
import shutil
import subprocess
import sys
import time

import tomli_w

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VF_EVAL = os.path.join(os.path.dirname(sys.executable), "vf-eval")


def child_env(extra: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if k not in ("PRIME_API_KEY",)}
    env.update({"PRIME_RUNS_MODE": "disabled", "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
                "JAX_PLATFORMS": "cpu", "PYTHONDONTWRITEBYTECODE": "1",
                "XLA_FLAGS": "--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"})
    if not os.path.exists("/proc/sys/net/ipv6") and sys.platform == "linux":   # see tools/docker_shim/docker
        env["PATH"] = os.path.join(HERE, "docker_shim") + os.pathsep + env.get("PATH", "")
    env.update(extra or {})
    return env


def run_eval(name: str, *, store: str, out_dir: str, harness: dict, instances=None, task: dict | None = None,
             cpu: float | None = 2, env: dict | None = None, timeout: float = 3600, image: str | None = None) -> dict:
    """Returns {"episodes": [...], "wall_s", "host_cpu_s", "returncode", "run_dir", "log_tail"}."""
    cfg = {"model": "none/scripted", "num_rollouts": 1, "max_concurrent": 1, "push": False, "output_dir": out_dir,
           "run": {"name": name},
           "env": {"id": "isolated-verifier",
                   "taskset": {"id": "physim2-env", "store": store},
                   "agent": {"runtime": {"type": "docker"}, "harness": dict({"id": "physim2-script"}, **harness)},
                   "retries": {"max_retries": 0},
                   "verifier": {"retries": 0}}}
    cfg["env"]["agent"]["retries"] = {"max_retries": 0}
    if cpu:
        cfg["env"]["agent"]["runtime"]["cpu"] = cpu
    if instances is not None:
        cfg["env"]["taskset"]["instances"] = list(instances)
    if image:
        cfg["env"]["taskset"]["image"] = image
    if task:
        cfg["env"]["taskset"]["task"] = task
    os.makedirs(out_dir, exist_ok=True)
    run_dir = os.path.join(out_dir, name)
    if os.path.exists(run_dir):
        shutil.rmtree(run_dir)
    toml = os.path.join(out_dir, f"{name}.toml")
    with open(toml, "wb") as f:
        tomli_w.dump(cfg, f)
    t0, r0 = time.time(), resource.getrusage(resource.RUSAGE_CHILDREN)
    p = subprocess.run(["nice", "-n", "10", VF_EVAL, "@", toml, "--no-rich"], env=child_env(env), capture_output=True,
                       text=True, timeout=timeout, cwd=out_dir)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    episodes = []
    f = os.path.join(run_dir, "traces.jsonl")
    if os.path.exists(f):
        episodes = [json.loads(line) for line in open(f)]
    return {"episodes": episodes, "wall_s": time.time() - t0, "returncode": p.returncode, "run_dir": run_dir, "config": toml,
            "host_cpu_s": (r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime), "log_tail": (p.stdout + p.stderr)[-3000:]}


def rollout(ep: dict) -> dict:
    """The public-safe summary of one saved episode (one solver trace), with K for a rollout without a reward."""
    tr = ep["traces"][0]
    info = tr.get("info", {})
    ph, sc = info.get("physim2", {}), info.get("physim2_script", {})
    tm = tr.get("timing", {})
    g = ph.get("grade") or {}
    span = lambda k: (tm.get(k, {}).get("end", 0) or 0) - (tm.get(k, {}).get("start", 0) or 0)  # noqa: E731
    reward = (tr.get("rewards", {}).get("skill") or {}).get("score")
    return {"trace_id": tr["id"], "instance_id": tr["task"]["data"].get("instance_id"), "ok": tr.get("ok"),
            "errors": [e.get("type") for e in tr.get("errors", [])], "stop_condition": tr.get("stop_condition"),
            "graded": reward is not None, "reward_skill_vs_O": 0.0 if reward is None else reward,
            "scored_as_K_because_ungraded": reward is None,
            "script_exit_code": sc.get("exit_code"), "address_file_matches_tool_url": sc.get("address_file_matches_tool_url"),
            "submission": ph.get("submission"), "lab": ph.get("lab"), "grade": g, "verifier_box": ph.get("verifier_box"),
            "wall_s": {"boot": span("boot"), "setup": span("setup"), "agent": span("agent"), "finalize": span("finalize"),
                       "verifier": g.get("verifier_wall_s"),
                       "total": span("boot") + span("setup") + span("agent") + span("finalize") + (g.get("verifier_wall_s") or 0.0)},
            "cpu_s": {"agent_box": ph.get("agent_box_cpu_s"), "verifier_box": g.get("verifier_box_cpu_s"),
                      "worker_in_reward": g.get("worker_cpu_s")},
            "info": ph}
