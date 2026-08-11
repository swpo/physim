"""physim.jail — sandboxed executor for agent-submitted policy/simulator code.

Threat model: agent code must never see world internals (it runs in a separate
process that HOLDS NO SECRETS) and must be limited in host access (restricted
builtins, no import machinery, curated numpy without file IO, rlimits,
timeouts). The engine talks to the jail over line-JSON pipes, one round-trip
per tick.

Policy contract (agent code must define):
    def policy(t: int, y: list[float], mem: dict) -> list[float]   # len n_in

Simulator contract (M3, agent code must define):
    def init(y_history: list[list[float]]) -> state
    def step(state, a: list[float]) -> (state, list[float])        # y_pred len n_out
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
from queue import Empty, Queue

CODE_CAP = 65_536
TICK_TIMEOUT = 5.0          # seconds per round-trip (first tick pays compile)
TOTAL_CPU_SECONDS = 120     # rlimit on jail process
MEMORY_BYTES = 1 << 30      # 1 GB address space (best-effort on macOS)
LINE_CAP = 1_000_000

_RUNNER = r"""
import json, math, resource, signal, sys

resource.setrlimit(resource.RLIMIT_CPU, (%(cpu)d, %(cpu)d))
try:
    resource.setrlimit(resource.RLIMIT_AS, (%(mem)d, %(mem)d))
except (ValueError, OSError):
    pass
signal.signal(signal.SIGALRM, lambda *a: sys.exit(3))

import numpy as _np

class _NP:
    _BLOCKED = {"load", "save", "savez", "savez_compressed", "loadtxt", "savetxt",
                "fromfile", "genfromtxt", "memmap", "lib", "ctypeslib", "f2py",
                "DataSource", "distutils", "testing", "test"}
    def __getattr__(self, name):
        if name.startswith("_") or name in self._BLOCKED:
            raise AttributeError(f"np.{name} is not available in the sandbox")
        return getattr(_np, name)

_SAFE_BUILTINS = {k: getattr(__builtins__, k) if not isinstance(__builtins__, dict)
                  else __builtins__[k]
                  for k in ("abs", "all", "any", "bool", "dict", "divmod",
                            "enumerate", "filter", "float", "int", "isinstance",
                            "getattr", "hasattr", "len", "list", "map", "max", "min", "pow", "print",
                            "range", "reversed", "round", "set", "sorted", "str",
                            "sum", "tuple", "zip", "Exception", "ValueError",
                            "TypeError", "KeyError", "IndexError", "StopIteration",
                            "ZeroDivisionError", "ArithmeticError", "True", "False",
                            "None") if (k in __builtins__ if isinstance(__builtins__, dict)
                                        else hasattr(__builtins__, k))}

def _reply(obj):
    sys.stdout.write(json.dumps(obj, separators=(",", ":")) + "\n")
    sys.stdout.flush()

def _strip_allowed_imports(code):
    # Models habitually write `import math` / `import numpy as np` even when
    # told the modules are preloaded. Rewrite those lines to no-ops; anything
    # else stays and fails loudly.
    out = []
    for line in code.splitlines():
        s = line.strip()
        indent = line[:len(line) - len(line.lstrip())]
        if s in ("import math", "import numpy", "import numpy as np",
                 "import math as math"):
            out.append(indent + "pass")
        elif s.startswith("from math import"):
            names = s.split("import", 1)[1]
            stmts = "; ".join(n.strip() + " = getattr(math, '" + n.strip() + "')"
                              for n in names.split(",") if n.strip().isidentifier())
            out.append(indent + (stmts or "pass"))
        elif s.startswith("from numpy import"):
            names = s.split("import", 1)[1]
            stmts = "; ".join(n.strip() + " = getattr(np, '" + n.strip() + "')"
                              for n in names.split(",") if n.strip().isidentifier())
            out.append(indent + (stmts or "pass"))
        else:
            out.append(line)
    return chr(10).join(out)

def main():
    header = json.loads(sys.stdin.readline())
    code = _strip_allowed_imports(header["code"])
    mode = header.get("mode", "policy")
    env = {"__builtins__": _SAFE_BUILTINS, "math": math, "np": _NP()}
    try:
        exec(compile(code, "<agent_code>", "exec"), env)
    except BaseException as e:
        _reply({"fatal": f"compile/exec error: {type(e).__name__}: {e}"})
        return
    if mode == "policy":
        fn = env.get("policy")
        if not callable(fn):
            _reply({"fatal": "code must define policy(t, y, mem)"})
            return
        mem = {}
        _reply({"ok": True})
        for line in sys.stdin:
            signal.alarm(30)
            req = json.loads(line)
            if req.get("stop"):
                break
            try:
                a = fn(req["t"], req["y"], mem)
                a = [float(x) for x in (a.tolist() if hasattr(a, "tolist") else a)]
                _reply({"a": a})
            except BaseException as e:
                _reply({"fatal": f"policy error at t={req.get('t')}: {type(e).__name__}: {e}"})
                return
            signal.alarm(0)
    else:  # simulator
        init_fn, step_fn = env.get("init"), env.get("step")
        if not callable(init_fn) or not callable(step_fn):
            _reply({"fatal": "code must define init(y_history) and step(state, a)"})
            return
        state = None
        _reply({"ok": True})
        for line in sys.stdin:
            signal.alarm(30)
            req = json.loads(line)
            if req.get("stop"):
                break
            try:
                if "init" in req:
                    state = init_fn(req["init"])
                    _reply({"ok": True})
                else:
                    state, y = step_fn(state, req["a"])
                    y = [float(v) for v in (y.tolist() if hasattr(y, "tolist") else y)]
                    _reply({"y": y})
            except BaseException as e:
                _reply({"fatal": f"simulator error: {type(e).__name__}: {e}"})
                return
            signal.alarm(0)

main()
"""


class JailError(Exception):
    """Agent-code failure (compile error, runtime error, timeout, bad output)."""


class Jail:
    """One sandboxed process running agent code in `policy` or `simulator` mode."""

    def __init__(self, code: str, mode: str = "policy"):
        if not isinstance(code, str) or not code.strip():
            raise JailError("empty code")
        if len(code) > CODE_CAP:
            raise JailError(f"code exceeds {CODE_CAP} bytes")
        runner = _RUNNER % {"cpu": TOTAL_CPU_SECONDS, "mem": MEMORY_BYTES}
        self.proc = subprocess.Popen(
            [sys.executable, "-I", "-c", runner],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, bufsize=1,
            env={"PATH": "/usr/bin:/bin"},  # no secrets, no HOME
        )
        self._q: Queue = Queue()
        self._reader = threading.Thread(target=self._pump, daemon=True)
        self._reader.start()
        self._send({"code": code, "mode": mode})
        first = self._recv(timeout=TICK_TIMEOUT * 4)   # compile may be slow
        if first.get("fatal"):
            self.close()
            raise JailError(first["fatal"])

    def _pump(self):
        try:
            for line in self.proc.stdout:
                if len(line) > LINE_CAP:
                    self._q.put({"fatal": "output line too long"})
                    return
                try:
                    self._q.put(json.loads(line))
                except json.JSONDecodeError:
                    self._q.put({"fatal": "non-JSON output from jail"})
                    return
        finally:
            self._q.put(None)

    def _send(self, obj):
        try:
            self.proc.stdin.write(json.dumps(obj, separators=(",", ":")) + "\n")
            self.proc.stdin.flush()
        except (BrokenPipeError, ValueError) as e:
            raise JailError(f"jail died: {e}") from e

    def _recv(self, timeout=TICK_TIMEOUT):
        try:
            msg = self._q.get(timeout=timeout)
        except Empty:
            self.close()
            raise JailError(f"jail timed out (> {timeout}s)")
        if msg is None:
            raise JailError("jail exited unexpectedly")
        if msg.get("fatal"):
            self.close()
            raise JailError(msg["fatal"])
        return msg

    # ---- policy mode ----
    def act(self, t: int, y: list[float]) -> list[float]:
        self._send({"t": t, "y": y})
        msg = self._recv()
        a = msg.get("a")
        if not isinstance(a, list):
            raise JailError("policy returned non-list")
        return a

    # ---- simulator mode (M3) ----
    def sim_init(self, y_history: list[list[float]]) -> None:
        self._send({"init": y_history})
        self._recv()

    def sim_step(self, a: list[float]) -> list[float]:
        self._send({"a": a})
        msg = self._recv()
        y = msg.get("y")
        if not isinstance(y, list):
            raise JailError("simulator returned non-list")
        return y

    def close(self):
        try:
            if self.proc.poll() is None:
                self._send({"stop": True})
        except Exception:
            pass
        try:
            self.proc.kill()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()
