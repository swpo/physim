"""physim2._item -- run ONE predictor request in this box as an unprivileged user, then leave the box clean.

Public and trusted: the same file runs in the grader's box (as /runtime/item.py, started by root once per exam
item) and in your own box when you call `lab.validate(...)`. It is the port of PhySim v1's predictor launcher
and worker (v1: physim/runtime_sandbox.py:156-179, physim/container_worker.py:14-19) with one addition: after
every request, root kills every process of the unprivileged user and deletes everything that user owns, so a
predictor cannot leave a file, a shared-memory segment or a background process for the next item. What this
cleanup does NOT reset: timestamps of files the user may read, the box's process-id counter and the kernel's
counters of the box (loopback traffic, cgroup statistics). The grader therefore gives every exam item a box of
its own by default; one box for all items is a pilot mode.

Root never trusts what the predictor leaves in its reply directory: the directory is held open before the
predictor starts and the reply and the error text are read through that handle, without following a link and
without blocking, and only from regular files (a named pipe left as stderr.txt would otherwise block root for
ever).

    python -I -B _item.py --uid N --submission DIR --runner physim2/predict_runner.py --request request.npz \
        --cpu 30 --wall 60 --mem-gib 4 [--file-mib 256] [--max-reply-mib 64] [--no-cleanup] [--no-box]
    python -I -B _item.py --uid N --scan          (once per box, before the first request)

--uid is required and has no default: it must be the number the environment wrote into THIS box
(/etc/physim2/predictor_uid), from the reserved range 20000-59999.

Prints one JSON line:
    ok, returncode, timed_out, cpu_s, wall_s, why, stderr (tail), reply_b64 (the reply .npz when ok),
    layers {uid, rlimits}, cleanup {killed, removed, ipc_removed, left_pids, left_files, roots}

Layers: resource limits always (CPU seconds hard = soft, address space, file size, no core dumps, process
count); when started as root INSIDE A DISPOSABLE BOX also a drop to --uid with no supplementary groups, and the
cleanup. "Inside a disposable box" is decided by require_box below and needs all of: a root caller, the marker
the environment's setup writes (/etc/physim2/predictor_uid), signs of a container, the variable
PHYSIM2_BOX_CLEANUP=disposable-box that only the grading route sets, a target uid equal to the marker's and
inside 20000-59999, and a mount table that holds nothing but what Docker gives a container started WITHOUT any
-v, --mount or --tmpfs (a mounted host folder, a volume or an extra tmpfs makes every function here refuse).

Anywhere else NOTHING runs: the predictor is not started and the reply is a "driver error" that says why. The
one exception is the explicit flag --no-box (and no route variable): the predictor then runs as the calling
user under the resource limits only, without the uid drop and without the cleanup. That is for an agent's own
check in its own box (physim2/validate.py passes it); it runs the given predict.py with the caller's rights,
so never use it on a machine you care about with code you did not write. The network policy and the absence
of hidden files are properties of the box, not of this file.

What the cleanup removes: exactly the paths the uid owns, a file by unlink and a directory by rmdir (only once
it is empty), deepest first, never a mount point. No tree is ever removed by walking it (no shutil.rmtree in
this file): a file of another owner below a directory of the uid stays, and the report lists what stayed.
"""
import argparse
import base64
import json
import os
import re
import resource
import signal
import stat
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


# ----------------------------------------------------------------------------- the box guard
# The cleanup below kills every process and deletes every file of one uid on EVERY writable file system it can
# see. That is right in a disposable box and destructive on a real machine (it happened once: a test ran this
# file as root on a development host and the home directory of uid 1000 was deleted). Every function that kills,
# deletes or changes modes therefore asks require_box(uid) first, and that needs ALL of:
#   root        the caller's real uid is 0 (in a box the grading route runs this file as root)
#   marker      /etc/physim2 is a root-owned directory (no link) and /etc/physim2/predictor_uid a root-owned
#               regular file that only root may write: the environment's setup writes both into every box
#   container   this process runs inside a container (see container_evidence)
#   route       the variable PHYSIM2_BOX_CLEANUP=disposable-box is set: the grading route sets it on its own
#               commands, nothing else does
#   uid         the target uid is the one written in the marker, lies in MIN_UID..MAX_UID (the range the
#               grading route draws from; 1000, the first account of most machines, is far below it), is
#               not 0 and is not the real uid of the caller
#   mounts      the mount table can be read and holds nothing a prepared box does not have (foreign_mounts):
#               a host folder mounted into a hand-started container makes everything refuse
BOX_DIR = "/etc/physim2"
UID_FILE = BOX_DIR + "/predictor_uid"
ROUTE_VAR, ROUTE_VALUE = "PHYSIM2_BOX_CLEANUP", "disposable-box"
MIN_UID, MAX_UID = 20000, 59999
MOUNT_TABLE = "/proc/self/mountinfo"
ROOT_FS = {"overlay"}                                        # the root of a Docker container (overlay2, containerd overlayfs)
KERNEL_DIRS = ("/proc", "/sys", "/dev")                      # mounts at or below these are the container's own ...
KERNEL_FS = SKIP_FS | {"tmpfs", "devtmpfs", "mqueue"}        # ... if they are of a kernel or memory file-system type
ETC_FILES = ("/etc/hostname", "/etc/hosts", "/etc/resolv.conf")   # the three files Docker mounts into every container
# round 4: a box of the pilot has a read-only root, and the four places the exam writes to are memory file
# systems that the runtime mounts with fixed sizes (physim2_env/boxcaps.py: TMPFS). They belong to the box.
BOX_TMPFS = ("/workspace", "/tmp", "/etc/physim2", "/runtime")
# Second pass (code audit K1): and each with the size the runtime gives it (boxcaps.TMPFS: 1024m, 512m, 1m, 16m),
# as the kernel shows it among the mount's own options. A tmpfs of somebody else's bound there (a hand-started
# container on a Linux host) has its own size, or none.
BOX_TMPFS_SIZE = {"/workspace": "size=1048576k", "/tmp": "size=524288k", "/etc/physim2": "size=1024k", "/runtime": "size=16384k"}


def container_evidence():
    """Signs that this process is inside a container: the file Docker creates in every container, the one Podman
    creates, or a control-group path of pid 1 that names a container engine. Empty on an ordinary machine."""
    ev = [p for p in ("/.dockerenv", "/run/.containerenv") if os.path.exists(p)]
    try:
        with open("/proc/1/cgroup") as f:
            cg = f.read()
        if any(k in cg for k in ("docker", "containerd", "kubepods", "libpod", "lxc")):
            ev.append("/proc/1/cgroup")
    except OSError:
        pass
    return ev


def dedicated_uid():
    """The predictor uid the environment wrote into this box, or None (no marker, or a marker root does not own)."""
    try:
        d, f = os.lstat(BOX_DIR), os.lstat(UID_FILE)
        if not stat.S_ISDIR(d.st_mode) or not stat.S_ISREG(f.st_mode) or d.st_uid != 0 or f.st_uid != 0 or f.st_mode & 0o022:
            return None
        with open(UID_FILE) as fh:
            return int(fh.read(32).strip())
    except (OSError, ValueError):
        return None


def parse_mounts(text):
    """[(mount point, file-system type, root of the mount inside its file system, the file system's own options)]
    from the text of /proc/<pid>/mountinfo. Pure. Raises ValueError for a line it cannot read and for an empty
    table: a table that cannot be read is never treated as a table without mounts."""
    def plain(s):                                            # the kernel writes space, tab, newline, backslash as \ooo
        return re.sub(r"\\([0-7]{3})", lambda m: chr(int(m.group(1), 8)), s)
    out = []
    for line in text.splitlines():
        if not line.strip():
            continue
        p = line.split(" ")
        try:
            sep = p.index("-", 6)                            # after the optional fields
            out.append((plain(p[4]), p[sep + 1], plain(p[3]), p[sep + 3] if len(p) > sep + 3 else ""))
        except (ValueError, IndexError):
            raise ValueError("a line of the mount table cannot be read") from None
    if not out:
        raise ValueError("the mount table is empty")
    return out


def foreign_mounts(mounts, isfile=None):
    """Mounts that a box prepared by this environment does not have, as "mount point (type)"; an empty list is
    the stock table of a Docker container started without any -v, --mount or --tmpfs. Pure: `mounts` comes from
    parse_mounts, `isfile(path)` (optional) says whether a path is a regular file. Allowed, and nothing else:
      /                                  exactly once, as the container's own overlay root
      /proc, /sys, /dev and below        of a kernel or memory file-system type (proc, sysfs, tmpfs, cgroup, ...)
      /etc/hostname, /etc/hosts, /etc/resolv.conf     the three FILES Docker mounts into every container
      /workspace, /tmp, /etc/physim2, /runtime        each at most once, as a tmpfs of its own (the capped box of
                                                      round 4: read-only root, these four memory file systems)
                                                      with the size the runtime gives it (BOX_TMPFS_SIZE)
    A host folder or a volume anywhere, a tmpfs anywhere else outside /dev, a bind mount below /dev: foreign."""
    bad = []
    roots = [m for m in mounts if m[0] == "/"]
    if len(roots) != 1:
        bad.append(f"/ ({len(roots)} entries)")
    for mp, fs, root, *rest in mounts:
        opts = rest[0].split(",") if rest and isinstance(rest[0], str) else []
        if mp == "/":
            if fs not in ROOT_FS or root != "/":
                bad.append(f"/ ({fs})")
        elif any(mp == d or mp.startswith(d + "/") for d in KERNEL_DIRS):
            if fs not in KERNEL_FS:
                bad.append(f"{mp} ({fs})")
        elif mp in ETC_FILES:
            if isfile is not None and not isfile(mp):
                bad.append(f"{mp} (not a regular file)")
        elif mp in BOX_TMPFS:                                # exactly once, a tmpfs of its own (root "/") of the box's size
            if fs != "tmpfs" or root != "/" or sum(1 for m in mounts if m[0] == mp) != 1:
                bad.append(f"{mp} ({fs})")
            elif BOX_TMPFS_SIZE[mp] not in opts:
                bad.append(f"{mp} ({fs}, not the box's size)")
        else:
            bad.append(f"{mp} ({fs})")
    return bad


def box_mounts():
    """The mount table of this process, parsed. Raises RuntimeError("refused: ...") when it cannot be read:
    no caller ever falls back to walking "/" (there is no /proc on macOS, and an unreadable table means this
    is not a box whose content is known)."""
    try:
        with open(MOUNT_TABLE) as f:
            return parse_mounts(f.read())
    except (OSError, ValueError) as e:
        raise RuntimeError(f"refused: the mount table {MOUNT_TABLE} cannot be read ({type(e).__name__})") from None


def _regular(path):
    try:
        return stat.S_ISREG(os.lstat(path).st_mode)
    except OSError:
        return False


def guard_reasons(uid, *, dedicated, evidence, route, caller, mounts):
    """Why a cleanup for `uid` must be refused (empty list = allowed). Pure: every input is passed in.
    `mounts` is foreign_mounts(...) of this box, or None when the mount table could not be read."""
    why = []
    if caller != 0:
        why.append("the caller is not root")
    if dedicated is None:
        why.append(f"no marker ({UID_FILE} written by the environment's setup)")
    if not evidence:
        why.append("no sign of a container (/.dockerenv, /run/.containerenv, control group of pid 1)")
    if route != ROUTE_VALUE:
        why.append(f"{ROUTE_VAR} is not set by the grading route")
    if not isinstance(uid, int) or isinstance(uid, bool) or uid <= 0:
        why.append("the target uid is 0 or not a uid")
    else:
        if not MIN_UID <= uid <= MAX_UID:
            why.append(f"the target uid is outside {MIN_UID}-{MAX_UID}")
        if uid == caller:
            why.append("the target uid is the caller's own")
        if dedicated is not None and uid != dedicated:
            why.append("the target uid is not this box's predictor uid")
    if mounts is None:
        why.append("the mount table cannot be read")
    elif mounts:
        why.append("mounted file systems that a prepared box does not have: " + ", ".join(mounts[:6]))
    return why


def box_guard(uid):
    try:
        foreign = foreign_mounts(box_mounts(), isfile=_regular)
    except RuntimeError:
        foreign = None
    why = guard_reasons(uid, dedicated=dedicated_uid(), evidence=container_evidence(), route=os.environ.get(ROUTE_VAR),
                        caller=os.getuid(), mounts=foreign)
    return {"ok": not why, "why": why}


def require_box(uid):
    g = box_guard(uid)
    if not g["ok"]:
        raise RuntimeError("refused: not a disposable box (" + "; ".join(g["why"]) + ")")


# ----------------------------------------------------------------------------- cleanup (root, in a box only)
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


def become_reaper():
    """Orphans of this process tree are re-parented to THIS process (not to the box's init, which may never
    wait for them), so that killed predictor processes can be reaped instead of staying as zombies: a zombie
    keeps its pid, its uid and its 15-character name visible to later requests."""
    try:
        import ctypes
        ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0)          # PR_SET_CHILD_SUBREAPER
    except Exception:
        pass


def reap():
    n = 0
    while True:
        try:
            pid, _ = os.waitpid(-1, os.WNOHANG)
        except ChildProcessError:
            return n
        if pid == 0:
            return n
        n += 1


NOT_CHANGED = 96                                             # exit status of a child whose identity did not change


def is_only(uid):
    """True if this process is uid and nothing else: real, effective and saved user and group, no other group."""
    return os.getresuid() == (uid, uid, uid) and os.getresgid() == (uid, uid, uid) and set(os.getgroups()) <= {uid}


def as_user(uid, fn):
    """Run fn() in a child that has become uid (things only the owner may do: signal all, remove IPC objects).
    fn runs ONLY if the child really is uid afterwards (kill(-1) issued under any other identity would hit that
    identity's processes); if not, the child exits with NOT_CHANGED, nothing was done, and this raises."""
    require_box(uid)
    pid = os.fork()
    if pid == 0:
        code = 0
        try:
            os.setgroups([])
            os.setgid(uid)
            os.setuid(uid)
            if is_only(uid):
                fn()
            else:
                code = NOT_CHANGED
        except BaseException:
            code = code or 1
        finally:
            os._exit(code)
    _, status = os.waitpid(pid, 0)
    if os.WIFEXITED(status) and os.WEXITSTATUS(status) == NOT_CHANGED:
        raise RuntimeError("refused: the helper process did not become the predictor uid; nothing was signalled or removed")


def kill_user(uid, tries=200):
    """SIGKILL every process running as uid and reap it, until none is left. Returns (number seen, pids left).
    First kill(-1) issued AS that user (one pass of the kernel over its processes, which a fork loop cannot
    outrun), then a /proc scan as the check."""
    require_box(uid)
    seen = set(user_pids(uid))
    if seen:
        as_user(uid, lambda: os.kill(-1, signal.SIGKILL))
    for _ in range(tries):
        reap()
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
    reap()
    return len(seen), user_pids(uid)


def mount_points(mounts=None):
    """The mount points the cleanup looks at: every mount of the table except kernel file systems. Raises
    (box_mounts) when the table cannot be read; there is no fallback to "/"."""
    mounts = box_mounts() if mounts is None else mounts
    return sorted({m[0] for m in mounts if m[1] not in SKIP_FS})


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
    """Remove what uid owns: exactly the paths owned_by lists, deepest first (a path is longer than its parent),
    a directory by rmdir and anything else by unlink. rmdir removes an EMPTY directory only, so a file of
    another owner below a directory of uid stays, and so does that directory; no tree is removed by walking it.
    A mount point is never removed. Returns (number removed, paths of uid that survived)."""
    require_box(uid)
    mounts = box_mounts()
    points = {m[0] for m in mounts}
    paths = sorted(owned_by(uid, mount_points(mounts)), key=len, reverse=True)
    n = 0
    for p in paths:
        if p in points or os.path.ismount(p):
            continue
        try:
            st = os.lstat(p)
            if st.st_uid != uid:                             # changed since the walk: not this uid's any more
                continue
            if stat.S_ISDIR(st.st_mode):
                os.rmdir(p)
            else:
                os.unlink(p)
            n += 1
        except OSError:
            pass
    return n, (owned_by(uid) if paths else [])


IPC = (("shm", 7, 9), ("sem", 4, 6), ("msg", 7, 9))             # /proc/sysvipc table, uid column, cuid column


def ipc_ids(uid):
    """System V objects whose owner or creator is uid: {table: [ids]}. They outlive every process."""
    out = {}
    for table, cu, cc in IPC:
        try:
            with open(f"/proc/sysvipc/{table}") as f:
                rows = [r.split() for r in f.read().splitlines()[1:]]
        except OSError:
            continue
        ids = []
        for r in rows:
            try:
                if uid in (int(r[cu]), int(r[cc])):
                    ids.append(int(r[1]))
            except (IndexError, ValueError):
                pass
        if ids:
            out[table] = ids
    return out


def ipc_user(uid):
    """Remove them. Root in a container has no CAP_SYS_ADMIN and may not remove another user's objects, so the
    removal is issued AS that user. Returns (number removed, what is left)."""
    require_box(uid)
    before = ipc_ids(uid)
    if not before:
        return 0, {}

    def remove():
        import ctypes
        libc = ctypes.CDLL(None, use_errno=True)
        for i in before.get("shm", []):
            libc.shmctl(i, 0, None)                           # IPC_RMID
        for i in before.get("sem", []):
            libc.semctl(i, 0, 0)
        for i in before.get("msg", []):
            libc.msgctl(i, 0, None)
    as_user(uid, remove)
    left = ipc_ids(uid)
    return sum(len(v) for v in before.values()) - sum(len(v) for v in left.values()), left


def cleanup(uid):
    require_box(uid)
    killed, left = kill_user(uid)
    ipc, left_ipc = ipc_user(uid)
    removed, left_files = wipe_user(uid)
    killed2, left = kill_user(uid)                           # anything started while the files went away
    return {"killed": killed + killed2, "removed": removed, "ipc_removed": ipc, "left_pids": left,
            "left_files": left_files[:5], "left_ipc": left_ipc, "mounts": mount_points()}


def remove_io(io, io_fd):
    """Remove the reply directory this process created, through the handle taken before the predictor ran: its
    entries by unlink relative to that handle (never following a link, never leaving that one directory), then
    the directory itself, by rmdir, if the path still names that same directory. No recursion: a subdirectory
    the predictor made there is the predictor's and goes with the cleanup of its uid (in a box)."""
    try:
        for nm in os.listdir(io_fd):
            try:
                os.unlink(nm, dir_fd=io_fd)
            except OSError:
                pass
        held, named = os.fstat(io_fd), os.lstat(io)
        if stat.S_ISDIR(named.st_mode) and (held.st_dev, held.st_ino) == (named.st_dev, named.st_ino):
            os.rmdir(io)
    except OSError:
        pass


# ----------------------------------------------------------------------------- one request
def read_regular(dir_fd, name, max_bytes, tail=False):
    """(bytes | None, why). The content of the REGULAR file `name` inside the directory held open as dir_fd:
    never follows a link, never blocks (a fifo has no writer once the predictor's processes are gone), never
    reads more than max_bytes (`tail`: the last max_bytes; otherwise a larger file is refused)."""
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC, dir_fd=dir_fd)
    except OSError:
        return None, "missing"
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            return None, "not a regular file"
        if tail:
            os.lseek(fd, max(0, st.st_size - max_bytes), os.SEEK_SET)
        elif st.st_size > max_bytes:
            return None, "too large"
        chunks, left = [], max_bytes
        while left > 0:
            b = os.read(fd, min(left, 1 << 20))
            if not b:
                break
            chunks.append(b)
            left -= len(b)
        return b"".join(chunks), None
    except OSError:
        return None, "unreadable"
    finally:
        os.close(fd)


def box_cpu_s():
    """CPU seconds of every process of this box so far (its cgroup counter; cgroup v2, then v1), or None."""
    try:
        with open("/sys/fs/cgroup/cpu.stat") as f:
            for line in f:
                if line.startswith("usage_usec"):
                    return int(line.split()[1]) / 1e6
    except (OSError, ValueError, IndexError):
        pass
    try:
        with open("/sys/fs/cgroup/cpuacct/cpuacct.usage") as f:
            return int(f.read().split()[0]) / 1e9
    except (OSError, ValueError, IndexError):
        return None


def run(a):
    root = os.geteuid() == 0
    guard = box_guard(a.uid)
    drop = root and guard["ok"]
    if not drop:
        why = "refused: not a disposable box (" + "; ".join(guard["why"] or ["not started as root"]) + ")"
        if os.environ.get(ROUTE_VAR) == ROUTE_VALUE:
            # the grading route asked for the unprivileged run and this is not a disposable box: run NOTHING
            raise RuntimeError(why)
        if not a.no_box:
            # no route variable and no explicit flag: the given predict.py is not run with the caller's rights
            raise RuntimeError(why + "; nothing was run (--no-box runs the predictor as the calling user, without "
                               "the uid drop and the cleanup: for your own code in a box of your own)")
    become_reaper()
    if drop and not a.no_cleanup and user_pids(a.uid):
        kill_user(a.uid)                                     # never start a request next to a stray process
    layers = {"rlimits": True, "uid": a.uid if drop else None, "cleanup": bool(drop and not a.no_cleanup)}
    if not drop:
        layers["refused"] = guard["why"]                     # --no-box: no uid drop, no cleanup, and why
    io = tempfile.mkdtemp(prefix="physim2-io-")              # the only place the predictor may write its reply
    os.chmod(io, 0o700)
    io_fd = os.open(io, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)    # root reads the reply through THIS handle
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
            if not is_only(a.uid):                           # never run the predictor under another identity
                raise RuntimeError("the uid drop did not take effect")
        os.nice(10)

    if drop:
        os.chmod(a.request, 0o444)                           # whatever umask the transport used (in a box only)
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
    k0 = 0
    if drop and not a.no_cleanup:
        k0, _ = kill_user(a.uid)                             # nothing of the predictor runs while root reads its reply
    ok = p.returncode == 0
    if ok:
        reply, why = read_regular(io_fd, "reply.npz", int(a.max_reply_mib) << 20)
        if reply is None:
            ok, res["why"] = False, "reply too large" if why == "too large" else f"no reply file ({why})"
        else:
            res["reply_b64"] = base64.b64encode(reply).decode("ascii")
            del reply
    if not ok:
        err, _ = read_regular(io_fd, "stderr.txt", 4000, tail=True)
        res["stderr"] = (err or b"").decode("utf-8", "replace")
        res.setdefault("why", "wall-clock limit" if timed_out else "CPU-time limit" if cpu and res["cpu_s"] >= 0.98 * cpu
                       else f"exit code {p.returncode}")
    res["ok"] = bool(ok)
    remove_io(io, io_fd)
    os.close(io_fd)
    if drop and not a.no_cleanup:
        res["cleanup"] = cleanup(a.uid)
        res["cleanup"]["killed"] += k0
    res["box_cpu_s"] = box_cpu_s()
    return res


def scan(uid, fix=True):
    """Before the first request (grader's box): what could a later request find or leave? Outside a disposable
    box (require_box) it walks nothing and changes nothing; the report then says why in "guard". In a box: removes the write bit
    of world-writable regular files and of world-writable directories that are not sticky temporary directories
    (some container engines run setup commands with umask 0), then lists where the unprivileged user can still
    write and anything it already owns."""
    dirs, fixed_dirs, fixed_files = [], [], []
    guard = box_guard(uid)
    fix = bool(fix and guard["ok"] and os.geteuid() == 0)
    if not guard["ok"]:                                      # not a box: no walk, no change, only the refusal
        return {"writable_dirs": [], "fixed_dirs": [], "fixed_files": [], "fixed": 0, "owned_by_user": [], "user_pids": [],
                "root": os.geteuid() == 0, "box_limits": {}, "guard": guard, "fixing": False,
                "container_evidence": container_evidence()}
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
    limits = {}
    for nm, path in (("pids_max", "/sys/fs/cgroup/pids.max"), ("pids_max", "/sys/fs/cgroup/pids/pids.max"),
                     ("memory_max", "/sys/fs/cgroup/memory.max"), ("memory_max", "/sys/fs/cgroup/memory/memory.limit_in_bytes")):
        try:
            with open(path) as f:
                limits.setdefault(nm, f.read().strip())
        except OSError:
            pass
    return {"writable_dirs": sorted(set(dirs) - set(fixed_dirs)), "fixed_dirs": sorted(set(fixed_dirs))[:20],
            "fixed_files": fixed_files[:20], "fixed": len(set(fixed_dirs)) + len(fixed_files),
            "owned_by_user": owned_by(uid)[:20], "user_pids": user_pids(uid), "root": os.geteuid() == 0,
            "box_limits": limits, "guard": guard, "fixing": fix, "container_evidence": container_evidence()}


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
    ap.add_argument("--uid", type=int, required=True,
                    help="the predictor uid of THIS box (/etc/physim2/predictor_uid); no default")
    ap.add_argument("--no-cleanup", action="store_true")
    ap.add_argument("--no-box", action="store_true",
                    help="outside a disposable box: run the predictor as the calling user (limits only, no uid drop, no "
                         "cleanup). Without this flag nothing runs outside a box")
    a = ap.parse_args(argv)
    try:
        res = scan(a.uid) if a.scan else run(a)
    except Exception as e:                                   # the driver itself failed: not the predictor's fault
        res = {"ok": False, "driver_error": type(e).__name__ + ": " + str(e)[:900], "why": "driver error",
               "cpu_s": 0.0, "wall_s": 0.0, "timed_out": False, "returncode": None, "stderr": ""}
    sys.stdout.write(json.dumps(res) + "\n")


if __name__ == "__main__":
    main()
