"""Private channel from the laboratory process to the task controller (both on the trusted worker).

The laboratory is a separate host process with no handle on the agent's box. The task controller, which runs in
the vf-eval process and holds the verifiers Runtime of that box, listens on a Unix socket and serves three requests:

    status {}         the run's own clocks for `lab.usage()` (ruling E4): seconds elapsed and left of the
                      wall-time limit, turns used and left of the turn limit (counted on the trace, here)

    announce {port}   write the laboratory's address into the box (/etc/physim2/lab.json), so that
                      `physim2.Lab()` works from any Python script under any harness
    check {path, final}
                      run the public validator (physim2/validate.py: freeze rules, then the three example calls
                      through the grader's driver) IN THE AGENT'S BOX and return its report. final (the agent
                      called `submit`): if the report is good, collect submission/ from the box NOW with
                      verifiers' own `collect`, apply the freeze rules on the worker and keep the frozen archive
                      for the grader.

The report of `check` comes from a box in which the agent is root: it is feedback FOR the agent (round 5's
"validate before you freeze", so that a submit of a broken predictor is refused and the laboratory stays open),
never evidence for the grader. The grader repeats the three calls in the verifier box (grading.validate).

The socket path and a 256-bit secret travel in `trace.state` (never saved in a trace) over verifiers' state
channel; the socket is never reachable from a box. Pattern: PhySim v1, physim/runtime_access.py.

Round 4: the same dictionary also carries the laboratory's bearer (`lab_bearer`, bearer.py), drawn here per
rollout. The laboratory reads it over the state channel and answers no request without it; at `announce` the
box's own proxy, inside this process, is told to put it on what it forwards to the laboratory's port
(runtime.set_lab_bearer). It is never written into a box, a file, a log or a command line.

CHECKPOINTS (round 4, ruling E1: whatever is in submission/ when the run ends is graded, however it ends).
verifiers runs a task's finalize, and with it the final collection, only when the rollout did not fail. For a
run that fails (the harness dies, the model route breaks) the controller therefore keeps the last frozen copy
of submission/ it could take while the run was alive: the baseline at setup, then one before every model call
(the task's stop hook asks for it) and one every `checkpoint_s` seconds, each only when a cheap fingerprint of
the directory changed. The newest one is kept in memory and, as one tar archive that the freeze rules wrote
(regular files only), in the run's folder of the store: <store>/<instance>/captures/<rollout>/checkpoint.tar
with checkpoint.json. The env physim2_verifier grades that copy when a run failed.
"""
from __future__ import annotations

import asyncio
import io
import json
import os
import posixpath
import secrets
import socket
import tarfile
import tempfile
import time
import weakref
from pathlib import Path

import verifiers.v1 as vf

from . import bearer as BEARER
from . import runtime as RUNTIME
from .grading import ROUTE_ENV, require_container
from .public import _rules

ADDRESS_FILE = "/etc/physim2/lab.json"


async def collect_frozen(runtime, artifacts, transport_bytes: int, max_mib: float) -> dict:
    """Stock collection, then the freeze rules on the worker. Never raises: a submission that cannot be
    collected or frozen is recorded as absent, and the grader scores it as K."""
    workdir = str(getattr(runtime.config, "workdir", None) or "/").rstrip("/")
    root = f"{workdir}/{artifacts[0].source}" if not artifacts[0].source.startswith("/") else artifacts[0].source
    try:
        require_container(runtime)
        got = await vf.collect(runtime, artifacts, max_bytes=transport_bytes, sweep=False)
        raw = got.get(root)
        err0 = None
    except Exception as e:                                   # tooling in the agent's box, size, a dead box
        raw, err0 = None, f"collection failed ({type(e).__name__})"
    try:
        frozen, man, err = _rules.freeze(raw, root, max_mib)
    except Exception as e:
        frozen, man, err = None, {"files": [], "bytes": 0}, f"freeze failed ({type(e).__name__})"
    return {"root": root, "archive": frozen, "manifest": man, "error": err0 or err, "ok": frozen is not None}


REPORT_KEYS = {"ok": bool, "stage": str, "error": str, "note": str, "files": int, "cpu_s": float, "wall_s": float,
               "cpu_s_per_request": float, "wall_s_per_request": float, "as_graded": bool, "grading": str,
               "package_changed_files": int}
VALIDATE = ("import json, sys\n"
            "sys.path.insert(0, sys.argv[1])\n"
            "import physim2.validate as V\n"
            "print(json.dumps(V.check(sys.argv[2]), default=str))\n")


def clean_report(text: str) -> dict:
    """The validator's last output line as a small, typed report (the box is the agent's: take nothing else)."""
    try:
        raw = json.loads(text.strip().splitlines()[-1])
        assert isinstance(raw, dict)
    except Exception:
        return {"ok": False, "stage": "validator", "error": "the validator in the box returned no report"}
    out = {}
    for k, typ in REPORT_KEYS.items():
        v = raw.get(k)
        if typ is bool:
            if k in raw:
                out[k] = v is True
        elif typ is str and isinstance(v, str):
            out[k] = v[:6000]
        elif typ in (int, float) and isinstance(v, (int, float)) and not isinstance(v, bool) and v == v and abs(v) < 1e12:
            out[k] = typ(v)
    out.setdefault("ok", False)
    return out


FINGERPRINT = ("cd {root} 2>/dev/null && find . -xdev \\( -type f -o -type l \\) -printf '%s %T@ %p\\n' 2>/dev/null | sort | sha256sum "
               "|| echo absent")


def frozen_files(files: dict, root: str, max_mib: float) -> dict:
    """The frozen form (as collect_frozen returns it) of files this package made itself: {name: bytes} below
    `root`. Used for the baseline, which is known without asking the box."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        for nm in sorted(files):
            ti = tarfile.TarInfo(f"{root.strip('/')}/{nm}")
            ti.size = len(files[nm])
            tar.addfile(ti, io.BytesIO(files[nm]))
    frozen, man, err = _rules.freeze(buf.getvalue(), root, max_mib)
    return {"root": root, "archive": frozen, "manifest": man, "error": err, "ok": frozen is not None}


def write_checkpoint(folder: str, frozen: dict, meta: dict) -> None:
    """The newest frozen copy as <folder>/checkpoint.tar + checkpoint.json. Each file is written beside its
    place and then put in place in one step (the laboratory's state.json is kept the same way), so a reader
    never sees half a file; the archive goes first and the description names the archive's hash."""
    import hashlib
    os.makedirs(folder, mode=0o700, exist_ok=True)
    raw = frozen["archive"]
    for name, data in (("checkpoint.tar", raw),
                       ("checkpoint.json", json.dumps(dict(meta, root=frozen["root"], manifest=frozen["manifest"],
                                                           archive_sha256=hashlib.sha256(raw).hexdigest(), archive_bytes=len(raw)),
                                                      indent=1).encode())):
        tmp = os.path.join(folder, name + ".tmp")
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, os.path.join(folder, name))


def read_checkpoint(folder: str, max_mib: float) -> dict | None:
    """The checkpoint of a run as a frozen dict, or None. The archive is read from the worker's own store and
    checked again: its hash must be the recorded one and it must pass the freeze rules unchanged."""
    import hashlib
    try:
        with open(os.path.join(folder, "checkpoint.json")) as f:
            meta = json.load(f)
        with open(os.path.join(folder, "checkpoint.tar"), "rb") as f:
            raw = f.read(int(max_mib * _rules.MIB) + (64 << 20))
        if hashlib.sha256(raw).hexdigest() != meta["archive_sha256"]:
            return None
        frozen, man, err = _rules.freeze(raw, meta["root"], max_mib)
        if frozen is None or man.get("sha256") != meta["manifest"].get("sha256"):
            return None
        return {"root": meta["root"], "archive": frozen, "manifest": man, "error": None, "ok": True,
                "meta": {k: meta.get(k) for k in ("source", "turn", "time", "n")}}
    except Exception:
        return None


class BoxAccess:
    def __init__(self, runtime, artifacts, transport_bytes: int, max_mib: float, workdir: str = "/workspace", limits: dict | None = None,
                 *, trace=None, max_turns: int | None = None, wall_s: float | None = None, capture_dir: str | None = None,
                 checkpoint_s: float = 30.0):
        self._runtime = weakref.ref(runtime)
        self.artifacts, self.transport_bytes, self.max_mib = artifacts, transport_bytes, max_mib
        self.workdir = workdir
        self.check_timeout = 3 * float((limits or {}).get("wall_seconds") or 60) + 120.0
        self.directory = tempfile.TemporaryDirectory(prefix="physim2-io-")
        self.path = str(Path(self.directory.name) / "io.sock")
        self.secret = secrets.token_hex(32)
        self.lab_bearer = BEARER.new_secret()                # round 4: the laboratory's bearer of this rollout (memory only)
        self.server = None
        self.frozen: dict | None = None                      # set by `freeze`; the grader's copy from then on
        self.address: str | None = None
        # ---- the run's clocks (status) and the checkpoints (ruling E1) ----
        self._trace = weakref.ref(trace) if trace is not None else (lambda: None)
        self.max_turns, self.wall_s, self.t0 = max_turns, wall_s, time.time()
        self.capture_dir, self.checkpoint_s = capture_dir, float(checkpoint_s)
        self.checkpointed: dict | None = None                # the newest frozen copy taken while the run was alive
        self.checkpoints = {"taken": 0, "unchanged": 0, "failed": 0, "last_source": None}
        self._fingerprint: str | None = None
        self._lock = asyncio.Lock()
        self._ticker: asyncio.Task | None = None
        self._closed = False

    @property
    def runtime(self):
        runtime = self._runtime()
        if runtime is None:
            raise RuntimeError("the agent's box has closed")
        return runtime

    async def start(self) -> dict:
        self.server = await asyncio.start_unix_server(self.handle, self.path, limit=8192)
        if self.checkpoint_s > 0:
            self._ticker = asyncio.create_task(self._tick())
        return {"path": self.path, "secret": self.secret, "lab_bearer": self.lab_bearer}

    # ---- the run's clocks ----
    def status(self) -> dict:
        """Seconds and turns, used and left, of THIS run (ruling E4). Turns are the trace's own count of model
        replies; the wall clock starts with the agent's phase (verifiers' deadline starts at the same moment)."""
        tr = self._trace()
        start = getattr(getattr(getattr(tr, "timing", None), "agent", None), "start", None) or self.t0
        elapsed = max(0.0, time.time() - float(start))
        turns = int(getattr(tr, "num_turns", 0) or 0) if tr is not None else None
        return {"seconds_elapsed": round(elapsed, 1),
                "seconds_left": None if self.wall_s is None else round(max(0.0, float(self.wall_s) - elapsed), 1),
                "turns_used": turns,
                "turns_left": None if self.max_turns is None or turns is None else max(0, int(self.max_turns) - turns)}

    # ---- checkpoints ----
    def keep(self, frozen: dict, source: str) -> None:
        """Make `frozen` (ok) the newest checkpoint: in memory and in the run's folder of the store."""
        tr = self._trace()
        self.checkpointed = frozen
        self.checkpoints["taken"] += 1
        self.checkpoints["last_source"] = source
        if self.capture_dir:
            try:
                write_checkpoint(self.capture_dir, frozen, {"source": source, "time": time.time(), "n": self.checkpoints["taken"],
                                                            "turn": int(getattr(tr, "num_turns", 0) or 0) if tr is not None else None})
            except Exception:
                self.checkpoints["failed"] += 1

    async def checkpoint(self, source: str) -> bool:
        """Take a frozen copy of submission/ if it changed since the last one. Never raises; never waits long."""
        if self._closed or (self.frozen is not None and self.frozen.get("ok")):
            return False                                     # after an accepted submit the submitted copy stands
        try:
            async with self._lock, asyncio.timeout(120):
                runtime = self._runtime()
                if runtime is None or self._closed:
                    return False
                require_container(runtime)
                root = posixpath.join(self.workdir, self.artifacts[0].source)
                r = await runtime.run(["sh", "-c", FINGERPRINT.format(root=root)], {})
                mark = (r.stdout or "").strip()[:200]
                if mark and mark == self._fingerprint:
                    self.checkpoints["unchanged"] += 1
                    return False
                got = await collect_frozen(runtime, self.artifacts, self.transport_bytes, self.max_mib)
                if not got["ok"]:                            # an empty or unfreezable directory: the older copy stands
                    self.checkpoints["failed"] += 1
                    self._fingerprint = mark or None
                    return False
                if self.frozen is not None and self.frozen.get("ok"):
                    return False
                self._fingerprint = mark or None
                self.keep(got, source)
                return True
        except Exception:
            self.checkpoints["failed"] += 1
            return False

    async def _tick(self) -> None:
        """The timer behind the checkpoints: ends with the controller, with the box, or after three failures in
        a row (a rollout that failed never reaches finalize, so nothing else would end it)."""
        bad = 0
        try:
            while not self._closed and bad < 3:
                await asyncio.sleep(self.checkpoint_s)
                if self._closed or self._runtime() is None or getattr(self._runtime(), "stopped", False):
                    return
                before = self.checkpoints["failed"]
                await self.checkpoint("timer")
                bad = bad + 1 if self.checkpoints["failed"] > before else 0
        except asyncio.CancelledError:
            return
        except Exception:
            return

    async def close(self) -> None:
        self._closed = True
        if self._ticker is not None:
            self._ticker.cancel()
            self._ticker = None
        if self.server is not None:
            self.server.close()
            try:
                await asyncio.wait_for(self.server.wait_closed(), 5)
            except Exception:
                pass
            self.server = None
        self.directory.cleanup()

    async def handle(self, reader, writer):
        try:
            async with asyncio.timeout(self.check_timeout + 600):
                request = json.loads(await reader.readline())
                if not secrets.compare_digest(request.pop("secret", ""), self.secret):
                    raise PermissionError("unauthorized")
                if request["op"] == "announce":
                    value = await self.announce(int(request["port"]))
                elif request["op"] == "status":
                    value = self.status()
                elif request["op"] == "check":
                    value = await self.check(str(request["path"]), bool(request["final"]))
                else:
                    raise ValueError("unknown operation")
                response = {"value": value}
        except Exception as exc:
            response = {"error": type(exc).__name__}
        try:
            writer.write(json.dumps(response).encode() + b"\n")
            await writer.drain()
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass

    async def announce(self, port: int) -> dict:
        # the same translation verifiers applies to the tool URL it hands to the harness (mcp/launch.py:457-460)
        require_container(self.runtime)
        if isinstance(port, bool) or not 0 < port < 65536:
            raise ValueError("not a port")
        # round 4: before the address reaches the box, its proxy learns the bearer for exactly this port
        RUNTIME.set_lab_bearer(self.runtime, port, self.lab_bearer)
        self.address = self.runtime.host_url(f"http://127.0.0.1:{port}").rstrip("/") + "/mcp"
        await self.runtime.write(ADDRESS_FILE, json.dumps({"url": self.address, "tool": "call"}).encode())
        await self.runtime.run(["chmod", "755", "/etc/physim2"], {})
        await self.runtime.run(["chmod", "644", ADDRESS_FILE], {})
        return {"written": ADDRESS_FILE}

    async def check(self, path: str, final: bool) -> dict:
        """{"report": the in-box validator's report, "frozen": None | {ok, error, files, bytes, sha256}}."""
        if final and posixpath.normpath(posixpath.join(self.workdir, path)) != posixpath.join(self.workdir, self.artifacts[0].source):
            return {"report": {"ok": False, "stage": "artifact", "error": "format: only submission/ is collected; copy your "
                               "directory there first (physim2.Lab().submit(path) does it)"}, "frozen": None}
        try:
            require_container(self.runtime)
            async with asyncio.timeout(self.check_timeout):
                # ROUTE_ENV: in the agent's box too the predictor then runs as the box's unprivileged user (the
                # uid setup wrote into /etc/physim2/predictor_uid, from the reserved range)
                r = await self.runtime.run(["python3", "-B", "-c", VALIDATE, self.workdir, path], dict(ROUTE_ENV))
            report = clean_report(r.stdout)
        except TimeoutError:
            report = {"ok": False, "stage": "validator", "error": "the validator in the box did not finish in time"}
        except Exception as e:
            report = {"ok": False, "stage": "validator", "error": f"the validator could not run in the box ({type(e).__name__})"}
        if not final or not report["ok"]:
            return {"report": report, "frozen": None}
        if self.frozen is None or not self.frozen["ok"]:
            async with self._lock:                           # never beside a checkpoint's collection
                self.frozen = await collect_frozen(self.runtime, self.artifacts, self.transport_bytes, self.max_mib)
            if self.frozen["ok"]:
                self.keep(self.frozen, "accepted submit")    # a run that fails after its submit is graded on this copy
        f = self.frozen
        return {"report": report, "frozen": {"ok": f["ok"], "error": f["error"], "files": len(f["manifest"]["files"]),
                                             "bytes": f["manifest"].get("bytes", 0), "sha256": f["manifest"].get("sha256")}}


def request(access: dict, op: str, timeout: float = 1800.0, **args):
    """Blocking client, used by the laboratory process."""
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as c:
        c.settimeout(timeout)
        c.connect(access["path"])
        c.sendall(json.dumps(dict(args, secret=access["secret"], op=op)).encode() + b"\n")
        with c.makefile("rb") as stream:
            raw = stream.readline(1 << 20)
    rep = json.loads(raw)
    if "error" in rep:
        raise RuntimeError(f"task controller: {rep['error']}")
    return rep["value"]
