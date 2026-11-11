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
    obs = lab.experiment("ep-3", 16)   # an integer T instead of U: T ticks without input (also lab.advance(T))
    lab.validate("submission")      # runs the predictor as the grader will (no accuracy feedback); runs HERE
    lab.submit("submission")        # takes the copy that is graded and ENDS YOUR RUN

A rejected command raises LabError; nothing runs and nothing is charged (the message says why, using
public information only).

Every reply is saved: after each operation this client appends one JSON line to /workspace/lab_log.jsonl
(LOG below) with the time, the operation, its arguments and the full result (arrays as nested lists) or the
error. Real observations cost budget and cannot be asked for twice, and a script that ends takes its variables
with it: `Lab.read_log()` gives every reply back. Only this client writes the log; a call made through the
tool directly is not in it.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.request

import numpy as np

ADDRESS_FILE = "/etc/physim2/lab.json"
TOOL = "call"
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.environ.get("PHYSIM2_LAB_LOG") or os.path.join(os.path.dirname(HERE), "lab_log.jsonl")
MAX_BLOCK = 4096                                             # ticks per call (the laboratory's own bound)


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
        self.log_failures = 0                                # round 5 (X14): replies this client could not write to the log
        self._http = urllib.request.build_opener(urllib.request.ProxyHandler({}))   # the address is a direct route
        self.log_path = LOG
        try:                                                 # n_in of this exam, for the argument check of advance/experiment
            with open(os.path.join(HERE, "exam.json")) as f:
                self._n_in = int(json.load(f)["n_in"])
        except Exception:
            self._n_in = None

    # ---- every reply is saved (see the module text) ----
    def _log(self, op: str, args: dict, ok: bool, **rest) -> None:
        try:
            line = json.dumps(dict({"t": round(time.time(), 3), "n": self._n, "op": op, "args": _plain(args), "ok": ok}, **rest))
            with open(self.log_path, "a") as f:
                f.write(line + "\n")
        except Exception as e:                               # a full disk never breaks a call, but it is said (round 5, X14)
            self.log_failures += 1
            if self.log_failures == 1 or self.log_failures % 50 == 0:
                try:
                    sys.stderr.write(f"physim2.Lab: this reply ({op}) could NOT be saved to {self.log_path} ({type(e).__name__}: "
                                     f"{str(e)[:80]}); {self.log_failures} replies of this client are missing from the log\n")
                    sys.stderr.flush()
                except Exception:
                    pass

    @staticmethod
    def read_log(path: str | None = None) -> list:
        """Every saved reply, oldest first: [{"t", "n", "op", "args", "ok", "result" | "error", "kind"}].
        Results of reset, advance and experiment are nested lists: np.asarray(entry["result"])."""
        out = []
        try:
            with open(path or LOG) as f:
                for line in f:
                    try:
                        out.append(json.loads(line))
                    except ValueError:
                        pass
        except OSError:
            pass
        return out

    def _call(self, op: str, **args):
        try:
            res = self._send(op, **args)
        except LabError as e:
            self._log(op, args, False, error=str(e), kind=e.kind)
            raise
        self._log(op, args, True, result=res)
        return res

    def _block(self, op: str, inputs) -> dict:
        """The inputs argument of advance / experiment as the request's arguments: {"n": T} for an integer T,
        {"inputs": array (T, n_in)} for a block of inputs. Anything else raises LabError with one line of usage,
        here, before anything is sent."""
        shape = f"(T, {self._n_in})" if self._n_in else "(T, n_in)"
        call = "lab.advance(U)" if op == "advance" else "lab.experiment(label, U)"
        usage = (f"usage: {call} with U an array {shape} of finite numbers, 1 <= T <= {MAX_BLOCK}, or an integer T "
                 "for T ticks without input")
        if inputs is None or isinstance(inputs, (bool, np.bool_, str, bytes, dict)):
            raise LabError(usage, "request")
        if isinstance(inputs, (int, np.integer)):
            if not 1 <= int(inputs) <= MAX_BLOCK:
                raise LabError(usage, "request")
            return {"n": int(inputs)}
        try:
            U = np.asarray(inputs, np.float64)
        except (ValueError, TypeError, OverflowError):
            raise LabError(usage, "request") from None
        if U.ndim != 2 or not 1 <= U.shape[0] <= MAX_BLOCK or (self._n_in and U.shape[1] != self._n_in) or not np.all(np.isfinite(U)):
            raise LabError(usage, "request")
        return {"inputs": U}

    # ---- transport: one MCP tools/call over HTTP per operation ----
    def _send(self, op: str, **args):
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
            if e.code == 413:                                # the laboratory reads at most 4 MiB of one request
                raise LabError("the request is too large for the laboratory (HTTP 413: at most 4 MiB per call); send fewer ticks "
                               "per call", "request") from None
            if e.code == 503:                                # it serves a few requests at once
                raise LabError("the laboratory is busy with other requests of yours (HTTP 503); try again", "busy") from None
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
        rep = self._call("usage")
        if isinstance(rep, dict):
            rep["lab_log_failures"] = self.log_failures      # X14: replies of THIS client that could not be saved
        return rep

    def reset(self, label) -> np.ndarray:
        """Start a new episode at the hidden start named `label` (a name, not a seed: the same label
        gives the same start with fresh dynamics noise). Returns o(0) (n_obs,)."""
        return np.asarray(self._call("reset", label=label), np.float64)

    def advance(self, inputs) -> np.ndarray:
        """Run T ticks of the current episode. `inputs`: an array (T, n_in) of inputs (zeros = no input), or an
        integer T for T ticks without input. Returns the T observations after each tick (T, n_obs).
        The whole block is validated first: on a violation nothing runs and nothing is charged."""
        return np.asarray(self._call("advance", **self._block("advance", inputs)), np.float64)

    def experiment(self, label, inputs) -> np.ndarray:
        """reset(label) then advance(inputs): observations (T + 1, n_obs), row 0 = o(0). `inputs`: an array
        (T, n_in), or an integer T for T ticks without input (lab.experiment("free-1", 16))."""
        return np.asarray(self._call("experiment", label=label, **self._block("experiment", inputs)), np.float64)

    def validate(self, path: str = "submission") -> dict:
        """Format, limits and reproducibility on two public example requests, run in this box the way the grader
        will run your predictor: from a clean copy of the directory alone, next to the original physim2 package,
        as an unprivileged user that cannot read /workspace nor what this box already holds in /tmp, /dev/shm, /etc/physim2, /runtime
        (physim2/validate.py). The laboratory starts the check and returns its report; you can also run
        `python -m physim2.validate <path>` yourself, without the laboratory (then with your rights)."""
        from . import validate as V
        try:
            V.resolve(path)
        except ValueError as e:
            raise LabError(str(e), "request") from None
        return self._call("validate", path=str(path))

    def submit(self, path: str = "submission") -> dict:
        """Validate, then freeze, and END YOUR RUN: if the check passes, the grader's worker takes its copy of
        submission/ now, the laboratory closes ("accepted": True) and the run ends before your next turn; if
        not, nothing is frozen and nothing ends. You do not need to submit to be graded: whatever is in
        submission/ when the run ends is graded. A directory other than submission/ is copied there first
        (only submission/ is collected)."""
        from . import validate as V
        try:
            src = V.resolve(path)
        except ValueError as e:
            raise LabError(str(e), "request") from None
        dst = os.path.join(V.WORKSPACE, "submission")
        if os.path.isdir(src) and os.path.realpath(src) != os.path.realpath(dst) and not self.usage().get("submitted"):
            # replacing submission/ is for the exam box only (its marker); anywhere else, copy it yourself
            if not (os.path.isdir("/etc/physim2") and os.path.isfile(os.path.join(V.WORKSPACE, "TASK.md"))):
                raise LabError("submit(path) replaces submission/ only inside the exam box; copy your directory there yourself", "request")
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst, symlinks=True)
        return self._call("submit", path="submission")
