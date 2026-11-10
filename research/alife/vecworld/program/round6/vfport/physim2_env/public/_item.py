"""physim2._item -- run ONE predictor request in this box as an unprivileged user, then leave the box clean.

Public and trusted: the same file runs in the grader's box (as /runtime/item.py, started by root once per exam
item) and in your own box when you call `lab.validate(...)`. It is the port of PhySim v1's predictor launcher
and worker (v1: physim/runtime_sandbox.py:156-179, physim/container_worker.py:14-19) with one addition: after
every request, root kills every process of the unprivileged user and deletes everything that user owns, so a
predictor cannot leave a file, a shared-memory segment or a background process for the next item.

    python -I -B _item.py --submission DIR --runner physim2/predict_runner.py --request request.npz \
        --cpu 30 --wall 60 --mem-gib 4 [--uid 1000] [--file-mib 256] [--max-reply-mib 64] [--no-cleanup]
    python -I -B _item.py --scan          (once per box, before the first request)

Prints one JSON line:
    ok, returncode, timed_out, cpu_s, wall_s, why, stderr (tail), reply_b64 (the reply .npz when ok),
    layers {uid, rlimits}, cleanup {killed, removed, ipc_removed, left_pids, left_files, roots}

Layers: resource limits always (CPU seconds hard = soft, address space, file size, no core dumps, process
count); when started as root also a drop to --uid with no supplementary groups, and the cleanup. Without root
(your own tests) the request still runs, without the drop and without the cleanup. The network policy and the
absence of hidden files are properties of the box, not of this file.
"""
import argparse
import base64
import json
import os
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
import time

GIB = 1024 ** 3
SKIP_FS = {"proc", "sysfs", "devpts", "cgroup", "cgroup2", "securityfs", "debugfs", "tracefs", "pstore", "bpf",
           "configfs", "fusectl", "binfmt_misc", "autofs", "hugetlbfs", "nsfs", "rpc_pipefs"}
ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/tmp", "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1",
       "MKL_NUM_THREADS": "1", "PYTHONDONTWRITEBYTECODE": "1", "JAX_PLATFORMS": "cpu",
       "XLA_FLAGS": "--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"}


# ----------------------------------------------------------------------------- cleanup (root only)
def _uids(pid):
    try:
        with open(f"/proc/{pid}/status") as f:
            for line in f:
                if line.startswith("Uid:"):
                    return {int(x) for x in line.split()[1:]}
    except OSError:
        pass
    return set()


def user_pids(uid):
    return [int(d) for d in os.listdir("/proc") if d.isdigit() and uid in _uids(d)]


def kill_user(uid, tries=200):
    """SIGKILL every process running as uid until none is left. Returns (number seen, pids left).
    First kill(-1) issued AS that user (one pass of the kernel over its processes, which a fork loop cannot
    outrun), then a /proc scan as the check."""
    seen = set(user_pids(uid))
    if seen:
        pid = os.fork()
        if pid == 0:
            try:
                os.setgroups([])
                os.setgid(uid)
                os.setuid(uid)
                os.kill(-1, signal.SIGKILL)
            finally:
                os._exit(0)
        os.waitpid(pid, 0)
    for _ in range(tries):
        pids = user_pids(uid)
        if not pids:
            return len(seen), []
        for p in pids:
            try:
                os.kill(p, signal.SIGKILL)
                seen.add(p)
            except ProcessLookupError:
                pass
        time.sleep(0.01)
    return len(seen), user_pids(uid)


def mount_points():
    out = []
    try:
        with open("/proc/self/mounts") as f:
            for line in f:
                p = line.split()
                if len(p) >= 3 and p[2] not in SKIP_FS:
                    out.append(p[1].replace("\\040", " "))
    except OSError:
        out = ["/"]
    return sorted(set(out) | {"/"})


def owned_by(uid, mounts=None):
    """Every path owned by uid on the box's file systems (one walk per mount point, not crossing into others)."""
    found = []
    mounts = mounts or mount_points()
    mset = set(mounts)
    for m in mounts:
        try:
            dev = os.lstat(m).st_dev
        except OSError:
            continue
        for root, dirs, files in os.walk(m, topdown=True):
            keep = []
            for d in dirs:
                p = os.path.join(root, d)
                try:
                    st = os.lstat(p)
                except OSError:
                    continue
                if st.st_uid == uid:
                    found.append(p)
                if st.st_dev == dev and p not in mset and not os.path.islink(p):
                    keep.append(d)
            dirs[:] = keep
            for nm in files:
                p = os.path.join(root, nm)
                try:
                    if os.lstat(p).st_uid == uid:
                        found.append(p)
                except OSError:
                    pass
    return found


def wipe_user(uid):
    """Delete everything owned by uid, deepest first. Returns (number removed, paths that survived)."""
    paths = sorted(owned_by(uid), key=len, reverse=True)
    n = 0
    for p in paths:
        try:
            if os.path.isdir(p) and not os.path.islink(p):
                shutil.rmtree(p, ignore_errors=True)
            else:
                os.unlink(p)
            n += 1
        except OSError:
            pass
    return n, (owned_by(uid) if paths else [])


def ipc_user(uid):
    """Remove System V shared memory, semaphores and message queues owned by uid (they outlive processes)."""
    n = 0
    for table, flag in (("shm", "-m"), ("sem", "-s"), ("msg", "-q")):
        try:
            with open(f"/proc/sysvipc/{table}") as f:
                rows = [r.split() for r in f.read().splitlines()[1:]]
        except OSError:
            continue
        for r in rows:
            try:
                ident, owner = int(r[1]), int(r[4] if table == "sem" else r[7])
            except (IndexError, ValueError):
                continue
            if owner == uid and shutil.which("ipcrm"):
                n += subprocess.run(["ipcrm", flag, str(ident)], capture_output=True).returncode == 0
    return n


def cleanup(uid):
    killed, left = kill_user(uid)
    ipc = ipc_user(uid)
    removed, left_files = wipe_user(uid)
    killed2, left = kill_user(uid)                           # anything started while the files went away
    return {"killed": killed + killed2, "removed": removed, "ipc_removed": ipc, "left_pids": left,
            "left_files": left_files[:5], "mounts": mount_points()}


# ----------------------------------------------------------------------------- one request
def run(a):
    root = os.geteuid() == 0
    drop = root and a.uid is not None and a.uid > 0
    layers = {"rlimits": True, "uid": a.uid if drop else None, "cleanup": bool(drop and not a.no_cleanup)}
    io = tempfile.mkdtemp(prefix="physim2-io-")              # the only place the predictor may write its reply
    os.chmod(io, 0o700)
    err_path = os.path.join(io, "stderr.txt")
    out_path = os.path.join(io, "reply.npz")
    if drop:
        os.chown(io, a.uid, a.uid)
    cpu = int(a.cpu) if a.cpu else None

    def pre():
        os.setsid()
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        if cpu:
            resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))          # hard = soft: SIGKILL at the limit
        if a.mem_gib:
            resource.setrlimit(resource.RLIMIT_AS, (int(a.mem_gib * GIB), int(a.mem_gib * GIB)))
        if a.file_mib:
            resource.setrlimit(resource.RLIMIT_FSIZE, (int(a.file_mib) << 20, int(a.file_mib) << 20))
        if drop:
            resource.setrlimit(resource.RLIMIT_NPROC, (256, 256))
            os.setgroups([])
            os.setgid(a.uid)
            os.setuid(a.uid)
        os.nice(10)

    if root:
        os.chmod(a.request, 0o444)                           # whatever umask the transport used
    cmd = [sys.executable, "-I", "-B", os.path.abspath(a.runner), os.path.abspath(a.submission),
           os.path.abspath(a.request), out_path]
    t0 = time.time()
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    timed_out = False
    with open(err_path, "wb") as ef:
        if drop:
            os.fchown(ef.fileno(), a.uid, a.uid)
        p = subprocess.Popen(cmd, cwd=io, env=dict(ENV), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=ef, preexec_fn=pre)
        try:
            p.wait(timeout=a.wall or None)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            p.wait()
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    res = {"returncode": p.returncode, "timed_out": timed_out, "wall_s": time.time() - t0,
           "cpu_s": (r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime), "layers": layers}
    try:
        os.killpg(p.pid, signal.SIGKILL)                     # the request's own session, with or without root
    except (ProcessLookupError, PermissionError):
        pass
    if drop and not a.no_cleanup:
        kill_user(a.uid)                                     # nothing of the predictor runs while root reads its reply
    ok = p.returncode == 0 and os.path.isfile(out_path) and not os.path.islink(out_path)
    if ok and os.path.getsize(out_path) > (int(a.max_reply_mib) << 20):
        ok, res["why"] = False, "reply too large"
    if ok:
        with open(out_path, "rb") as f:
            res["reply_b64"] = base64.b64encode(f.read()).decode("ascii")
    else:
        try:
            with open(err_path, "rb") as f:
                f.seek(max(0, os.path.getsize(err_path) - 1500))
                res["stderr"] = f.read().decode("utf-8", "replace")
        except OSError:
            res["stderr"] = ""
        res.setdefault("why", "wall-clock limit" if timed_out else "CPU-time limit" if cpu and res["cpu_s"] >= 0.98 * cpu
                       else f"exit code {p.returncode}")
    res["ok"] = bool(ok)
    shutil.rmtree(io, ignore_errors=True)
    if drop and not a.no_cleanup:
        res["cleanup"] = cleanup(a.uid)
    return res


def scan(uid, fix=True):
    """Before the first request (grader's box): what could a later request find or leave? Removes the write bit
    of world-writable regular files and of world-writable directories that are not sticky temporary directories
    (some container engines run setup commands with umask 0), then lists where the unprivileged user can still
    write and anything it already owns."""
    dirs, fixed_dirs, fixed_files = [], [], []
    for m in mount_points():
        try:
            dev = os.lstat(m).st_dev
        except OSError:
            continue
        for root, ds, fs in os.walk(m, topdown=True):
            ds[:] = [d for d in ds if not os.path.islink(os.path.join(root, d)) and os.lstat(os.path.join(root, d)).st_dev == dev]
            for d in ds + ["."]:
                p = os.path.normpath(os.path.join(root, d))
                try:
                    st = os.lstat(p)
                except OSError:
                    continue
                if st.st_mode & 0o002:
                    if fix and not st.st_mode & 0o1000:
                        try:
                            os.chmod(p, st.st_mode & 0o7755)
                            fixed_dirs.append(p)
                            continue
                        except OSError:
                            pass
                    dirs.append(p)
            for nm in fs:
                p = os.path.join(root, nm)
                try:
                    st = os.lstat(p)
                except OSError:
                    continue
                if (st.st_mode & 0o170000) == 0o100000 and st.st_mode & 0o002 and fix:
                    try:
                        os.chmod(p, st.st_mode & 0o7755)
                        fixed_files.append(p)
                    except OSError:
                        pass
    return {"writable_dirs": sorted(set(dirs) - set(fixed_dirs)), "fixed_dirs": sorted(set(fixed_dirs))[:20],
            "fixed_files": fixed_files[:20], "fixed": len(set(fixed_dirs)) + len(fixed_files),
            "owned_by_user": owned_by(uid)[:20], "user_pids": user_pids(uid), "root": os.geteuid() == 0}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--submission")
    ap.add_argument("--runner")
    ap.add_argument("--request")
    ap.add_argument("--cpu", type=float, default=None)
    ap.add_argument("--wall", type=float, default=None)
    ap.add_argument("--mem-gib", type=float, default=None)
    ap.add_argument("--file-mib", type=float, default=256)
    ap.add_argument("--max-reply-mib", type=float, default=64)
    ap.add_argument("--uid", type=int, default=1000)
    ap.add_argument("--no-cleanup", action="store_true")
    a = ap.parse_args(argv)
    try:
        res = scan(a.uid) if a.scan else run(a)
    except Exception as e:                                   # the driver itself failed: not the predictor's fault
        res = {"ok": False, "driver_error": type(e).__name__ + ": " + str(e)[:300], "why": "driver error",
               "cpu_s": 0.0, "wall_s": 0.0, "timed_out": False, "returncode": None, "stderr": ""}
    sys.stdout.write(json.dumps(res) + "\n")


if __name__ == "__main__":
    main()
