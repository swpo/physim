"""physim2.labclient -- the agent's client for the real (hidden) world.

The real world runs in another process that holds the hidden parameters and the noise secret; this
client only sends commands and receives observations. Address: environment variable PHYSIM2_LAB
("unix:/path/to/lab.sock" or "tcp://host:port") and, for tcp, PHYSIM2_TOKEN.

    from physim2 import Lab
    lab = Lab()
    lab.card()                      # public declaration: sizes, budgets, exam, limits
    lab.usage()                     # ticks and nats used / left
    o0 = lab.reset("my-episode-1")  # new episode from a fresh hidden start; costs reset_cost ticks
    obs = lab.advance(U)            # U (T, n_in) inputs for the next T ticks -> observations (T, n_obs)
    obs = lab.experiment("ep-2", U) # reset + advance: (T + 1, n_obs), row 0 is o(0)
    lab.validate("submission")      # format and reproducibility check only (no accuracy feedback)
    lab.submit("submission")        # freeze the predictor; ends the investigation

A rejected command raises LabError; nothing runs and nothing is charged (the message says why, using
public information only).
"""
from __future__ import annotations

import os
import socket

import numpy as np

from . import wire


class LabError(RuntimeError):
    def __init__(self, msg, kind="request"):
        super().__init__(msg)
        self.kind = kind


class Lab:
    def __init__(self, address: str | None = None, token: str | None = None, timeout: float = 3600.0):
        self.address = address or os.environ.get("PHYSIM2_LAB", "")
        self.token = token if token is not None else os.environ.get("PHYSIM2_TOKEN", "")
        if not self.address:
            raise LabError("PHYSIM2_LAB is not set (unix:/path or tcp://host:port)")
        self.timeout = timeout
        self._sock = None
        self._buf = b""

    # ---- transport ----
    def _connect(self):
        if self.address.startswith("unix:"):
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect(self.address[5:])
        elif self.address.startswith("tcp://"):
            host, port = self.address[6:].rsplit(":", 1)
            s = socket.create_connection((host, int(port)), timeout=self.timeout)
        else:
            raise LabError(f"bad PHYSIM2_LAB address {self.address!r}")
        self._sock, self._buf = s, b""

    def _call(self, op: str, **args):
        if self._sock is None:
            self._connect()
        self._sock.sendall(wire.dumps({"op": op, "args": args, "token": self.token}))
        while b"\n" not in self._buf:
            chunk = self._sock.recv(1 << 20)
            if not chunk:
                self._sock = None
                raise LabError("the lab closed the connection", "closed")
            self._buf += chunk
            if len(self._buf) > wire.MAX_LINE:
                raise LabError("reply too large")
        line, self._buf = self._buf.split(b"\n", 1)
        rep = wire.loads(line)
        if not rep.get("ok"):
            raise LabError(rep.get("error", "lab error"), rep.get("kind", "request"))
        return rep["result"]

    def close(self):
        if self._sock is not None:
            try:
                self._sock.close()
            finally:
                self._sock = None

    # ---- operations ----
    def card(self) -> dict:
        return self._call("card")

    def usage(self) -> dict:
        return self._call("usage")

    def reset(self, label) -> np.ndarray:
        """Start a new episode at the hidden start named `label` (a name, not a seed: the same label
        gives the same start with fresh dynamics noise). Returns o(0) (n_obs,)."""
        return self._call("reset", label=label)

    def advance(self, inputs) -> np.ndarray:
        """Run len(inputs) ticks of the current episode; inputs (T, n_in) (zeros = no input) or an
        integer T for T ticks without input. Returns the T observations after each tick (T, n_obs).
        The whole block is validated first: on a violation nothing runs and nothing is charged."""
        if isinstance(inputs, (int, np.integer)):
            return self._call("advance", n=int(inputs))
        return self._call("advance", inputs=np.asarray(inputs, np.float64))

    def experiment(self, label, inputs) -> np.ndarray:
        """reset(label) then advance(inputs): observations (T + 1, n_obs), row 0 = o(0)."""
        if isinstance(inputs, (int, np.integer)):
            return self._call("experiment", label=label, n=int(inputs))
        return self._call("experiment", label=label, inputs=np.asarray(inputs, np.float64))

    def validate(self, path: str = "submission") -> dict:
        return self._call("validate", path=str(path))

    def submit(self, path: str = "submission") -> dict:
        return self._call("submit", path=str(path))
