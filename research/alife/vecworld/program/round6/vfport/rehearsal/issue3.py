"""issue3 -- issue ONE command of the round-3 RUNBOOK_MAC.md the way a session issues it, and keep a literal
record of it. The successor of rehearsal/issue.py (round 2, kept as it was for its record).

Every command is issued as ONE `sh -c '<text of the fenced command>'`, the text taken from the runbook that is on
disk in the clone; nothing is ever written to a script file. What differs from round 2:

  * `$HOME` is NOT replaced in the text. The rehearsal's home folder is given to the command as the variable HOME,
    so the text that runs is the runbook's text byte for byte except for the substitutions below. That folder
    holds a made-up `.prime/config.json`, which an inotify watcher of the rehearsal observes (finding M3).
  * the command's environment is built from nothing, like a clean session: PATH, HOME, USER, LANG, and what the
    operator adds by name for that one call (--env K=V, or --inherit NAME for a value of this machine that the
    record must not hold: the proxy settings uv needs here). The names are recorded, never an inherited value.
  * substitutions, each recorded:
        /ABSOLUTE/PATH/TO/vfport -> --study               (the one the runbook itself asks for)
        PID_FROM_THE_STATUS_LINE / NAME_FROM_THE_STATUS_LINE -> --pid / --name
        with --floor F:  `--disk-floor-gib 8` -> `--disk-floor-gib F`  and  `8388608` -> F GiB in kB
                         (this machine has 2 GiB free for everyone; without --floor the runbook's own floor of
                         8 GiB is used, which is how the refusal is rehearsed)
  * actions that are NOT runbook commands, marked as such in the record:
        --observe         every process whose command line holds the study path (pid, parent, command cut at 220)
        --hard-kill PID   SIGKILL to the rehearsal's own vf-eval; refused unless the command line of PID begins
                          with <study>/.venv/bin/python -B <study>/tools/vfeval.py @
        --ballast-mb N    write N MiB of zeros to <inside>/ballast.bin (once; it is never removed by this tool):
                          how the disk watchdog is made to trip during a run
        --say TEXT        a note of the operator

It refuses to run unless PHYSIM2_DEV_MACHINE=cloud-container is set, the platform is Linux, the operator has
made the marker file <inside>/REHEARSAL-SCRATCH, and --study and --home are both below --inside. It is not for
the Mac (RUNBOOK_MAC.md, rule 8).

usage (one command per call):
  PHYSIM2_DEV_MACHINE=cloud-container python3 -B rehearsal/issue3.py --inside SCRATCH --runbook CLONE/.../RUNBOOK_MAC.md \
      --study CLONE/.../vfport --home SCRATCH/home --record SCRATCH/record.jsonl --floor 0.5 --label 2-status
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
    "0c-session": ["env | cut -d= -f1 | awk", "docker context show"],
    "0d-docker-and-folders": ['echo "NO-PILOT-FOLDERS"'],
    "0e-disk": ["DISK-OK"],
    "1a-uv-dry-run": ["uv sync", "--dry-run"],
    "1b-mkdir-ca": [f'mkdir -m 700 "$HOME/{PILOT}" &&', "extra-ca.crt"],
    "1c-uv-sync": ["nohup uv sync", "sync.log"],
    "1c-status": ["tail -n 3", "sync.log", "!nohup"],
    "1d-import": ["import physim2_env, physim2_script, verifiers, numpy, scipy, jax"],
    "1e-interpreter": ["INTERPRETER-OK"],
    "1f-build": ["nohup docker build"],
    "1f-status": ["tail -n 2", "build.log", "!nohup"],
    "1g-image-check": ["docker run --rm --network none"],
    "1h-make-instances": ['-B tools/make_instances.py --store'],
    "2-quiet": ['echo "RUNNING-LISTED"'],
    "2-status": ['echo "status done"', "prove.log"],
    "2a-prove": ['-B tools/prove.py --store'],
    "2a-check": ["proof_mac.json'))"],
    "2b-probe": ['-B tools/check_probe.py --store'],
    "2b-report": ["probe_mac.json'))"],
    "2c-single": ["--config configs/scripted_ring.toml"],
    "2c-report": ["tools/run_report.py", "single/single-d"],
    "I2-stop": ["kill -TERM PID_FROM_THE_STATUS_LINE"],
    "I3-docker-rm": ["docker rm -f NAME_FROM_THE_STATUS_LINE"],
    "I6-reset": ["pilot folders reset"],
    "3-dry": ["qwen_ring_bash.toml", "--dry-run"],
    "3-paid": ["qwen_ring_bash.toml", "--model-credentials prime"],
    "3-status": ['echo "status done"', "qwen.log"],
    "3-report": ["tools/run_report.py", "qwen/qwen", "!total_hits"],
    "3-trace": ["tools/run_report.py", "total_hits"],
    "4a-copy-delete": [f"{PILOT}-results/\" && test -s"],
    "4b-docker": ["docker system df"],
}
NEVER_HERE = ("1f-build", "1f-status", "3-paid", "3-dry", "3-status", "3-report", "3-trace")   # not rehearsed: see the record
RM = f'rm -rf "$HOME/{PILOT}/store" "$HOME/{PILOT}/scratch"'


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


def matches(block, want):
    return all((w[1:] not in block) if w.startswith("!") else (w in block) for w in want)


def pick(text, label):
    hits = [b for b in blocks(text) if matches(b, LABELS[label])]
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
    ap.add_argument("--inside", required=True, help="the rehearsal's scratch folder; --study, --home and --record must be below it")
    ap.add_argument("--runbook", required=True)
    ap.add_argument("--study", required=True)
    ap.add_argument("--home", required=True)
    ap.add_argument("--record", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--label", choices=sorted(LABELS))
    g.add_argument("--list", action="store_true")
    g.add_argument("--observe", action="store_true")
    g.add_argument("--hard-kill", type=int, metavar="PID")
    g.add_argument("--ballast-mb", type=int)
    g.add_argument("--say")
    ap.add_argument("--pid", type=int)
    ap.add_argument("--name")
    ap.add_argument("--floor", type=float, help="GiB: replaces the runbook's floor of 8 GiB in this one command")
    ap.add_argument("--shell", default="sh", choices=["sh", "bash"])
    ap.add_argument("--env", action="append", default=[], metavar="K=V", help="a variable of the session for this one call (recorded with its value)")
    ap.add_argument("--inherit", action="append", default=[], metavar="NAME", help="a variable of THIS machine for this one call (only its name is recorded)")
    ap.add_argument("--timeout", type=float, default=600)
    ap.add_argument("--note", default="")
    ap.add_argument("--allow-unrehearsed", action="store_true")
    a = ap.parse_args()

    if os.environ.get("PHYSIM2_DEV_MACHINE") != "cloud-container" or sys.platform != "linux":
        raise SystemExit("refused: this tool issues runbook commands for the CLOUD rehearsal only "
                         "(PHYSIM2_DEV_MACHINE=cloud-container, Linux). It is not for the Mac.")
    inside, study, home = (os.path.realpath(p) for p in (a.inside, a.study, a.home))
    if not os.path.isfile(os.path.join(inside, "REHEARSAL-SCRATCH")):
        raise SystemExit(f"refused: {inside} holds no marker file REHEARSAL-SCRATCH (the operator makes it by hand in the rehearsal's own scratch folder)")
    for p in (study, home, os.path.realpath(a.record)):
        if not p.startswith(inside + os.sep):
            raise SystemExit(f"refused: {p} is not below --inside {inside}")
    if study != a.study or home != a.home or not re.fullmatch(r"[A-Za-z0-9/._-]+", study):
        raise SystemExit("refused: --study and --home must be given as real absolute paths of plain characters")
    text = open(a.runbook).read()

    if a.list:
        for label in sorted(LABELS):
            print(f"{label:24s} {sum(matches(b, LABELS[label]) for b in blocks(text))} block(s)")
        print(f"{len(blocks(text))} fenced blocks; without a label: "
              f"{sum(1 for b in blocks(text) if not any(matches(b, w) for w in LABELS.values()))}")
        return
    if a.say is not None:
        print(json.dumps(append(a.record, {"kind": "note of the operator (not a runbook command)", "utc": utc(), "note": a.say})))
        return
    if a.observe:
        r = subprocess.run(["ps", "axww", "-o", "pid=", "-o", "ppid=", "-o", "command="], capture_output=True, text=True)
        me = str(os.getpid())
        rows = [ln[:220] for ln in r.stdout.splitlines() if study in ln and ln.split()[0] != me and "rehearsal/issue3.py" not in ln]
        append(a.record, {"kind": "observation (not a runbook command)", "utc": utc(),
                          "what": "every process whose command line holds the study path: pid, parent pid, command (cut at 220 characters)",
                          "output": "\n".join(rows), "note": a.note})
        print("\n".join(rows))
        return
    if a.hard_kill is not None:
        line = ps_line(a.hard_kill)
        want = f"{study}/.venv/bin/python -B {study}/tools/vfeval.py @ "
        if not line.startswith(want):
            raise SystemExit(f"refused: pid {a.hard_kill} is not the rehearsal's own vf-eval ({line[:120]!r})")
        os.kill(a.hard_kill, signal.SIGKILL)
        print(json.dumps(append(a.record, {"kind": "DELIBERATE INTERRUPTION (not a runbook command)", "utc": utc(),
                                           "text": f"kill -KILL {a.hard_kill}", "target_command_line": line[:220], "note": a.note})))
        return
    if a.ballast_mb is not None:
        path = os.path.join(inside, "ballast.bin")
        if os.path.lexists(path) or not 1 <= a.ballast_mb <= 64:
            raise SystemExit("refused: the ballast file exists already, or the size is not 1 to 64 MiB")
        before = os.statvfs(home).f_bavail * os.statvfs(home).f_frsize
        with open(path, "wb") as f:
            for _ in range(a.ballast_mb):
                f.write(b"\0" * (1 << 20))
            f.flush()
            os.fsync(f.fileno())
        after = os.statvfs(home).f_bavail * os.statvfs(home).f_frsize
        print(json.dumps(append(a.record, {"kind": "DELIBERATE DISK USE (not a runbook command)", "utc": utc(),
                                           "text": f"{a.ballast_mb} MiB of zeros written to <inside>/ballast.bin",
                                           "free_bytes_before": before, "free_bytes_after": after, "note": a.note})))
        return

    if a.label in NEVER_HERE and not a.allow_unrehearsed:
        raise SystemExit(f"refused: {a.label} is not rehearsed in the cloud container (the image build; step 3)")
    block = pick(text, a.label)
    subs = [[PLACE, study]]
    cmd = block.replace(PLACE, study)
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
    if a.floor is not None:
        if not 0.25 <= a.floor < 8:
            raise SystemExit("--floor must be from 0.25 to below 8")
        for old, new in (("--disk-floor-gib 8", f"--disk-floor-gib {a.floor:g}"), ("8388608", str(int(a.floor * 1048576)))):
            if old in cmd:
                cmd = cmd.replace(old, new)
                subs.append([old, new])
    if PLACE in cmd or "rm -rf" in cmd and (cmd.count("rm -rf") != 1 or RM not in cmd):
        raise SystemExit("refused: a placeholder is left, or an rm -rf that does not name the two pilot folders of $HOME")
    env = {"PATH": os.environ["PATH"], "HOME": home, "USER": "rehearsal", "LANG": "C.UTF-8"}
    added = {}
    for kv in a.env:
        k, _, v = kv.partition("=")
        env[k] = v
        added[k] = v
    for k in a.inherit:
        if k in os.environ:
            env[k] = os.environ[k]
            added[k] = "<the value of this machine; not recorded>"
    started, t0 = utc(), time.time()
    try:
        r = subprocess.run(["nice", "-n", "10", a.shell, "-c", cmd], cwd="/", env=env, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=a.timeout)
        out, code = r.stdout, r.returncode
    except subprocess.TimeoutExpired as ex:
        out, code = (ex.stdout or b"").decode(errors="replace") if isinstance(ex.stdout, bytes) else (ex.stdout or ""), "CUT after %.0f s" % a.timeout
    e = append(a.record, {"kind": "runbook command", "label": a.label, "issued_as": f"{a.shell} -c '<text>', started in /, no terminal",
                          "text": cmd, "substitutions": subs, "session_environment": sorted(env), "session_environment_added": added,
                          "started_utc": started, "seconds": round(time.time() - t0, 2), "exit": code, "output": out, "note": a.note})
    sys.stdout.write(out)
    print(f"[n={e['n']} {a.label} exit={code} {e['seconds']} s]")


if __name__ == "__main__":
    main()
