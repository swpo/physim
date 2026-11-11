"""Private channel from the laboratory process to the task controller (both on the trusted worker).

The laboratory is a separate host process with no handle on the agent's box. The task controller, which runs in
the vf-eval process and holds the verifiers Runtime of that box, listens on a Unix socket and serves two requests:

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
"""
from __future__ import annotations

import asyncio
import json
import posixpath
import secrets
import socket
import tempfile
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
               "cpu_s_per_request": float, "wall_s_per_request": float}
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


class BoxAccess:
    def __init__(self, runtime, artifacts, transport_bytes: int, max_mib: float, workdir: str = "/workspace", limits: dict | None = None):
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

    @property
    def runtime(self):
        runtime = self._runtime()
        if runtime is None:
            raise RuntimeError("the agent's box has closed")
        return runtime

    async def start(self) -> dict:
        self.server = await asyncio.start_unix_server(self.handle, self.path, limit=8192)
        return {"path": self.path, "secret": self.secret, "lab_bearer": self.lab_bearer}

    async def close(self) -> None:
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
            self.frozen = await collect_frozen(self.runtime, self.artifacts, self.transport_bytes, self.max_mib)
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
