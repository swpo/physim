"""physim2.labclient -- the agent's client for the real (hidden) world.

The real world runs in another process on another machine side: it holds the hidden parameters and the noise
secret; this client only sends commands and receives observations. The laboratory is one MCP tool, `call`
(one call = one operation), served over HTTP; the same tool is offered to a model harness directly. Address: the
environment variable PHYSIM2_LAB, else the file /etc/physim2/lab.json that the environment writes into the box.

    from physim2 import Lab
    lab = Lab()
    lab.card()                      # public declaration: sizes, budgets, exam, limits
    lab.usage()                     # ticks and nats used / left
    o0 = lab.reset("my-episode-1")  # new episode from a fresh hidden start; costs reset_cost ticks
    obs = lab.advance(U)            # U (T, n_in) inputs for the next T ticks -> observations (T, n_obs)
    obs = lab.experiment("ep-2", U) # reset + advance: (T + 1, n_obs), row 0 is o(0)
    lab.validate("submission")      # format and reproducibility check only (no accuracy feedback); runs HERE
    lab.submit("submission")        # freeze the predictor; ends the investigation

A rejected command raises LabError; nothing runs and nothing is charged (the message says why, using
public information only).
"""
from __future__ import annotations

import json
import os
import shutil
import urllib.error
import urllib.request

import numpy as np

ADDRESS_FILE = "/etc/physim2/lab.json"
TOOL = "call"


class LabError(RuntimeError):
    def __init__(self, msg, kind="request"):
        super().__init__(msg)
        self.kind = kind


def _plain(o):
    """Arguments as plain JSON: arrays become nested lists (float64 survives the round trip exactly)."""
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, dict):
        return {str(k): _plain(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_plain(v) for v in o]
    if isinstance(o, np.generic):
        return o.item()
    return o


class Lab:
    def __init__(self, address: str | None = None, token: str | None = None, timeout: float = 3600.0):
        self.address = address or os.environ.get("PHYSIM2_LAB", "")
        if not self.address and os.path.exists(ADDRESS_FILE):
            self.address = json.load(open(ADDRESS_FILE))["url"]
        if not self.address:
            raise LabError(f"no laboratory address: PHYSIM2_LAB is not set and {ADDRESS_FILE} does not exist")
        self.timeout = timeout
        self._n = 0
        self._http = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # the address is a direct route

    # ---- transport: one MCP tools/call over HTTP per operation ----
    def _call(self, op: str, **args):
        self._n += 1
        body = {"jsonrpc": "2.0", "id": self._n, "method": "tools/call",
                "params": {"name": TOOL, "arguments": {"op": op, "args": _plain(args)}}}
        req = urllib.request.Request(self.address, data=json.dumps(body, allow_nan=False).encode(), method="POST",
                                     headers={"Content-Type": "application/json",
                                              "Accept": "application/json, text/event-stream"})
        try:
            with self._http.open(req, timeout=self.timeout) as r:
                raw = r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            raise LabError(f"the lab refused the connection (HTTP {e.code})", "closed") from None
        except (urllib.error.URLError, OSError) as e:
            raise LabError(f"the lab cannot be reached ({type(e).__name__})", "closed") from None
        if raw.lstrip().startswith("event:") or raw.lstrip().startswith("data:"):   # an SSE-framed reply
            raw = "".join(line[5:].strip() for line in raw.splitlines() if line.startswith("data:"))
        msg = json.loads(raw)
        if "error" in msg:
            raise LabError(str(msg["error"].get("message", "lab error")), "request")
        res = msg["result"]
        text = "".join(c.get("text", "") for c in res.get("content", []) if c.get("type") == "text")
        if res.get("isError"):
            raise LabError(text or "lab error", "infrastructure")
        rep = json.loads(text)
        if not rep.get("ok"):
            raise LabError(rep.get("error", "lab error"), rep.get("kind", "request"))
        return rep["result"]

    def close(self):
        pass

    # ---- operations ----
    def card(self) -> dict:
        return self._call("card")

    def usage(self) -> dict:
        return self._call("usage")

    def reset(self, label) -> np.ndarray:
        """Start a new episode at the hidden start named `label` (a name, not a seed: the same label
        gives the same start with fresh dynamics noise). Returns o(0) (n_obs,)."""
        return np.asarray(self._call("reset", label=label), np.float64)

    def advance(self, inputs) -> np.ndarray:
        """Run len(inputs) ticks of the current episode; inputs (T, n_in) (zeros = no input) or an
        integer T for T ticks without input. Returns the T observations after each tick (T, n_obs).
        The whole block is validated first: on a violation nothing runs and nothing is charged."""
        if isinstance(inputs, (int, np.integer)):
            return np.asarray(self._call("advance", n=int(inputs)), np.float64)
        return np.asarray(self._call("advance", inputs=np.asarray(inputs, np.float64)), np.float64)

    def experiment(self, label, inputs) -> np.ndarray:
        """reset(label) then advance(inputs): observations (T + 1, n_obs), row 0 = o(0)."""
        if isinstance(inputs, (int, np.integer)):
            return np.asarray(self._call("experiment", label=label, n=int(inputs)), np.float64)
        return np.asarray(self._call("experiment", label=label, inputs=np.asarray(inputs, np.float64)), np.float64)

    def validate(self, path: str = "submission") -> dict:
        """Format, limits and reproducibility on two public example requests, run in this box with the grader's
        driver (physim2/validate.py). The laboratory starts the check and returns its report; you can also run
        `python -m physim2.validate <path>` yourself, without the laboratory."""
        from . import validate as V
        try:
            V.resolve(path)
        except ValueError as e:
            raise LabError(str(e), "request") from None
        return self._call("validate", path=str(path))

    def submit(self, path: str = "submission") -> dict:
        """Validate, then freeze: if the check passes, the grader's worker takes its copy of submission/ now and
        the laboratory closes ("accepted": True); if not, nothing is frozen. A directory other than submission/
        is copied there first (only submission/ is collected)."""
        from . import validate as V
        try:
            src = V.resolve(path)
        except ValueError as e:
            raise LabError(str(e), "request") from None
        dst = os.path.join(V.WORKSPACE, "submission")
        if os.path.isdir(src) and os.path.realpath(src) != os.path.realpath(dst) and not self.usage().get("submitted"):
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst, symlinks=True)
        return self._call("submit", path="submission")
