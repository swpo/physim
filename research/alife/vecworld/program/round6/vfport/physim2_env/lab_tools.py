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


def make_service(hidden: str, name: str, freeze=None):
    """agentenv's LabService with the two operations that needed the agent's files replaced (see _check)."""
    use_agentenv()
    from evaluator.lab_service import LabService, Rejected

    class VfLabService(LabService):
        def _check(self, path, final: bool):
            # head: verbatim from LabService._check (attempt caps and counters)
            if self.state["submitted"]:
                return {"ok": True, "accepted": True, "finalized": True}
            kind = "submissions" if final else "validations"
            cap = self.cfg["validation"]["max_attempts"]
            if cap is not None and self.state[kind] >= cap:
                raise Rejected(f"{kind} attempt limit ({cap}) reached", "budget")
            if not isinstance(path, str):
                raise Rejected("format: path must be a string")
            self.state[kind] += 1
            if not final:                                    # the check itself is public and runs in the agent's box
                return {"ok": True, "counted": self.state[kind], "finalized": False, "runs": "physim2/validate.py"}
            got = freeze() if freeze is not None else {"ok": False, "error": "no collection channel"}
            if not got.get("ok"):
                return {"ok": False, "stage": "artifact", "error": got.get("error") or "the submission could not be collected",
                        "finalized": False, "accepted": False}
            self.state["submitted"] = True
            json.dump({"files": got.get("files"), "bytes": got.get("bytes"), "sha256": got.get("sha256"),
                       "usage": self.lab.usage(), "time": time.time()}, open(os.path.join(self.dir, "frozen.json"), "w"), indent=1)
            return {"ok": True, "accepted": True, "finalized": True, "files": got.get("files"), "sha256": got.get("sha256")}

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
        freeze = (lambda: ACCESS.request(chan, "freeze")) if chan else None
        self.service = make_service(hidden, state.get("rollout") or f"lab-{os.getpid()}", freeze)
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
        op "validate": {"path": "submission"} -> counts one validation attempt (the check runs in your box).
        op "submit": {"path": "submission"} -> freezes submission/ as it is now and closes the laboratory.
        From Python in the workspace the same operations are `physim2.Lab()` methods (see TASK.md)."""
        if self.service is None:
            return NEUTRAL
        if not isinstance(op, str) or (args is not None and not isinstance(args, dict)):
            return json.dumps({"ok": False, "error": "format: op must be a string and args an object", "kind": "request"})
        rep = await asyncio.to_thread(self.service.handle, {"op": op, "args": args or {}})
        return json.dumps(plain(rep), allow_nan=False)


if __name__ == "__main__":
    LabTools.run()
