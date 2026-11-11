"""probe_caps -- what the box caps of round 4 look like FROM INSIDE a box, when each one is hit.

A scripted test agent for the agent's box (physim2-script harness; tools/check_step3.py starts it). It runs into
every cap on purpose and writes what it saw to /workspace/caps_report.json: the read-only root, the two
memory-backed places, the process limit and the memory limit. It submits nothing: the rollout is then graded on
the baseline predictor the box started with.

IT FILLS MEMORY AND STARTS HUNDREDS OF THREADS. In a box that is the point (the box is capped and thrown away);
on a real machine it would not be. The first statement below therefore refuses to do anything unless this
process is inside a box that the environment prepared: the same gate as agents/hostile_submission.py
(host-safety audit, change 3).
"""
import errno
import json
import os
import stat
import sys


def _in_prepared_box() -> bool:
    try:
        d, f = os.lstat("/etc/physim2"), os.lstat("/etc/physim2/predictor_uid")
    except OSError:
        return False
    return (os.path.exists("/.dockerenv") and stat.S_ISDIR(d.st_mode) and stat.S_ISREG(f.st_mode) and d.st_uid == 0 and f.st_uid == 0
            and not f.st_mode & 0o022)


if not _in_prepared_box():
    sys.exit("refused: probe_caps.py runs only inside a box prepared by the PhySim v2 environment "
             "(/.dockerenv and a root-owned /etc/physim2/predictor_uid); it fills memory and starts threads until it is stopped")

import subprocess  # noqa: E402
import threading  # noqa: E402
import time  # noqa: E402

MIB = 1 << 20
REPORT = "/workspace/caps_report.json"


def first(*paths):
    for p in paths:
        try:
            with open(p) as f:
                return f.read().strip()
        except OSError:
            continue
    return None


def try_write(path: str) -> str:
    try:
        with open(path, "w") as f:
            f.write("x")
    except OSError as e:
        return errno.errorcode.get(e.errno, str(e.errno)) + ": " + os.strerror(e.errno)
    os.unlink(path)                                          # this script's own one-byte file, in a box
    return "written"


def fill(path: str, limit_mib: int) -> dict:
    """Write 1 MiB blocks into one file until the file system refuses; then remove the file."""
    block, n, err = b"\0" * MIB, 0, None
    try:
        with open(path, "wb") as f:
            while n < limit_mib:
                f.write(block)
                f.flush()
                n += 1
    except OSError as e:
        err = errno.errorcode.get(e.errno, str(e.errno)) + ": " + os.strerror(e.errno)
    try:
        os.unlink(path)
    except OSError:
        pass
    return {"mib_written": n, "error": err}


def threads_until_refused(limit: int = 4000) -> dict:
    stop, made, err = threading.Event(), [], None
    try:
        for _ in range(limit):
            t = threading.Thread(target=stop.wait, daemon=True)
            t.start()
            made.append(t)
    except RuntimeError as e:
        err = str(e)
    stop.set()
    for t in made:
        t.join()
    return {"threads_started": len(made), "error": err}


def memory_until_killed() -> dict:
    """A CHILD allocates and touches memory in 64 MiB steps until the kernel stops it; this process only watches."""
    code = ("import sys\nblocks = []\nn = 0\n"
            "while n < 16384:\n    b = bytearray(64 << 20)\n    b[::4096] = b'x' * len(b[::4096])\n    blocks.append(b)\n    n += 64\n"
            "    sys.stdout.write(str(n) + '\\n'); sys.stdout.flush()\n")
    p = subprocess.Popen([sys.executable, "-B", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    lines = [x for x in out.split() if x.isdigit()]
    return {"returncode": p.returncode, "mib_reached": int(lines[-1]) if lines else 0, "stderr_last_line": (err.strip().splitlines() or [""])[-1][:200],
            "shell_would_print": "Killed" if p.returncode == -9 else None}


def main() -> int:
    rep = {"uid": os.getuid(), "time": time.time()}
    rep["limits_seen"] = {
        "pids_max": first("/sys/fs/cgroup/pids.max", "/sys/fs/cgroup/pids/pids.max"),
        "memory_max": first("/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"),
        "swap_max": first("/sys/fs/cgroup/memory.swap.max", "/sys/fs/cgroup/memory/memory.memsw.limit_in_bytes"),
        "cpu_max": first("/sys/fs/cgroup/cpu.max") or (first("/sys/fs/cgroup/cpu/cpu.cfs_quota_us") or "?") + " " + (first("/sys/fs/cgroup/cpu/cpu.cfs_period_us") or "?"),
        "nproc": os.cpu_count()}
    mounts = {}
    with open("/proc/self/mountinfo") as f:
        for line in f:
            p = line.split(" ")
            sep = p.index("-", 6)
            if p[4] in ("/", "/workspace", "/tmp", "/etc/physim2", "/runtime", "/dev/shm"):
                mounts[p[4]] = {"type": p[sep + 1], "options": p[5], "super": p[sep + 3].strip()}
    rep["mounts"] = mounts
    rep["write_one_byte"] = {p: try_write(os.path.join(p, f"physim2-caps-probe-{os.getpid()}"))
                             for p in ("/root", "/usr", "/etc", "/opt", "/var/tmp", "/home", "/", "/workspace", "/tmp", "/dev/shm", "/etc/physim2", "/runtime")}
    rep["home"] = {"HOME": os.environ.get("HOME"), "expanduser": os.path.expanduser("~")}
    rep["fill_tmp"] = fill("/tmp/physim2-caps-probe.bin", 4096)
    rep["fill_workspace"] = fill("/workspace/physim2-caps-probe.bin", 4096)
    rep["fill_shm"] = fill("/dev/shm/physim2-caps-probe.bin", 4096)
    rep["threads"] = threads_until_refused()
    try:
        r = subprocess.run(["sh", "-c", "for i in $(seq 1 700); do sleep 20 & done 2>&1 | tail -n 1; wait"], capture_output=True, text=True, timeout=120)
        rep["fork_in_a_shell"] = {"last_line": (r.stdout.strip().splitlines() or [""])[-1][:200], "stderr_last_line": (r.stderr.strip().splitlines() or [""])[-1][:200]}
    except Exception as e:
        rep["fork_in_a_shell"] = {"error": type(e).__name__}
    rep["memory"] = memory_until_killed()
    rep["after"] = {"still_running": True, "write_workspace": try_write("/workspace/physim2-caps-probe-after")}
    with open(REPORT, "w") as f:
        json.dump(rep, f, indent=1)
    print(json.dumps({k: rep[k] for k in ("limits_seen", "fill_tmp", "fill_workspace", "threads", "memory")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
