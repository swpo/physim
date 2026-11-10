"""Private channel from the laboratory process to the task controller (both on the trusted worker).

The laboratory is a separate host process with no handle on the agent's box. The task controller, which runs in
the vf-eval process and holds the verifiers Runtime of that box, listens on a Unix socket and serves two requests:

    announce {port}   write the laboratory's address into the box (/etc/physim2/lab.json), so that
                      `physim2.Lab()` works from any Python script under any harness
    freeze            collect submission/ from the box NOW with verifiers' own `collect`, apply the public freeze
                      rules on the worker, keep the frozen archive for the grader (the agent called `submit`)

The socket path and a 256-bit secret travel in `trace.state` (never saved in a trace) over verifiers' state
channel; the socket is never reachable from a box. Pattern: PhySim v1, physim/runtime_access.py.
"""
from __future__ import annotations

import asyncio
import json
import secrets
import socket
import tempfile
import weakref
from pathlib import Path

import verifiers.v1 as vf

from .public import _rules

ADDRESS_FILE = "/etc/physim2/lab.json"


async def collect_frozen(runtime, artifacts, transport_bytes: int, max_mib: float) -> dict:
    """Stock collection, then the freeze rules on the worker. Never raises: a submission that cannot be
    collected or frozen is recorded as absent, and the grader scores it as K."""
    workdir = str(getattr(runtime.config, "workdir", None) or "/").rstrip("/")
    root = f"{workdir}/{artifacts[0].source}" if not artifacts[0].source.startswith("/") else artifacts[0].source
    try:
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


class BoxAccess:
    def __init__(self, runtime, artifacts, transport_bytes: int, max_mib: float):
        self._runtime = weakref.ref(runtime)
        self.artifacts, self.transport_bytes, self.max_mib = artifacts, transport_bytes, max_mib
        self.directory = tempfile.TemporaryDirectory(prefix="physim2-io-")
        self.path = str(Path(self.directory.name) / "io.sock")
        self.secret = secrets.token_hex(32)
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
        return {"path": self.path, "secret": self.secret}

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
            async with asyncio.timeout(600):
                request = json.loads(await reader.readline())
                if not secrets.compare_digest(request.pop("secret", ""), self.secret):
                    raise PermissionError("unauthorized")
                if request["op"] == "announce":
                    value = await self.announce(int(request["port"]))
                elif request["op"] == "freeze":
                    value = await self.freeze()
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
        self.address = self.runtime.host_url(f"http://127.0.0.1:{port}").rstrip("/") + "/mcp"
        await self.runtime.write(ADDRESS_FILE, json.dumps({"url": self.address, "tool": "call"}).encode())
        await self.runtime.run(["chmod", "755", "/etc/physim2"], {})
        await self.runtime.run(["chmod", "644", ADDRESS_FILE], {})
        return {"written": ADDRESS_FILE}

    async def freeze(self) -> dict:
        if self.frozen is None or not self.frozen["ok"]:
            self.frozen = await collect_frozen(self.runtime, self.artifacts, self.transport_bytes, self.max_mib)
        f = self.frozen
        return {"ok": f["ok"], "error": f["error"], "files": len(f["manifest"]["files"]),
                "bytes": f["manifest"].get("bytes", 0), "sha256": f["manifest"].get("sha256")}


def request(access: dict, op: str, timeout: float = 620.0, **args):
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
