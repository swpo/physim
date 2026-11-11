"""The laboratory as a verifiers Toolset: ONE tool, `call`, around agentenv's LabService.handle.

Placement: a host process of the trusted worker, one per rollout, started by verifiers (never colocated in
the agent's box; Physim2Task.toolsets refuses any other placement). The process loads the hidden instance named
by the task row's pointer, then removes every token-like variable from its own environment.

Round 4: the listener needs a bearer. Every HTTP request must carry `Authorization: Bearer <secret>`, a 256-bit
value of this rollout that arrives over verifiers' state channel and is kept in memory only (bearer.py); the
MCP library's DNS-rebinding protection is on, with this server's own `127.0.0.1:<port>` as the only allowed
Host (LabTools._serve). A box does not hold the bearer: its proxy inside vf-eval adds it (runtime.py).

Budgets (ticks, nats, attempts) are enforced inside LabService under its own lock, never in verifiers' shared
state: this Toolset declares no state fields, so no call pulls or pushes state (verifiers replaces the whole
state on a push, last writer wins: mcp/server.py:221-247). Internal errors never reach the agent: LabService
replies "infrastructure error" without detail and logs the traceback on the worker; anything raised outside it
is replaced by a neutral reply here (the wrapper of PhySim v1, physim/taskset.py:308-338).
"""
from __future__ import annotations

import asyncio
import json
import os
import time
from functools import wraps
from pathlib import Path

import numpy as np
import verifiers.v1 as vf

from . import access as ACCESS
from . import bearer as BEARER
from . import store as STORE
from ._paths import use_agentenv

MAX_REQUEST_VALUES = 4096 * 512                              # one block of inputs: at most MAX_BLOCK ticks


class LabToolsConfig(vf.ToolsetConfig):
    store: str = ""
    """Instance store on the worker (default: $PHYSIM2_STORE). Never a path inside a box."""


USAGE = {"advance": "usage: advance(inputs) with inputs an array (T, {n_in}) of finite numbers, 1 <= T <= {max_block}, or advance(n) "
                    "with an integer n for n ticks without input",
         "experiment": "usage: experiment(label, inputs) with inputs an array (T, {n_in}) of finite numbers, 1 <= T <= {max_block}, or "
                       "experiment(label, n) with an integer n for n ticks without input"}


def make_service(hidden: str, name: str, check=None, status=None):
    """agentenv's LabService with the operations that needed the agent's files replaced (_check), and with two
    request checks moved in front of anything that runs or is charged (advance, experiment).
    `check(path, final)` asks the task controller (access.BoxAccess.check); `status()` asks it for the run's
    clocks, which `usage` then reports next to the laboratory's own budgets (ruling E4)."""
    use_agentenv()
    from evaluator.lab_service import MAX_BLOCK, LabService, Rejected

    class VfLabService(LabService):
        def _usage_line(self, op):
            return USAGE[op].format(n_in=self.lab.world.n_in, max_block=MAX_BLOCK)

        def _inputs(self, inputs, op="advance"):
            """A block of inputs as a float array, or a format rejection with one line of usage (round 5 let
            numpy's own error through, which the agent then saw as "infrastructure error")."""
            n_in = self.lab.world.n_in
            try:
                U = np.asarray(inputs, float)
            except (ValueError, TypeError, OverflowError):
                U = None
            if U is None or U.ndim != 2 or U.shape[1] != n_in or not 1 <= U.shape[0] <= MAX_BLOCK or not np.all(np.isfinite(U)):
                raise Rejected("format: " + self._usage_line(op))
            return U

        def _block(self, op, inputs, n):
            """(inputs, n) of advance or experiment, checked: exactly one of them, in the documented form."""
            if inputs is None:
                if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= MAX_BLOCK:
                    raise Rejected("format: " + self._usage_line(op))
                return None, n
            if n is not None:
                raise Rejected("format: " + self._usage_line(op))
            return self._inputs(inputs, op), None

        def advance(self, inputs=None, n=None):
            inputs, n = self._block("advance", inputs, n)
            return super().advance(inputs=inputs, n=n)

        def experiment(self, label, inputs=None, n=None):
            # everything about the block is checked BEFORE the reset is charged
            inputs, n = self._block("experiment", inputs, n)
            return super().experiment(label, inputs=inputs, n=n)

        def usage(self):
            u = super().usage()
            if status is not None:                           # the run's own clocks, from the task controller
                try:
                    got = status()
                    u.update({k: got[k] for k in ("seconds_elapsed", "seconds_left", "turns_used", "turns_left", "context_tokens_used",
                                                  "context_tokens_left") if k in got})
                except Exception:
                    pass
            return u

        def _check(self, path, final: bool):
            # head: verbatim from LabService._check (attempt caps and counters)
            if self.state["submitted"]:
                return {"ok": True, "accepted": True, "finalized": True}
            kind = "submissions" if final else "validations"
            cap = self.cfg["validation"]["max_attempts"]
            if cap is not None and self.state[kind] >= cap:
                raise Rejected(f"{kind} attempt limit ({cap}) reached", "budget")
            if not isinstance(path, str) or not 0 < len(path) <= 1024:
                raise Rejected("format: path must be a string")
            self.state[kind] += 1
            if check is None:
                return {"ok": False, "stage": "artifact", "error": "no channel to the box", "finalized": False, "accepted": False}
            got = check(path, final)
            rep, frozen = dict(got["report"]), got.get("frozen")
            if final and rep["ok"] and not (frozen and frozen.get("ok")):
                rep = {"ok": False, "stage": "artifact", "error": (frozen or {}).get("error") or "the submission could not be collected"}
            if final and rep["ok"]:
                self.state["submitted"] = True
                json.dump({"files": frozen.get("files"), "bytes": frozen.get("bytes"), "sha256": frozen.get("sha256"),
                           "usage": self.lab.usage(), "time": time.time()}, open(os.path.join(self.dir, "frozen.json"), "w"), indent=1)
                rep.update(files=frozen.get("files"), sha256=frozen.get("sha256"))
            rep.update(finalized=self.state["submitted"], accepted=bool(final and rep["ok"]))
            return rep

    return VfLabService(hidden, "", "/nonexistent-workspace", name)


def plain(o):
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, dict):
        return {str(k): plain(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [plain(v) for v in o]
    if isinstance(o, np.generic):
        return o.item()
    return o


NEUTRAL = json.dumps({"ok": False, "error": "infrastructure error; the evaluator must intervene", "kind": "infrastructure"})


class LabTools(vf.Toolset[LabToolsConfig]):
    TOOL_PREFIX = "lab"

    def __init__(self, config):
        super().__init__(config)
        self.service = None
        self.scrubbed: list[str] = []
        self.bearer: str | None = None                       # round 4: set by setup_task from the state channel; never written anywhere

    def _with_state(self, fn):
        @wraps(fn)
        async def neutral(*args, **kwargs):
            try:
                return await fn(*args, **kwargs)
            except Exception:                                # nothing raised here may become MCP error text
                return NEUTRAL
        return super()._with_state(neutral)

    async def setup_task(self, task) -> None:
        """Load the instance the row points to; announce the address into the box; drop tokens."""
        from verifiers.v1.mcp.server import _channel_request
        url, secret, _ = self._state_channel()
        state = (await _channel_request("GET", url, secret, client=self._state_client)).json() if url else {}
        hidden = STORE.hidden_dir(STORE.store_root(self.config.store), task.instance_id)
        chan = state.get("access") or None
        # round 4: the bearer every request to this server must carry. It comes over the state channel only
        # (trace.state is never saved); the copy handed to the controller's client below does not hold it.
        self.bearer = (chan or {}).get("lab_bearer")
        if chan:
            chan = {k: chan[k] for k in ("path", "secret") if k in chan}
        check = (lambda path, final: ACCESS.request(chan, "check", path=path, final=final)) if chan else None
        status = (lambda: ACCESS.request(chan, "status", timeout=20.0)) if chan else None
        self.service = make_service(hidden, state.get("rollout") or f"lab-{os.getpid()}", check, status)
        if json.load(open(os.path.join(hidden, "instance.json")))["secret_commitment"] != task.secret_commitment:
            raise RuntimeError("the stored instance is not the one the task row commits to")
        self.scrubbed = STORE.scrub_environment()            # hole 5: after loading, no token stays in this process
        port_file = os.environ.get("MCP_PORT_FILE")
        if chan and port_file:
            await asyncio.to_thread(ACCESS.request, chan, "announce", port=int(Path(port_file).read_text()))
        with open(os.path.join(self.service.dir, "process.json"), "w") as f:
            json.dump({"pid": os.getpid(), "scrubbed_variables": self.scrubbed, "announced": bool(chan and port_file),
                       "bearer_required": BEARER.well_formed(self.bearer),      # yes or no, never the value
                       "token_values_left_in_environ": STORE.environ_still_has(self.scrubbed),
                       "token_like_names_left_in_os_environ": STORE.token_like(os.environ)}, f)

    @vf.tool
    async def call(self, op: str, args: dict | None = None) -> str:
        """The laboratory of the real (hidden) world: one call = one operation. Returns JSON
        {"ok": true, "result": ...} or {"ok": false, "error": "...", "kind": "..."}; a rejected operation ran
        nothing and cost nothing.
        op "card": {} -> the public declaration (sizes, budgets, exam, limits).
        op "usage": {} -> ticks and nats used and left, attempts, submitted; and of this run: seconds_elapsed,
        seconds_left, turns_used, turns_left.
        op "reset": {"label": str|int} -> o(0), a list of n_obs numbers; starts a new episode (costs reset_cost ticks).
        op "advance": {"inputs": [[n_in numbers] x T]} or {"n": T} (T ticks without input) -> T observations.
        op "experiment": {"label": ..., "inputs": [[n_in numbers] x T]} or {"label": ..., "n": T} -> T + 1
        observations, row 0 is o(0).
        op "validate": {"path": "submission"} -> runs your predictor in your box the way the grader will (a clean
        copy of submission/ alone, an unprivileged user that cannot read /workspace; format, limits, same seed ->
        same samples; no accuracy feedback) and returns the report.
        op "submit": {"path": "submission"} -> the same check; if it passes, submission/ is frozen as it is now,
        the laboratory closes and YOUR RUN ENDS ("accepted": true). If it fails nothing is frozen and the
        laboratory stays open. Without a submit, submission/ is graded as it is when the run ends.
        From Python in the workspace the same operations are `physim2.Lab()` methods (see TASK.md); only that
        client saves every reply to /workspace/lab_log.jsonl."""
        if self.service is None:
            return NEUTRAL
        if not isinstance(op, str) or (args is not None and not isinstance(args, dict)):
            return json.dumps({"ok": False, "error": "format: op must be a string and args an object", "kind": "request"})
        rep = await asyncio.to_thread(self.service.handle, {"op": op, "args": args or {}})
        return json.dumps(plain(rep), allow_nan=False)

    # ---- round 4: the listener. verifiers' own _serve (mcp/server.py:267-338) answers anybody who reaches the
    #      port and switches the MCP library's DNS-rebinding protection off. This one is the same sequence
    #      (bind, report the port, set up, serve) with three differences: the address is 127.0.0.1 whatever the
    #      environment says, every request needs the rollout's bearer (bearer.guard), and the protection is on
    #      with this server's own address as the only allowed Host. Without a bearer nothing is served. ----
    def _serve(self) -> None:
        import socket

        import uvicorn
        from mcp.server.mcpserver import MCPServer
        from mcp.server.transport_security import TransportSecuritySettings
        from verifiers import __version__
        from verifiers.v1.mcp.server import STATE_TIMEOUT, _die_with_parent

        _die_with_parent()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 0))                          # loopback, a port the system chooses: never MCP_HOST or MCP_PORT
        port = sock.getsockname()[1]
        port_file = os.environ.get("MCP_PORT_FILE")
        if port_file:
            Path(port_file).write_text(str(port))

        async def serve() -> None:
            import httpx
            try:
                async with self._exit_stack, httpx.AsyncClient(timeout=STATE_TIMEOUT) as client:
                    self._state_client = client
                    await self.setup()
                    state_url, secret, _ = self._state_channel()
                    await self._setup_task_from_channel(state_url, secret)
                    if not BEARER.well_formed(self.bearer):
                        raise RuntimeError("the laboratory was given no bearer over the state channel: it serves nothing")
                    security = TransportSecuritySettings(enable_dns_rebinding_protection=True,
                                                         allowed_hosts=[f"127.0.0.1:{port}"], allowed_origins=[])
                    mcp = MCPServer(self.server_name or type(self).__name__, version=__version__)
                    self.register(mcp)
                    app = BEARER.guard(mcp.streamable_http_app(json_response=True, stateless_http=True,
                                                               transport_security=security), self.bearer)
                    server = uvicorn.Server(uvicorn.Config(app, log_level="critical", access_log=False))
                    await server.serve(sockets=[sock])
            finally:
                self._state_client = None

        asyncio.run(serve())


if __name__ == "__main__":
    # The laboratory answers on this machine's loopback, on a port the system chooses, whatever the environment
    # of the worker says (LabTools._serve binds 127.0.0.1:0 itself; the two lines stay as a second lock).
    os.environ["MCP_HOST"] = "127.0.0.1"
    os.environ.pop("MCP_PORT", None)
    LabTools.run()
