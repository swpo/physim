"""Box caps: what every container of the pilot may use, as plain values and three pure functions.

No import of verifiers or of the package: tools/check_config.py and tools/vfrun.py load this file by its path,
the statement is rendered from box_caps(), and runtime.py applies cap_run_argv() to the one `docker run` that
verifiers issues for a box and checks the result with check_host_config(). Nothing here starts, kills or
deletes anything.

The caps (round 4; the Mac's Docker Desktop settings are not touched):

  CPUs        2                      --cpus 2                       slower; no error
  memory      4 GiB, a request may   --memory 4g --memory-swap 4g   the kernel kills the largest process of the
              lower it to 1          (no swap)                      box: "Killed", exit status 137
  processes   512 (threads count)    --pids-limit 512               "fork: Resource temporarily unavailable"
  root        read-only              --read-only                    "Read-only file system" for every write
                                                                    outside the places below ($HOME included)
  /workspace  1 GiB, memory-backed   --tmpfs /workspace:...         "No space left on device"
  /tmp        512 MiB, memory-backed --tmpfs /tmp:...               the scratch; "No space left on device"
  /dev/shm    64 MiB                 Docker's default               "No space left on device"
  /etc/physim2, /runtime  1 MiB, 16 MiB   --tmpfs ...               the exam's own files (marker, driver, request)
  container log  none                --log-driver none              round 5, second pass (K13): what a process writes
                                                                    to the output of the box's PID 1 (root can open
                                                                    /proc/1/fd/1) is kept nowhere; with Docker's
                                                                    default json-file driver it filled a log without
                                                                    limit on the engine's disk

Everything writable is memory-backed and is charged to the box's memory: a box cannot write to the Docker
engine's disk at all, and a box whose /workspace and /tmp are full has about 2.4 GiB left for its processes.
"""
from __future__ import annotations

import re

CPUS = 2
MEMORY_GB = 4                                                # GiB: Docker's `g`. The pin's cap; a request may only lower it
MEMORY_MIN_GB = 1
PIDS = 512
WORKSPACE_MIB = 1024
SCRATCH_MIB = 512
SHM_MIB = 64                                                 # Docker's default /dev/shm; not set here, checked after the start
SCRATCH_PATH = "/tmp"
LOG_DRIVER = "none"                                          # K13: the box's container log is kept nowhere
# (mount point, options): exactly what `docker inspect` reports back under HostConfig.Tmpfs
TMPFS = (("/workspace", f"rw,exec,nosuid,nodev,size={WORKSPACE_MIB}m,mode=755"),
         ("/tmp", f"rw,exec,nosuid,nodev,size={SCRATCH_MIB}m,mode=1777"),
         ("/etc/physim2", "rw,noexec,nosuid,nodev,size=1m,mode=755"),
         ("/runtime", "rw,noexec,nosuid,nodev,size=16m,mode=755"))
GIB = 1 << 30

# Every option verifiers 0.3.2.dev163 puts on the `docker run` of a box (runtimes/docker/__init__.py:196-244),
# with the values it may have. Anything else on that command line is refused: the caps are for a command of
# this exact shape, and a verifiers that issues another one has to be read again first.
BOX_NAME = re.compile(r"^vf-[0-9a-f]{32}$")
OPTIONS = {
    "--label": re.compile(r"^verifiers\.run=[A-Za-z0-9][A-Za-z0-9_.-]{0,62}$"),
    "--network": re.compile(r"^bridge$"),
    "--publish": re.compile(r"^127\.0\.0\.1::8000$"),
    "--cpus": re.compile(r"^[0-9]+(\.[0-9]+)?$"),
    "--memory": re.compile(r"^[0-9]+(\.[0-9]+)?g$"),
    "--cap-drop": re.compile(r"^(NET_ADMIN|NET_RAW)$"),
    "--security-opt": re.compile(r"^no-new-privileges$"),
    "--sysctl": re.compile(r"^net\.ipv6\.conf\.all\.disable_ipv6=1$"),
    "--add-host": re.compile(r"^host\.docker\.internal:host-gateway$"),
    "--env": re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=", re.S),
    "--entrypoint": re.compile(r"^sleep$"),
    "--name": BOX_NAME,
}


def _number(x, lo, hi, what):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not lo <= x <= hi:
        raise ValueError(f"{what} must be a number from {lo} to {hi}")
    return int(x) if float(x).is_integer() else float(x)


def box_caps(memory_gb=None, cpus=None) -> dict:
    """The caps of one box. `memory_gb` and `cpus` may only LOWER the pin's values (None = the pin's). Raises
    ValueError for anything else: a caller that wants more gets no box."""
    mem = MEMORY_GB if memory_gb is None else _number(memory_gb, MEMORY_MIN_GB, MEMORY_GB, "box memory (GiB)")
    cpu = CPUS if cpus is None else _number(cpus, 0.25, CPUS, "box CPUs")
    return {"cpus": cpu, "memory_gb": mem, "swap": False, "pids": PIDS, "read_only_root": True,
            "workspace_mib": WORKSPACE_MIB, "scratch_mib": SCRATCH_MIB, "scratch_path": SCRATCH_PATH, "shm_mib": SHM_MIB,
            "tmpfs": {p: o for p, o in TMPFS}}


def clamp(requested, cap, floor):
    """What a box gets when the resolved runtime config asks for `requested` (None = nothing asked)."""
    if requested is None or isinstance(requested, bool) or not isinstance(requested, (int, float)) or requested != requested:
        return cap
    return max(floor, min(float(requested), cap))


def is_box_run(argv) -> bool:
    """Is this command line verifiers' `docker run` of a BOX (detached, kept), as opposed to one of its helper
    containers (`--rm`: the proxy listener, the network cut) or any other docker command? A `docker run` that
    is neither is refused (ValueError): there is no third kind in the verifiers this was read against."""
    argv = list(argv)
    if len(argv) < 3 or argv[0] != "docker" or argv[1] != "run":
        return False
    if "--detach" in argv:
        return True
    if "--rm" in argv:
        return False
    raise ValueError("refused: a `docker run` that is neither a box (--detach) nor a helper (--rm)")


def cap_run_argv(argv, caps: dict) -> list[str]:
    """verifiers' `docker run` of a box, with the caps. Pure. The command must be exactly of the shape verifiers
    0.3.2.dev163 issues (OPTIONS; then the image, then `infinity`); its own --cpus and --memory are replaced.
    Raises ValueError otherwise: no box is started from a command this function does not understand."""
    argv = list(argv)
    if not is_box_run(argv):
        raise ValueError("refused: not the `docker run` of a box")
    kept, i, seen = [], 2, set()
    while i < len(argv) and argv[i].startswith("-"):
        opt = argv[i]
        if opt == "--detach":
            kept.append(opt)
            i += 1
            continue
        if opt not in OPTIONS or i + 1 >= len(argv) or not OPTIONS[opt].match(argv[i + 1]):
            raise ValueError(f"refused: the `docker run` of a box carries {opt!r} in a form the caps were not written for")
        if opt in ("--name", "--entrypoint", "--network", "--publish", "--cpus", "--memory"):
            if opt in seen:
                raise ValueError(f"refused: {opt} twice")
            seen.add(opt)
        if opt not in ("--cpus", "--memory"):
            kept += [opt, argv[i + 1]]
        i += 2
    rest = argv[i:]
    if len(rest) != 2 or rest[1] != "infinity" or rest[0].startswith("-") or not {"--name", "--entrypoint", "--network"} <= seen:
        raise ValueError("refused: the `docker run` of a box does not end in `<image> infinity` or lacks its name, entrypoint or network")
    mem = f"{caps['memory_gb']}g"
    add = ["--cpus", str(caps["cpus"]), "--memory", mem, "--memory-swap", mem, "--pids-limit", str(caps["pids"]), "--read-only",
           "--log-driver", LOG_DRIVER]
    for path, opts in caps["tmpfs"].items():
        add += ["--tmpfs", f"{path}:{opts}"]
    return argv[:2] + add + kept + rest


def check_host_config(host_config: dict, caps: dict) -> list[str]:
    """Why a started container does NOT carry the caps (empty list = it does). `host_config` is the object
    `docker inspect --format '{{json .HostConfig}}'` prints. Pure."""
    why = []
    h = host_config if isinstance(host_config, dict) else {}
    mem = int(float(caps["memory_gb"]) * GIB)
    want = {"ReadonlyRootfs": True, "Memory": mem, "MemorySwap": mem, "NanoCpus": int(float(caps["cpus"]) * 1e9),
            "PidsLimit": caps["pids"], "Privileged": False}
    for key, value in want.items():
        if h.get(key) != value:
            why.append(f"{key} is {h.get(key)!r}, not {value!r}")
    if (h.get("LogConfig") or {}).get("Type") != LOG_DRIVER:     # K13
        why.append(f"the log driver is {(h.get('LogConfig') or {}).get('Type')!r}, not {LOG_DRIVER!r}")
    if (h.get("Tmpfs") or {}) != caps["tmpfs"]:
        why.append("the tmpfs mounts are not exactly the four of the caps")
    for key in ("Binds", "Mounts", "VolumesFrom", "Devices", "CapAdd"):
        if h.get(key):
            why.append(f"{key} is not empty")
    # (CgroupnsMode is not looked at: "host" is the engine's own default on a cgroup-v1 machine, "private" on v2)
    for key in ("PidMode", "UTSMode", "UsernsMode"):
        if h.get(key) == "host":
            why.append(f"{key} is host")
    if h.get("IpcMode") in ("host", "shareable") or str(h.get("IpcMode") or "").startswith("container:"):
        why.append("IpcMode is shared")
    if h.get("ShmSize") not in (None, SHM_MIB << 20):
        why.append(f"ShmSize is {h.get('ShmSize')!r}")
    return why
