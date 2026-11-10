"""check_driver -- the item driver's cleanup and its guard, exercised where they belong: INSIDE A THROWAWAY CONTAINER.

The cleanup of physim2_env/public/_item.py kills every process and deletes every file of one uid. It must never run
on a real machine, so nothing here runs it on the host: this tool only starts `docker run --rm --network none`
with the exam image and feeds one script to the Python inside. There, as root:

  guard_*    with a canary process and canary files of two unprivileged uids in place, the cleanup is asked for
             with one layer of the guard missing at a time (no marker, marker not root's, no route variable, uid 0,
             a uid that is not the box's predictor uid, a uid below 1000, no sign of a container [simulated]):
             every call must be refused and every canary must survive
  cleanup_*  with every layer present, the cleanup removes the process and the files of the box's predictor uid and
             leaves the other uid's alone
  driver_*   the driver as the grader starts it: an honest predictor; a named pipe or a link left as stderr.txt or
             reply.npz (red team 3: root must neither block nor follow); the driver without the route variable
             (runs, no drop, no cleanup); with the route variable but without the marker (refuses, and the
             predictor does not run at all)

usage: python tools/check_driver.py --out results/driver_container.json [--image physim2-ring:1]
"""
import argparse
import base64
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from physim2_env._paths import agentenv_root  # noqa: E402

INSIDE = r'''
import base64, importlib.util, json, os, shutil, signal, subprocess, sys, time
assert os.path.exists("/.dockerenv") or "docker" in open("/proc/1/cgroup").read(), "this script is for a throwaway container only"
ITEM, RUNNER = "/runtime/item.py", "/w/physim2/predict_runner.py"
os.makedirs("/runtime"); os.makedirs("/w/physim2"); os.makedirs("/w/sub")
open(ITEM, "wb").write(base64.b64decode(ITEM_B64)); open(RUNNER, "wb").write(base64.b64decode(RUNNER_B64))
spec = importlib.util.spec_from_file_location("item", ITEM); item = importlib.util.module_from_spec(spec); spec.loader.exec_module(item)
X, Y = 31001, 31002
VAR, VAL = item.ROUTE_VAR, item.ROUTE_VALUE
checks, ev = {}, {}


def canary(uid):
    pid = os.fork()
    if pid == 0:
        os.setgroups([]); os.setgid(uid); os.setuid(uid)
        os.execv("/bin/sleep", ["sleep", "600"])
    for d in ("/tmp", "/var/tmp", "/dev/shm"):
        p = f"{d}/canary_{uid}"
        open(p, "w").write("canary"); os.chown(p, uid, uid)
    return pid


def alive(pid):
    try:
        return open(f"/proc/{pid}/stat").read().rsplit(")", 1)[1].split()[0] != "Z"
    except OSError:
        return False


def files(uid):
    return sorted(d for d in ("/tmp", "/var/tmp", "/dev/shm") if os.path.exists(f"{d}/canary_{uid}"))


def marker(uid=X, owner=0, mode=0o644, link=False):
    shutil.rmtree("/etc/physim2", ignore_errors=True)
    if os.path.islink("/etc/physim2"):
        os.unlink("/etc/physim2")
    if uid is None:
        return
    if link:
        os.makedirs("/etc/elsewhere", exist_ok=True); os.symlink("/etc/elsewhere", "/etc/physim2")
    else:
        os.makedirs("/etc/physim2")
    open("/etc/physim2/predictor_uid", "w").write(str(uid)); os.chown("/etc/physim2/predictor_uid", owner, owner); os.chmod("/etc/physim2/predictor_uid", mode)


def refused(uid):
    """Ask for the full cleanup; True if it was refused before anything happened."""
    try:
        item.cleanup(uid)
        return False
    except RuntimeError as e:
        return str(e).startswith("refused")


px, py = canary(X), canary(Y)
real_evidence = item.container_evidence
CASES = [  # name, marker kwargs (None = no marker), route variable, target uid, simulate no container evidence
    ("no_marker", None, VAL, X, False),
    ("marker_owned_by_the_predictor_uid", dict(owner=X), VAL, X, False),
    ("marker_writable_by_others", dict(mode=0o666), VAL, X, False),
    ("marker_directory_is_a_link", dict(link=True), VAL, X, False),
    ("no_route_variable", dict(), None, X, False),
    ("wrong_route_variable", dict(), "1", X, False),
    ("uid_0", dict(uid=0), VAL, 0, False),
    ("uid_is_not_the_box_predictor_uid", dict(uid=X), VAL, Y, False),
    ("uid_below_1000", dict(uid=500), VAL, 500, False),
    ("no_sign_of_a_container_simulated", dict(), VAL, X, True),
]
for name, mk, route, uid, no_ev in CASES:
    marker(**mk) if mk is not None else marker(uid=None)
    os.environ.pop(VAR, None)
    if route is not None:
        os.environ[VAR] = route
    item.container_evidence = (lambda: []) if no_ev else real_evidence
    r = refused(uid)
    each = {}
    for fn in ("kill_user", "wipe_user", "ipc_user"):
        try:
            getattr(item, fn)(uid); each[fn] = "RAN"
        except RuntimeError as e:
            each[fn] = "refused" if str(e).startswith("refused") else "error"
    ev[name] = {"cleanup_refused": r, "each_function": each, "why": item.box_guard(uid)["why"],
                "canaries_alive": [alive(px), alive(py)], "canary_files": [files(X), files(Y)]}
    checks[f"guard_refuses_{name}"] = r and set(each.values()) == {"refused"} and alive(px) and alive(py) and len(files(X)) == 3 and len(files(Y)) == 3
item.container_evidence = real_evidence
# ---- every layer present: the cleanup works, and only on the box's predictor uid ----
marker(uid=X); os.environ[VAR] = VAL
ev["container_evidence"] = item.container_evidence()
rep = item.cleanup(X)
time.sleep(0.2)
try:
    os.waitpid(px, os.WNOHANG)
except ChildProcessError:
    pass
ev["all_layers"] = {"report": {k: rep[k] for k in ("killed", "removed", "left_pids", "left_files")}, "x_alive": alive(px), "x_files": files(X),
                    "y_alive": alive(py), "y_files": files(Y)}
checks["cleanup_with_every_layer_removes_the_predictor_uid"] = not alive(px) and files(X) == [] and rep["left_pids"] == [] and rep["left_files"] == []
checks["cleanup_leaves_another_uid_alone"] = alive(py) and len(files(Y)) == 3
os.kill(py, signal.SIGKILL); os.waitpid(py, 0)
for d in files(Y):
    os.unlink(f"{d}/canary_{Y}")

# ---- the driver as a program ----
import numpy as np
np.savez("/runtime/request.npz", history=np.zeros((17, 6)), prefix=np.zeros((16, 24)), test=np.zeros((32, 24)),
         queries=json.dumps({"1": [1, 2], "2": [16]}), n_samples=4, seed=0)
os.chmod("/runtime/request.npz", 0o444); os.chmod("/runtime", 0o755); os.chmod("/w", 0o755)
open("/etc/shadow_like", "w").write("ROOT-ONLY-CONTENT"); os.chmod("/etc/shadow_like", 0o600)
PRED = {
    "honest": "import numpy as np\ndef predict(h, p, q, n, s):\n    return {l: np.zeros((n, len(ts), {1: 6, 2: 3}[l])) for l, ts in q.items()}\n",
    "fifo_as_stderr": "import os, sys\ndef predict(h, p, q, n, s):\n    p = os.path.join(os.path.dirname(sys.argv[3]), 'stderr.txt')\n    os.unlink(p); os.mkfifo(p, 0o666); os._exit(1)\n",
    "fifo_as_reply": "import os, sys\ndef predict(h, p, q, n, s):\n    os.mkfifo(sys.argv[3], 0o666); os._exit(0)\n",
    "link_as_stderr": "import os, sys\ndef predict(h, p, q, n, s):\n    p = os.path.join(os.path.dirname(sys.argv[3]), 'stderr.txt')\n    os.unlink(p); os.symlink('/etc/shadow_like', p); os._exit(1)\n",
    "link_as_reply": "import os, sys\ndef predict(h, p, q, n, s):\n    os.symlink('/etc/shadow_like', sys.argv[3]); os._exit(0)\n",
    "moved_reply_directory": "import os, sys\ndef predict(h, p, q, n, s):\n    d = os.path.dirname(sys.argv[3]); os.rename(d, d + '.moved'); os.symlink('/etc', d); os._exit(1)\n",
    "leaves_a_mark": "import os\ndef predict(h, p, q, n, s):\n    open('/tmp/predictor_ran', 'w').close(); os._exit(1)\n",
}


def drive(name, route=True, mk=True, uid=X):
    sub = f"/w/{name}"
    os.makedirs(sub, exist_ok=True); open(f"{sub}/predict.py", "w").write(PRED[name]); os.chmod(sub, 0o755); os.chmod(f"{sub}/predict.py", 0o644)
    marker(uid=X) if mk else marker(uid=None)
    env = {k: v for k, v in os.environ.items() if k != VAR}
    if route:
        env[VAR] = VAL
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, "-I", "-B", ITEM, "--submission", sub, "--runner", RUNNER, "--request", "/runtime/request.npz",
                            "--cpu", "20", "--wall", "30", "--mem-gib", "4", "--uid", str(uid)], capture_output=True, text=True, timeout=60, env=env)
        r = json.loads(p.stdout.strip().splitlines()[-1])
        return {"returned": True, "ok": r.get("ok"), "why": r.get("why"), "stderr": (r.get("stderr") or "")[-80:], "layers": r.get("layers"),
                "driver_error": r.get("driver_error"), "cleanup": {k: (r.get("cleanup") or {}).get(k) for k in ("killed", "removed", "left_pids", "left_files")},
                "seconds": round(time.time() - t0, 2)}
    except subprocess.TimeoutExpired:
        return {"returned": False, "seconds": round(time.time() - t0, 2)}


D = {k: drive(k) for k in ("honest", "fifo_as_stderr", "fifo_as_reply", "link_as_stderr", "link_as_reply", "moved_reply_directory")}
ev["driver"] = D
checks["driver_honest_predictor_runs_as_the_box_uid_with_cleanup"] = D["honest"].get("ok") is True and D["honest"]["layers"] == {"rlimits": True, "uid": X, "cleanup": True}
checks["driver_returns_within_seconds_for_every_predictor"] = all(v["returned"] and v["seconds"] < 20 for v in D.values())
checks["driver_named_pipe_or_link_is_never_a_reply"] = D["fifo_as_reply"].get("ok") is False and D["link_as_reply"].get("ok") is False
checks["driver_never_returns_root_only_content"] = all("ROOT-ONLY" not in json.dumps(v) for v in D.values())
checks["driver_box_clean_after_every_predictor"] = all(v["returned"] and v["cleanup"]["left_pids"] == [] and v["cleanup"]["left_files"] == [] for v in D.values())
no_route = drive("leaves_a_mark", route=False)
ran_without_route = os.path.exists("/tmp/predictor_ran")
if ran_without_route:
    os.unlink("/tmp/predictor_ran")
no_marker = drive("leaves_a_mark", route=True, mk=False)
ev["driver_without_route_variable"], ev["driver_with_route_variable_but_no_marker"] = no_route, no_marker
checks["driver_without_route_variable_neither_drops_nor_cleans"] = no_route["returned"] and no_route["layers"].get("uid") is None \
    and no_route["layers"].get("cleanup") is False and bool(no_route["layers"].get("refused")) and ran_without_route
checks["driver_on_the_grading_route_refuses_and_runs_nothing_without_the_marker"] = no_marker["returned"] and no_marker.get("ok") is False \
    and "refused" in str(no_marker.get("driver_error")) and not os.path.exists("/tmp/predictor_ran")
print("RESULT" + json.dumps({"checks": checks, "evidence": ev}))
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--image", default="physim2-ring:1")
    ap.add_argument("--package-root", default=ROOT)
    a = ap.parse_args()
    item = open(os.path.join(a.package_root, "physim2_env", "public", "_item.py"), "rb").read()
    runner = open(os.path.join(agentenv_root(), "physim2", "predict_runner.py"), "rb").read()
    script = f"ITEM_B64 = {base64.b64encode(item).decode()!r}\nRUNNER_B64 = {base64.b64encode(runner).decode()!r}\n" + INSIDE
    p = subprocess.run(["docker", "run", "--rm", "-i", "--network", "none", a.image, "python3", "-B", "-"], input=script, capture_output=True,
                       text=True, timeout=600)
    line = next((ln for ln in p.stdout.splitlines() if ln.startswith("RESULT")), None)
    if line is None:
        raise SystemExit("the container gave no result:\n" + (p.stdout + p.stderr)[-2000:])
    res = json.loads(line[6:])
    out = {"where": f"inside `docker run --rm --network none {a.image}` (nothing of this ran on the host)", "n_checks": len(res["checks"]),
           "n_passed": sum(v is True for v in res["checks"].values()), "failed": [k for k, v in res["checks"].items() if v is not True], **res}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("where", "n_checks", "n_passed", "failed")}))


if __name__ == "__main__":
    main()
