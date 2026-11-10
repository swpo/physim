"""The laboratory as a verifiers Toolset: ONE tool, `call`, around agentenv's LabService.handle.

Placement: a host process of the trusted worker, one per rollout, started by verifiers (never colocated in
the agent's box; Physim2Task.toolsets refuses any other placement). The process loads the hidden instance named
by the task row's pointer, then removes every token-like variable from its own environment.

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
from . import store as STORE
from ._paths import use_agentenv

MAX_REQUEST_VALUES = 4096 * 512                              # one block of inputs: at most MAX_BLOCK ticks


class LabToolsConfig(vf.ToolsetConfig):
    store: str = ""
    """Instance store on the worker (default: $PHYSIM2_STORE). Never a path inside a box."""


def make_service(hidden: str, name: str, check=None):
    """agentenv's LabService with the operations that needed the agent's files replaced (_check), and with two
    request checks moved in front of anything that runs or is charged (advance, experiment).
    `check(path, final)` asks the task controller (access.BoxAccess.check)."""
    use_agentenv()
    from evaluator.lab_service import MAX_BLOCK, LabService, Rejected

    class VfLabService(LabService):
        def _inputs(self, inputs):
            """A block of inputs as a float array, or a format rejection (round 5 let numpy's own error through,
            which the agent then saw as "infrastructure error")."""
            n_in = self.lab.world.n_in
            try:
                U = np.asarray(inputs, float)
            except (ValueError, TypeError, OverflowError):
                U = None
            if U is None or U.ndim != 2 or U.shape[1] != n_in or not 1 <= U.shape[0] <= MAX_BLOCK or not np.all(np.isfinite(U)):
                raise Rejected(f"format: inputs must be finite numbers with shape (T, {n_in}), 1 <= T <= {MAX_BLOCK}")
            return U

        def advance(self, inputs=None, n=None):
            return super().advance(inputs=None if inputs is None else self._inputs(inputs), n=n)

        def experiment(self, label, inputs=None, n=None):
            # everything about the block is checked BEFORE the reset is charged
            if inputs is None:
                if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= MAX_BLOCK:
                    raise Rejected(f"format: n must be an integer in [1, {MAX_BLOCK}]")
            else:
                inputs = self._inputs(inputs)
            return super().experiment(label, inputs=inputs, n=n)

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
        check = (lambda path, final: ACCESS.request(chan, "check", path=path, final=final)) if chan else None
        self.service = make_service(hidden, state.get("rollout") or f"lab-{os.getpid()}", check)
        if json.load(open(os.path.join(hidden, "instance.json")))["secret_commitment"] != task.secret_commitment:
            raise RuntimeError("the stored instance is not the one the task row commits to")
        self.scrubbed = STORE.scrub_environment()            # hole 5: after loading, no token stays in this process
        port_file = os.environ.get("MCP_PORT_FILE")
        if chan and port_file:
            await asyncio.to_thread(ACCESS.request, chan, "announce", port=int(Path(port_file).read_text()))
        with open(os.path.join(self.service.dir, "process.json"), "w") as f:
            json.dump({"pid": os.getpid(), "scrubbed_variables": self.scrubbed, "announced": bool(chan and port_file),
                       "token_values_left_in_environ": STORE.environ_still_has(self.scrubbed),
                       "token_like_names_left_in_os_environ": STORE.token_like(os.environ)}, f)

    @vf.tool
    async def call(self, op: str, args: dict | None = None) -> str:
        """The laboratory of the real (hidden) world: one call = one operation. Returns JSON
        {"ok": true, "result": ...} or {"ok": false, "error": "...", "kind": "..."}; a rejected operation ran
        nothing and cost nothing.
        op "card": {} -> the public declaration (sizes, budgets, exam, limits).
        op "usage": {} -> ticks and nats used and left, attempts, submitted.
        op "reset": {"label": str|int} -> o(0), a list of n_obs numbers; starts a new episode (costs reset_cost ticks).
        op "advance": {"inputs": [[n_in numbers] x T]} or {"n": T} -> T observations after each tick.
        op "experiment": {"label": ..., "inputs": [...] or "n": T} -> T + 1 observations, row 0 is o(0).
        op "validate": {"path": "submission"} -> runs the public check in your box (physim2/validate.py: format,
        limits, same seed -> same samples; no accuracy feedback) and returns its report.
        op "submit": {"path": "submission"} -> the same check; if it passes, submission/ is frozen as it is now
        and the laboratory closes ("accepted": true). If it fails nothing is frozen and the laboratory stays open.
        From Python in the workspace the same operations are `physim2.Lab()` methods (see TASK.md)."""
        if self.service is None:
            return NEUTRAL
        if not isinstance(op, str) or (args is not None and not isinstance(args, dict)):
            return json.dumps({"ok": False, "error": "format: op must be a string and args an object", "kind": "request"})
        rep = await asyncio.to_thread(self.service.handle, {"op": op, "args": args or {}})
        return json.dumps(plain(rep), allow_nan=False)


if __name__ == "__main__":
    # The laboratory answers on this machine's loopback, on a port the system chooses, whatever the environment
    # of the worker says: verifiers' server would otherwise bind $MCP_HOST and $MCP_PORT (mcp/server.py:278-283).
    os.environ["MCP_HOST"] = "127.0.0.1"
    os.environ.pop("MCP_PORT", None)
    LabTools.run()
