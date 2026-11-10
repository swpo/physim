"""vfrun -- drive `vf-eval` for a scripted, model-free run and read back what it saved.

One call = one vf-eval process: the stock isolated grader (`env.id = "isolated-verifier"`), the Docker runtime,
the physim2-env taskset, the physim2-script harness, no upload (`push = false`, PRIME_RUNS_MODE=disabled), no
retries, one episode at a time, and NO MODEL CREDENTIAL: the child is given a stand-in client (NO_MODEL_CLIENT)
and is started through tools/vfeval.py, which closes verifiers' reader of ~/.prime/config.json before verifiers
is imported.

The child's environment (host-safety audit, round 3, M1) is built from an ALLOW-LIST: of the caller's
environment only the names in ENV_PASS reach vf-eval, and through it the `docker` client and the laboratory
process (both inherit vf-eval's environment). Everything else is set here. A tool also refuses to start when
its own environment holds a name of ENV_REFUSE (the names RUNBOOK_MAC.md, step 0, looks for): such a name
could send Docker commands to another engine or imports to another checkout before this code can do anything.

Interruption (host safety): VF_RUN_ID must be set by whoever starts a tool; verifiers puts it on every container
it creates as the label `verifiers.run`, so the containers of an interrupted run can be listed by that label
and by nothing wider (a name filter `vf-` also matches other people's verifiers runs). vf-eval is never killed
outright: when the time is up, when the disk watchdog trips, or when this process is told to stop (SIGTERM,
Ctrl-C), it gets ONE SIGTERM, on which it removes its containers and stops its laboratory process itself, and
SIGKILL only if it is still there after STOP_GRACE_S. A vf-eval that this tool had to stop, or that died of a
signal, ends the tool with a status other than 0 (EXIT_STOPPED, EXIT_DISK): nothing further is started.
Before each run Docker must answer; if it does not, nothing is started and nothing is recorded as run.

Disk watchdog (coordinator's requirement D1): before a run the free space of the file system that holds the
home folder must be at least the floor (--disk-floor-gib of the tools, default 8); during a run it is looked at
every DISK_CHECK_S seconds and, below the floor, the run is stopped through the same stop path as a time limit.
The reason is written to <out_dir>/<name>.stopped.json and to the log. The watchdog deletes nothing, ever.

Also a command of its own, for a rollout from a plain config file (RUNBOOK_MAC.md, steps 2c and 3):

    VF_RUN_ID=<label> python -B tools/vfrun.py --config configs/scripted_ring.toml --run-name single-d \
        --out-dir DIR --store DIR --disk-floor-gib 8 [--dry-run] [--model-credentials prime]

Without --model-credentials the config must name the stand-in client and the scripted harness and no credential
is passed or loaded. `--model-credentials prime` is for step 3 only: PRIME_API_KEY and PRIME_TEAM_ID of the
caller are passed on and verifiers may read ~/.prime/config.json.
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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
# The child: verifiers' own `vf-eval` entry point, started in this interpreter by tools/vfeval.py (not the console
# script .venv/bin/vf-eval: that one imports verifiers before anything of ours can close the credential reader).
VF_EVAL = [sys.executable, "-B", os.path.join(HERE, "vfeval.py")]
STOP_GRACE_S = 120.0                                         # after SIGTERM: time for vf-eval to remove its containers
HELPER_GRACE_S = 20.0                                        # after SIGTERM: time for one of our own helper scripts to end
RUN_FILES = {"traces.jsonl", "configs", "logs", "metadata.json", "results.jsonl"}   # what vf-eval itself writes into a run folder

# ---- the environment (M1) ----
# The ONLY names a child takes from the caller's environment. Everything a run needs beyond them is set in child_env.
ENV_PASS = ("PATH", "HOME", "TMPDIR", "USER", "LOGNAME", "LANG", "LC_ALL", "LC_CTYPE", "TZ")
# Step 3 only (--model-credentials prime): the model key and the team it is billed to. Never the inference URL.
ENV_PASS_MODEL = ("PRIME_API_KEY", "PRIME_TEAM_ID")
# Names that must not be in the environment of a tool at all: the same list as the step-0 check of RUNBOOK_MAC.md.
# VF_RUN_ID is the one exception: the command that starts a tool sets it.
ENV_REFUSE = re.compile(r"^(PHYSIM2_|UV_|VIRTUAL_ENV|PYTHON(PATH|HOME)|DOCKER_|BUILDX_|VF_|MCP_HOST|MCP_PORT|PRIME_RUNS_MODE)")
ENV_REFUSE_EXCEPT = ("VF_RUN_ID",)
# ...and two names are accepted with exactly the value a tool itself gives its children (child_env), so that a
# helper started by a tool (tools/make_instances.py) can make the same check: this checkout, and no upload.
ENV_OWN = {"PYTHONPATH": ROOT, "PRIME_RUNS_MODE": "disabled"}
MODEL_ENV = "PHYSIM2_MODEL_CREDENTIALS"                      # read by physim2_env/_nokey.py; set here for step 3 only

# ---- no model in a scripted run (M3) ----
NO_MODEL_VAR = "PHYSIM2_NO_MODEL_KEY"                        # a name that is never set: verifiers then loads no key at all
NO_MODEL_URL = "http://127.0.0.1:9/v1"                       # the discard port on loopback: nothing listens there
NO_MODEL_CLIENT = {"type": "eval", "base_url": NO_MODEL_URL, "api_key_var": NO_MODEL_VAR}

# ---- the disk watchdog (D1) ----
GIB = 1 << 30
DISK_FLOOR_GIB = 8.0                                         # the tools set this from --disk-floor-gib
DISK_CHECK_S = 15.0
EXIT_DISK = 97                                               # refused to start, or stopped a run: free space below the floor
EXIT_STOPPED = 98                                            # vf-eval was stopped by this tool (time limit) or died of a signal


def refused_names(environ=None) -> list[str]:
    """The names in `environ` (default: this process's own environment) that no tool may be started with."""
    environ = os.environ if environ is None else environ
    return sorted(k for k in environ if ENV_REFUSE.match(k) and k not in ENV_REFUSE_EXCEPT and ENV_OWN.get(k) != environ[k])


def require_clean_environment() -> None:
    """Stop before anything is imported from the package, created or started, if this tool's own environment
    holds one of the names RUNBOOK_MAC.md, step 0, checks for. Names only are printed, never a value."""
    bad = refused_names()
    if bad:
        raise SystemExit("refused: the environment of this command holds " + ", ".join(bad) + ".\n"
                         "A tool of the pilot starts only from an environment without PHYSIM2_*, UV_*, VIRTUAL_ENV, PYTHONPATH, "
                         "PYTHONHOME, DOCKER_*, BUILDX_*, VF_* (other than the VF_RUN_ID of the command itself), MCP_HOST, MCP_PORT "
                         "and PRIME_RUNS_MODE: one of them could send Docker commands to another engine or imports to another "
                         "checkout (RUNBOOK_MAC.md, step 0). Nothing was started. Stop and report.")


def run_label() -> str:
    """$VF_RUN_ID, which becomes the label `verifiers.run` of every container of the run. Required."""
    v = os.environ.get("VF_RUN_ID", "")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{5,62}", v):
        raise SystemExit("VF_RUN_ID is not set (or not a plain label of 6 to 63 characters). Start this tool as\n"
                         "    VF_RUN_ID=<label of this run, e.g. physim2-pilot-20261110> python tools/...\n"
                         "verifiers labels every container it creates with it (verifiers.run=<label>): after an interruption\n"
                         "that label is the only way to find this run's containers without touching anybody else's.")
    return v


def child_env(extra: dict | None = None, *, model_credentials: bool = False) -> dict:
    """The environment of everything a tool starts: vf-eval (and through it the `docker` client and the
    laboratory), our helper scripts, and the tool's own `docker` calls. Built from nothing: the names of ENV_PASS
    are copied from the caller, the rest is set here, `extra` (given by the calling code, never by the session)
    comes last. No PHYSIM2_*, DOCKER_*, MCP_*, PYTHONPATH or credential of the caller can get through."""
    env = {k: os.environ[k] for k in ENV_PASS if k in os.environ}
    if os.environ.get("VF_RUN_ID"):
        env["VF_RUN_ID"] = run_label()
    if model_credentials:                                    # step 3 only
        env.update({k: os.environ[k] for k in ENV_PASS_MODEL if k in os.environ})
        env[MODEL_ENV] = "prime"
    env.update({"PRIME_RUNS_MODE": "disabled", "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
                "JAX_PLATFORMS": "cpu", "PYTHONDONTWRITEBYTECODE": "1",
                "XLA_FLAGS": "--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"})
    if not os.path.exists("/proc/sys/net/ipv6") and sys.platform == "linux":   # see tools/docker_shim/docker
        env["PATH"] = os.path.join(HERE, "docker_shim") + os.pathsep + env.get("PATH", "")
    env["PYTHONPATH"] = ROOT                                 # THIS checkout's physim2_env and physim2_script, and nothing else
    env.update(extra or {})
    return env


def endpoint_is_local(host: str) -> bool:
    """Is a Docker endpoint (`docker context inspect`: .Endpoints.docker.Host) a Unix socket of this machine?
    `tcp://`, `ssh://`, `npipe://` and an empty answer are not."""
    return isinstance(host, str) and host.startswith("unix:///") and "\n" not in host and len(host) > len("unix:///")


def require_docker() -> str:
    """The Docker server's version, or stop: a run started against a daemon that does not answer would be
    recorded as a finished, failed rollout and never repeated. Before that, the engine must be a local one: the
    context that the `docker` client of this environment uses must name a Unix socket (the allow-list keeps
    DOCKER_HOST and DOCKER_CONTEXT out, but the context file in the home folder still decides where commands
    go: finding M1). (On a timeout Python kills these `docker` clients, its own children.)"""
    env = child_env()
    try:
        c = subprocess.run(["docker", "context", "inspect", "--format", "{{.Endpoints.docker.Host}}"], capture_output=True, text=True,
                           timeout=60, env=env)
        if c.returncode or not endpoint_is_local(c.stdout.strip()):
            raise SystemExit("refused: the Docker context of this session does not name a Unix socket of this machine ("
                             + (c.stdout.strip().split("://")[0][:12] or "no answer") + "); nothing was started. Stop and report.")
        r = subprocess.run(["docker", "info", "--format", "{{.ServerVersion}}"], capture_output=True, text=True, timeout=60, env=env)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise SystemExit(f"Docker does not answer ({type(e).__name__}); nothing was started. Stop and report.") from None
    if r.returncode or not r.stdout.strip():
        raise SystemExit("Docker does not answer (`docker info` failed); nothing was started. Stop and report.\n" + r.stderr.strip()[-300:])
    return r.stdout.strip()


def free_bytes(path: str | None = None) -> int:
    """Free space, for this user, of the file system that holds `path` (default: the home folder)."""
    st = os.statvfs(path or os.path.expanduser("~"))
    return st.f_bavail * st.f_frsize


def disk_floor_bytes(gib: float | None = None) -> int:
    gib = DISK_FLOOR_GIB if gib is None else gib
    if not isinstance(gib, (int, float)) or isinstance(gib, bool) or not 0.25 <= gib <= 4096:
        raise SystemExit("refused: --disk-floor-gib must be a number from 0.25 to 4096")
    return int(gib * GIB)


def require_disk(floor: int, what: str = "this run") -> int:
    """Stop (status EXIT_DISK) before `what` if the home file system has less free space than `floor` bytes.
    Returns the free space. Deletes nothing: making room is the lead's decision, never a tool's."""
    free = free_bytes()
    if free < floor:
        print(f"refused: the disk watchdog did not start {what}: {free / GIB:.2f} GiB free on the file system of the home "
              f"folder, the floor is {floor / GIB:.2f} GiB. Nothing was started and nothing was deleted. Stop and report.", flush=True)
        raise SystemExit(EXIT_DISK)
    return free


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


def stop_child(p, grace: float | None = None) -> str:
    """Stop a child of this tool so that it cleans up after itself: ONE SIGTERM (vf-eval then removes the
    containers it created and stops its laboratory process; it ignores further signals while it does), wait up
    to `grace` seconds, and SIGKILL only if it is still running then (its containers stay in that case:
    RUNBOOK_MAC.md, "If a run was interrupted"). Returns what it took."""
    if p.poll() is not None:
        return "had exited"
    grace = STOP_GRACE_S if grace is None else grace
    p.send_signal(signal.SIGTERM)
    try:
        p.wait(timeout=grace)
        return "SIGTERM"
    except subprocess.TimeoutExpired:
        p.kill()
        p.wait()
        return "SIGTERM, then SIGKILL"


def run_child(cmd: list[str], *, env: dict, cwd: str, timeout: float, grace: float | None = None, capture: bool = True,
              disk_floor: int | None = None, check_s: float | None = None):
    """(returncode, stdout, stderr, how it ended) of one child process (vf-eval). The child ends in one of four
    ways: it exits by itself ("exited"); `timeout` is over ("stopped after ..."); the disk watchdog finds less
    than `disk_floor` bytes free ("stopped by the disk watchdog ...": looked at every `check_s` seconds); or THIS
    process is told to stop (SIGTERM, Ctrl-C) or fails, and the exception goes on. In the last three the child
    is stopped with stop_child: the one stop path. With capture=False the child writes to this process's own
    output (the log of a detached command) and the two strings are empty."""
    def on_term(signum, frame):                              # `kill <pid of the tool>` behaves like Ctrl-C
        raise KeyboardInterrupt
    main = threading.current_thread() is threading.main_thread()
    old = signal.signal(signal.SIGTERM, on_term) if main else None
    check_s = DISK_CHECK_S if check_s is None else check_s
    pipe = subprocess.PIPE if capture else None
    p = subprocess.Popen(cmd, env=env, cwd=cwd, stdin=subprocess.DEVNULL, stdout=pipe, stderr=pipe, text=True)
    out = err = ""
    try:
        deadline = time.monotonic() + timeout
        while True:
            left = deadline - time.monotonic()
            try:
                out, err = p.communicate(timeout=max(0.05, min(left, check_s) if disk_floor is not None else left))
                how = "exited"
                break
            except subprocess.TimeoutExpired:
                pass
            if time.monotonic() >= deadline:
                how = f"stopped after {timeout:.0f} s: " + stop_child(p, grace)
                out, err = p.communicate()
                break
            if disk_floor is not None:
                free = free_bytes()
                if free < disk_floor:
                    how = (f"stopped by the disk watchdog ({free / GIB:.2f} GiB free on the file system of the home folder, "
                           f"floor {disk_floor / GIB:.2f} GiB): " + stop_child(p, grace))
                    out, err = p.communicate()
                    break
    except BaseException:
        stop_child(p, grace)
        raise
    finally:
        if main:
            signal.signal(signal.SIGTERM, old)
    return p.returncode, out or "", err or "", how


def run_helper(cmd: list[str], *, cwd: str | None = None, env: dict | None = None, capture: bool = False):
    """Run one of OUR OWN helper scripts (tools/make_instances.py, tools/build_reference.py) to its end and return
    the finished process. If this tool is told to stop while the helper runs (SIGTERM, Ctrl-C), the helper is
    stopped first (ONE SIGTERM, SIGKILL after HELPER_GRACE_S) and the exception goes on: no helper is left behind
    without its tool (finding m4). A helper holds no container and no laboratory."""
    def on_term(signum, frame):
        raise KeyboardInterrupt
    main = threading.current_thread() is threading.main_thread()
    old = signal.signal(signal.SIGTERM, on_term) if main else None
    pipe = subprocess.PIPE if capture else None
    p = subprocess.Popen(["nice", "-n", "10", *cmd], cwd=cwd, env=child_env() if env is None else env, stdin=subprocess.DEVNULL,
                         stdout=pipe, stderr=pipe, text=True)
    try:
        out, err = p.communicate()
    except BaseException:
        stop_child(p, HELPER_GRACE_S)
        raise
    finally:
        if main:
            signal.signal(signal.SIGTERM, old)
    return subprocess.CompletedProcess(cmd, p.returncode, out or "", err or "")


def stopped_record(path: str, how: str, returncode, floor: int | None) -> dict:
    """Write down why a run was stopped (counts and words only) and return the record."""
    rec = {"ended": how, "returncode": returncode, "time_unix": time.time(), "free_bytes_now": free_bytes(),
           "disk_floor_bytes": floor, "deleted_by_the_watchdog": "nothing"}
    try:
        with open(path, "w") as f:
            json.dump(rec, f, indent=1)
    except OSError:
        pass
    return rec


def end_of_child(rc, how: str, record: str, floor: int | None) -> None:
    """After a child ended: return if it exited by itself; otherwise record why, say so, and end THIS tool with a
    status other than 0. A vf-eval that was killed outright (SIGKILL after the grace period, or a signal from
    elsewhere) could not remove its containers, and on macOS its laboratory process stays as well: the next
    thing to do is RUNBOOK_MAC.md, "If a run was interrupted", not another rollout (finding m5)."""
    if how == "exited" and (rc is None or rc >= 0):
        return
    stopped_record(record, how, rc, floor)
    if "disk watchdog" in how:
        print(f"refused: {how}. The run was stopped through the tool's one stop path; nothing was deleted. Stop and report "
              "(RUNBOOK_MAC.md, \"If a run was interrupted\", points 1 to 5).", flush=True)
        raise SystemExit(EXIT_DISK)
    left = " Its containers and its laboratory process may be left." if "SIGKILL" in how or (rc is not None and rc < 0 and how == "exited") else ""
    print(f"refused to go on: vf-eval {how if how != 'exited' else f'died of signal {-rc}'}.{left} Nothing further was started. "
          "Stop and report (RUNBOOK_MAC.md, \"If a run was interrupted\").", flush=True)
    raise SystemExit(EXIT_STOPPED)


def run_eval(name: str, *, store: str, out_dir: str, harness: dict, instances=None, task: dict | None = None,
             cpu: float | None = 2, env: dict | None = None, timeout: float = 3600, image: str | None = None,
             timeouts: dict | None = None, disk_floor_gib: float | None = None) -> dict:
    """Returns {"episodes": [...], "wall_s", "host_cpu_s", "returncode", "run_dir", "log_tail"}.
    The task option `agent_key` defaults to the run name: `single_use` stays ON, and each scripted policy or
    probe is its own agent (the same run name on the same instance is refused, as a re-roll would be)."""
    import tomli_w
    cfg = {"model": "none/scripted", "num_rollouts": 1, "max_concurrent": 1, "push": False, "output_dir": out_dir,
           "client": dict(NO_MODEL_CLIENT),                  # no model is called, and no model credential is loaded
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
    require_clean_environment()
    label = run_label()                                      # before anything is created or removed
    floor = disk_floor_bytes(disk_floor_gib)
    require_disk(floor, f"the run {name}")
    require_docker()
    os.makedirs(out_dir, exist_ok=True)
    run_dir = os.path.join(out_dir, name)
    clear_run_dir(run_dir, name)                             # only ever a folder an earlier call of this function made
    toml = os.path.join(out_dir, f"{name}.toml")
    with open(toml, "wb") as f:
        tomli_w.dump(cfg, f)
    t0, r0 = time.time(), resource.getrusage(resource.RUSAGE_CHILDREN)
    rc, out, err, how = run_child(["nice", "-n", "10", *VF_EVAL, "@", toml, "--no-rich"], env=child_env(env), cwd=out_dir,
                                  timeout=timeout, disk_floor=floor)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    if how != "exited" or rc < 0:
        print((out + err)[-1500:], flush=True)
    end_of_child(rc, how, os.path.join(out_dir, f"{name}.stopped.json"), floor)
    episodes = []
    f = os.path.join(run_dir, "traces.jsonl")
    if os.path.exists(f):
        episodes = [json.loads(line) for line in open(f)]
    return {"episodes": episodes, "wall_s": time.time() - t0, "returncode": rc, "run_dir": run_dir, "config": toml,
            "host_cpu_s": (r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime), "log_tail": (out + err)[-3000:],
            "ended": how, "run_label": label}


def check_config(path: str, *, model_credentials: bool, dry_run: bool) -> dict:
    """Read a config file for the command form of this tool and refuse what it must not start. Always: no upload.
    Without model credentials (and not a dry run): the stand-in client and the scripted harness, so that no model
    can be called and no key is looked for."""
    import tomllib
    with open(path, "rb") as f:
        cfg = json.loads(json.dumps(tomllib.load(f)))
    if cfg.get("push") is not False:
        raise SystemExit("refused: the config does not say `push = false`")
    if (((cfg.get("env") or {}).get("agent") or {}).get("runtime") or {}).get("type") != "docker":
        raise SystemExit("refused: the config does not use the docker runtime")
    if not model_credentials and not dry_run:
        client = cfg.get("client") or {}
        harness = (((cfg.get("env") or {}).get("agent") or {}).get("harness") or {}).get("id")
        if client.get("api_key_var") != NO_MODEL_VAR or client.get("base_url") != NO_MODEL_URL or harness != "physim2-script":
            raise SystemExit("refused: without --model-credentials this tool starts scripted rollouts only: the config must have\n"
                             f"    [client]\n    base_url = \"{NO_MODEL_URL}\"\n    api_key_var = \"{NO_MODEL_VAR}\"\n"
                             "and the harness physim2-script. A model rollout is step 3 of RUNBOOK_MAC.md and has its own command.")
    return cfg


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="one rollout through vf-eval from a config file, with the environment allow-list, "
                                             "the disk watchdog and the one stop path of this tool")
    ap.add_argument("--config", required=True, help="a TOML file, relative to the study folder or absolute")
    ap.add_argument("--run-name", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--store", required=True)
    ap.add_argument("--disk-floor-gib", type=float, default=DISK_FLOOR_GIB)
    ap.add_argument("--timeout", type=float, default=5400.0, help="seconds after which vf-eval is told to stop")
    ap.add_argument("--dry-run", action="store_true", help="vf-eval resolves the config, writes it and exits; no rollout")
    ap.add_argument("--model-credentials", choices=["prime"], default=None,
                    help="STEP 3 ONLY: pass PRIME_API_KEY and PRIME_TEAM_ID on and let verifiers read ~/.prime/config.json")
    a = ap.parse_args(argv)
    require_clean_environment()
    run_label()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,40}", a.run_name):
        raise SystemExit("refused: --run-name must be lower-case letters, digits and hyphens")
    config = a.config if os.path.isabs(a.config) else os.path.join(ROOT, a.config)
    check_config(config, model_credentials=bool(a.model_credentials), dry_run=a.dry_run)
    floor = disk_floor_bytes(a.disk_floor_gib)
    store, out_dir = os.path.abspath(os.path.expanduser(a.store)), os.path.abspath(os.path.expanduser(a.out_dir))
    cmd = ["nice", "-n", "10", *VF_EVAL, "@", config, "--run.name", a.run_name, "-o", out_dir]
    if a.dry_run:
        cmd.append("--dry-run")
    else:
        cmd.append("--no-rich")
        require_disk(floor, f"the run {a.run_name}")
        require_docker()
    os.makedirs(out_dir, exist_ok=True)
    # cwd = the study folder: `agent_dir` of a config file is relative to it
    rc, _, _, how = run_child(cmd, env=child_env({"PHYSIM2_STORE": store}, model_credentials=bool(a.model_credentials)), cwd=ROOT,
                              timeout=a.timeout, capture=False, disk_floor=None if a.dry_run else floor)
    end_of_child(rc, how, os.path.join(out_dir, f"{a.run_name}.stopped.json"), floor)
    return rc


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


if __name__ == "__main__":
    sys.exit(main())
