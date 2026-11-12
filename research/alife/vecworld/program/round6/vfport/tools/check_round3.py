"""check_round3 -- tests of round 3 of the host-safety fixes (the Mac session's review: M1, M2, M3, m1, m4, m5; the
coordinator's disk requirement D1). Nothing here kills or deletes on a host.

Three parts. This process itself is only the harness: it starts the children below and reads what they print.

  host_*       code of the port run ON THIS HOST in a child process which, before it imports or calls anything of
               the port, installs tools/tripwires.py (every primitive that kills, deletes, moves, re-owns or starts
               a process raises and is recorded). Pure functions on made-up inputs only:
                 env     the child environment is an allow-list; a tool refuses a session environment that holds
                         one of the names RUNBOOK_MAC.md, step 0, looks for                              (M1)
                 disk    the floor, and the refusal before a run (free space injected, never changed)    (D1)
                 config  the command form of tools/vfrun.py starts scripted configs only                 (M3)
                 theta   tools/build_reference.py takes the parameters from a 0600 file only            (m1)
  nokey_*      a made-up credential file `<scratch home>/.prime/config.json` and Python's audit hook on every
               `open`: the stock import of verifiers opens the file and loads its (made-up) key; the same import
               through the package, a laboratory process in step-3 mode, and `tools/vfeval.py --dry-run` on the
               scripted config open it not once                                                          (M3)
  box_*        real processes and real signals, INSIDE `docker run --rm --network none <image>` (no host path
               mounted): tools/vfrun.py with a stand-in for vf-eval that writes down what it gets:
                 the one stop path for a time limit, the disk watchdog and a stop of the tool; SIGKILL only
                 after the grace period; a status other than 0 whenever vf-eval was stopped or died of a signal;
                 what reaches the child's environment; a helper is stopped with its tool          (M1, M2, m4, m5, D1)

The made-up credential file holds the text FAKE-KEY-NOT-A-CREDENTIAL; no real credential file is read, and the
environment handed to every child of this harness is built from PATH alone.

usage: PHYSIM2_DEV_MACHINE=cloud-container python -B tools/check_round3.py --scratch DIR --out results/round3_checks.json

ROUND 4 NOTE: round 4 replaced the route by which a model run starts: from a request only (tools/vfrun.py
--request ... --stage rollout; tools/check_round4.py and tools/check_step3.py test that route). The integrator
brought this check's part on the command form in line with that: a model config (configs/qwen_ring_bash.toml,
kept as a fixture) and the flag `--model-credentials` are now REFUSED on the command form, and the checks say
so. The allow-list, the credential stand-in, the watchdog and the stop path that it tests are unchanged except
where tools/check_round4.py says so (one SIGTERM per child: D40).
"""
import argparse
import base64
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

HOST = r'''
import json, os, sys
ROOT, SCRATCH = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(ROOT, "tools")); sys.path.insert(0, ROOT)
import tripwires
tw = tripwires.install()                                    # BEFORE anything of the port is imported
import vfrun, build_reference
checks, ev = {}, {}

# ---- env (M1) ----
real_environ = os.environ
session = {"PATH": "/usr/bin:/bin", "HOME": "/Users/lead", "TMPDIR": "/var/folders/x/T/", "USER": "lead", "LANG": "en_US.UTF-8",
           "VF_RUN_ID": "physim2-pilot-r6",
           # everything below must NOT get through
           "DOCKER_HOST": "tcp://203.0.113.7:2375", "DOCKER_CONTEXT": "elsewhere", "DOCKER_CONFIG": "/tmp/x", "BUILDX_BUILDER": "remote",
           "MCP_HOST": "0.0.0.0", "MCP_PORT": "8000", "PHYSIM2_AGENTENV": "/tmp/other-checkout", "PHYSIM2_STORE": "/tmp/other-store",
           "PYTHONPATH": "/tmp/other", "PYTHONHOME": "/tmp/py", "PYTHONSTARTUP": "/tmp/s.py", "VIRTUAL_ENV": "/tmp/venv", "UV_PROJECT_ENVIRONMENT": "/tmp/e",
           "PRIME_API_KEY": "made-up", "PRIME_TEAM_ID": "made-up-team", "PRIME_INFERENCE_URL": "https://elsewhere.example", "PRIME_RUNS_MODE": "online",
           "HF_TOKEN": "made-up", "AWS_SECRET_ACCESS_KEY": "made-up", "SSH_AUTH_SOCK": "/tmp/agent", "XDG_CACHE_HOME": "/tmp/cache",
           "HTTPS_PROXY": "http://proxy.example:1", "VF_STATE_SECRET": "made-up", "LD_PRELOAD": "/tmp/x.so", "DYLD_INSERT_LIBRARIES": "/tmp/x.dylib"}
os.environ = dict(session)
try:
    env = vfrun.child_env({"HF_TOKEN": "canary-given-by-the-tool"})
    fixed = {"PRIME_RUNS_MODE": "disabled", "PYTHONPATH": ROOT, "JAX_PLATFORMS": "cpu", "PYTHONDONTWRITEBYTECODE": "1"}
    from_session = sorted(k for k in env if k in session and env[k] == session[k])
    ev["env"] = {"names_in_the_made_up_session": len(session), "names_the_child_gets": sorted(env),
                 "taken_from_the_session_unchanged": from_session}
    checks["host_env_only_the_allow_list_is_taken_from_the_session"] = set(from_session) <= set(vfrun.ENV_PASS) | {"VF_RUN_ID"} \
        and from_session == sorted(["HOME", "LANG", "PATH", "TMPDIR", "USER", "VF_RUN_ID"]) or (
        # on a Linux host without IPv6 the tool puts its docker shim first on PATH: PATH is then not "unchanged"
        from_session == sorted(["HOME", "LANG", "TMPDIR", "USER", "VF_RUN_ID"]) and env["PATH"].endswith(":/usr/bin:/bin"))
    checks["host_env_no_docker_mcp_physim2_python_or_credential_name_gets_through"] = not any(
        k.startswith(("DOCKER_", "BUILDX_", "MCP_", "PHYSIM2_", "UV_", "AWS_", "SSH_", "XDG_", "LD_", "DYLD_", "PRIME_API", "PRIME_TEAM", "PRIME_INF", "VF_STATE"))
        or k in ("PYTHONHOME", "PYTHONSTARTUP", "VIRTUAL_ENV", "HTTPS_PROXY") for k in env)
    checks["host_env_fixed_values_are_set_by_the_tool"] = all(env.get(k) == v for k, v in fixed.items()) and env["HF_TOKEN"] == "canary-given-by-the-tool"
    m = vfrun.child_env(model_credentials=True)
    checks["host_env_model_credentials_only_when_asked_and_never_the_inference_url"] = "PRIME_API_KEY" not in env and vfrun.MODEL_ENV not in env \
        and m.get("PRIME_API_KEY") == "made-up" and m.get("PRIME_TEAM_ID") == "made-up-team" and m.get(vfrun.MODEL_ENV) == "prime" \
        and "PRIME_INFERENCE_URL" not in m and "DOCKER_HOST" not in m
    bad = vfrun.refused_names()
    ev["env"]["refused_names_of_the_made_up_session"] = bad
    checks["host_env_refused_names_are_those_of_the_step_0_check"] = bad == sorted(
        ["DOCKER_HOST", "DOCKER_CONTEXT", "DOCKER_CONFIG", "BUILDX_BUILDER", "MCP_HOST", "MCP_PORT", "PHYSIM2_AGENTENV", "PHYSIM2_STORE",
         "PYTHONPATH", "PYTHONHOME", "VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT", "PRIME_RUNS_MODE", "VF_STATE_SECRET",
         "DYLD_INSERT_LIBRARIES"])            # round 4: DYLD_* joined the names step 0 looks for (the Mac review's R3-7)
    try:
        vfrun.require_clean_environment()
        said = None
    except SystemExit as e:
        said = str(e)
    ev["env"]["refusal_first_line"] = (said or "").splitlines()[0][:200] if said else None
    checks["host_env_a_tool_refuses_such_a_session_and_prints_names_only"] = bool(said) and said.startswith("refused: ") \
        and "DOCKER_HOST" in said and "203.0.113.7" not in said and "made-up" not in said
    os.environ = {k: v for k, v in session.items() if k in ("PATH", "HOME", "TMPDIR", "USER", "LANG", "VF_RUN_ID", "HF_TOKEN", "SSH_AUTH_SOCK")}
    try:
        vfrun.require_clean_environment()
        clean_ok = True
    except SystemExit:
        clean_ok = False
    checks["host_env_a_session_without_those_names_is_accepted"] = clean_ok and vfrun.refused_names() == []
    # a helper that a tool starts gets the tool's own child environment and must pass the same check (and only then)
    os.environ = vfrun.child_env()
    own = vfrun.refused_names()
    os.environ = dict(vfrun.child_env(), PYTHONPATH="/tmp/other-checkout", PRIME_RUNS_MODE="online")
    other = vfrun.refused_names()
    ev["env"]["a_tools_own_child_environment"] = {"refused": own, "with_another_PYTHONPATH_and_upload_mode": other}
    checks["host_env_a_tools_own_child_environment_passes_and_other_values_do_not"] = own == [] and other == ["PRIME_RUNS_MODE", "PYTHONPATH"]
finally:
    os.environ = real_environ

ends = {"unix:///Users/lead/.docker/run/docker.sock": True, "unix:///var/run/docker.sock": True, "tcp://203.0.113.7:2375": False,
        "ssh://someone@elsewhere": False, "npipe:////./pipe/docker_engine": False, "": False, "unix:///": False, "unix:///a\ntcp://b": False}
ev["env"]["endpoints"] = {k: vfrun.endpoint_is_local(k) for k in ends}
checks["host_env_only_a_unix_socket_counts_as_a_local_docker_engine"] = ev["env"]["endpoints"] == ends
src = open(os.path.join(ROOT, "tools", "vfrun.py")).read()
# round 4: three `docker` calls in tools/vfrun.py (the context, `docker info`, and the listing by run label of stage
# `close`); each must name the allow-listed environment inside its own call
calls = [src[i:i + 400].split("\n\n")[0] for i in range(len(src)) if src.startswith('subprocess.run(["docker"', i)]
ev["env"]["docker_calls_in_vfrun"] = len(calls)
checks["host_env_every_docker_call_of_the_tools_gets_the_allow_listed_environment"] = len(calls) == 3 \
    and all(("env=env)" in c.split("subprocess.run(", 2)[1] or "env=child_env())" in c.split("subprocess.run(", 2)[1]) for c in calls) \
    and all('env=vfrun.child_env()' in open(os.path.join(ROOT, "tools", f)).read() for f in ("prove.py", "check_probe.py"))

# ---- disk (D1) ----
real_free = vfrun.free_bytes
try:
    checks["host_disk_floor_is_8_gib_by_default"] = vfrun.DISK_FLOOR_GIB == 8.0 and vfrun.disk_floor_bytes() == 8 << 30
    bad_floor = []
    for v in (0, -1, 0.1, 1e9, True, "8"):
        try:
            vfrun.disk_floor_bytes(v); bad_floor.append(v)
        except SystemExit:
            pass
    checks["host_disk_a_floor_outside_its_range_is_refused"] = bad_floor == []
    vfrun.free_bytes = lambda path=None: (8 << 30) - 1
    import io, contextlib
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            vfrun.require_disk(8 << 30, "the run x")
        code = None
    except SystemExit as e:
        code = e.code
    ev["disk"] = {"one byte under the floor": {"status": code, "said": buf.getvalue().strip()[:220]}}
    checks["host_disk_one_byte_under_the_floor_refuses_with_status_97"] = code == vfrun.EXIT_DISK == 97 and buf.getvalue().startswith("refused: ") \
        and "nothing was deleted" in buf.getvalue()
    vfrun.free_bytes = lambda path=None: 8 << 30
    checks["host_disk_exactly_the_floor_is_accepted"] = vfrun.require_disk(8 << 30) == 8 << 30
    vfrun.free_bytes = real_free
    here = vfrun.free_bytes()
    ev["disk"]["free_bytes_of_this_host_home"] = here
    checks["host_disk_free_space_is_read_with_statvfs_of_the_home_folder"] = isinstance(here, int) and here > 0 \
        and here == os.statvfs(os.path.expanduser("~")).f_bavail * os.statvfs(os.path.expanduser("~")).f_frsize
finally:
    vfrun.free_bytes = real_free

# ---- config (M3) ----
def refused(path, **kw):
    try:
        vfrun.check_config(path, **kw)
        return None
    except SystemExit as e:
        return str(e).splitlines()[0][:120]
scripted, qwen = os.path.join(ROOT, "configs", "scripted_ring.toml"), os.path.join(ROOT, "configs", "qwen_ring_bash.toml")
pushy = os.path.join(SCRATCH, "pushy.toml")
open(pushy, "w").write(open(scripted).read().replace("push = false", "push = true"))
nocl = os.path.join(SCRATCH, "noclient.toml")
open(nocl, "w").write(open(scripted).read().replace('api_key_var = "PHYSIM2_NO_MODEL_KEY"', 'api_key_var = "PRIME_API_KEY"'))
# round 4: the command form of tools/vfrun.py starts SCRIPTED configs only, whatever flag is given; a model run
# starts from a request (tools/check_round4.py, section D, tests that route). check_config has no credentials
# argument any more, and the flag itself is refused on the command form (vfrun.main; tested in the box part).
ev["config"] = {"scripted": refused(scripted, dry_run=False),
                "model config": refused(qwen, dry_run=False),
                "model config, dry run": refused(qwen, dry_run=True),
                "push = true": refused(pushy, dry_run=False),
                "push = true, dry run": refused(pushy, dry_run=True),
                "scripted with the default key variable": refused(nocl, dry_run=False)}
checks["host_config_the_scripted_config_is_accepted"] = ev["config"]["scripted"] is None
checks["host_config_a_model_config_is_never_started_from_a_config_file"] = (ev["config"]["model config"] or "").startswith(
    "refused: from a config file this tool starts scripted rollouts only") and ev["config"]["model config, dry run"] is None
checks["host_config_upload_and_the_default_key_variable_are_refused"] = (ev["config"]["push = true"] or "").startswith("refused: the config does not say") \
    and (ev["config"]["push = true, dry run"] or "").startswith("refused: the config does not say") \
    and (ev["config"]["scripted with the default key variable"] or "").startswith("refused: from a config file this tool starts scripted rollouts only")
import tomllib
sc = tomllib.load(open(scripted, "rb"))
checks["host_config_stand_in_client_is_loopback_discard_and_a_name_never_set"] = sc["client"] == vfrun.NO_MODEL_CLIENT \
    and vfrun.NO_MODEL_URL == "http://127.0.0.1:9/v1" and vfrun.NO_MODEL_VAR == "PHYSIM2_NO_MODEL_KEY"

# ---- theta (m1) ----
def theta(path):
    try:
        return build_reference.read_theta(path)
    except SystemExit as e:
        return "refused"
    except OSError as e:
        return type(e).__name__
good = os.path.join(SCRATCH, "theta-good.json")
fd = os.open(good, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
os.write(fd, json.dumps({"theta": [0.25, 1.5, -3.0]}).encode()); os.close(fd)
wide = os.path.join(SCRATCH, "theta-wide.json")
fd = os.open(wide, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
os.write(fd, json.dumps({"theta": [0.25]}).encode()); os.close(fd)
tw.real(os, "chmod")(wide, 0o644)                           # the test's own file: make the mode certain whatever the umask
link = os.path.join(SCRATCH, "theta-link.json")
os.symlink(good, link)
ev["theta"] = {"mode 0600": theta(good), "mode 0644": theta(wide), "a symbolic link": theta(link), "missing": theta(link + ".none")}
checks["host_theta_is_read_from_a_0600_regular_file_only"] = ev["theta"] == {"mode 0600": [0.25, 1.5, -3.0], "mode 0644": "refused",
                                                                         "a symbolic link": "refused", "missing": "FileNotFoundError"}
src = open(os.path.join(ROOT, "tools", "prove.py")).read()
checks["host_theta_prove_py_puts_no_value_on_a_command_line"] = '"--theta"' not in src and '"--theta-file", theta_file' in src \
    and "os.O_EXCL" in src and "0o600" in src and "build_reference.py" in src
checks["host_no_tripwire_was_reached"] = tw.hits == []
ev["tripwires"] = {"installed": len(tw.names), "hits": tw.hits}
print("RESULT" + json.dumps({"checks": checks, "evidence": ev}))
'''

NOKEY = r'''
import json, os, sys
ROOT, mode, arg = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.join(ROOT, "tools")); sys.path.insert(0, ROOT)
tw = None
if mode != "launcher":
    import tripwires
    tw = tripwires.install()
seen = []
def hook(event, args):
    if event == "open" and isinstance(args[0], (str, bytes)) and "/.prime/" in os.fsdecode(args[0]):
        seen.append(os.path.basename(os.fsdecode(args[0])))
sys.addaudithook(hook)
out = {"mode": mode, "home": os.path.expanduser("~").replace(arg, "<scratch>") if mode != "launcher" else None}
if mode == "launcher":                                      # tools/vfeval.py on the scripted config, --dry-run: no rollout
    import runpy
    sys.argv = [os.path.join(ROOT, "tools", "vfeval.py"), "@", os.path.join(ROOT, "configs", "scripted_ring.toml"), "--dry-run",
                "--run.name", "dry", "-o", arg]
    try:
        runpy.run_path(sys.argv[0], run_name="__main__")
        out["exit"] = "returned"
    except SystemExit as e:
        out["exit"] = e.code
    from physim2_env import _nokey
    out["state"] = _nokey.state()
    out["resolved_config_written"] = sorted(os.listdir(os.path.join(arg, "dry", "configs"))) if os.path.isdir(os.path.join(arg, "dry", "configs")) else None
else:
    if mode != "stock":
        import physim2_env
        from physim2_env import _nokey
        out["state"] = _nokey.state()
    import verifiers.v1.configs.cli.eval
    from verifiers.v1.configs.client import EvalClientConfig, resolve_api_key
    d = EvalClientConfig()
    n = EvalClientConfig(base_url="http://127.0.0.1:9/v1", api_key_var="PHYSIM2_NO_MODEL_KEY")
    k = resolve_api_key(d)
    before_sdk = len(seen)
    import prime_runs                                       # what vf-eval does once per run, upload or not (utils/platform.py:93)
    run = prime_runs.init(mode="disabled", name="x", environments=[], model="none/scripted", framework="verifiers", config={})
    run.finish()
    from prime_runs.config import Config as RunsConfig
    sdk_key = RunsConfig().api_key
    out.update(default_client_key="EMPTY" if k == "EMPTY" else "a key was loaded (%d characters, the made-up one: %s)" % (len(k), k.startswith("FAKE-KEY")),
               default_client_headers=sorted(d.headers), stand_in_client_key=resolve_api_key(n), tripwire_hits=tw.hits,
               opens_by_the_prime_runs_sdk_for_a_disabled_run=len(seen) - before_sdk,
               key_the_prime_runs_sdk_holds="none" if not sdk_key else "a key was loaded (the made-up one: %s)" % sdk_key.startswith("FAKE-KEY"))
out["opens_of_the_made_up_credential_file"] = len(seen)
print("RESULT" + json.dumps(out))
'''

INSIDE = r'''
import base64, io, json, os, signal, subprocess, sys, time, types, contextlib
assert os.path.exists("/.dockerenv"), "this script is for a throwaway container only"
os.makedirs("/t/tools"); os.makedirs("/t/configs")
open("/t/tools/vfrun.py", "wb").write(base64.b64decode(VFRUN_B64))
open("/t/configs/scripted.toml", "wb").write(base64.b64decode(SCRIPTED_B64))
open("/t/configs/model.toml", "wb").write(base64.b64decode(MODEL_B64))
STUB = """#!/usr/local/bin/python3
import json, os, signal, sys, time
LOG = "/t/stub.log"
def note(s):
    open(LOG, "a").write(s + "\\n")
mode = open("/t/stub.mode").read().strip() if os.path.exists("/t/stub.mode") else "obey"
def on_term(signum, frame):
    note("got SIGTERM")
    if mode == "ignore":
        return
    time.sleep(0.3)                      # the stand-in for vf-eval removing its containers
    note("cleaned up, exiting")
    sys.exit(130)
signal.signal(signal.SIGTERM, on_term)
note("started")
json.dump({"argv": sys.argv[1:], "cwd": os.getcwd(), "env": {k: (v if k in ("PHYSIM2_STORE", "PHYSIM2_MODEL_CREDENTIALS", "PRIME_RUNS_MODE", "PYTHONPATH", "VF_RUN_ID") else "<set>") for k, v in os.environ.items()}},
          open("/t/stub.seen.json", "w"))
if mode == "exit0":
    note("ended by itself"); sys.exit(0)
if mode == "selfkill":
    os.kill(os.getpid(), signal.SIGKILL)
end = time.time() + 60
while time.time() < end:
    time.sleep(0.05)
note("ended by itself")
"""
VF = "/t/vf-eval-stand-in"
open(VF, "w").write(STUB); os.chmod(VF, 0o755)
PRELUDE = ("import json, sys, types\n"
           "sys.modules['tomli_w'] = types.SimpleNamespace(dump=lambda cfg, f: f.write(json.dumps(cfg).encode()))\n"
           "sys.path.insert(0, '/t/tools')\nimport vfrun\nvfrun.require_docker = lambda: 'none in this container'\n"
           "vfrun.VF_EVAL = ['/t/vf-eval-stand-in']\nvfrun.DISK_FLOOR_GIB = 0.25\n")
exec(PRELUDE)
BASE = {"PATH": os.environ["PATH"], "HOME": "/root", "VF_RUN_ID": "physim2-round3-test"}
os.environ.clear(); os.environ.update(BASE)
checks, ev = {}, {}


def log():
    try:
        return open("/t/stub.log").read().splitlines()
    except OSError:
        return []


def seen():
    try:
        return json.load(open("/t/stub.seen.json"))
    except OSError:
        return None


def fresh(mode="obey"):
    for f in ("/t/stub.log", "/t/stub.seen.json"):
        if os.path.exists(f):
            os.unlink(f)
    open("/t/stub.mode", "w").write(mode)


def stub_running():
    for d in os.listdir("/proc"):
        if d.isdigit():
            try:
                if b"vf-eval-stand-in" in open(f"/proc/{d}/cmdline", "rb").read() and open(f"/proc/{d}/stat").read().rsplit(")", 1)[1].split()[0] != "Z":
                    return True
            except OSError:
                pass
    return False


def call(fn):
    """(what the function returned or the status it ended the tool with, what it printed)."""
    buf = io.StringIO()
    t0 = time.time()
    try:
        with contextlib.redirect_stdout(buf):
            r = fn()
        return {"returned": r if isinstance(r, (int, str, type(None))) else "a result", "printed": buf.getvalue().strip()[-400:], "seconds": round(time.time() - t0, 2)}
    except SystemExit as e:
        return {"status": e.code if isinstance(e.code, int) else str(e.code)[:300], "printed": buf.getvalue().strip()[-400:], "seconds": round(time.time() - t0, 2)}


def stopped(name, out_dir="/t/runs"):
    try:
        return json.load(open(f"{out_dir}/{name}.stopped.json"))
    except OSError:
        return None


kw = dict(store="/t/store", out_dir="/t/runs", harness={})
# 1. the time limit: ONE SIGTERM, the stand-in cleans up by itself; the tool ends with status 98
fresh()
r = call(lambda: vfrun.run_eval("stub-a", timeout=1, **kw))
ev["time_limit"] = dict(r, stub_log=log(), stub_still_running=stub_running(), record=stopped("stub-a"))
checks["box_time_limit_one_sigterm_then_the_tool_ends_with_status_98"] = r.get("status") == 98 == vfrun.EXIT_STOPPED and log() == ["started", "got SIGTERM", "cleaned up, exiting"] \
    and not stub_running() and stopped("stub-a")["ended"] == "stopped after 1 s: SIGTERM" and stopped("stub-a")["returncode"] == 130
# 2. a stand-in that ignores SIGTERM: SIGKILL only after the grace period; status 98 and the words "may be left"
fresh("ignore")
vfrun.STOP_GRACE_S = 2.0
r = call(lambda: vfrun.run_eval("stub-b", timeout=1, **kw))
ev["ignores_sigterm"] = dict(r, stub_log=log(), stub_still_running=stub_running(), record=stopped("stub-b"))
checks["box_sigkill_only_after_sigterm_and_the_grace_period_then_status_98"] = r.get("status") == 98 and log() == ["started", "got SIGTERM"] and r["seconds"] >= 3.0 \
    and not stub_running() and stopped("stub-b")["ended"] == "stopped after 1 s: SIGTERM, then SIGKILL" and stopped("stub-b")["returncode"] == -9 \
    and "may be left" in r["printed"] and "If a run was interrupted" in r["printed"]
vfrun.STOP_GRACE_S = 120.0
# 3. vf-eval dies of a signal it did not get from the tool
fresh("selfkill")
r = call(lambda: vfrun.run_eval("stub-c", timeout=30, **kw))
ev["dies_of_sigkill"] = dict(r, stub_log=log(), record=stopped("stub-c"))
checks["box_a_vf_eval_that_dies_of_sigkill_ends_the_tool_with_status_98"] = r.get("status") == 98 and stopped("stub-c")["returncode"] == -9 \
    and "died of signal 9" in r["printed"] and "may be left" in r["printed"]
# 4. the disk watchdog before a run: nothing is started, nothing is created
fresh()
real_free = vfrun.free_bytes
vfrun.free_bytes = lambda path=None: 3 << 30
r = call(lambda: vfrun.run_eval("stub-d", store="/t/store", out_dir="/t/runs-never", harness={}, timeout=30, disk_floor_gib=8))
ev["watchdog_before_a_run"] = dict(r, stub_log=log(), out_dir_created=os.path.exists("/t/runs-never"))
checks["box_watchdog_refuses_before_a_run_and_starts_nothing"] = r.get("status") == 97 == vfrun.EXIT_DISK and log() == [] and not os.path.exists("/t/runs-never") \
    and r["printed"].startswith("refused: the disk watchdog did not start the run stub-d: 3.00 GiB free")
# 5. the disk watchdog during a run: the same stop path as the time limit; the reason is recorded; nothing is deleted
fresh()
calls = {"n": 0}
def falling(path=None):
    calls["n"] += 1
    return (20 << 30) if calls["n"] <= 3 else (7 << 30)
vfrun.free_bytes = falling
vfrun.DISK_CHECK_S = 0.3
before = sorted(os.listdir("/t/runs"))
r = call(lambda: vfrun.run_eval("stub-e", timeout=30, disk_floor_gib=8, **kw))
vfrun.free_bytes, vfrun.DISK_CHECK_S = real_free, 15.0
rec = stopped("stub-e")
ev["watchdog_during_a_run"] = dict(r, stub_log=log(), stub_still_running=stub_running(), record=rec, looks_at_the_disk=calls["n"],
                                   files_of_earlier_runs_still_there=all(f in os.listdir("/t/runs") for f in before))
checks["box_watchdog_stops_a_run_through_the_one_stop_path_with_status_97"] = r.get("status") == 97 and log() == ["started", "got SIGTERM", "cleaned up, exiting"] \
    and not stub_running() and rec["ended"].startswith("stopped by the disk watchdog (7.00 GiB free") and rec["ended"].endswith("): SIGTERM") \
    and rec["deleted_by_the_watchdog"] == "nothing" and "refused: stopped by the disk watchdog" in r["printed"]
checks["box_watchdog_deletes_nothing"] = ev["watchdog_during_a_run"]["files_of_earlier_runs_still_there"] and os.path.exists("/t/runs/stub-e.toml")
# 6. a run that ends by itself: status 0, a result, no record of a stop
fresh("exit0")
r = call(lambda: vfrun.run_eval("stub-f", timeout=30, **kw)["ended"])
ev["ends_by_itself"] = dict(r, stub_log=log(), record=stopped("stub-f"))
checks["box_a_run_that_ends_by_itself_returns_normally"] = r.get("returned") == "exited" and stopped("stub-f") is None
# 7. what reaches the child: the allow-list, from a session full of other names (and the stand-in client in the config)
fresh("exit0")
noisy = {"HF_TOKEN": "x", "AWS_SECRET_ACCESS_KEY": "x", "PRIME_API_KEY": "made-up", "PRIME_TEAM_ID": "made-up", "SSH_AUTH_SOCK": "/x", "XDG_CACHE_HOME": "/x",
         "HTTPS_PROXY": "http://x", "LD_PRELOAD": "", "PYTHONSTARTUP": "/x", "TMPDIR": "/tmp", "LANG": "C.UTF-8"}
os.environ.update(noisy)
r = call(lambda: vfrun.run_eval("stub-g", timeout=30, **kw)["ended"])
got = seen()
cfg = json.load(open("/t/runs/stub-g.toml"))
allowed = set(vfrun.ENV_PASS) | {"VF_RUN_ID", "PRIME_RUNS_MODE", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "JAX_PLATFORMS",
                                 "PYTHONDONTWRITEBYTECODE", "XLA_FLAGS", "PYTHONPATH"}
ev["child_environment"] = {"session_names": sorted(os.environ), "child_names": sorted(got["env"]), "child_argv": got["argv"], "client_in_the_config": cfg.get("client")}
checks["box_the_child_gets_the_allow_list_and_nothing_else_of_the_session"] = set(got["env"]) <= allowed and "HF_TOKEN" not in got["env"] and "PRIME_API_KEY" not in got["env"] \
    and got["env"]["PRIME_RUNS_MODE"] == "disabled" and got["env"]["VF_RUN_ID"] == "physim2-round3-test" and got["env"]["PYTHONPATH"] == vfrun.ROOT
checks["box_the_config_of_a_tool_run_names_the_stand_in_client_and_no_upload"] = cfg.get("client") == vfrun.NO_MODEL_CLIENT and cfg.get("push") is False
# 8. a session with DOCKER_HOST: refused before anything starts
fresh("exit0")
os.environ["DOCKER_HOST"] = "tcp://203.0.113.7:2375"
r = call(lambda: vfrun.run_eval("stub-h", timeout=30, **kw))
os.environ.pop("DOCKER_HOST")
ev["dirty_session"] = dict(r, stub_log=log())
checks["box_a_session_with_docker_host_is_refused_before_anything_starts"] = str(r.get("status", "")).startswith("refused: the environment of this command holds DOCKER_HOST") \
    and log() == [] and not os.path.exists("/t/runs/stub-h.toml")
for k in noisy:
    os.environ.pop(k, None)
os.environ["PRIME_API_KEY"], os.environ["PRIME_TEAM_ID"] = "made-up", "made-up"
# 9. the command form (step 2c): a scripted config is accepted; a model config is never started from a config file,
#    with or without the credentials flag (round 4: a model run starts from a request)
fresh("exit0")
args = ["--run-name", "single-d", "--out-dir", "/t/single", "--store", "/t/store", "--disk-floor-gib", "0.25"]
r = call(lambda: vfrun.main(["--config", "/t/configs/scripted.toml", *args]))
got = seen()
ev["command_scripted"] = dict(r, child_argv=got and got["argv"], child_cwd=got and got["cwd"], child_env=got and sorted(got["env"]), store=got and got["env"].get("PHYSIM2_STORE"))
checks["box_command_form_starts_a_scripted_config_without_any_credential"] = r.get("returned") == 0 and got["argv"] == ["@", "/t/configs/scripted.toml", "--run.name", "single-d", "-o", "/t/single", "--no-rich"] \
    and got["cwd"] == vfrun.ROOT and got["env"].get("PHYSIM2_STORE") == "/t/store" and "PRIME_API_KEY" not in got["env"] and "PHYSIM2_MODEL_CREDENTIALS" not in got["env"]
fresh("exit0")
r = call(lambda: vfrun.main(["--config", "/t/configs/model.toml", *args]))
ev["command_model_without_flag"] = dict(r, stub_log=log())
checks["box_command_form_refuses_a_model_config"] = str(r.get("status", "")).startswith("refused: from a config file this tool starts scripted rollouts only") and log() == []
fresh("exit0")
r = call(lambda: vfrun.main(["--config", "/t/configs/model.toml", "--dry-run", *args]))
got = seen()
ev["command_model_dry_run"] = dict(r, child_argv=got and got["argv"], child_env=got and sorted(got["env"]))
checks["box_command_form_dry_run_of_a_model_config_gets_no_credential"] = r.get("returned") == 0 and got["argv"][-1] == "--dry-run" and "PRIME_API_KEY" not in got["env"] \
    and "PHYSIM2_MODEL_CREDENTIALS" not in got["env"]
fresh("exit0")
r = call(lambda: vfrun.main(["--config", "/t/configs/model.toml", "--model-credentials", "prime", *args]))
ev["command_model_with_flag"] = dict(r, stub_log=log())
# round 4: the flag belongs to the request route (stage rollout) only; on the command form it starts nothing
checks["box_command_form_refuses_the_model_credentials_flag"] = str(r.get("status", "")).startswith("refused: a model rollout is started by a request") and log() == []
fresh()
vfrun.free_bytes = lambda path=None: 5 << 30
r = call(lambda: vfrun.main(["--config", "/t/configs/scripted.toml", "--run-name", "single-d", "--out-dir", "/t/single2", "--store", "/t/store", "--disk-floor-gib", "8"]))
vfrun.free_bytes = real_free
ev["command_under_the_floor"] = dict(r, stub_log=log())
checks["box_command_form_is_refused_under_the_floor"] = r.get("status") == 97 and log() == [] and not os.path.exists("/t/single2")
os.environ.pop("PRIME_API_KEY"); os.environ.pop("PRIME_TEAM_ID")
# 10. the tool itself is told to stop (`kill <pid>`) while a run is under way: the stand-in gets SIGTERM
fresh()
tool = subprocess.Popen([sys.executable, "-B", "-c", PRELUDE + "vfrun.run_eval('stub-i', store='/t/store', out_dir='/t/runs', harness={}, timeout=50)\n"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
for _ in range(100):
    if log():
        break
    time.sleep(0.05)
time.sleep(0.2)
tool.send_signal(signal.SIGTERM)                 # what the runbook's "if a run was interrupted" does to the tool, by pid
out, err = tool.communicate(timeout=30)
ev["tool_told_to_stop"] = {"tool_returncode": tool.returncode, "tool_last_line": err.strip().splitlines()[-1][:60] if err.strip() else "",
                           "stub_log": log(), "stub_still_running": stub_running()}
checks["box_a_sigterm_to_the_tool_reaches_the_stand_in_as_sigterm"] = log() == ["started", "got SIGTERM", "cleaned up, exiting"] and not stub_running() \
    and tool.returncode != 0 and "KeyboardInterrupt" in err
# 11. a helper (make_instances, build_reference) is stopped with its tool, not left behind (m4)
HELPER = ("import os, signal, sys, time\n"
          "def on(s, f):\n    open('/t/helper.log', 'a').write('helper got SIGTERM\\n'); sys.exit(143)\n"
          "signal.signal(signal.SIGTERM, on)\nopen('/t/helper.log', 'a').write('helper started %d\\n' % os.getpid())\ntime.sleep(60)\n")
open("/t/helper.py", "w").write(HELPER)
tool = subprocess.Popen([sys.executable, "-B", "-c", PRELUDE + "vfrun.run_helper([sys.executable, '-B', '/t/helper.py'])\n"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
for _ in range(100):
    if os.path.exists("/t/helper.log"):
        break
    time.sleep(0.05)
time.sleep(0.2)
hpid = int(open("/t/helper.log").read().split()[2])
tool.send_signal(signal.SIGTERM)
out, err = tool.communicate(timeout=30)
time.sleep(0.2)
ev["helper"] = {"helper_log": open("/t/helper.log").read().splitlines(), "helper_still_running": os.path.exists(f"/proc/{hpid}"),
                "tool_returncode": tool.returncode, "tool_last_line": err.strip().splitlines()[-1][:60] if err.strip() else ""}
checks["box_a_helper_is_stopped_with_its_tool"] = ev["helper"]["helper_log"][1:] == ["helper got SIGTERM"] and not ev["helper"]["helper_still_running"] \
    and tool.returncode != 0 and "KeyboardInterrupt" in err
print("RESULT" + json.dumps({"checks": checks, "evidence": ev}))
'''


def result(p, what):
    line = next((ln for ln in p.stdout.splitlines() if ln.startswith("RESULT")), None)
    if line is None:
        raise SystemExit(f"{what} gave no result:\n" + (p.stdout + p.stderr)[-3000:])
    return json.loads(line[6:])


def main():
    if sys.platform != "linux" or os.environ.get("PHYSIM2_DEV_MACHINE") != "cloud-container":
        raise SystemExit("check_round3.py is a development check for the Linux build container; it is NOT part of the Mac runbook.")
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True, help="an existing folder of the caller for the test's own small files")
    ap.add_argument("--out", required=True)
    ap.add_argument("--image", default="physim2-ring:4")
    ap.add_argument("--skip-container", action="store_true")
    a = ap.parse_args()
    scratch = os.path.realpath(a.scratch)
    work = os.path.join(scratch, "check_round3")
    if os.path.lexists(work):
        raise SystemExit(f"{work} exists already: give a fresh --scratch (this tool removes nothing)")
    home = os.path.join(work, "home")
    os.makedirs(os.path.join(home, ".prime"))
    os.makedirs(os.path.join(work, "files"))
    with open(os.path.join(home, ".prime", "config.json"), "w") as f:
        json.dump({"api_key": "FAKE-KEY-NOT-A-CREDENTIAL-0000", "team_id": "made-up-team"}, f)
    env = {"PATH": os.environ["PATH"], "HOME": home}        # nothing else of this session reaches a child
    checks, ev = {}, {}
    # ---- host, under tripwires ----
    p = subprocess.run(["nice", "-n", "10", sys.executable, "-B", "-c", HOST, ROOT, os.path.join(work, "files")], capture_output=True, text=True,
                       env=env, cwd=work, timeout=600)
    got = result(p, "the host child")
    checks.update(got["checks"])
    ev["host_under_tripwires"] = got["evidence"]
    # ---- the made-up credential file ----
    nk = {}
    for mode, extra in (("stock", {}), ("package", {}), ("laboratory in step-3 mode", {"PHYSIM2_MODEL_CREDENTIALS": "prime", "VF_CONFIG": "{}"}),
                        ("launcher", {})):
        arg = os.path.join(work, "dry") if mode == "launcher" else work
        p = subprocess.run(["nice", "-n", "10", sys.executable, "-B", "-c", NOKEY, ROOT, "package" if mode.startswith("lab") else mode, arg],
                           capture_output=True, text=True, env=dict(env, **extra), cwd=work, timeout=600)
        nk[mode] = result(p, f"the credential trace ({mode})")
    ev["made_up_credential_file"] = {"file": "<scratch>/check_round3/home/.prime/config.json, holding the text FAKE-KEY-NOT-A-CREDENTIAL", "traces": nk}
    checks["nokey_control_the_stock_import_of_verifiers_opens_the_file_and_loads_its_key"] = nk["stock"]["opens_of_the_made_up_credential_file"] >= 1 \
        and nk["stock"]["default_client_key"].startswith("a key was loaded") and nk["stock"]["default_client_key"].endswith("True)")
    checks["nokey_through_the_package_the_file_is_never_opened"] = nk["package"]["opens_of_the_made_up_credential_file"] == 0 \
        and nk["package"]["state"] == "stand-in" and nk["package"]["default_client_key"] == "EMPTY" and nk["package"]["default_client_headers"] == []
    checks["nokey_the_stand_in_client_has_no_key"] = nk["package"]["stand_in_client_key"] == "EMPTY" and nk["stock"]["stand_in_client_key"] == "EMPTY"
    checks["nokey_control_the_prime_runs_sdk_reads_the_file_even_for_a_disabled_run"] = nk["stock"]["opens_by_the_prime_runs_sdk_for_a_disabled_run"] >= 1 \
        and nk["stock"]["key_the_prime_runs_sdk_holds"].endswith("True)")
    checks["nokey_through_the_package_the_prime_runs_sdk_opens_nothing_and_holds_no_key"] = nk["package"]["opens_by_the_prime_runs_sdk_for_a_disabled_run"] == 0 \
        and nk["package"]["key_the_prime_runs_sdk_holds"] == "none" and nk["laboratory in step-3 mode"]["key_the_prime_runs_sdk_holds"] == "none"
    checks["nokey_a_laboratory_process_never_opens_it_even_in_step_3_mode"] = nk["laboratory in step-3 mode"]["opens_of_the_made_up_credential_file"] == 0 \
        and nk["laboratory in step-3 mode"]["state"] == "stand-in"
    checks["nokey_the_launcher_resolves_the_scripted_config_without_opening_it"] = nk["launcher"]["opens_of_the_made_up_credential_file"] == 0 \
        and nk["launcher"]["state"] == "stand-in" and nk["launcher"]["exit"] in (0, "returned") and bool(nk["launcher"]["resolved_config_written"])
    checks["nokey_no_tripwire_was_reached_by_the_imports"] = all(nk[m].get("tripwire_hits") == [] for m in ("stock", "package", "laboratory in step-3 mode"))
    # ---- real signals, inside a throwaway container (no host path mounted) ----
    if not a.skip_container:
        b64 = lambda path: base64.b64encode(open(path, "rb").read()).decode()  # noqa: E731
        script = (f"VFRUN_B64 = {b64(os.path.join(HERE, 'vfrun.py'))!r}\nSCRIPTED_B64 = {b64(os.path.join(ROOT, 'configs', 'scripted_ring.toml'))!r}\n"
                  f"MODEL_B64 = {b64(os.path.join(ROOT, 'configs', 'qwen_ring_bash.toml'))!r}\n" + INSIDE)
        name = "vfr3fix1-check-round3"
        p = subprocess.run(["docker", "run", "--rm", "-i", "--name", name, "--network", "none", a.image, "python3", "-B", "-"], input=script,
                           capture_output=True, text=True, timeout=600)
        got = result(p, "the container")
        checks.update(got["checks"])
        ev["in_a_throwaway_container"] = got["evidence"]
        ev["container"] = {"started_as": f"docker run --rm -i --name {name} --network none {a.image} python3 -B -   (no mount, no socket, not privileged)",
                           "still_there_afterwards": name in subprocess.run(["docker", "ps", "-a", "--format", "{{.Names}}"], capture_output=True, text=True).stdout.split()}
        checks["box_the_test_container_is_gone"] = ev["container"]["still_there_afterwards"] is False
    out = {"what": "round 3 of the host-safety fixes: the environment allow-list (M1), the one stop path and its exit statuses (M2, m5), no model "
                   "credential in a scripted run (M3), theta by file (m1), helpers stopped with their tool (m4), the disk watchdog (D1)",
           "evidence_labels": {"host_*": "run on the cloud host in a child process under tools/tripwires.py (pure functions on made-up inputs)",
                               "nokey_*": "run on the cloud host: imports of verifiers and of the package under tripwires with an audit hook on every open; "
                                          "the launcher's dry run without tripwires (verifiers' own config resolution, no rollout); a made-up credential file in a scratch home",
                               "box_*": "run in a throwaway container (docker run --rm --network none, no host path): real processes and real signals, a stand-in for vf-eval"},
           "n_checks": len(checks), "n_passed": sum(v is True for v in checks.values()), "failed": [k for k, v in checks.items() if v is not True],
           "checks": checks, "evidence": ev,
           "left_behind": f"{work} (small files of this test; the caller removes its scratch)"}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("n_checks", "n_passed", "failed")}))


if __name__ == "__main__":
    main()
