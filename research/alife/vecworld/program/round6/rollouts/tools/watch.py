"""watch -- look at a running rollout from a second shell without touching it, and keep a copy of submission/.

    <venv python> -B rollouts/tools/watch.py --label RUN_LABEL --store STORE --instance IID --out DIR --log LOGFILE

Every PERIOD seconds, until the rollout's log ends with an `EXIT` line and no container of the run is left, it
appends one JSON line to <out>/timeline.jsonl:

  containers   name and status of the containers that carry the label verifiers.run=RUN_LABEL (`docker ps`)
  lab          the counters of the newest laboratory record of the instance in the store (ticks, resets, nats,
               requests, rejected, validations, submissions, submitted): numbers and booleans only
  free_gib     free space of the home file system

and it copies /workspace/submission out of the first two long-lived boxes of the run (the agent's box, then the
verifier's box, which holds the frozen copy that is graded) with `docker cp NAME:/workspace/submission -`,
keeping the newest copy per box: <out>/<name>.submission.tar. verifiers keeps the frozen submission in memory
only, so this is the one way to have the folder after the run.

What it does NOT do: it starts nothing inside a box (no `docker exec`), sends no signal, removes nothing, and
reads no text the model wrote (not the rollout's log beyond its last 12 characters, not the trace). A copy is
cut at MAX_TAR bytes and then discarded, so a box that fills its folder cannot fill this machine's disk through
the watcher. The tar files are data: nothing in them is ever run on the host.
"""
import argparse
import json
import os
import subprocess
import time

PERIOD = 20.0
MIN_AGE = 12.0                                               # item boxes live a few seconds: not copied
MAX_TAR = 100 << 20
MAX_BOXES = 2


def sh(cmd, timeout=60):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout
    except (OSError, subprocess.TimeoutExpired):
        return 1, ""


def lab_counters(store, iid):
    d = os.path.join(store, iid, "hidden", "labs")
    try:
        labs = sorted((os.path.getmtime(os.path.join(d, n)), n) for n in os.listdir(d))
        s = json.load(open(os.path.join(d, labs[-1][1], "state.json")))
        out = {k: s.get(k) for k in ("ticks_used", "resets", "total_nats", "episodes")}
        out.update({k: s["state"].get(k) for k in ("requests", "rejected", "validations", "submissions", "submitted")})
        out["n_lab_records"] = len(labs)
        return out
    except Exception:
        return None


def copy_submission(name, out):
    tmp, dst = os.path.join(out, name + ".submission.tar.tmp"), os.path.join(out, name + ".submission.tar")
    try:
        with open(tmp, "wb") as f:
            p = subprocess.Popen(["docker", "cp", f"{name}:/workspace/submission", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            n = 0
            while True:
                b = p.stdout.read(1 << 20)
                if not b:
                    break
                n += len(b)
                if n > MAX_TAR:
                    p.kill()
                    break
                f.write(b)
            rc = p.wait()
        if rc == 0 and 0 < n <= MAX_TAR:
            os.replace(tmp, dst)
            return n
    except OSError:
        pass
    try:
        os.unlink(tmp)
    except OSError:
        pass
    return None


def main():
    ap = argparse.ArgumentParser()
    for k in ("label", "store", "instance", "out", "log"):
        ap.add_argument("--" + k, required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    first_seen, boxes, t0 = {}, [], time.time()
    while True:
        now = time.time()
        rc, txt = sh(["docker", "ps", "--filter", f"label=verifiers.run={a.label}", "--format", "{{.Names}}\t{{.Status}}"])
        live = [line.split("\t") for line in txt.splitlines() if "\t" in line]
        copied = {}
        for name, _ in live:
            first_seen.setdefault(name, now)
            if name not in boxes and len(boxes) < MAX_BOXES and now - first_seen[name] >= MIN_AGE:
                boxes.append(name)
            if name in boxes:
                copied[name] = copy_submission(name, a.out)
        try:
            with open(a.log, "rb") as f:
                f.seek(max(0, os.path.getsize(a.log) - 12))
                tail = f.read().decode("ascii", "replace").strip().splitlines()[-1:]
            ended = bool(tail) and tail[0].startswith("EXIT")
        except OSError:
            ended, tail = False, []
        st = os.statvfs(os.path.expanduser("~"))
        rec = {"t": round(now - t0, 1), "unix": round(now, 1), "docker_ok": rc == 0, "containers": [{"name": n, "status": s} for n, s in live],
               "boxes_copied": copied, "lab": lab_counters(a.store, a.instance), "free_gib": round(st.f_bavail * st.f_frsize / (1 << 30), 2),
               "log_ends_with_exit": tail[0] if ended else None}
        with open(os.path.join(a.out, "timeline.jsonl"), "a") as f:
            f.write(json.dumps(rec) + "\n")
        if ended and not live:
            break
        time.sleep(PERIOD)
    json.dump({"boxes_in_order": boxes, "first_seen_unix": first_seen}, open(os.path.join(a.out, "boxes.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
