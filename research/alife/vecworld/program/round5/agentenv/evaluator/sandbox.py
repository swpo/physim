"""evaluator.sandbox -- run an untrusted command with resource limits and, when root, without access to
hidden paths, the network or the evaluator's uid.

Layers (each applied when available; the result records which were):
  rlimits    CPU seconds, address space, file size, core dumps off (always)
  wall       wall-clock timeout; the whole process group is killed
  env        a clean environment (PATH, HOME, thread caps, plus what the caller passes)
  mount ns   `unshare -m` (root only): the directories in `binds` appear under /mnt/<name> (read-only unless
             marked rw), then a tmpfs covers every path in `hide`: hidden files do not exist inside, and the
             process needs no access to the evaluator's own directories
  net ns     `unshare -n` (root only, optional): no network inside
  pid ns     `unshare -p -f --mount-proc` (root only): the process sees no other process of the machine
  uid        `setpriv --reuid/--regid` to an unprivileged user (root only)
In a deployment the same boundary is a container or a Prime sandbox; this module is the local equivalent,
used for the predictor (grading, validation) and for the scripted agent in the end-to-end proof.
"""
from __future__ import annotations

import os
import resource
import shlex
import shutil
import signal
import subprocess
import time

GIB = 1024 ** 3


def capabilities() -> dict:
    root = os.geteuid() == 0
    ok_ns = False
    if root and shutil.which("unshare"):
        try:
            ok_ns = subprocess.run(["unshare", "-m", "-n", "true"], capture_output=True, timeout=10).returncode == 0
        except Exception:
            ok_ns = False
    ok_pid = False
    if ok_ns:
        try:
            ok_pid = subprocess.run(["unshare", "-m", "-p", "-f", "--mount-proc", "true"], capture_output=True,
                                    timeout=10).returncode == 0
        except Exception:
            ok_pid = False
    return {"root": root, "namespaces": ok_ns, "pid_namespace": ok_pid, "setpriv": bool(root and shutil.which("setpriv"))}


_CAPS = None


def caps() -> dict:
    global _CAPS
    if _CAPS is None:
        _CAPS = capabilities()
    return _CAPS


MNT = "/mnt"


def plan(binds) -> dict:
    """binds: [(source_dir, name, 'ro' | 'rw')] -> {name: path as seen inside the sandbox}."""
    ns = caps()["namespaces"]
    return {name: (os.path.join(MNT, name) if ns else src) for src, name, _ in binds}


def run(cmd, cwd, env=None, cpu_seconds=None, wall_seconds=None, memory_gib=None, file_mib=256, hide=(), uid=None,
        gid=None, no_network=False, stdout=None, stderr=None, nice=10, binds=()) -> dict:
    """Run cmd (list) under the layers above; cmd and cwd use the paths of plan(binds).
    Returns {returncode, wall_s, cpu_s, timed_out, layers}."""
    c = caps()
    base_env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/tmp", "OMP_NUM_THREADS": "1",
                "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "PYTHONDONTWRITEBYTECODE": "1",
                "XLA_FLAGS": "--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1",
                "JAX_PLATFORMS": "cpu"}
    base_env.update(env or {})
    layers = {"rlimits": True, "mount_ns": False, "net_ns": False, "pid_ns": False, "uid": None}
    inner = list(cmd)
    if uid is not None and c["setpriv"]:
        inner = ["setpriv", f"--reuid={int(uid)}", f"--regid={int(gid if gid is not None else uid)}", "--clear-groups",
                 "--"] + inner
        layers["uid"] = int(uid)
    hide = [h for h in hide if os.path.exists(h)]
    outer_cwd = cwd
    if c["namespaces"] and (hide or no_network or binds):
        script = ""
        if binds:
            script += f"mount -t tmpfs -o size=1m,mode=0755 none {MNT} && "
            for src, name, mode in binds:
                dst = shlex.quote(os.path.join(MNT, name))
                script += f"mkdir {dst} && mount --bind {shlex.quote(src)} {dst} && "
                if mode != "rw":
                    script += f"mount -o remount,bind,ro {dst} && "
        script += "".join(f"mount -t tmpfs -o size=1m,mode=0555 none {shlex.quote(h)} && " for h in hide)
        script += f"cd {shlex.quote(cwd)} && exec " + " ".join(shlex.quote(x) for x in inner)
        flags = ["-m"] + (["-n"] if no_network else []) + (["-p", "-f", "--mount-proc"] if c["pid_namespace"] else [])
        inner = ["unshare"] + flags + ["--", "sh", "-c", script]
        outer_cwd = "/"
        layers["mount_ns"], layers["net_ns"], layers["pid_ns"] = True, bool(no_network), bool(c["pid_namespace"])
        layers["hidden_paths"], layers["binds"] = len(hide), [n for _, n, _ in binds]

    lim = ["--core=0"]
    if cpu_seconds:
        lim.append(f"--cpu={int(cpu_seconds)}:{int(cpu_seconds)}")     # hard = soft: SIGKILL (a namespace init ignores SIGXCPU)
    if memory_gib:
        lim.append(f"--as={int(memory_gib * GIB)}")
    if file_mib:
        lim.append(f"--fsize={int(file_mib) << 20}")
    pre = None
    if shutil.which("prlimit"):                           # limits set by exec'd tools: no Python runs after fork
        inner = ["nice", "-n", str(int(nice)), "prlimit"] + lim + ["--"] + inner
    else:
        def pre():
            os.nice(nice)
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
            if cpu_seconds:
                resource.setrlimit(resource.RLIMIT_CPU, (int(cpu_seconds), int(cpu_seconds)))
            if memory_gib:
                resource.setrlimit(resource.RLIMIT_AS, (int(memory_gib * GIB), int(memory_gib * GIB)))
            if file_mib:
                resource.setrlimit(resource.RLIMIT_FSIZE, (int(file_mib) << 20, int(file_mib) << 20))

    t0 = time.time()
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    p = subprocess.Popen(inner, cwd=outer_cwd, env=base_env, stdout=stdout or subprocess.DEVNULL,
                         stderr=stderr or subprocess.DEVNULL, stdin=subprocess.DEVNULL, preexec_fn=pre, start_new_session=True)
    timed_out = False
    try:
        p.wait(timeout=wall_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        p.wait()
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    return {"returncode": p.returncode, "wall_s": time.time() - t0,
            "cpu_s": (r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime), "timed_out": timed_out, "layers": layers}
