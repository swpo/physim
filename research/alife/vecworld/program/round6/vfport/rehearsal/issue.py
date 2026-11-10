"""issue -- issue ONE command of RUNBOOK_MAC.md the way a session issues it, and keep a literal record of it.

Round-1 verdict of the host-safety audit, remaining change 7: the first rehearsal ran the runbook's commands
from files, which hid that a session's detached command leaves a waiting shell whose command line is the whole
command text. Here every command is issued as ONE `sh -c '<text of the fenced command>'` (or `bash -c`), with the
text taken from the runbook that is on disk in the clone, and nothing is ever written to a script file.

What this tool does, and nothing else:
  * reads the fenced `sh` blocks of the runbook and picks ONE by its label (LABELS below: a label is a set of
    substrings that exactly one block must contain);
  * makes the textual substitutions a cloud rehearsal needs and records them:
        /ABSOLUTE/PATH/TO/vfport -> --study          (the one substitution the runbook itself asks for)
        $HOME                    -> --home           (this session may delete inside its scratch only, and the
                                                      runbook deletes its pilot folders)
        PID_FROM_THE_STATUS_LINE / NAME_FROM_THE_STATUS_LINE -> --pid / --name (as the runbook says)
  * starts `nice -n 10 <shell> -c <text>` in the folder `/` (a wrong folder on purpose), without a terminal,
    waits for it, and appends to --record one JSON line with the literal text, the complete output (stdout and
    stderr together), the exit status and the times;
  * three actions that are NOT runbook commands, marked as such in the record:
        --observe        a listing of every process whose command line holds the study path (pid, parent, command
                         cut at 220 characters): it shows the waiting shells, which the status command must not list
        --hard-kill PID  SIGKILL to the rehearsal's own vf-eval (the deliberate interruption the audit describes in
                         A2); refused unless the command line of PID begins with
                         <study>/.venv/bin/python <study>/.venv/bin/vf-eval
        --say TEXT       a note of the operator

It refuses to run unless PHYSIM2_DEV_MACHINE=cloud-container is set, the platform is Linux, and --study and
--home are both below --inside (the rehearsal's scratch folder). It is not for the Mac (RUNBOOK_MAC.md, rule 7).

usage (one command per call):
  PHYSIM2_DEV_MACHINE=cloud-container python3 -B rehearsal/issue.py --inside SCRATCH --runbook CLONE/.../RUNBOOK_MAC.md \
      --study CLONE/.../vfport --home SCRATCH/home --record SCRATCH/record.jsonl --label 2-status
"""
import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time

PLACE = "/ABSOLUTE/PATH/TO/vfport"
PILOT = "physim2-pilot-20261110"
# label -> substrings that the block must contain; a leading "!" means: must NOT contain
LABELS = {
    "0a-commit": ["git rev-parse HEAD"],
    "0b-pin": ["shasum -a 256 -c PIN.sha256"],
    "0c-docker-and-folders": ['grep -c "No such file"'],
    "1a-uv-dry-run": ["uv sync", "--dry-run"],
    "1b-mkdir-ca": [f'mkdir "$HOME/{PILOT}" &&', "extra-ca.crt"],
    "1c-uv-sync": ["nohup uv sync", "sync.log"],
    "1c-status": ["tail -n 3", "sync.log", "!nohup"],
    "1d-import": ["import verifiers, numpy, scipy, jax, physim2_env"],
    "1e-interpreter": ["INTERPRETER-OK"],
    "1f-build": ["nohup docker build"],
    "1f-status": ["tail -n 2", "build.log", "!nohup"],
    "1g-image-check": ["docker run --rm --network none"],
    "1h-make-instances": ["tools/make_instances.py"],
    "2-status": ['echo "status done"', "prove.log"],
    "2a-prove": ["tools/prove.py"],
    "2a-check": ["proof_mac.json'))"],
    "2b-probe": ["tools/check_probe.py"],
    "2b-report": ["probe_mac.json'))"],
    "2c-single": ["configs/scripted_ring.toml"],
    "2c-report": ["tools/run_report.py", "single/single-d"],
    "I2-stop": ["kill -TERM PID_FROM_THE_STATUS_LINE"],
    "I3-docker-rm": ["docker rm -f NAME_FROM_THE_STATUS_LINE"],
    "I6-reset": ["pilot folders reset"],
    "3-dry": ["qwen_ring_bash.toml", "--dry-run"],
    "3-paid": ["qwen_ring_bash.toml", "LEAD-GO-STEP3"],
    "3-status": ['echo "status done"', "qwen.log"],
    "3-report": ["tools/run_report.py", "qwen/qwen", "!total_hits"],
    "3-trace": ["tools/run_report.py", "total_hits"],
    "4a-copy-delete": [f"{PILOT}-results/\" && test -s"],
    "4b-docker": ["docker images --format"],
}
NEVER_HERE = ("1f-build", "3-paid", "3-dry", "3-status", "3-report", "3-trace")   # not rehearsed: see the record


def blocks(text):
    """The fenced sh blocks, each as one string (the same reading as tools/check_runbook.py)."""
    out, cur = [], None
    for line in text.splitlines():
        s = line.strip()
        if cur is None and s == "```sh":
            cur = []
        elif cur is not None and s == "```":
            out.append("\n".join(cur))
            cur = None
        elif cur is not None:
            cur.append(line.strip() if not cur else line)
    return out


def pick(text, label):
    want = LABELS[label]
    hits = [b for b in blocks(text) if all((w[1:] not in b) if w.startswith("!") else (w in b) for w in want)]
    if len(hits) != 1:
        raise SystemExit(f"label {label}: {len(hits)} blocks of the runbook match, expected exactly 1")
    return hits[0]


def utc():
    return time.strftime("%H:%M:%S", time.gmtime())


def ps_line(pid):
    r = subprocess.run(["ps", "-ww", "-p", str(pid), "-o", "command="], capture_output=True, text=True)
    return r.stdout.strip()


def append(record, entry):
    n = 0
    if os.path.exists(record):
        n = sum(1 for _ in open(record))
    entry = dict({"n": n}, **entry)
    with open(record, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inside", required=True, help="the rehearsal's scratch folder; --study and --home must be below it")
    ap.add_argument("--runbook", required=True)
    ap.add_argument("--study", required=True)
    ap.add_argument("--home", required=True)
    ap.add_argument("--record", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--label", choices=sorted(LABELS))
    g.add_argument("--list", action="store_true")
    g.add_argument("--observe", action="store_true")
    g.add_argument("--hard-kill", type=int, metavar="PID")
    g.add_argument("--say")
    ap.add_argument("--pid", type=int)
    ap.add_argument("--name")
    ap.add_argument("--shell", default="sh", choices=["sh", "bash"])
    ap.add_argument("--path-prefix", help="a folder put first on PATH for this one call (the IPv6 shim, step 2c on this kernel)")
    ap.add_argument("--env", action="append", default=[], metavar="K=V", help="a variable of the session for this one call")
    ap.add_argument("--timeout", type=float, default=600)
    ap.add_argument("--note", default="")
    ap.add_argument("--allow-unrehearsed", action="store_true")
    a = ap.parse_args()

    if os.environ.get("PHYSIM2_DEV_MACHINE") != "cloud-container" or sys.platform != "linux":
        raise SystemExit("refused: this tool issues runbook commands for the CLOUD rehearsal only "
                         "(PHYSIM2_DEV_MACHINE=cloud-container, Linux). It is not for the Mac.")
    inside, study, home = (os.path.realpath(p) for p in (a.inside, a.study, a.home))
    for p in (study, home, os.path.realpath(a.record)):
        if not p.startswith(inside + os.sep):
            raise SystemExit(f"refused: {p} is not below --inside {inside}")
    if study != a.study or home != a.home or not re.fullmatch(r"[A-Za-z0-9/._-]+", study):
        raise SystemExit("refused: --study and --home must be given as real absolute paths of plain characters")
    text = open(a.runbook).read()

    if a.list:
        for label in sorted(LABELS):
            want = LABELS[label]
            n = sum(all((w[1:] not in b) if w.startswith("!") else (w in b) for w in want) for b in blocks(text))
            print(f"{label:24s} {n} block(s)")
        return
    if a.say is not None:
        e = append(a.record, {"kind": "note of the operator (not a runbook command)", "utc": utc(), "note": a.say})
        print(json.dumps(e))
        return
    if a.observe:
        r = subprocess.run(["ps", "axww", "-o", "pid=", "-o", "ppid=", "-o", "command="], capture_output=True, text=True)
        me = str(os.getpid())
        rows = [ln[:220] for ln in r.stdout.splitlines() if study in ln and ln.split()[0] != me and "rehearsal/issue.py" not in ln]
        e = append(a.record, {"kind": "observation (not a runbook command)", "utc": utc(),
                              "what": "every process whose command line holds the study path: pid, parent pid, command (cut at 220 characters)",
                              "output": "\n".join(rows), "note": a.note})
        print("\n".join(rows))
        return
    if a.hard_kill is not None:
        line = ps_line(a.hard_kill)
        want = f"{study}/.venv/bin/python {study}/.venv/bin/vf-eval "
        if not line.startswith(want):
            raise SystemExit(f"refused: pid {a.hard_kill} is not the rehearsal's own vf-eval ({line[:120]!r})")
        os.kill(a.hard_kill, signal.SIGKILL)
        e = append(a.record, {"kind": "DELIBERATE INTERRUPTION (not a runbook command)", "utc": utc(),
                              "text": f"kill -KILL {a.hard_kill}", "target_command_line": line[:220], "note": a.note})
        print(json.dumps(e))
        return

    if a.label in NEVER_HERE and not a.allow_unrehearsed:
        raise SystemExit(f"refused: {a.label} is not rehearsed in the cloud container (the image build; step 3)")
    block = pick(text, a.label)
    subs = [[PLACE, study], ["$HOME", home]]
    cmd = block.replace(PLACE, study).replace("$HOME", home)
    if "PID_FROM_THE_STATUS_LINE" in cmd:
        if a.pid is None:
            raise SystemExit("this command needs --pid")
        cmd = cmd.replace("PID_FROM_THE_STATUS_LINE", str(a.pid))
        subs.append(["PID_FROM_THE_STATUS_LINE", str(a.pid)])
    if "NAME_FROM_THE_STATUS_LINE" in cmd:
        if not a.name or not re.fullmatch(r"vf-[0-9a-f]{32}", a.name):
            raise SystemExit("this command needs --name vf-<32 hex>, copied from the status output")
        cmd = cmd.replace("NAME_FROM_THE_STATUS_LINE", a.name)
        subs.append(["NAME_FROM_THE_STATUS_LINE", a.name])
    if "$HOME" in cmd or PLACE in cmd or "rm -rf" in cmd and f'rm -rf "{home}/{PILOT}/store" "{home}/{PILOT}/scratch"' not in cmd:
        raise SystemExit("refused: a placeholder is left, or an rm -rf that does not name the rehearsal's two pilot folders")
    env = dict(os.environ)
    session_env = {}
    for kv in a.env:
        k, _, v = kv.partition("=")
        env[k] = v
        session_env[k] = v
    if a.path_prefix:
        env["PATH"] = a.path_prefix + os.pathsep + env.get("PATH", "")
        session_env["PATH"] = a.path_prefix + ":<PATH of the session>"
    started, t0 = utc(), time.time()
    try:
        r = subprocess.run(["nice", "-n", "10", a.shell, "-c", cmd], cwd="/", env=env, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=a.timeout)
        out, code = r.stdout, r.returncode
    except subprocess.TimeoutExpired as ex:
        out, code = (ex.stdout or b"").decode(errors="replace") if isinstance(ex.stdout, bytes) else (ex.stdout or ""), "CUT after %.0f s" % a.timeout
    e = append(a.record, {"kind": "runbook command", "label": a.label, "issued_as": f"{a.shell} -c '<text>', started in /, no terminal",
                          "text": cmd, "substitutions": subs, "session_environment_added": session_env,
                          "started_utc": started, "seconds": round(time.time() - t0, 2), "exit": code, "output": out, "note": a.note})
    sys.stdout.write(out)
    print(f"[n={e['n']} {a.label} exit={code} {e['seconds']} s]")


if __name__ == "__main__":
    main()
