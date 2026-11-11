"""issue4 -- issue ONE command of the round-4 RUNBOOK_MAC.md the way a session issues it, and keep a literal
record of it. The successor of rehearsal/issue3.py (round 3, kept as it was for its record).

Every command is issued as ONE `sh -c '<text of the fenced command>'`, the text taken from the runbook that is on
disk in the clone; nothing is ever written to a script file. As in round 3:

  * `$HOME` is NOT replaced in the text: the rehearsal's home folder (a folder of the scratch) is the variable
    HOME of every command, so the pilot folders of steps 1 and 2 and the folder of step 3 (`$HOME/physim2-rollouts`)
    are where the runbook's text puts them.
  * the command's environment is built from nothing, like a clean session: PATH, HOME, USER, LANG, and what the
    operator adds by name for that one call (--env K=V, or --inherit NAME for a value of this machine that the
    record must not hold: the proxy settings uv needs here, and in step 3 the model key, which reaches the one
    paid command BY ENVIRONMENT ONLY). The names are recorded, never an inherited value.
  * substitutions, each recorded:
        /ABSOLUTE/PATH/TO/vfport -> --study               (the one the runbook itself asks for)
        PID_FROM_THE_STATUS_LINE / NAME_FROM_THE_STATUS_LINE -> --pid / --name
        JOB_ID, SOURCE_COMMIT, CEILING_USD, GO_DATE -> --job / --source-commit / --ceiling / --go-date (step 3; each
                         is checked against the shape the runbook gives for it before it is put into the text)
        with --floor F:  `--disk-floor-gib 8` -> `--disk-floor-gib F`  and  `8388608` -> F GiB in kB
                         (this machine has about 2 GiB free for everyone; without --floor the runbook's own floor
                         of 8 GiB is used, which is how the refusal is rehearsed)
        with --run-label L:  the run label `physim2-pilot-20261110` -> L wherever it is a LABEL (VF_RUN_ID=, the
                         label filters, the label a removal compares), never where it is the name of a pilot
                         folder under $HOME. (New in round 4: other jobs run on this machine, and every role
                         labels its containers with its own run id.)
        with --build-arg-proxy:  in the image build of step 1 only, `docker build` ->
                         `docker build --network host --build-arg HTTPS_PROXY=... --build-arg EXTRA_CA_B64=...`
                         (this machine sits behind a TLS-intercepting proxy; docker/Dockerfile.ring names exactly
                         these two arguments for that case; the values are this machine's and are not recorded)
        with --fetch-from PREFIX:  in step 3a's second command only, `-B tools/check_request.py --fetch` ->
                         `-B rehearsal/fetch4.py --requests-prefix PREFIX --fetch`: the pinned tool is run with the
                         one constant that says where requests live in the repository changed in memory, because
                         a rehearsal request is never committed under a `requests/` folder (the Mac's runner
                         executes what appears there)
  * actions that are NOT runbook commands, marked as such in the record:
        --observe         every process whose command line holds the study path (pid, parent, command cut at 220)
        --hard-kill PID [--also-kill PID2]
                          SIGKILL to the rehearsal's own tool and/or vf-eval; refused unless each pid's command
                          line begins with <study>/.venv/bin/python -B tools/vfrun.py , ... -B tools/prove.py or
                          ... -B <study>/tools/vfeval.py @ . With --when-settled FILE N the kill waits (at most
                          --timeout seconds) until the spend log FILE of a model run holds at least N settled
                          calls and no call that was sent and not settled: a crash between two model calls
        --ballast-mb N    write N MiB of zeros to <inside>/ballast.bin (once; it is never removed by this tool):
                          how the disk watchdog is made to trip during a run
        --say TEXT        a note of the operator

It refuses to run unless PHYSIM2_DEV_MACHINE=cloud-container is set, the platform is Linux, the operator has
made the marker file <inside>/REHEARSAL-SCRATCH, and --study and --home are both below --inside. It is not for
the Mac (RUNBOOK_MAC.md, rule 8).

usage (one command per call):
  PHYSIM2_DEV_MACHINE=cloud-container python3 -B rehearsal/issue4.py --inside SCRATCH --runbook CLONE/.../RUNBOOK_MAC.md \
      --study CLONE/.../vfport --home SCRATCH/home --record SCRATCH/record.jsonl --floor 1.2 --run-label L --label 2-status
"""
import argparse
import base64
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
    "0a-commit": ["git rev-parse HEAD", "TREE-LISTED"],
    "0b-pin": ["shasum -a 256 -c PIN.sha256"],
    "0c-session": ["env | cut -d= -f1 | awk", "docker context show"],
    "0d-docker-and-folders": ['echo "NO-PILOT-FOLDERS"'],
    "0e-disk": ["DISK-OK"],
    "1a-uv-dry-run": ["uv sync", "--dry-run"],
    "1b-mkdir": [f'mkdir -m 700 "$HOME/{PILOT}" &&', "PILOT-FOLDER-MADE"],
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
    "I8-close": ["--stage close"],
    "3.0-folder": ["ROLLOUTS-FOLDER-MADE"],
    "3.0-go": ["physim2-lead-go/v1"],
    "3a-git-fetch": ["git fetch origin", "FETCH_HEAD"],
    "3a-fetch": ["tools/check_request.py --fetch"],
    "3b-check": ["tools/check_request.py --request", "--prices"],
    "3c-instance": ["--stage instance"],
    "3d-reference": ["--stage reference"],
    "3-status": ['echo "status done"', "reference.log"],
    "3e-dry-run": ["--stage dry-run"],
    "3-paid": ["--stage rollout", "--model-credentials prime"],
    "3g-report": ["tools/run_report.py", "physim2-rollouts/store"],
    "3h-pack": ["tools/pack_rollout.py"],
    "4a-copy-delete": [f"{PILOT}-results/\" && test -s"],
    "4b-docker": ["docker system df"],
}
# the one command of the runbook that is not in a fence (step 3g, the settling of a run without a reward)
INLINE = {"3g-settle": "tools/settle.py --store"}
RM = f'rm -rf "$HOME/{PILOT}/store" "$HOME/{PILOT}/scratch"'
SHAPES = {"JOB_ID": r"[a-z0-9][a-z0-9-]{2,62}", "SOURCE_COMMIT": r"[0-9a-f]{40}", "CEILING_USD": r"[0-9]+(\.[0-9]+)?",
          "GO_DATE": r"[0-9]{4}-[0-9]{2}-[0-9]{2}"}
OWN = ("-B tools/vfrun.py ", "-B tools/prove.py ", "-B tools/check_probe.py ")


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


def inline(text, needle):
    """A command the runbook prints in backticks on one line (it must start with the guard)."""
    hits = [m for m in re.findall(r"`(cd \"/ABSOLUTE/PATH/TO/vfport\" && [^`\n]+)`", text) if needle in m]
    return hits


def matches(block, want):
    return all((w[1:] not in block) if w.startswith("!") else (w in block) for w in want)


def pick(text, label):
    hits = inline(text, INLINE[label]) if label in INLINE else [b for b in blocks(text) if matches(b, LABELS[label])]
    if len(hits) != 1:
        raise SystemExit(f"label {label}: {len(hits)} commands of the runbook match, expected exactly 1")
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


def settled_state(path):
    """(settled calls, calls sent and not settled) of a spend log; numbers only are read."""
    sent, settled = set(), set()
    try:
        for line in open(path):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("event") == "sent":
                sent.add(r.get("n"))
            elif r.get("event") == "settled":
                settled.add(r.get("n"))
    except OSError:
        return 0, 0
    return len(settled), len(sent - settled)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inside", required=True, help="the rehearsal's scratch folder; --study, --home and --record must be below it")
    ap.add_argument("--runbook", required=True)
    ap.add_argument("--study", required=True)
    ap.add_argument("--home", required=True)
    ap.add_argument("--record", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--label", choices=sorted(list(LABELS) + list(INLINE)))
    g.add_argument("--list", action="store_true")
    g.add_argument("--observe", action="store_true")
    g.add_argument("--hard-kill", type=int, metavar="PID")
    g.add_argument("--ballast-mb", type=int)
    g.add_argument("--say")
    ap.add_argument("--also-kill", type=int, metavar="PID2")
    ap.add_argument("--when-settled", nargs=2, metavar=("SPEND_LOG", "N"))
    ap.add_argument("--pid", type=int)
    ap.add_argument("--name")
    ap.add_argument("--job")
    ap.add_argument("--source-commit")
    ap.add_argument("--ceiling")
    ap.add_argument("--go-date")
    ap.add_argument("--floor", type=float, help="GiB: replaces the runbook's floor of 8 GiB in this one command")
    ap.add_argument("--run-label", help="this machine's own run label in place of the runbook's, where it is a label")
    ap.add_argument("--build-arg-proxy", action="store_true")
    ap.add_argument("--fetch-from", metavar="PREFIX", help="repository folder of the rehearsal requests (step 3a only)")
    ap.add_argument("--shell", default="sh", choices=["sh", "bash"])
    ap.add_argument("--env", action="append", default=[], metavar="K=V", help="a variable of the session for this one call (recorded with its value)")
    ap.add_argument("--inherit", action="append", default=[], metavar="NAME", help="a variable of THIS machine for this one call (only its name is recorded)")
    ap.add_argument("--timeout", type=float, default=600)
    ap.add_argument("--note", default="")
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
        for label in sorted(INLINE):
            print(f"{label:24s} {len(inline(text, INLINE[label]))} inline command(s)")
        print(f"{len(blocks(text))} fenced blocks; without a label: "
              f"{sum(1 for b in blocks(text) if not any(matches(b, w) for w in LABELS.values()))}")
        return
    if a.say is not None:
        print(json.dumps(append(a.record, {"kind": "note of the operator (not a runbook command)", "utc": utc(), "note": a.say})))
        return
    if a.observe:
        r = subprocess.run(["ps", "axww", "-o", "pid=", "-o", "ppid=", "-o", "command="], capture_output=True, text=True)
        me = str(os.getpid())
        rows = [ln[:220] for ln in r.stdout.splitlines() if study in ln and ln.split()[0] != me and "rehearsal/issue4.py" not in ln]
        append(a.record, {"kind": "observation (not a runbook command)", "utc": utc(),
                          "what": "every process whose command line holds the study path: pid, parent pid, command (cut at 220 characters)",
                          "output": "\n".join(rows), "note": a.note})
        print("\n".join(rows))
        return
    if a.hard_kill is not None:
        py = f"{study}/.venv/bin/python "
        want = tuple(py + w for w in OWN) + (f"{py}-B {study}/tools/vfeval.py @ ",)
        pids = [a.hard_kill] + ([a.also_kill] if a.also_kill is not None else [])
        lines = {p: ps_line(p) for p in pids}
        for p, line in lines.items():
            if not line.startswith(want):
                raise SystemExit(f"refused: pid {p} is not the rehearsal's own tool or vf-eval ({line[:120]!r})")
        waited = None
        if a.when_settled:
            log = os.path.realpath(a.when_settled[0])
            if not log.startswith(home + os.sep):
                raise SystemExit("refused: the spend log is not below --home")
            n_want, t0 = int(a.when_settled[1]), time.time()
            while True:
                n, hanging = settled_state(log)
                if n >= n_want and hanging == 0:
                    break
                if time.time() - t0 > a.timeout:
                    raise SystemExit(f"gave up after {a.timeout:.0f} s: {n} settled calls, {hanging} sent and not settled; nothing was signalled")
                time.sleep(0.02)
            waited = {"seconds": round(time.time() - t0, 2), "settled_calls_at_the_kill": n, "sent_and_not_settled": hanging}
        for p in pids:                                       # the tool first, so that it cannot write its closing row
            os.kill(p, signal.SIGKILL)
        after = settled_state(os.path.realpath(a.when_settled[0])) if a.when_settled else None
        print(json.dumps(append(a.record, {"kind": "DELIBERATE INTERRUPTION (not a runbook command)", "utc": utc(),
                                           "text": " ; ".join(f"kill -KILL {p}" for p in pids),
                                           "target_command_lines": [lines[p][:220] for p in pids], "waited_for_a_moment_between_two_model_calls": waited,
                                           "spend_log_right_after": None if after is None else {"settled": after[0], "sent_and_not_settled": after[1]},
                                           "note": a.note})))
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

    block = pick(text, a.label)
    subs = [[PLACE, study]]
    cmd = block.replace(PLACE, study)
    if "PID_FROM_THE_STATUS_LINE" in cmd:
        if a.pid is None:
            raise SystemExit("this command needs --pid")
        cmd = cmd.replace("PID_FROM_THE_STATUS_LINE", str(a.pid))
        subs.append(["PID_FROM_THE_STATUS_LINE", str(a.pid)])
    if "NAME_FROM_THE_STATUS_LINE" in cmd:
        if not a.name or not re.fullmatch(r"vf-[0-9a-f]{32}|[a-z]+_[a-z]+", a.name):
            raise SystemExit("this command needs --name vf-<32 hex> (or two lower-case words joined by _), copied from the status output")
        cmd = cmd.replace("NAME_FROM_THE_STATUS_LINE", a.name)
        subs.append(["NAME_FROM_THE_STATUS_LINE", a.name])
    for place, value in (("JOB_ID", a.job), ("SOURCE_COMMIT", a.source_commit), ("CEILING_USD", a.ceiling), ("GO_DATE", a.go_date)):
        if place in cmd:
            if value is None or not re.fullmatch(SHAPES[place], value):
                raise SystemExit(f"this command needs a value for {place} of the shape the runbook gives ({SHAPES[place]})")
            cmd = cmd.replace(place, value)
            subs.append([place, value])
    if a.floor is not None:
        if not 0.25 <= a.floor < 8:
            raise SystemExit("--floor must be from 0.25 to below 8")
        for old, new in (("--disk-floor-gib 8", f"--disk-floor-gib {a.floor:g}"), ("8388608", str(int(a.floor * 1048576)))):
            if old in cmd:
                cmd = cmd.replace(old, new)
                subs.append([old, new])
    if a.run_label:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{2,40}", a.run_label):
            raise SystemExit("--run-label must be lower-case letters, digits and hyphens")
        new, n = re.subn(r"(?<!\$HOME/)" + re.escape(PILOT) + r"(?!-results)", a.run_label, cmd)
        if n:
            cmd = new
            subs.append([f"{PILOT} (as a run label, {n} time(s); never as a folder name under $HOME)", a.run_label])
    added = {}
    if a.build_arg_proxy:
        if a.label != "1f-build" or cmd.count("docker build -f") != 1:
            raise SystemExit("--build-arg-proxy is for the image build of step 1 only")
        ca = "/root/.ccr/agent-proxy-ca.crt"
        proxy = os.environ.get("HTTPS_PROXY", "")
        if not proxy or not os.path.isfile(ca):
            raise SystemExit("refused: this machine has no HTTPS_PROXY or no proxy CA file")
        cmd = cmd.replace("docker build -f", 'docker build --network host --build-arg HTTPS_PROXY="$REHEARSAL_PROXY" --build-arg EXTRA_CA_B64="$REHEARSAL_CA_B64" -f')
        subs.append(["docker build -f", 'docker build --network host --build-arg HTTPS_PROXY="$REHEARSAL_PROXY" --build-arg EXTRA_CA_B64="$REHEARSAL_CA_B64" -f'])
        added.update(REHEARSAL_PROXY="<the value of this machine; not recorded>", REHEARSAL_CA_B64="<base64 of this machine's proxy CA certificate; not recorded>")
    if a.fetch_from:
        if a.label != "3a-fetch" or not re.fullmatch(r"research/[A-Za-z0-9/._-]+/", a.fetch_from) or "/requests/" in "/" + a.fetch_from:
            raise SystemExit("--fetch-from is for step 3a's second command only, and names a repository folder that is no `requests/` folder")
        old, new = "-B tools/check_request.py --fetch", f"-B rehearsal/fetch4.py --requests-prefix {a.fetch_from} --fetch"
        if cmd.count(old) != 1:
            raise SystemExit("refused: the fetch command has another shape")
        cmd = cmd.replace(old, new)
        subs.append([old, new])
    left = [p for p in (PLACE, "PID_FROM_THE_STATUS_LINE", "NAME_FROM_THE_STATUS_LINE", *SHAPES) if p in cmd]
    if left or "rm -rf" in cmd and (cmd.count("rm -rf") != 1 or RM not in cmd):
        raise SystemExit(f"refused: a placeholder is left ({left}), or an rm -rf that does not name the two pilot folders of $HOME")
    env = {"PATH": os.environ["PATH"], "HOME": home, "USER": "rehearsal", "LANG": "C.UTF-8"}
    if a.build_arg_proxy:
        env["REHEARSAL_PROXY"] = os.environ["HTTPS_PROXY"]
        env["REHEARSAL_CA_B64"] = base64.b64encode(open("/root/.ccr/agent-proxy-ca.crt", "rb").read()).decode()
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
    # an inherited value must never reach the record: the output of every command is searched for each of them
    leaked = sorted(k for k in a.inherit if os.environ.get(k) and len(os.environ[k]) >= 8 and os.environ[k] in (out + cmd))
    if leaked:
        out = "<output withheld: it held the value of " + ", ".join(leaked) + ">"
    e = append(a.record, {"kind": "runbook command", "label": a.label, "issued_as": f"{a.shell} -c '<text>', started in /, no terminal",
                          "text": cmd, "substitutions": subs, "session_environment": sorted(env), "session_environment_added": added,
                          "started_utc": started, "seconds": round(time.time() - t0, 2), "exit": code, "output": out, "note": a.note})
    sys.stdout.write(out)
    print(f"[n={e['n']} {a.label} exit={code} {e['seconds']} s]")


if __name__ == "__main__":
    main()
