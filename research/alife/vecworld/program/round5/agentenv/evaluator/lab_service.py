"""evaluator.lab_service -- the real world behind a socket: the only door between the agent and the hidden side.

LabService   vw.harness.Lab on the hidden world (hidden theta, secret keys; nats and tick budgets) plus
             validate / submit. Operations: card, usage, reset, advance, experiment, validate, submit.
             Every block of inputs is validated as a whole before anything runs (bounds, per-tick, per-episode
             and total nats, ticks); a rejection charges nothing and its message uses public information only.
             Internal errors are reported as "infrastructure error" without detail (v1 policy).
serve        JSON lines over a Unix socket (unix:/path) or TCP with a token (tcp://host:port).

usage: python -m evaluator.lab_service --hidden DIR --public DIR --workspace DIR --listen unix:/path/lab.sock
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import threading
import time
import traceback

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from evaluator import instance as INST  # noqa: E402
from evaluator import submission as SUB  # noqa: E402
from physim2 import wire  # noqa: E402

MAX_BLOCK = 4096


class Rejected(Exception):
    def __init__(self, msg, kind="request"):
        super().__init__(msg)
        self.kind = kind


class LabService:
    def __init__(self, hidden_dir: str, public_dir: str, workspace_dir: str, name: str = "agent", hide=(), work_dir=None):
        from vw.harness import Lab
        self.hidden, self.public, self.workspace, self.name = hidden_dir, public_dir, os.path.realpath(workspace_dir), name
        self.hide = tuple(hide) + (hidden_dir,)
        inst, W, sec = INST.load_instance(hidden_dir)
        self.W, self.cfg = W, inst["config"]
        self.decl = INST.exam_decl(W, self.cfg)
        lc = self.cfg["lab"]
        self.lab = Lab(W.build_world(np.array(inst["theta"])), sec.child("lab", name),
                       nats=W.nats_budget(total=lc["total_nats"]), max_ticks=lc["max_ticks"], reset_cost=int(lc["reset_cost"]))
        self.dir = os.path.join(hidden_dir, "labs", name)           # evaluator records (state, request log)
        self.work = os.path.join(work_dir or os.path.join(os.path.dirname(os.path.abspath(hidden_dir)), "work"), name)
        os.makedirs(self.dir, exist_ok=True)                       # snapshots and scratch: outside the hidden directory
        os.makedirs(os.path.join(self.work, "tmp"), exist_ok=True)
        self.state = {"submitted": False, "validations": 0, "submissions": 0, "requests": 0, "rejected": 0}
        self._log = open(os.path.join(self.dir, "log.jsonl"), "a")
        self.lock = threading.Lock()
        self._restore()

    # ---- persistence (a restarted server keeps the counters) ----
    def _restore(self):
        f = os.path.join(self.dir, "state.json")
        if os.path.exists(f):
            s = json.load(open(f))
            self.state.update(s["state"])
            self.lab.ticks_used, self.lab.n_resets, self.lab._count = s["ticks_used"], s["resets"], s["count"]
            if self.lab.acct is not None:
                self.lab.acct.total_used, self.lab.acct.n_episodes = s["total_nats"], s["episodes"]

    def _save(self):
        a = self.lab.acct
        s = {"state": self.state, "ticks_used": self.lab.ticks_used, "resets": self.lab.n_resets, "count": self.lab._count,
             "total_nats": 0.0 if a is None else a.total_used, "episodes": 0 if a is None else a.n_episodes}
        tmp = os.path.join(self.dir, "state.json.tmp")
        json.dump(s, open(tmp, "w"))
        os.replace(tmp, os.path.join(self.dir, "state.json"))

    # ---- public operations ----
    def card(self) -> dict:
        W, d, c = self.W, self.decl, self.cfg
        return {"world": W.NAME, "n_in": W.N_IN, "n_obs": W.N_OBS, "level_dims": {str(k): v for k, v in W.LEVEL_DIMS.items()},
                "theta_names": list(W.THETA_NAMES), "prior_lo": W.PRIOR_LO.tolist(), "prior_hi": W.PRIOR_HI.tolist(),
                "burn_in_ticks": W.BURN_IN, "input_bounds": [W.IN_LO, W.IN_HI],
                "nats": {"cost": f"|u|^2 / (2 * {W.SIGMA_IN}^2) per tick", "tick_cap": W.TICK_CAP,
                         "episode_cap": W.EPISODE_CAP, "total_cap": c["lab"]["total_nats"]},
                "ticks": {"max_ticks": c["lab"]["max_ticks"], "reset_cost": c["lab"]["reset_cost"]},
                "exam": {"prefix_P": d["P"], "queries": {str(l): v for l, v in d["queries"].items()},
                         "n_samples": c["predictor"]["n_samples"], "items": c["exam"]["n_items"],
                         "replicate_truths": c["exam"]["R"], "program_classes": list(W.program_mix().names)},
                "predictor_limits": c["predictor"], "compute_envelope": c["envelope"],
                "validation_attempts": c["validation"]["max_attempts"]}

    def usage(self) -> dict:
        u = self.lab.usage()
        u.update({k: self.state[k] for k in ("submitted", "validations", "submissions")})
        return u

    def _open(self):
        if self.state["submitted"]:
            raise Rejected("the predictor is submitted; the laboratory is closed", "closed")

    def reset(self, label):
        self._open()
        if isinstance(label, bool) or not isinstance(label, (str, int)):
            raise Rejected("format: label must be a string or a non-negative integer")
        if isinstance(label, str) and not 0 < len(label) <= 64:
            raise Rejected("format: label must have 1 to 64 characters")
        if isinstance(label, int) and not 0 <= label < 2 ** 62:
            raise Rejected("format: integer labels must lie in [0, 2**62)")
        return np.asarray(self.lab.reset(label))

    def advance(self, inputs=None, n=None):
        self._open()
        lab, w = self.lab, self.lab.world
        if inputs is None:
            if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= MAX_BLOCK:
                raise Rejected(f"format: n must be an integer in [1, {MAX_BLOCK}]")
            U = np.zeros((n, w.n_in))
        else:
            U = np.asarray(inputs, float)
            if U.ndim != 2 or U.shape[1] != w.n_in or not 1 <= U.shape[0] <= MAX_BLOCK:
                raise Rejected(f"format: inputs must have shape (T, {w.n_in}) with 1 <= T <= {MAX_BLOCK}")
            if not np.all(np.isfinite(U)):
                raise Rejected("format: inputs must be finite")
        if lab._ep is None:
            raise Rejected("call reset(label) first")
        T = U.shape[0]
        C = w.inport.admissible
        prog = [(t, U[t]) for t in range(T) if np.any(U[t])]
        vp = w._validate_program(prog, lab._ep.t, lab._last_in, lab._spent_l1, T)
        if lab.acct is not None:
            lab.acct.check_program([(t, C.canonical(a)) for t, a in vp], episode_used=lab.acct.episode_used)
        lab._check_ticks(T)
        return np.stack([np.asarray(lab.step(U[t] if np.any(U[t]) else None)) for t in range(T)])

    def experiment(self, label, inputs=None, n=None):
        self._open()
        lab = self.lab
        T = int(n) if inputs is None and isinstance(n, int) else (np.asarray(inputs).shape[0] if inputs is not None else 0)
        if lab.max_ticks is not None and lab.ticks_used + lab.reset_cost + T > lab.max_ticks:
            raise Rejected(f"budget: {lab.ticks_used} + {lab.reset_cost + T} ticks > max_ticks={lab.max_ticks}; nothing ran",
                           "budget")
        if inputs is not None:                               # validate the block against a fresh episode first
            U = np.asarray(inputs, float)
            if U.ndim != 2 or U.shape[1] != lab.world.n_in or not np.all(np.isfinite(U)):
                raise Rejected(f"format: inputs must be finite with shape (T, {lab.world.n_in})")
            C = lab.world.inport.admissible
            vp = lab.world._validate_program([(t, U[t]) for t in range(len(U)) if np.any(U[t])], 0, None, 0.0, len(U))
            if lab.acct is not None:
                lab.acct.check_program([(t, C.canonical(a)) for t, a in vp], episode_used=0.0)
        o0 = self.reset(label)
        return np.concatenate([o0[None], self.advance(inputs=inputs, n=n)], 0)

    def _sub_path(self, path):
        p = os.path.realpath(os.path.join(self.workspace, str(path)))
        if not (p == self.workspace or p.startswith(self.workspace + os.sep)):
            raise Rejected("format: the submission path must lie inside the workspace")
        return p

    def _check(self, path, final: bool):
        if self.state["submitted"]:
            return {"ok": True, "accepted": True, "finalized": True}
        kind = "submissions" if final else "validations"
        cap = self.cfg["validation"]["max_attempts"]
        if cap is not None and self.state[kind] >= cap:
            raise Rejected(f"{kind} attempt limit ({cap}) reached", "budget")
        self.state[kind] += 1
        dst = os.path.join(self.work, ("submit" if final else "validate") + f"_{self.state[kind]:02d}")
        try:
            man = SUB.snapshot(self._sub_path(path), dst, self.cfg["predictor"]["artifact_mib"])
        except ValueError as e:
            return {"ok": False, "stage": "artifact", "error": str(e), "finalized": False}
        ex = np.load(os.path.join(self.hidden, "examples.npz"))
        rep = SUB.validate(dst, self.public, ex, self.decl["queries"], dict(self.W.LEVEL_DIMS), self.cfg["predictor"],
                           hide=self.hide, work=os.path.join(self.work, "tmp"))
        rep["files"] = len(man["files"])
        if final and rep["ok"]:
            self.state["submitted"] = True
            json.dump({"path": dst, "manifest": man, "usage": self.lab.usage(), "time": time.time()},
                      open(os.path.join(self.dir, "frozen.json"), "w"), indent=1)
        rep.update(finalized=self.state["submitted"], accepted=bool(final and rep["ok"]))
        return rep

    def validate(self, path="submission"):
        return self._check(path, False)

    def submit(self, path="submission"):
        return self._check(path, True)

    # ---- dispatch ----
    OPS = ("card", "usage", "reset", "advance", "experiment", "validate", "submit")

    def handle(self, msg: dict) -> dict:
        from vw.ports import BudgetExhausted, InputViolation
        op, args = msg.get("op"), msg.get("args") or {}
        t0 = time.time()
        with self.lock:
            self.state["requests"] += 1
            before = self.lab.ticks_used
            try:
                if op not in self.OPS or not isinstance(args, dict):
                    raise Rejected(f"unknown operation {op!r}")
                rep = {"ok": True, "result": getattr(self, op)(**args)}
            except Rejected as e:
                rep = {"ok": False, "error": str(e), "kind": e.kind}
            except InputViolation as e:
                rep = {"ok": False, "error": str(e), "kind": "violation"}
            except BudgetExhausted as e:
                rep = {"ok": False, "error": str(e), "kind": "budget"}
            except TypeError as e:
                rep = {"ok": False, "error": f"format: bad arguments for {op}", "kind": "request", "_detail": str(e)}
            except Exception:
                rep = {"ok": False, "error": "infrastructure error; the evaluator must intervene", "kind": "infrastructure",
                       "_detail": traceback.format_exc()}
            if not rep["ok"]:
                self.state["rejected"] += 1
            a = self.lab.acct
            self._log.write(json.dumps({"t": t0, "op": op, "ok": rep["ok"], "kind": rep.get("kind"), "error": rep.get("error"),
                                        "detail": rep.pop("_detail", None), "ticks": self.lab.ticks_used - before,
                                        "ticks_used": self.lab.ticks_used, "total_nats": None if a is None else a.total_used,
                                        "seconds": time.time() - t0}) + "\n")
            self._log.flush()
            self._save()
        return rep


def serve(svc: LabService, listen: str, token: str = "", ready_file: str | None = None):
    if listen.startswith("unix:"):
        path = listen[5:]
        if os.path.exists(path):
            os.unlink(path)
        srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        srv.bind(path)
        os.chmod(path, 0o666)
    else:
        host, port = listen[6:].rsplit(":", 1)
        if not token:
            raise SystemExit("tcp needs --token")
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, int(port)))
    srv.listen(4)
    if ready_file:
        open(ready_file, "w").write("ready\n")

    def client(conn):
        buf = b""
        with conn:
            while True:
                try:
                    chunk = conn.recv(1 << 20)
                except OSError:
                    return
                if not chunk:
                    return
                buf += chunk
                if len(buf) > wire.MAX_LINE:
                    return
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    try:
                        msg = wire.loads(line)
                        if token and msg.get("token") != token:
                            rep = {"ok": False, "error": "bad token", "kind": "request"}
                        else:
                            rep = svc.handle(msg)
                    except Exception:
                        rep = {"ok": False, "error": "malformed request", "kind": "request"}
                    conn.sendall(wire.dumps(rep))

    while True:
        conn, _ = srv.accept()
        threading.Thread(target=client, args=(conn,), daemon=True).start()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hidden", required=True)
    ap.add_argument("--public", required=True)
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--listen", required=True)
    ap.add_argument("--token", default=os.environ.get("PHYSIM2_TOKEN", ""))
    ap.add_argument("--name", default="agent")
    ap.add_argument("--hide", action="append", default=[])
    ap.add_argument("--work", default=None)
    ap.add_argument("--ready-file", default=None)
    a = ap.parse_args()
    serve(LabService(a.hidden, a.public, a.workspace, a.name, a.hide, a.work), a.listen, a.token, a.ready_file)


if __name__ == "__main__":
    main()
