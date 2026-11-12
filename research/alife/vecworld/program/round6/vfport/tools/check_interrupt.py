"""check_interrupt -- what happens to a run that is cut off, tested where a real signal may be sent: INSIDE A
THROWAWAY CONTAINER; and how its containers are found afterwards, tested with containers this tool starts itself.

Audit finding A2, required change 2. Two parts, neither of which signals or removes anything of the host that
this tool did not start a moment before, and no host path is ever mounted:

  stop_*   `docker run --rm --network none <image>` runs tools/vfrun.py with a stand-in for vf-eval (a real process
           in that container which writes down every signal it gets):
             - under timeout=1 the stand-in records SIGTERM, cleans up and exits; it is never killed; the tool then
               ends with status 98 (round 3: a vf-eval that had to be stopped ends the tool)
             - a stand-in that ignores SIGTERM is killed, but only after the grace period
             - `kill <pid of the tool>` while a run is under way reaches the stand-in as SIGTERM
  label_*  two containers are started here (`sleep`, no mount): `vf-other` with the run label of somebody else's
           verifiers run, and one with the run label of this test. Listing by the label of this test shows the
           second and not `vf-other`; the old listing by the name substring `vf-` shows `vf-other`, which is what
           made it dangerous. Both are then removed by their exact names.

usage: PHYSIM2_DEV_MACHINE=cloud-container python -B tools/check_interrupt.py --out results/safety_interrupt.json
"""
import argparse
import base64
import json
import os
import secrets
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

INSIDE = r'''
import base64, json, os, signal, subprocess, sys, time, types
assert os.path.exists("/.dockerenv"), "this script is for a throwaway container only"
os.makedirs("/t")
open("/t/vfrun.py", "wb").write(base64.b64decode(VFRUN_B64))
STUB = """#!/usr/local/bin/python3
import os, signal, sys, time
LOG = "/t/stub.log"
def note(s):
    open(LOG, "a").write(s + "\\n")
def on_term(signum, frame):
    note("got SIGTERM")
    if os.environ.get("STUB_IGNORES_SIGTERM"):
        return
    time.sleep(0.3)                      # the stand-in for vf-eval removing its containers
    note("cleaned up, exiting")
    sys.exit(130)
signal.signal(signal.SIGTERM, on_term)
note("started pid %d argv %s" % (os.getpid(), " ".join(sys.argv[1:3])))
end = time.time() + 60
while time.time() < end:
    time.sleep(0.05)
note("ended by itself")
"""
VF = os.path.join(os.path.dirname(sys.executable), "vf-eval")
open(VF, "w").write(STUB); os.chmod(VF, 0o755)
sys.modules["tomli_w"] = types.SimpleNamespace(dump=lambda cfg, f: f.write(json.dumps(cfg).encode()))
sys.path.insert(0, "/t")
import vfrun
vfrun.require_docker = lambda: "none in this container"
vfrun.VF_EVAL = [VF]                               # the stand-in, in place of tools/vfeval.py
vfrun.DISK_FLOOR_GIB = 0.25                        # the disk watchdog has its own tests (tools/check_round3.py)
os.environ["VF_RUN_ID"] = "physim2-interrupt-test"
checks, ev = {}, {}


def log():
    try:
        return open("/t/stub.log").read().splitlines()
    except OSError:
        return []


def fresh():
    if os.path.exists("/t/stub.log"):
        os.unlink("/t/stub.log")


def stub_running():
    for d in os.listdir("/proc"):
        if d.isdigit():
            try:
                if b"vf-eval" in open(f"/proc/{d}/cmdline", "rb").read() and open(f"/proc/{d}/stat").read().rsplit(")", 1)[1].split()[0] != "Z":
                    return True
            except OSError:
                pass
    return False


# 1. timeout=1, a stand-in that obeys SIGTERM
fresh()
t0 = time.time()
try:
    vfrun.run_eval("stub-a", store="/t/store", out_dir="/t/runs", harness={}, timeout=1)
    status = None
except SystemExit as e:
    status = e.code
r = json.load(open("/t/runs/stub-a.stopped.json"))
ev["timeout_1"] = {"ended": r["ended"], "returncode": r["returncode"], "seconds": round(time.time() - t0, 2), "stub_log": log(),
                   "stub_still_running": stub_running(), "tool_status": status}
checks["stop_under_timeout_1_the_stand_in_records_sigterm_and_exits_by_itself"] = r["ended"] == "stopped after 1 s: SIGTERM" and r["returncode"] == 130 \
    and log()[1:] == ["got SIGTERM", "cleaned up, exiting"] and not stub_running() and status == 98
# 2. a stand-in that ignores SIGTERM: SIGKILL, but only after the grace period
fresh()
vfrun.STOP_GRACE_S = 2.0
os.environ["STUB_IGNORES_SIGTERM"] = "1"
t0 = time.time()
r = vfrun.run_child(["nice", "-n", "10", VF, "@", "x.toml"], env=dict(os.environ), cwd="/t", timeout=1, grace=2.0)
os.environ.pop("STUB_IGNORES_SIGTERM")
ev["ignores_sigterm"] = {"ended": r[3], "returncode": r[0], "seconds": round(time.time() - t0, 2), "stub_log": log(), "stub_still_running": stub_running()}
checks["stop_sigkill_comes_only_after_sigterm_and_the_grace_period"] = r[3] == "stopped after 1 s: SIGTERM, then SIGKILL" and r[0] == -9 \
    and log()[1:] == ["got SIGTERM"] and time.time() - t0 >= 3.0 and not stub_running()
# 3. the tool itself is told to stop (`kill <pid>`) while a run is under way
fresh()
tool = subprocess.Popen([sys.executable, "-B", "-c",
                         "import json, sys, types\n"
                         "sys.modules['tomli_w'] = types.SimpleNamespace(dump=lambda cfg, f: f.write(json.dumps(cfg).encode()))\n"
                         "sys.path.insert(0, '/t')\nimport vfrun\nvfrun.require_docker = lambda: 'none'\n"
                         f"vfrun.VF_EVAL = [{VF!r}]\nvfrun.DISK_FLOOR_GIB = 0.25\n"
                         "vfrun.run_eval('stub-c', store='/t/store', out_dir='/t/runs', harness={}, timeout=50)\n"],
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
checks["stop_a_sigterm_to_the_tool_reaches_the_stand_in_as_sigterm"] = log()[1:] == ["got SIGTERM", "cleaned up, exiting"] and not stub_running() \
    and tool.returncode != 0 and "KeyboardInterrupt" in err
print("RESULT" + json.dumps({"checks": checks, "evidence": ev}))
'''


def sh(*cmd, timeout=120):
    return subprocess.run(list(cmd), capture_output=True, text=True, timeout=timeout)


def names(*flt):
    return sorted(sh("docker", "ps", "-a", *flt, "--format", "{{.Names}}").stdout.split())


def main():
    if sys.platform != "linux" or os.environ.get("PHYSIM2_DEV_MACHINE") != "cloud-container":
        raise SystemExit("check_interrupt.py is a development check for the Linux build container; it is NOT part of the Mac runbook.")
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--image", default="physim2-ring:4")
    a = ap.parse_args()
    checks, ev = {}, {}
    # ---- part 1: a real process and real signals, inside a throwaway container (no host path mounted) ----
    script = f"VFRUN_B64 = {base64.b64encode(open(os.path.join(HERE, 'vfrun.py'), 'rb').read()).decode()!r}\n" + INSIDE
    p = subprocess.run(["docker", "run", "--rm", "-i", "--network", "none", a.image, "python3", "-B", "-"], input=script, capture_output=True,
                       text=True, timeout=300)
    line = next((ln for ln in p.stdout.splitlines() if ln.startswith("RESULT")), None)
    if line is None:
        raise SystemExit("the container gave no result:\n" + (p.stdout + p.stderr)[-2000:])
    got = json.loads(line[6:])
    checks.update(got["checks"])
    ev["in_a_throwaway_container"] = got["evidence"]
    # ---- part 2: finding the containers of ONE run. Both containers are started here and removed by exact name ----
    label = "physim2-label-test-" + secrets.token_hex(4)
    mine, other = "vfsafe-labelled-" + secrets.token_hex(4), "vf-other"
    if other in names():
        raise SystemExit("a container named vf-other exists already and is not this tool's: nothing was started, nothing was touched")
    started = []
    try:
        for name, lab in ((other, "somebody-elses-verifiers-run"), (mine, label)):
            r = sh("docker", "run", "-d", "--network", "none", "--name", name, "--label", f"verifiers.run={lab}", "--entrypoint", "sleep", a.image, "300")
            if r.returncode:
                raise SystemExit(f"could not start {name}: {r.stderr.strip()[-200:]}")
            started.append(name)
        by_label = names("--filter", f"label=verifiers.run={label}")
        by_name = names("--filter", "name=vf-")
        by_any_label = names("--filter", "label=verifiers.run")
        mounts = {n: sh("docker", "inspect", "--format", "{{json .Mounts}}", n).stdout.strip() for n in started}
        ev["label_listing"] = {"started_by_this_test": started, "run_label_of_this_test": label,
                               "docker ps -a --filter label=verifiers.run=<this label>": by_label,
                               "docker ps -a --filter name=vf- (the old runbook's listing)": [n for n in by_name if n in started],
                               "docker ps -a --filter label=verifiers.run (any verifiers run)": [n for n in by_any_label if n in started],
                               "others_listed_by_name_and_left_alone": len([n for n in by_name if n not in started]),
                               "mounts_of_the_two_containers": mounts}
        checks["label_listing_by_run_label_shows_this_run_only"] = by_label == [mine]
        checks["label_foreign_vf_other_is_absent_from_the_label_listing"] = other not in by_label
        checks["label_old_listing_by_name_would_have_shown_vf_other"] = other in by_name
        checks["label_no_host_path_in_the_test_containers"] = all(v == "[]" for v in mounts.values())
    finally:
        removed = {n: sh("docker", "rm", "-f", n).returncode == 0 for n in started}      # exactly the names started above
    ev["label_listing"]["removed_by_exact_name"] = removed
    checks["label_both_test_containers_removed_by_exact_name"] = all(removed.values()) and not any(n in names() for n in started)
    out = {"what": "audit A2 / required change 2: stopping vf-eval with SIGTERM first (real signals, inside `docker run --rm --network none`), "
                   "and listing the containers of one run by its label (two containers started and removed by this tool)",
           "evidence_label": "container", "n_checks": len(checks), "n_passed": sum(v is True for v in checks.values()),
           "failed": [k for k, v in checks.items() if v is not True], "checks": checks, "evidence": ev}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("n_checks", "n_passed", "failed")}))


if __name__ == "__main__":
    main()
