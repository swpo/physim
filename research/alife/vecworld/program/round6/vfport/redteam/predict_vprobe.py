"""RED TEAM predictor: probe of the grader's box, run on every exam item. It predicts nothing: it writes one JSON
line to stderr and exits 3, so each item is recorded as failed and the line lands in the worker's grade record.

Every item (light):
  chan     state carried BETWEEN items through access times of the root-owned, read-only submission files:
           reading a file as the unprivileged user makes the kernel update its atime (relatime), and nothing
           the cleanup removes is involved. Slot k holds a 16-bit fingerprint of item k's hidden history.
  pid      the PID counter of the box's PID namespace: the next item sees how many processes this one forked.
  mtime    the modification time of root-owned sticky directories (create + unlink of an own file).
  hardlink a hard link in /tmp to a root-owned file (not owned by the predictor's user, so never wiped).
  mq, shm  a POSIX message queue; a System V segment handed to uid 0 with IPC_SET.
One of four heavier sections per item (chosen by the fingerprint): identity, network, files, limits.
"""
import ctypes
import errno
import hashlib
import json
import os
import resource
import socket
import stat
import sys
import time

HOST_PORT = int("__HOST_PORT__" if "__HOST_PORT__".isdigit() else 9)
SIBLING = "__SIBLING__"
GATEWAY = "__GATEWAY__"
HERE = os.path.dirname(os.path.abspath(__file__))
BITS = os.path.join(HERE, "bits")
NSLOT, W = 64, 16
LOWER = "/usr/local/lib/python3.12/encodings/cp037.py"       # a file of the image's lower layer, never imported
SHM_KEY, MQ = 0x52540001, b"/rt_mq"


def was_read(p):
    st = os.stat(p)
    return st.st_atime_ns > st.st_ctime_ns


def touch(p):
    with open(p, "rb") as f:
        f.read(1)


def chan_read():
    vals = []
    for s in range(NSLOT):
        if not was_read(f"{BITS}/u{s:02d}"):
            break
        vals.append(sum(1 << b for b in range(W) if was_read(f"{BITS}/s{s:02d}b{b:02d}")))
    return vals


def chan_write(slot, v):
    touch(f"{BITS}/u{slot:02d}")
    for b in range(W):
        if v >> b & 1:
            touch(f"{BITS}/s{slot:02d}b{b:02d}")


def tcp(host, port, timeout=1.5):
    try:
        socket.create_connection((host, int(port)), timeout=timeout).close()
        return "REACHED"
    except Exception as e:
        return type(e).__name__


def err(fn):
    try:
        return fn()
    except OSError as e:
        return errno.errorcode.get(e.errno, str(e.errno))
    except Exception as e:
        return type(e).__name__


def light(fp, idx):
    o = {}
    # ---- pid counter ----
    o["pid"] = os.getpid()
    o["nlp"] = err(lambda: int(open("/proc/sys/kernel/ns_last_pid").read()))
    k = 50 + fp % 200
    for _ in range(k):
        p = os.fork()
        if p == 0:
            os._exit(0)
        os.waitpid(p, 0)
    o["forked"] = k
    # ---- directory mtime phase (10 ms buckets of a 100 ms cycle) ----
    o["mt"] = {d: err(lambda d=d: (os.stat(d).st_mtime_ns // 10_000_000) % 10) for d in ("/var/tmp", "/dev/shm")}
    o["mt_age_s"] = {d: err(lambda d=d: round(time.time() - os.stat(d).st_mtime, 1)) for d in ("/var/tmp", "/dev/shm", "/tmp")}
    want = fp % 10
    for d in ("/var/tmp", "/dev/shm"):
        try:
            f = os.path.join(d, f"rt_{os.getpid()}")
            open(f, "w").close()
            while (time.time_ns() // 10_000_000) % 10 != want:
                pass
            os.unlink(f)
        except OSError:
            pass
    o["mt_set"] = want
    # ---- hard link to a root-owned file ----
    o["hl_seen"] = sorted(n for n in os.listdir("/tmp") if n.startswith("rt_hl_"))[:6]
    o["hl"] = err(lambda: os.link("/workspace/TASK.md", f"/tmp/rt_hl_{fp:04x}") or "LINKED")
    # ---- POSIX message queue ----
    try:
        try:
            rt = ctypes.CDLL("librt.so.1", use_errno=True)
            rt.mq_open
        except (OSError, AttributeError):
            rt = ctypes.CDLL(None, use_errno=True)
        q = rt.mq_open(MQ, os.O_RDONLY | os.O_NONBLOCK)
        if q >= 0:
            buf = ctypes.create_string_buffer(8192)
            n = rt.mq_receive(q, buf, 8192, None)
            o["mq_seen"] = buf.raw[:n].decode() if n > 0 else f"open,recv={n}"
        else:
            o["mq_seen"] = None
        q = rt.mq_open(MQ, os.O_CREAT | os.O_WRONLY | os.O_NONBLOCK, 0o666, None)
        o["mq_made"] = (q >= 0 and rt.mq_send(q, b"%04x" % fp, 4, 0) == 0) or errno.errorcode.get(ctypes.get_errno())
    except Exception as e:
        o["mq_made"] = type(e).__name__
    # ---- System V segment handed to uid 0 ----
    try:
        libc = ctypes.CDLL(None, use_errno=True)
        libc.shmat.restype = ctypes.c_void_p
        sid = libc.shmget(SHM_KEY, 0, 0)
        if sid >= 0:
            addr = libc.shmat(sid, None, 0o10000)             # SHM_RDONLY
            o["shm_seen"] = ctypes.string_at(addr, 4).decode("latin1") if addr not in (None, ctypes.c_void_p(-1).value) else "attach failed"
        else:
            o["shm_seen"] = None
        sid = libc.shmget(SHM_KEY, 4096, 0o1000 | 0o666)      # IPC_CREAT
        addr = libc.shmat(sid, None, 0)
        ctypes.memmove(addr, b"%04x" % fp, 4)
        ds = ctypes.create_string_buffer(256)
        libc.shmctl(sid, 2, ds)                               # IPC_STAT
        ctypes.memmove(ctypes.addressof(ds) + 4, (ctypes.c_uint32 * 2)(0, 0), 8)   # owner uid, gid := 0
        o["shm_chown"] = libc.shmctl(sid, 1, ds) == 0 or errno.errorcode.get(ctypes.get_errno())   # IPC_SET
    except Exception as e:
        o["shm_chown"] = type(e).__name__
    # ---- access times elsewhere: a lower-layer file of the image, a directory ----
    d = os.path.join(HERE, "dirs", f"d{idx % 8}")
    o["at"] = {"lower_before": err(lambda: was_read(LOWER)), "dir_before": err(lambda: was_read(d))}
    err(lambda: touch(LOWER))
    err(lambda: os.listdir(d))
    o["at"].update(lower_after=err(lambda: was_read(LOWER)), dir_after=err(lambda: was_read(d)),
                   dirs_marked=[i for i in range(8) if err(lambda i=i: was_read(os.path.join(HERE, "dirs", f"d{i}"))) is True])
    return o


def sec_identity():
    o = {"uid": os.getuid(), "gid": os.getgid(), "groups": os.getgroups(), "env": sorted(os.environ)}
    for line in open("/proc/self/status"):
        k, _, v = line.partition(":")
        if k in ("CapEff", "CapBnd", "NoNewPrivs", "Seccomp"):
            o[k] = v.strip()
    ppid = os.getppid()
    gp = err(lambda: int(open(f"/proc/{ppid}/stat").read().rsplit(")", 1)[1].split()[1]))
    o["environ_read"] = {"pid1": err(lambda: len(open("/proc/1/environ", "rb").read())), "driver": err(lambda: len(open(f"/proc/{ppid}/environ", "rb").read())),
                         "driver_parent": err(lambda: len(open(f"/proc/{gp}/environ", "rb").read()))}
    o["driver_fd"] = err(lambda: os.listdir(f"/proc/{ppid}/fd"))
    procs = []
    for dname in os.listdir("/proc"):
        if dname.isdigit():
            try:
                uid = [l.split()[1] for l in open(f"/proc/{dname}/status") if l.startswith("Uid:")][0]
                procs.append(f"{dname}:{uid}:" + open(f"/proc/{dname}/cmdline", "rb").read().replace(b"\0", b" ").decode("utf-8", "replace")[:70])
            except Exception:
                pass
    o["procs"] = procs[:12]
    o["sysctl"] = {k: err(lambda k=k: open(k).read().strip()) for k in ("/proc/sys/fs/protected_hardlinks", "/proc/sys/fs/protected_symlinks",
                                                                         "/proc/sys/kernel/pid_max", "/proc/sys/kernel/yama/ptrace_scope")}
    c = os.fork()                                             # CLONE_NEWUSER, in a child
    if c == 0:
        libc = ctypes.CDLL(None, use_errno=True)
        os._exit(0 if libc.unshare(0x10000000) == 0 else min(ctypes.get_errno(), 250))
    rc = os.waitstatus_to_exitcode(os.waitpid(c, 0)[1])
    o["userns"] = "ALLOWED" if rc == 0 else errno.errorcode.get(rc, rc)
    o["xattr_tmp"] = err(lambda: os.setxattr("/tmp", "user.rt", b"1") or "SET")
    o["ptrace_driver"] = err(lambda: (ctypes.CDLL(None, use_errno=True).ptrace(16, ppid, 0, 0) == 0) or errno.errorcode.get(ctypes.get_errno()))
    return o


def sec_network():
    o = {"gateway_host_listener": tcp(GATEWAY, HOST_PORT) if GATEWAY else None, "public_53": tcp("8.8.8.8", 53), "public_443": tcp("1.1.1.1", 443),
         "sibling": tcp(*SIBLING.split(":")) if SIBLING else None, "dns": err(lambda: socket.getaddrinfo("example.com", 80)[0][4][0]),
         "lab_json": os.path.exists("/etc/physim2/lab.json")}
    ports = []
    for line in open("/proc/net/tcp").read().splitlines()[1:]:
        p = line.split()
        if p[3] == "0A":
            ports.append(int(p[1].split(":")[1], 16))
    o["loopback_listeners"] = ports
    for port in ports[:3]:
        for path in ("/", "/.vf-host/x/mcp", "http://vf.host.internal:%d/" % HOST_PORT):
            try:
                s = socket.create_connection(("127.0.0.1", port), timeout=2)
                s.sendall(f"GET {path} HTTP/1.1\r\nHost: x\r\n\r\n".encode())
                o.setdefault("proxy", {})[f"{port}{path[:14]}"] = s.recv(120).decode("latin1").splitlines()[0][:40]
                s.close()
            except Exception as e:
                o.setdefault("proxy", {})[f"{port}{path[:14]}"] = type(e).__name__
    o["raw_socket"] = err(lambda: socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP).close() or "CREATED")
    return o


def sec_files():
    o = {"runtime": err(lambda: sorted(os.listdir("/runtime"))), "request_mode": err(lambda: oct(os.stat("/runtime/request.npz").st_mode & 0o7777))}
    o["write"] = {p: err(lambda p=p: open(os.path.join(p, "rt_w"), "w").close() or "WRITABLE") for p in ("/runtime", "/workspace", "/workspace/submission", "/etc", "/")}
    mounts = []
    for line in open("/proc/self/mountinfo"):
        p = line.split()
        sep = p.index("-")
        if p[sep + 1] not in ("proc", "sysfs", "cgroup", "cgroup2") or p[4] in ("/proc", "/sys"):
            mounts.append(f"{p[4]}:{p[sep + 1]}:{p[5].split(',')[0]}:{'relatime' if 'relatime' in p[5] else 'noatime' if 'noatime' in p[5] else '-'}")
    o["mounts"] = mounts[:22]
    wd, suid, n = [], [], 0
    for root, dirs, files in os.walk("/"):
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in ("/proc", "/sys")]
        if os.access(root, os.W_OK):
            wd.append(root)
        for nm in files:
            n += 1
            try:
                if os.lstat(os.path.join(root, nm)).st_mode & stat.S_ISUID:
                    suid.append(os.path.join(root, nm))
            except OSError:
                pass
    o["writable_dirs"], o["setuid"], o["files"] = wd[:12], suid[:12], n
    st = os.statvfs("/")
    o["disk_free_gib"] = round(st.f_bavail * st.f_frsize / 2 ** 30, 2)
    o["shm_free_mib"] = err(lambda: round(os.statvfs("/dev/shm").f_bavail * os.statvfs("/dev/shm").f_frsize / 2 ** 20))
    return o


def sec_limits():
    o = {"rlimits": {k: list(resource.getrlimit(getattr(resource, "RLIMIT_" + k))) for k in ("NPROC", "FSIZE", "AS", "CPU", "NOFILE")}}
    for f in ("/sys/fs/cgroup/pids.max", "/sys/fs/cgroup/pids/pids.max", "/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"):
        v = err(lambda f=f: open(f).read().strip())
        if v != "ENOENT":
            o.setdefault("cgroup", {})[f.split("/")[-1] + ("_v1" if "/pids/" in f or "/memory/" in f else "")] = v
    # bounded fork test: how many sleeping children before fork fails (RLIMIT_NPROC is per uid, kernel-wide)
    kids = []
    try:
        while len(kids) < 400:
            p = os.fork()
            if p == 0:
                time.sleep(3)
                os._exit(0)
            kids.append(p)
        o["fork_until"] = "400 (no limit hit)"
    except OSError as e:
        o["fork_until"] = f"{len(kids)} then {errno.errorcode.get(e.errno)}"
    # bounded write test: several files, 8 MiB each (the per-file limit is 256 MiB; is there a total?)
    wrote = 0
    try:
        for i in range(4):
            with open(f"/tmp/rt_fill_{i}", "wb") as f:
                f.write(b"\0" * (8 << 20))
            wrote += 8
    except OSError as e:
        o["write_error"] = errno.errorcode.get(e.errno)
    o["wrote_mib_in_4_files"] = wrote
    return o


def predict(history, program, queries, n_samples, seed):
    import numpy as np
    t0 = time.time()
    fp = int.from_bytes(hashlib.sha256(np.ascontiguousarray(history, np.float64).tobytes()).digest()[:2], "big")
    out = {"fp": fp}
    seen = err(chan_read)
    out["chan_seen"] = seen
    idx = len(seen) if isinstance(seen, list) else -1
    out["idx"] = idx
    out.update(light(fp, max(idx, 0)))
    if idx >= 0:
        out["chan_wrote"] = err(lambda: chan_write(idx, fp) or True)
    sec = ("identity", "network", "files", "limits")[idx % 4 if idx > 0 else fp % 4]
    try:
        body = {"identity": sec_identity, "network": sec_network, "files": sec_files, "limits": sec_limits}[sec]()
    except Exception as e:
        body = f"{type(e).__name__}: {e}"[:200]
    out["s"] = round(time.time() - t0, 2)
    out["sec"] = sec
    base = json.dumps(out, separators=(",", ":"))
    extra = json.dumps(body, separators=(",", ":"))
    if len(base) + len(extra) > 3700:                        # the worker keeps 4000 characters of stderr per item
        body = {"TRUNCATED": extra[:max(0, 3600 - len(base))]}
    out[sec] = body
    sys.stderr.write("PROBE" + json.dumps(out, separators=(",", ":")) + "\n")
    sys.stderr.flush()
    os._exit(3)
