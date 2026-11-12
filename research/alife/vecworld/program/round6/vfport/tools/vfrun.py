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

Also a command of its own, in two forms:

    VF_RUN_ID=<label> python -B tools/vfrun.py --config configs/scripted_ring.toml --run-name single-d \
        --out-dir DIR --store DIR --disk-floor-gib 8 [--dry-run]

the COMMAND FORM (RUNBOOK_MAC.md, step 2c): a scripted rollout from a vf-eval config file. The config must name
the stand-in client and the scripted harness; no credential is passed or loaded; a model cannot be called.

    VF_RUN_ID=<label> python -B tools/vfrun.py --request JOB.json --pilot DIR --stage instance|reference|dry-run|rollout|close \
        --disk-floor-gib 8 [--shared-ledger FILE] [--model-credentials prime]

the REQUEST ROUTE (step 3, round 4): one stage of the rollout that a request file describes (schema
rollout-job/v1; tools/check_request.py). Every stage checks the request, the pin, the strict schema of the
rollout config (tools/check_config.py), the pilot folder and the lead's standing go. Stage `rollout` is the only
one that can spend money: it needs `--model-credentials prime` (PRIME_API_KEY and PRIME_TEAM_ID of the caller
are passed on to vf-eval, and verifiers may read ~/.prime/config.json), reads the model's listed prices, refuses
a cap below one worst-case call or a bound above the lead's ceiling (one total: the pilot folder's ledger plus
what --shared-ledger says other machines spent), reserves the bound in <pilot>/LEDGER.jsonl,
gives vf-eval the spend table of physim2_env/spend.py, and closes the ledger row when the run has ended, however
it ended.
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
# round 4 (audit round 3, G1): PYTHONEXECUTABLE and __PYVENV_LAUNCHER__ move the interpreter's idea of its own
# environment (CPython Modules/getpath.py) and are refused like PYTHONHOME.
# round 4 (the Mac review's R3-7): DYLD_* move the libraries a program of macOS loads; no tool starts with one.
ENV_REFUSE = re.compile(r"^(PHYSIM2_|UV_|VIRTUAL_ENV|PYTHON(PATH|HOME|EXECUTABLE)|__PYVENV_LAUNCHER__|DYLD_|DOCKER_|BUILDX_|VF_|MCP_HOST|MCP_PORT|"
                        r"PRIME_RUNS_MODE)")
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
                         "PYTHONHOME, PYTHONEXECUTABLE, __PYVENV_LAUNCHER__, DYLD_*, DOCKER_*, BUILDX_*, VF_* (other than the VF_RUN_ID of "
                         "the command itself), MCP_HOST, MCP_PORT "
                         "and PRIME_RUNS_MODE: one of them could send Docker commands to another engine or imports to another "
                         "checkout (RUNBOOK_MAC.md, step 0). Nothing was started. Stop and report.")


def run_label() -> str:
    """$VF_RUN_ID, which becomes the label `verifiers.run` of every container of the run. Required."""
    v = os.environ.get("VF_RUN_ID", "")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{5,62}", v):
        raise SystemExit("VF_RUN_ID is not set (or not a plain label of 6 to 63 characters). Start this tool as\n"
                         "    VF_RUN_ID=<label of this run, e.g. physim2-pilot-r6> python tools/...\n"
                         "verifiers labels every container it creates with it (verifiers.run=<label>): after an interruption\n"
                         "that label is the only way to find this run's containers without touching anybody else's.")
    return v


STAND_IN_VAR = "PHYSIM2_STAND_IN_KEY"                        # the key variable of a run against a LOCAL stand-in endpoint (tests)
STAND_IN_VALUE = "stand-in-not-a-key"                        # a made-up word: the stand-in checks nothing


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
    RUNBOOK_MAC.md, "If a run was interrupted"). Returns what it took.
    Round 4 (the Mac review's SIG-3 and R3-8): the SIGTERM is sent ONCE per child however often this function
    is called, and a signal that reaches THIS tool while it waits changes nothing: the wait goes on to the same
    deadline, so a tool that is told to stop twice neither signals vf-eval twice nor leaves it behind."""
    if p.poll() is not None:
        return "had exited"
    grace = STOP_GRACE_S if grace is None else grace
    sent = getattr(p, "_physim2_term_sent", None)
    if sent is None:
        sent = p._physim2_term_sent = time.monotonic()
        p.send_signal(signal.SIGTERM)
    while True:
        try:
            p.wait(timeout=max(0.0, sent + grace - time.monotonic()))
            return "SIGTERM"
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
            return "SIGTERM, then SIGKILL"
        except KeyboardInterrupt:                            # told to stop again while waiting: keep waiting
            continue


def run_child(cmd: list[str], *, env: dict, cwd: str, timeout: float, grace: float | None = None, capture: bool = True,
              disk_floor: int | None = None, check_s: float | None = None, on_stop=None):
    """(returncode, stdout, stderr, how it ended) of one child process (vf-eval). The child ends in one of four
    ways: it exits by itself ("exited"); `timeout` is over ("stopped after ..."); the disk watchdog finds less
    than `disk_floor` bytes free ("stopped by the disk watchdog ...": looked at every `check_s` seconds); or THIS
    process is told to stop (SIGTERM, Ctrl-C) or fails, and the exception goes on. In the last three the child
    is stopped with stop_child: the one stop path. With capture=False the child writes to this process's own
    output (the log of a detached command) and the two strings are empty.
    `on_stop(reason)` is called BEFORE the stop begins (round 4, the Mac review's NEWC-1): the caller writes the
    reason down while the child is still alive, so that a tool that dies during the stop leaves a record."""
    def note(reason: str) -> None:
        if on_stop is not None:
            try:
                on_stop(reason)
            except Exception:
                pass
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
                note(f"the time limit of {timeout:.0f} s is over")
                how = f"stopped after {timeout:.0f} s: " + stop_child(p, grace)
                out, err = p.communicate()
                break
            if disk_floor is not None:
                try:
                    free = free_bytes()
                except OSError:                              # a disk that cannot be measured is not a disk with room
                    free = -1
                if free < disk_floor:
                    seen = "the free space could not be read" if free < 0 else f"{free / GIB:.2f} GiB free on the file system of the home folder"
                    note(f"the disk watchdog ({seen}, floor {disk_floor / GIB:.2f} GiB)")
                    how = f"stopped by the disk watchdog ({seen}, floor {disk_floor / GIB:.2f} GiB): " + stop_child(p, grace)
                    out, err = p.communicate()
                    break
    except BaseException as e:
        note(f"this tool was told to stop or failed ({type(e).__name__})")
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
    try:
        free = free_bytes()
    except OSError:
        free = None
    rec = {"ended": how, "returncode": returncode, "time_unix": time.time(), "free_bytes_now": free,
           "disk_floor_bytes": floor, "deleted_by_the_watchdog": "nothing"}
    try:
        with open(path, "w") as f:
            json.dump(rec, f, indent=1)
    except OSError:
        pass
    return rec


def ended_by_signal(rc, how: str) -> bool:
    """Did a child that "exited" in fact end because of a signal: killed outright (negative status), or stopped
    by a SIGINT or SIGTERM that did not come from this tool (vf-eval then ends with 130 or 143; round 3's code
    re-audit, item 4)?"""
    return how == "exited" and rc is not None and (rc < 0 or rc in (130, 143))


def end_of_child(rc, how: str, record: str, floor: int | None) -> None:
    """After a child ended: return if it exited by itself; otherwise record why, say so, and end THIS tool with a
    status other than 0. A vf-eval that was killed outright (SIGKILL after the grace period, or a signal from
    elsewhere) could not remove its containers, and on macOS its laboratory process stays as well: the next
    thing to do is RUNBOOK_MAC.md, "If a run was interrupted", not another rollout (finding m5)."""
    if how == "exited" and not ended_by_signal(rc, how):
        return
    stopped_record(record, how if how != "exited" else f"ended by a signal from outside this tool (status {rc})", rc, floor)
    killed = "SIGKILL" in how or (rc is not None and rc < 0 and how == "exited")
    left = " Its containers and its laboratory process may be left." if killed else ""
    if "disk watchdog" in how:
        print(f"refused: {how}. The run was stopped through the tool's one stop path; nothing was deleted.{left} Stop and report "
              "(RUNBOOK_MAC.md, \"If a run was interrupted\", points 1 to 5).", flush=True)
        raise SystemExit(EXIT_DISK)
    what = how if how != "exited" else (f"died of signal {-rc}" if rc < 0 else f"ended with status {rc} after a signal from outside this tool")
    print(f"refused to go on: vf-eval {what}.{left} Nothing further was started. "
          "Stop and report (RUNBOOK_MAC.md, \"If a run was interrupted\").", flush=True)
    raise SystemExit(EXIT_STOPPED)


def run_eval(name: str, *, store: str, out_dir: str, harness: dict, instances=None, task: dict | None = None,
             cpu: float | None = 2, env: dict | None = None, timeout: float = 3600, image: str | None = None,
             timeouts: dict | None = None, disk_floor_gib: float | None = None, memory: float | None = None,
             env_id: str = "isolated-verifier") -> dict:
    """Returns {"episodes": [...], "wall_s", "host_cpu_s", "returncode", "run_dir", "log_tail"}.
    The task option `agent_key` defaults to the run name: `single_use` stays ON, and each scripted policy or
    probe is its own agent (the same run name on the same instance is refused, as a re-roll would be)."""
    import tomli_w
    cfg = {"model": "none/scripted", "num_rollouts": 1, "max_concurrent": 1, "push": False, "output_dir": out_dir,
           "client": dict(NO_MODEL_CLIENT),                  # no model is called, and no model credential is loaded
           "run": {"name": name},
           "env": {"id": env_id if env_id in ("isolated-verifier", "physim2-verifier") else "isolated-verifier",
                   "taskset": {"id": "physim2-env", "store": store},
                   "agent": {"runtime": {"type": "docker"}, "harness": dict({"id": "physim2-script"}, **harness)},
                   "retries": {"max_retries": 0},
                   "verifier": {"retries": 0}}}
    cfg["env"]["agent"]["retries"] = {"max_retries": 0}
    if cpu:
        cfg["env"]["agent"]["runtime"]["cpu"] = cpu
    if memory:                                               # GiB; the runtime clamps it to the pin's cap (physim2_env/boxcaps.py)
        cfg["env"]["agent"]["runtime"]["memory"] = memory
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
    record = os.path.join(out_dir, f"{name}.stopped.json")
    rc, out, err, how = run_child(["nice", "-n", "10", *VF_EVAL, "@", toml, "--no-rich"], env=child_env(env), cwd=out_dir,
                                  timeout=timeout, disk_floor=floor,
                                  on_stop=lambda why: stopped_record(record, "stopping: " + why, None, floor))
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    if how != "exited" or rc < 0:
        print((out + err)[-1500:], flush=True)
    end_of_child(rc, how, record, floor)
    episodes = []
    f = os.path.join(run_dir, "traces.jsonl")
    if os.path.exists(f):
        episodes = [json.loads(line) for line in open(f)]
    return {"episodes": episodes, "wall_s": time.time() - t0, "returncode": rc, "run_dir": run_dir, "config": toml,
            "host_cpu_s": (r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime), "log_tail": (out + err)[-3000:],
            "ended": how, "run_label": label}


def check_config(path: str, *, dry_run: bool) -> dict:
    """Read a vf-eval config file for the COMMAND FORM of this tool (step 2c of RUNBOOK_MAC.md) and refuse what it
    must not start. Always: no upload, the docker runtime. Unless it is a dry run: the stand-in client and the
    scripted harness, so that no model can be called and no key is looked for. A model rollout is never started
    from a config file alone: it needs a request (`--request`, step 3)."""
    import tomllib
    with open(path, "rb") as f:
        cfg = json.loads(json.dumps(tomllib.load(f)))
    if cfg.get("push") is not False:
        raise SystemExit("refused: the config does not say `push = false`")
    if (((cfg.get("env") or {}).get("agent") or {}).get("runtime") or {}).get("type") != "docker":
        raise SystemExit("refused: the config does not use the docker runtime")
    if not dry_run:
        client = cfg.get("client") or {}
        harness = (((cfg.get("env") or {}).get("agent") or {}).get("harness") or {}).get("id")
        if client.get("api_key_var") != NO_MODEL_VAR or client.get("base_url") != NO_MODEL_URL or harness != "physim2-script":
            raise SystemExit("refused: from a config file this tool starts scripted rollouts only: the config must have\n"
                             f"    [client]\n    base_url = \"{NO_MODEL_URL}\"\n    api_key_var = \"{NO_MODEL_VAR}\"\n"
                             "and the harness physim2-script. A model rollout is step 3 of RUNBOOK_MAC.md: it is started by a "
                             "request (--request FILE --pilot DIR --stage rollout).")
    return cfg


# ----------------------------------------------------------------------------- the request route (step 3)
# One rollout = one request file (schema rollout-job/v1, tools/check_request.py) = one folder
# <pilot>/rollouts/<job_id>/ = one row pair in <pilot>/LEDGER.jsonl. The stages, in the order of RUNBOOK_MAC.md:
#   instance    the instance name is registered to this job (for ever) and the hidden instance is made
#   reference   the scripted policies of the profile on that instance (tools/prove.py; $0): the reference table
#   dry-run     listed prices and the bounds on the bill; vf-eval resolves the run's config and exits ($0)
#   rollout     the model run: needs --model-credentials prime, the reservation in the ledger, the spend meter
#   close       only after an interruption that killed this tool: closes the job's open ledger row as "cut"
# Every stage first checks the request, the pin, the strict config schema, the pilot folder and the lead's
# standing go (<pilot>/LEAD-GO-MODEL-SPEND.json): without that file nothing of step 3 starts.
STAGES = ("instance", "reference", "dry-run", "rollout", "close")
# The ONE address a model run talks to, written into the run's config so that neither the Prime login file nor a
# variable can move it (verifiers/v1/configs/client.py:37-57 takes `inference_url` from the login file otherwise).
PRIME_INFERENCE_URL = "https://api.pinference.ai/api/v1"
KEY_VAR = "PRIME_API_KEY"
GRADING_ALLOWANCE_S = 9600.0                                 # set-up, finalize and the grading boxes, on top of the agent's wall time


def _write_status(p: dict, stage: str, record: dict) -> None:
    """<job>/status.json: one entry per stage, the latest record of each (numbers, names and words only)."""
    try:
        with open(p["status"]) as f:
            status = json.load(f)
    except (OSError, ValueError):
        status = {"stages": {}}
    status["stages"][stage] = dict(record, time_unix=round(time.time(), 3))
    tmp = p["status"] + ".new"
    with open(tmp, "w") as f:
        json.dump(status, f, indent=1, sort_keys=True)
    os.replace(tmp, p["status"])


def _job_folder(p: dict, req: dict, cfg: dict, CR) -> None:
    """Create <pilot>/rollouts/<job_id>/ with copies of the request and of the config, or check that the copies
    there are of THIS request and config (a job folder is never reused for another request)."""
    os.makedirs(p["rollouts"], mode=0o700, exist_ok=True)
    with open(cfg["path"], "rb") as f:
        raw_cfg = f.read()
    if not os.path.lexists(p["job"]):
        os.mkdir(p["job"], 0o700)
        with open(p["request"], "w") as f:
            json.dump({k: v for k, v in req.items() if not k.startswith("_")}, f, indent=1, sort_keys=True)
        with open(p["config"], "wb") as f:
            f.write(raw_cfg)
        with open(os.path.join(p["job"], "PILOT_NEVER_REUSE_AS_EXAM.txt"), "w") as f:
            f.write("PILOT_NEVER_REUSE_AS_EXAM: this folder belongs to one pilot rollout; its instance is never to be used as an exam.\n")
        _write_status(p, "request", {"job_id": req["job_id"], "request_sha256": req["_sha256"], "config_sha256": cfg["sha256"],
                                      "pin": req["pin"], "pin_sha256": req["pin_sha256"]})
        return
    try:
        with open(p["status"]) as f:
            first = json.load(f)["stages"]["request"]
        same = first["request_sha256"] == req["_sha256"] and first["config_sha256"] == cfg["sha256"] and open(p["config"], "rb").read() == raw_cfg
    except (OSError, ValueError, KeyError):
        same = False
    if os.path.islink(p["job"]) or not same:
        raise CR.Refused("the job folder exists and was made for another request or config: a job id is used once")


def _helper_takes(tool: str, option: str) -> bool:
    try:
        with open(os.path.join(HERE, tool)) as f:
            return f'"{option}"' in f.read()
    except OSError:
        return False


def _instance_argv(req: dict, flat: dict, p: dict, profile: dict) -> list[str]:
    """The command that makes the job's hidden instance. tools/make_instances.py of round 4 takes --profile and
    --id; the round-3 form (a prefix, the name ending in -w0) is used while that tool does not."""
    base = [sys.executable, "-B", os.path.join(HERE, "make_instances.py"), "--store", p["store"]]
    if _helper_takes("make_instances.py", "--profile"):
        return base + ["--profile", flat["exam_profile"], "--id", req["instance"]]
    if not req["instance"].endswith("-w0"):
        raise SystemExit("refused: this pin's tools/make_instances.py names instances <prefix>-w0; the request's instance must end in -w0")
    return base + ["--world", profile["world"], "--config", profile["config_name"], "--n", "1", "--prefix", req["instance"][:-3]]


def _reference_argv(req: dict, flat: dict, p: dict, profile: dict, floor_gib: float) -> list[str]:
    """The command that builds the reference table: the profile's scripted policies on the job's instance."""
    base = [sys.executable, "-B", os.path.join("tools", "prove.py"), "--store", p["store"], "--scratch", os.path.join(p["job"], "reference"),
            "--no-cross-check", "--disk-floor-gib", str(floor_gib), "--out", p["reference"]]
    if _helper_takes("prove.py", "--profile"):                # ruling E8: the reference boxes get the caps of the model's box,
        memory = ["--memory", str(flat["box_memory_gb"])] if _helper_takes("prove.py", "--memory") else []   # a lowered memory included
        return base + ["--profile", flat["exam_profile"], "--instance", req["instance"]] + memory
    return base + ["--world", profile["world"], "--config", profile["config_name"], "--worlds", "1", "--prefix", req["instance"][:-3],
                   "--policies", ",".join(profile["reference_policies"]), "--sizes", json.dumps(profile["reference_sizes"]),
                   "--cpu", str(profile["box_cpus"]), "--box-check", ""]


def require_key_name(CR, environ=None) -> None:
    """A billed rollout starts only from a command whose environment holds the key's NAME: the key reaches vf-eval by
    the environment and no other way (the value is never read by this tool)."""
    env = os.environ if environ is None else environ
    if KEY_VAR not in env:
        raise CR.Refused(f"a model rollout needs {KEY_VAR} in the environment of its command (the name is looked for; the value is "
                         "never read by this tool): the key reaches vf-eval by the environment and no other way")
    if not env[KEY_VAR].strip():                             # round 5 (T24): an empty value makes verifiers fall back to the Prime login file
        raise CR.Refused(f"{KEY_VAR} is set but empty in the environment of this command: verifiers would then take a key from the "
                         "Prime login file; the key reaches vf-eval by the environment and no other way (only its emptiness was looked at)")


def command_line_of(pid) -> str:
    """The command line of a process of this user, or "" (it is gone, or `ps` did not answer). Read-only."""
    try:
        r = subprocess.run(["ps", "-ww", "-p", str(int(pid)), "-o", "command="], capture_output=True, text=True, timeout=20,
                           stdin=subprocess.DEVNULL, env=child_env())
    except (OSError, ValueError, TypeError, subprocess.TimeoutExpired):
        return ""
    return r.stdout.strip()


def containers_of_this_run() -> list[str]:
    """Names of the containers that carry this command's run label (running or not)."""
    r = subprocess.run(["docker", "ps", "-a", "--filter", f"label=verifiers.run={run_label()}", "--format", "{{.Names}}"],
                       capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL, env=child_env())
    if r.returncode:
        raise SystemExit("Docker does not answer (`docker ps` failed); nothing was changed. Stop and report.")
    return [x for x in r.stdout.split() if x]


def leftovers(p: dict, req: dict, ps=command_line_of, containers=containers_of_this_run) -> list[str]:
    """What an interrupted rollout of this job still has on the machine, in words: its tool, a laboratory of its
    instance, containers of the run label. Empty = the clean-up of RUNBOOK_MAC.md ("If a run was interrupted",
    points 1 to 5) is done. Looks; signals and removes nothing."""
    left = []
    try:
        with open(p["status"]) as f:
            pid = (json.load(f)["stages"].get("rollout") or {}).get("tool_pid")
    except (OSError, ValueError, KeyError):
        pid = None
    if pid and "tools/vfrun.py" in ps(pid) and "--stage rollout" in ps(pid):
        left.append(f"the tool of this job (pid {pid})")
    labs = os.path.join(p["store"], req["instance"], "hidden", "labs")
    for name in sorted(os.listdir(labs)) if os.path.isdir(labs) else []:
        try:
            with open(os.path.join(labs, name, "process.json")) as f:
                lab_pid = json.load(f).get("pid")
        except (OSError, ValueError):
            continue
        if lab_pid and "physim2_env.lab_tools" in ps(lab_pid):
            left.append(f"a laboratory of this job's instance (pid {lab_pid})")
    left += [f"container {n}" for n in containers()]
    return left


def close_job(p: dict, req: dict, CR, ps=command_line_of, containers=containers_of_this_run, write_status=None) -> dict:
    """Stage `close`: after an interruption that killed the tool itself (it could not write the job's closing row),
    and after the clean-up of the runbook, write that row: status `cut`, the cost counted from the run's spend log
    (one worst-case call for every call that was sent and never settled). Refused while anything of the job is
    still there, and when the ledger has nothing open for this job."""
    events = [r.get("event") for r in CR.ledger_rows(p) if r.get("job_id") == req["job_id"]]
    if "reserved" not in events or "ended" in events:
        raise CR.Refused("nothing to close: the ledger holds no open row for this job")
    left = leftovers(p, req, ps, containers)
    if left:
        raise CR.Refused("still on this machine: " + "; ".join(left[:6]) + ". First RUNBOOK_MAC.md, \"If a run was interrupted\", points 1 to 5")
    try:
        total = CR.spend_log_total(p["spend_log"])
    except CR.Refused:
        total = {"present": True, "counted_usd": None, "attempts": None, "complete": False}
    counted = 0.0 if not total["present"] else total["counted_usd"]
    row = {"event": "ended", "job_id": req["job_id"], "status": "cut", "how": "closed after an interruption (--stage close)", "returncode": None,
           "counted_usd": counted, "count_complete": bool(total["complete"] or not total["present"]), "attempts": total.get("attempts"),
           "worst_case_calls": total.get("worst_case_calls"), "stopped": total.get("stopped"), "billed": total.get("billed", True)}
    CR.ledger_append(p, row)
    (write_status or _write_status)(p, "rollout", {"ended": True, "status": "cut", "how": row["how"], "counted_usd": counted, "closed_by": "--stage close"})
    return row


def reference_done(p: dict) -> dict | None:
    """The finished reference table of a job (<job>/reference.json with every rollout graded), or None."""
    try:
        with open(p["reference"]) as f:
            ref = json.load(f)
    except (OSError, ValueError):
        return None
    return ref if ref.get("all_graded") is True else None


def request_route(a) -> int:
    """Stages of step 3. Returns the exit status; prints `refused: ...` and returns 2 when anything is not as the
    request route needs it (nothing was started then, unless the line says otherwise)."""
    import check_config as CC
    import check_request as CR
    floor = disk_floor_bytes(a.disk_floor_gib)
    stand_in = a.stand_in_endpoint
    try:
        if stand_in and not re.fullmatch(r"http://127\.0\.0\.1:[0-9]{2,5}/v1", stand_in):
            raise CR.Refused("--stand-in-endpoint is for tests against a stand-in on this machine: http://127.0.0.1:<port>/v1 and nothing else")
        if stand_in and a.model_credentials:
            raise CR.Refused("a stand-in endpoint and model credentials do not go together")
        CR.use_pilot_configs(a.pilot)                        # the runner's copy of the job's config: <pilot>/configs/<name>.toml
        req = CR.read_request(a.request)
        if os.path.basename(a.request) != req["job_id"] + ".json":
            raise CR.Refused("the request file is not named <job_id>.json")
        CR.check_pin(req)
        cfg = CR.check_config(req)
        flat = cfg["flat"]
        profile = CC.light("profiles").get(flat["exam_profile"])
        p = dict(CR.require_pilot(a.pilot), **CR.pilot_paths(a.pilot, req["job_id"]))
        rows = CR.ledger_rows(p)
        started = [r for r in rows if r.get("job_id") == req["job_id"]]
        if a.stage == "close":                               # spends nothing and starts nothing: it needs no go
            require_docker()
            row = close_job(p, req, CR)
            print(json.dumps({"stage": "close", "job_id": req["job_id"], "status": "cut", "counted_usd": row["counted_usd"],
                              "count_complete": row["count_complete"]}))
            return 0
        go = CR.read_go(p)                                   # the lead's standing go: nothing of step 3 starts without it
        still_open = CR.open_jobs(rows)
        if still_open:                                       # one rollout at a time, and none while an interrupted one is not closed
            raise CR.Refused(f"the ledger holds a job that was started and has not ended ({still_open[0]}): one rollout at a time. If "
                             "it was interrupted: RUNBOOK_MAC.md, \"If a run was interrupted\", then --stage close for that job")

        if a.stage == "instance":
            if started:
                raise CR.Refused("the ledger already holds this job id")
            CR.check_instance(p, req, must_exist=False)
            require_disk(floor, "the instance")
            _job_folder(p, req, cfg, CR)
            CR.register_instance(p, req)                     # FIRST: from here on the name is used, whatever happens next
            r = run_helper(_instance_argv(req, flat, p, profile), capture=True)
            if r.returncode or not CR.instance_state(p, req["instance"])["in_index"]:
                print((r.stdout + r.stderr)[-800:])
                _write_status(p, "instance", {"ok": False, "returncode": r.returncode})
                raise CR.Refused("the instance was not made (its name stays registered and cannot be used again): stop and report")
            with open(os.path.join(p["store"], "PILOT_NEVER_REUSE_AS_EXAM.txt"), "a") as f:
                f.write(f"PILOT_NEVER_REUSE_AS_EXAM: {req['instance']} (job {req['job_id']}) is pilot material, never an exam.\n")
            _write_status(p, "instance", {"ok": True, "instance": req["instance"]})
            print(json.dumps({"stage": "instance", "job_id": req["job_id"], "instance": req["instance"], "made": True}))
            return 0

        CR.check_instance(p, req, must_exist=True)
        _job_folder(p, req, cfg, CR)
        if a.stage == "reference":
            if started:
                raise CR.Refused("the ledger already holds this job id: the reference table is built before the rollout")
            if reference_done(p) is not None:
                raise CR.Refused("the reference table of this job exists already")
            require_disk(floor, "the reference table")
            require_docker()
            _write_status(p, "reference", {"started": True, "policies": profile["reference_policies"]})
            argv = _reference_argv(req, flat, p, profile, a.disk_floor_gib)
            sys.stdout.flush()
            os.chdir(ROOT)                                   # from here on this process IS tools/prove.py (same pid, same log)
            os.execve(sys.executable, argv, child_env({"VF_RUN_ID": run_label()}))

        if reference_done(p) is None:
            raise CR.Refused("the reference table of this job is not finished (stage `reference`; <job>/reference.json with all_graded true)")
        # ---- prices and bounds: one GET without a credential; refused when cap_usd is below one worst-case call ----
        entry = CR.fetch_model_entry(flat["model"], stand_in)
        prices = CR.prices_of(entry)
        b = CR.bounds(flat, prices)
        if a.shared_ledger is None and not stand_in and a.stage == "rollout":
            raise CR.Refused("a model rollout needs --shared-ledger FILE: a fresh copy of the program's shared ledger (the lead's ceiling "
                             "is one total across machines; RUNBOOK_MAC.md, step 3)")
        elsewhere = CR.shared_ledger(a.shared_ledger) if a.shared_ledger else None
        ceiling = CR.check_ceiling(p, go, b, elsewhere)
        print(json.dumps({"job_id": req["job_id"], "model": flat["model"], "prices_usd_per_mtok": prices,
                          "one_worst_case_call_usd": round(b["worst_call_usd"], 6), "cap_usd": b["cap_usd"],
                          "bound_on_the_bill_usd": round(b["bound_usd"], 6), "crude_bound_without_the_spend_stop_usd": round(b["crude_bound_usd"], 2),
                          "ledger_sum_usd": round(ceiling["sum_usd"], 6), "spent_elsewhere_usd": round(ceiling["spent_elsewhere_usd"], 6),
                          "shared_ledger": None if elsewhere is None else {k: elsewhere[k] for k in ("updated_utc", "rows", "sha256")},
                          "ceiling_usd": ceiling["ceiling_usd"], "billed": not stand_in}), flush=True)
        spend = {"cap_usd": float(flat["cap_usd"]), "max_context_tokens": int(flat["max_context_tokens"]),
                 "max_output_tokens": int(flat["max_output_tokens_per_turn"]), "model": flat["model"],
                 "input_usd_per_mtok": prices["input_counted"], "output_usd_per_mtok": prices["output"], "context_window": prices["context_window"],
                 "prices_from": entry["source"] + f" at unix time {entry['fetched_unix']}"
                                + ("" if prices["input_counted"] == prices["input"] else "; input counted at the listed cache-write price, which is higher"),
                 "billed": not stand_in}
        if flat["reasoning_effort"] != "default":            # K10: the meter admits this effort only (left out: none at all)
            spend["reasoning_effort"] = flat["reasoning_effort"]
        if prices["cache_read"] is not None:
            spend["cache_read_usd_per_mtok"] = prices["cache_read"]
        resolved = json.loads(json.dumps(cfg["expanded"]))
        resolved["env"]["taskset"].setdefault("task", {})["spend"] = spend
        resolved["client"] = {"type": "eval", "base_url": stand_in, "api_key_var": STAND_IN_VAR} if stand_in else \
            {"type": "eval", "base_url": PRIME_INFERENCE_URL, "api_key_var": KEY_VAR}
        if CR.PRIME_MODELS_URL != PRIME_INFERENCE_URL + "/models":
            raise CR.Refused("the price listing and the inference address are not the same service")
        import tomli_w

        if a.stage == "dry-run":
            toml = os.path.join(p["job"], "dry-run.toml")
            with open(toml, "wb") as f:
                tomli_w.dump(resolved, f)
            cmd = ["nice", "-n", "10", *VF_EVAL, "@", toml, "--run.name", req["job_id"] + "-dry", "-o", os.path.join(p["job"], "dry-run"), "--dry-run"]
            rc, _, _, how = run_child(cmd, env=child_env({"PHYSIM2_STORE": p["store"], STAND_IN_VAR: STAND_IN_VALUE} if stand_in else
                                                          {"PHYSIM2_STORE": p["store"]}), cwd=ROOT, timeout=600, capture=False)
            _write_status(p, "dry-run", {"ok": rc == 0 and how == "exited", "returncode": rc, "bounds": {k: b[k] for k in ("worst_call_usd", "bound_usd", "crude_bound_usd")}})
            end_of_child(rc, how, os.path.join(p["job"], "dry-run.stopped.json"), floor)
            return rc

        # ---- stage rollout: the one command that can spend money ----
        if not stand_in and a.model_credentials != "prime":
            raise CR.Refused("a model rollout needs --model-credentials prime on its command (or, in a test, --stand-in-endpoint)")
        if started:
            raise CR.Refused("the ledger already holds this job id: a job runs once, and a run that was cut is not run again")
        if not stand_in:
            require_key_name(CR)
        try:
            with open(p["status"]) as f:
                dry = json.load(f)["stages"].get("dry-run") or {}
        except (OSError, ValueError, KeyError):
            dry = {}
        if not dry.get("ok"):
            raise CR.Refused("the free dry run of this job has not passed (stage `dry-run`)")
        if os.path.lexists(p["out"]) or os.path.lexists(p["spend_log"]):
            raise CR.Refused("this job has run files already: a job runs once")
        require_disk(floor, f"the rollout {req['job_id']}")
        require_docker()
        with open(p["model_entry"], "w") as f:               # the saved model entry: prices and window as read at run start
            json.dump(entry, f, indent=1)
        with open(p["resolved"], "wb") as f:
            tomli_w.dump(resolved, f)
        CR.ledger_append(p, {"event": "reserved", "job_id": req["job_id"], "model": flat["model"], "instance": req["instance"],
                             "cap_usd": b["cap_usd"], "worst_call_usd": b["worst_call_usd"], "bound_usd": b["bound_usd"],
                             "crude_bound_usd": b["crude_bound_usd"], "prices_usd_per_mtok": prices, "billed": not stand_in,
                             "ceiling_usd": go["ceiling_usd"], "go_date": go["date"], "spent_elsewhere_usd": ceiling["spent_elsewhere_usd"]})
    except (CR.Refused, CC.Refused) as e:
        print("refused: " + str(e), flush=True)
        return 2

    _write_status(p, "rollout", {"started": True, "bound_usd": b["bound_usd"], "billed": not stand_in, "tool_pid": os.getpid()})
    extra = {"PHYSIM2_STORE": p["store"], "PHYSIM2_SPEND_LOG": p["spend_log"]}
    if stand_in:
        extra[STAND_IN_VAR] = STAND_IN_VALUE
    cmd = ["nice", "-n", "10", *VF_EVAL, "@", p["resolved"], "--run.name", req["job_id"], "-o", p["out"], "--no-rich"]
    record = os.path.join(p["job"], "rollout.stopped.json")
    timeout = 60.0 * flat["wall_minutes"] + GRADING_ALLOWANCE_S
    rc, how, failure = None, "not started", None
    try:
        rc, _, _, how = run_child(cmd, env=child_env(extra, model_credentials=not stand_in), cwd=ROOT, timeout=timeout, capture=False,
                                  disk_floor=floor, on_stop=lambda why: stopped_record(record, "stopping: " + why, None, floor))
    except BaseException as e:                               # this tool was told to stop: the books are still closed below
        failure, how = e, f"this tool was stopped ({type(e).__name__})"
    finally:
        try:
            total = CR.spend_log_total(p["spend_log"])
        except CR.Refused:
            total = {"present": True, "counted_usd": None, "attempts": None, "complete": False}
        clean = how == "exited" and rc == 0
        counted = 0.0 if not total["present"] else total["counted_usd"]
        CR.ledger_append(p, {"event": "ended", "job_id": req["job_id"], "status": "done" if clean else "cut", "how": how, "returncode": rc,
                             "counted_usd": counted, "count_complete": bool(total["complete"] or not total["present"]),
                             "attempts": total.get("attempts"), "worst_case_calls": total.get("worst_case_calls"),
                             "stopped": total.get("stopped"), "billed": not stand_in})
        _write_status(p, "rollout", {"ended": True, "status": "done" if clean else "cut", "how": how, "returncode": rc, "counted_usd": counted,
                                     "bound_usd": b["bound_usd"], "within_bound": counted is not None and counted <= b["bound_usd"] + 1e-9})
        print(json.dumps({"job_id": req["job_id"], "ended": how, "returncode": rc, "counted_usd": counted, "bound_on_the_bill_usd": b["bound_usd"]}), flush=True)
    if failure is not None:
        raise failure
    end_of_child(rc, how, record, floor)
    return rc


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="one rollout through vf-eval, with the environment allow-list, the disk watchdog and the one stop "
                                             "path of this tool: a scripted one from a config file (step 2c), or a stage of a "
                                             "rollout request (step 3)")
    ap.add_argument("--config", help="COMMAND FORM: a vf-eval TOML file of a scripted run, relative to the study folder or absolute")
    ap.add_argument("--run-name")
    ap.add_argument("--out-dir")
    ap.add_argument("--store")
    ap.add_argument("--request", help="REQUEST ROUTE (step 3): a rollout-job/v1 file")
    ap.add_argument("--pilot", help="REQUEST ROUTE: the pilot folder (store, rollouts, ledger, the lead's go)")
    ap.add_argument("--stage", choices=STAGES, help="REQUEST ROUTE: which stage of the request to run")
    ap.add_argument("--disk-floor-gib", type=float, default=DISK_FLOOR_GIB)
    ap.add_argument("--timeout", type=float, default=5400.0, help="COMMAND FORM: seconds after which vf-eval is told to stop")
    ap.add_argument("--dry-run", action="store_true", help="COMMAND FORM: vf-eval resolves the config, writes it and exits; no rollout")
    ap.add_argument("--model-credentials", choices=["prime"], default=None,
                    help="REQUEST ROUTE, stage rollout ONLY: pass PRIME_API_KEY and PRIME_TEAM_ID on to vf-eval and let verifiers read "
                         "~/.prime/config.json")
    ap.add_argument("--shared-ledger", default=None,
                    help="REQUEST ROUTE, stages dry-run and rollout: a copy of the program's shared ledger (rollout-ledger/v1); what it "
                         "says other machines spent counts against the lead's ceiling. Required for a billed rollout")
    ap.add_argument("--stand-in-endpoint", default=None,
                    help="REQUEST ROUTE, TESTS ONLY: http://127.0.0.1:<port>/v1 of tools/standin_model.py instead of the provider; no "
                         "credential is passed or loaded and nothing is billed")
    a = ap.parse_args(argv)
    require_clean_environment()
    run_label()
    if a.request or a.pilot or a.stage:
        if not (a.request and a.pilot and a.stage) or a.config or a.run_name or a.out_dir or a.store or a.dry_run:
            raise SystemExit("refused: the request route takes --request, --pilot and --stage (and nothing of the command form)")
        return request_route(a)
    if a.model_credentials or a.stand_in_endpoint or a.shared_ledger:
        raise SystemExit("refused: a model rollout is started by a request: --request FILE --pilot DIR --stage rollout (RUNBOOK_MAC.md, step 3)")
    if not (a.config and a.run_name and a.out_dir and a.store):
        raise SystemExit("refused: the command form needs --config, --run-name, --out-dir and --store")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,40}", a.run_name):
        raise SystemExit("refused: --run-name must be lower-case letters, digits and hyphens")
    config = a.config if os.path.isabs(a.config) else os.path.join(ROOT, a.config)
    check_config(config, dry_run=a.dry_run)
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
    record = os.path.join(out_dir, f"{a.run_name}.stopped.json")
    # cwd = the study folder: `agent_dir` of a config file is relative to it
    rc, _, _, how = run_child(cmd, env=child_env({"PHYSIM2_STORE": store}), cwd=ROOT, timeout=a.timeout, capture=False,
                              disk_floor=None if a.dry_run else floor,
                              on_stop=lambda why: stopped_record(record, "stopping: " + why, None, floor))
    end_of_child(rc, how, record, floor)
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
