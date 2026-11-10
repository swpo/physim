"""vfrun -- drive `vf-eval` for a scripted, model-free run and read back what it saved.

One call = one vf-eval process: the stock isolated grader (`env.id = "isolated-verifier"`), the Docker runtime,
the physim2-env taskset, the physim2-script harness, no upload (`push = false`, PRIME_RUNS_MODE=disabled, and
PRIME_API_KEY removed from the child's environment), no retries, one episode at a time.

Interruption (host safety): VF_RUN_ID must be set by whoever starts a tool; verifiers puts it on every container
it creates as the label `verifiers.run`, so the containers of an interrupted run can be listed by that label
and by nothing wider (a name filter `vf-` also matches other people's verifiers runs). vf-eval is never killed
outright: when the time is up, or when this process is told to stop (SIGTERM, Ctrl-C), it gets ONE SIGTERM, on
which it removes its containers and stops its laboratory process itself, and SIGKILL only if it is still there
after STOP_GRACE_S. Before each run Docker must answer; if it does not, nothing is started and nothing is
recorded as run.
"""
from __future__ import annotations

import json
import os
import re
import resource
import shutil
import signal
import subprocess
import sys
import threading
import time

import tomli_w

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VF_EVAL = os.path.join(os.path.dirname(sys.executable), "vf-eval")
STOP_GRACE_S = 120.0                                         # after SIGTERM: time for vf-eval to remove its containers
RUN_FILES = {"traces.jsonl", "configs", "logs", "metadata.json", "results.jsonl"}   # what vf-eval itself writes into a run folder


def run_label() -> str:
    """$VF_RUN_ID, which becomes the label `verifiers.run` of every container of the run. Required."""
    v = os.environ.get("VF_RUN_ID", "")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{5,62}", v):
        raise SystemExit("VF_RUN_ID is not set (or not a plain label of 6 to 63 characters). Start this tool as\n"
                         "    VF_RUN_ID=<label of this run, e.g. physim2-pilot-20261110> python tools/...\n"
                         "verifiers labels every container it creates with it (verifiers.run=<label>): after an interruption\n"
                         "that label is the only way to find this run's containers without touching anybody else's.")
    return v


def require_docker() -> str:
    """The Docker server's version, or stop: a run started against a daemon that does not answer would be
    recorded as a finished, failed rollout and never repeated."""
    try:
        r = subprocess.run(["docker", "info", "--format", "{{.ServerVersion}}"], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise SystemExit(f"Docker does not answer ({type(e).__name__}); nothing was started. Stop and report.") from None
    if r.returncode or not r.stdout.strip():
        raise SystemExit("Docker does not answer (`docker info` failed); nothing was started. Stop and report.\n" + r.stderr.strip()[-300:])
    return r.stdout.strip()


def clear_run_dir(run_dir: str, name: str) -> bool:
    """Remove the run folder of an EARLIER call with the same name, and only if it is a real directory that holds
    nothing but vf-eval's own files. Anything else: refuse (SystemExit). Returns whether a folder was removed."""
    if not os.path.lexists(run_dir):
        return False
    inside = set(os.listdir(run_dir)) if os.path.isdir(run_dir) and not os.path.islink(run_dir) else {"?"}
    if not name or os.path.basename(run_dir) != name or not inside <= RUN_FILES:
        raise SystemExit(f"refusing to replace {run_dir}: it does not look like an earlier run of this tool (found {sorted(inside)[:6]})")
    shutil.rmtree(run_dir)
    return True


def stop_child(p, grace: float = STOP_GRACE_S) -> str:
    """Stop a vf-eval process so that it cleans up after itself: ONE SIGTERM (vf-eval then removes the containers
    it created and stops its laboratory process; it ignores further signals while it does), wait up to `grace`
    seconds, and SIGKILL only if it is still running then (its containers stay in that case: RUNBOOK_MAC.md,
    "If a run was interrupted"). Returns what it took."""
    if p.poll() is not None:
        return "had exited"
    p.send_signal(signal.SIGTERM)
    try:
        p.wait(timeout=grace)
        return "SIGTERM"
    except subprocess.TimeoutExpired:
        p.kill()
        p.wait()
        return "SIGTERM, then SIGKILL"


def run_child(cmd: list[str], *, env: dict, cwd: str, timeout: float, grace: float = STOP_GRACE_S):
    """(returncode, stdout, stderr, how it ended) of one vf-eval process. When `timeout` is over the child is
    stopped with stop_child and this returns; when THIS process is told to stop (SIGTERM, Ctrl-C) or fails, the
    child is stopped the same way before the exception goes on."""
    def on_term(signum, frame):                              # `kill <pid of the tool>` behaves like Ctrl-C
        raise KeyboardInterrupt
    main = threading.current_thread() is threading.main_thread()
    old = signal.signal(signal.SIGTERM, on_term) if main else None
    p = subprocess.Popen(cmd, env=env, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        try:
            out, err = p.communicate(timeout=timeout)
            how = "exited"
        except subprocess.TimeoutExpired:
            how = f"stopped after {timeout:.0f} s: " + stop_child(p, grace)
            out, err = p.communicate()
    except BaseException:
        stop_child(p, grace)
        raise
    finally:
        if main:
            signal.signal(signal.SIGTERM, old)
    return p.returncode, out or "", err or "", how


def child_env(extra: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if k not in ("PRIME_API_KEY",)}
    env.update({"PRIME_RUNS_MODE": "disabled", "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
                "JAX_PLATFORMS": "cpu", "PYTHONDONTWRITEBYTECODE": "1",
                "XLA_FLAGS": "--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"})
    if not os.path.exists("/proc/sys/net/ipv6") and sys.platform == "linux":   # see tools/docker_shim/docker
        env["PATH"] = os.path.join(HERE, "docker_shim") + os.pathsep + env.get("PATH", "")
    # THIS checkout's physim2_env and physim2_script, wherever the environment's editable install points
    env["PYTHONPATH"] = ROOT + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    env.update(extra or {})
    return env


def run_eval(name: str, *, store: str, out_dir: str, harness: dict, instances=None, task: dict | None = None,
             cpu: float | None = 2, env: dict | None = None, timeout: float = 3600, image: str | None = None,
             timeouts: dict | None = None) -> dict:
    """Returns {"episodes": [...], "wall_s", "host_cpu_s", "returncode", "run_dir", "log_tail"}.
    The task option `agent_key` defaults to the run name: `single_use` stays ON, and each scripted policy or
    probe is its own agent (the same run name on the same instance is refused, as a re-roll would be)."""
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
    cfg["env"]["taskset"]["task"] = dict({"agent_key": name}, **(task or {}))
    if timeouts:
        cfg["env"]["agent"]["timeout"] = timeouts
    label = run_label()                                      # before anything is created or removed
    require_docker()
    os.makedirs(out_dir, exist_ok=True)
    run_dir = os.path.join(out_dir, name)
    clear_run_dir(run_dir, name)                             # only ever a folder an earlier call of this function made
    toml = os.path.join(out_dir, f"{name}.toml")
    with open(toml, "wb") as f:
        tomli_w.dump(cfg, f)
    t0, r0 = time.time(), resource.getrusage(resource.RUSAGE_CHILDREN)
    rc, out, err, how = run_child(["nice", "-n", "10", VF_EVAL, "@", toml, "--no-rich"], env=child_env(env), cwd=out_dir,
                                  timeout=timeout)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    episodes = []
    f = os.path.join(run_dir, "traces.jsonl")
    if os.path.exists(f):
        episodes = [json.loads(line) for line in open(f)]
    return {"episodes": episodes, "wall_s": time.time() - t0, "returncode": rc, "run_dir": run_dir, "config": toml,
            "host_cpu_s": (r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime), "log_tail": (out + err)[-3000:],
            "ended": how, "run_label": label}


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
            "script_refused_to_run": "refused:" in (sc.get("log_tail") or ""),      # a box script's gate (agents/*.py) said no
            "submission": ph.get("submission"), "lab": ph.get("lab"), "grade": g, "verifier_box": ph.get("verifier_box"),
            "item_isolation": g.get("isolation"),
            "wall_s": {"boot": span("boot"), "setup": span("setup"), "agent": span("agent"), "finalize": span("finalize"),
                       "verifier": g.get("verifier_wall_s"),
                       "total": span("boot") + span("setup") + span("agent") + span("finalize") + (g.get("verifier_wall_s") or 0.0)},
            "cpu_s": {"agent_box_unverified": ph.get("agent_box_cpu_s_unverified"), "verifier_box": g.get("verifier_box_cpu_s"),
                      "item_boxes": g.get("item_boxes_cpu_s"), "worker_in_reward": g.get("worker_cpu_s")},
            "info": ph}
