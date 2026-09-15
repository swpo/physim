"""physim.baselines — scripted agents that play through the SAME session
interface as a model (JSON in, JSON out). Roles: solvability certification,
floor baselines for the report.

NullAgent      answers 0.0 with wide intervals (no exploration).
TailAgent      explores minimally; answers every contract with the world's
               autonomous resting mean of that channel (ignores protocols).
ReferenceAgent generic scripted scientist: sensor calibration, step-response
               map, relaxation/memory probes; predicts each contract by
               feature-matching its experiment library (no world access).
"""

from __future__ import annotations

import json
from typing import Any

import numpy as np

from physim.session import PhysimSession, render_protocol, TAIL


def _cmd(session: PhysimSession, obj: dict) -> dict:
    return session.handle(json.dumps(obj))


class NullAgent:
    name = "null"

    def play(self, session: PhysimSession) -> str:
        spec = _cmd(session, {"op": "ready", "confirm": True})
        answers = [{"id": c["id"], "mean": 0.0, "low": -1.5, "high": 1.5}
                   for c in spec["contracts"]]
        return json.dumps({"op": "answer", "answers": answers})


class TailAgent:
    name = "tail"

    def play(self, session: PhysimSession) -> str:
        n_in = session.world.p.n_in
        r = _cmd(session, {"op": "run",
                           "segments": [{"t": 150, "u": [0.0] * n_in}],
                           "observe": {"channels": "all"}})
        rest = {int(k): v for k, v in r["tail_mean"].items()}
        spec = _cmd(session, {"op": "ready", "confirm": True})
        answers = [{"id": c["id"],
                    "mean": rest.get(c["predict"]["channel"], 0.0),
                    "low": rest.get(c["predict"]["channel"], 0.0) - 0.5,
                    "high": rest.get(c["predict"]["channel"], 0.0) + 0.5}
                   for c in spec["contracts"]]
        return json.dumps({"op": "answer", "answers": answers})


class ReferenceAgent:
    """Generic pipeline, all through the public interface:
      1. noise floor (zero hold)
      2. global step responses at +/- several amplitudes, with release tails
      3. per-port probes (weak): which channels each port moves
      4. prediction: for a contract protocol, find the closest experiment in
         (drive-summary feature space) and read off that channel's tail mean;
         interval from noise + local disagreement of top matches.
    """

    name = "reference"

    def __init__(self, series_channels: int = 6):
        self.series_channels = series_channels

    def play(self, session: PhysimSession) -> str:
        w = session.world
        n_in, n_out = w.p.n_in, w.p.n_out
        lib: list[tuple[np.ndarray, dict[int, float]]] = []   # (features, tail means)

        def run(segments, channels="all"):
            r = _cmd(session, {"op": "run", "segments": segments,
                               "observe": {"channels": channels}})
            if "error" in r:
                return None
            means = {int(k): v for k, v in r["tail_mean"].items()}
            return means

        def feat(segments) -> np.ndarray:
            """Summary features of a protocol: final-u, signed peak, LAST
            nonzero drive (what the state was left in before release),
            release length, total ticks."""
            U = render_protocol(segments, n_in)
            g = U.mean(1)                      # aggregate drive per tick
            final_u = g[-min(TAIL, len(g)):].mean()
            peak = g[np.argmax(np.abs(g))] if len(g) else 0.0
            nz = np.nonzero(np.abs(g) > 0.02)[0]
            release = len(g) - 1 - (nz[-1] if len(nz) else -1)
            last_drive = g[nz[-1]] if len(nz) else 0.0
            return np.array([final_u, peak, 2.0 * last_drive,
                             min(release, 200) / 200.0,
                             min(len(g), 400) / 400.0])

        def record(segments):
            # contracts run from FRESH state: match that (reset costs 200 ticks)
            _cmd(session, {"op": "reset"})
            means = run(segments)
            if means is not None:
                lib.append((feat(segments), means))

        z = [0.0] * n_in
        # 1) noise floor + rest state
        record([{"t": 120, "u": z}])
        # 2) global steps with release, both signs, several amplitudes
        for amp in (0.3, 0.6, 0.9):
            for sgn in (+1.0, -1.0):
                u = [sgn * amp] * n_in
                record([{"t": 70, "u": u}])                                  # held
                record([{"t": 70, "u": u}, {"t": 90, "u": z}])               # release
        # 3) branch-flip probes (hysteresis): drive down, weak up, release, etc.
        for a, b in ((0.9, -0.3), (-0.9, 0.3), (0.9, -0.6), (-0.9, 0.6)):
            record([{"t": 70, "u": [a] * n_in},
                    {"t": 45, "u": [b] * n_in},
                    {"t": 90, "u": z}])
        # 4) single-port weak probes
        for i in range(n_in):
            u = list(z); u[i] = 0.5
            record([{"t": 50, "u": u}])
        # done exploring
        spec = _cmd(session, {"op": "ready", "confirm": True})
        F = np.stack([f for f, _ in lib])
        answers = []
        for c in spec["contracts"]:
            ch = c["predict"]["channel"]
            fc = feat(c["protocol"]["segments"])
            d = np.linalg.norm(F - fc[None, :], axis=1)
            order = np.argsort(d)[:3]
            vals = [lib[i][1].get(ch) for i in order if ch in lib[i][1]]
            vals = [v for v in vals if v is not None]
            if not vals:
                answers.append({"id": c["id"], "mean": 0.0, "low": -1.5, "high": 1.5})
                continue
            mean = float(np.mean(vals))
            spread = float(max(np.std(vals), 0.05)) + 0.05
            answers.append({"id": c["id"], "mean": round(mean, 4),
                            "low": round(mean - 2 * spread, 4),
                            "high": round(mean + 2 * spread, 4)})
        return json.dumps({"op": "answer", "answers": answers})


class PrepPIAgent:
    """Certifier/floor for preparation contracts: calibrates sensor polarity via
    global steps, then submits a P-controller policy per contract that drives
    the target channel toward its band using all input ports."""

    name = "prep_pi"

    def play(self, session: PhysimSession) -> str:
        n_in = session.world.p.n_in
        z = [0.0] * n_in
        # calibrate: which way does each channel move under +drive?
        r0 = _cmd(session, {"op": "run", "segments": [{"t": 60, "u": z}]})
        rp = _cmd(session, {"op": "run", "segments": [{"t": 60, "u": [0.8] * n_in}]})
        rest = {int(k): v for k, v in r0["tail_mean"].items()}
        up = {int(k): v for k, v in rp["tail_mean"].items()}
        spec = _cmd(session, {"op": "ready", "confirm": True})
        # prediction answers: resting means (tail-agent style)
        answers = [{"id": c["id"], "mean": rest.get(c["predict"]["channel"], 0.0),
                    "low": rest.get(c["predict"]["channel"], 0.0) - 0.6,
                    "high": rest.get(c["predict"]["channel"], 0.0) + 0.6}
                   for c in spec["contracts"]]
        for pc in spec.get("preparation_contracts", []):
            ch = pc["goal"]["channel"]
            lo, hi = pc["goal"]["band"]
            mid = (lo + hi) / 2
            sgn = 1.0 if up.get(ch, 0.0) >= rest.get(ch, 0.0) else -1.0
            code = f"""
def policy(t, y, mem):
    err = {mid} - y[{ch}]
    drive = {sgn} * max(-1.0, min(1.0, 3.0 * err))
    return [drive] * {n_in}
"""
            _cmd(session, {"op": "answer_prep", "id": pc["id"], "code": code})
        return json.dumps({"op": "answer", "answers": answers})


AGENTS = {a.name: a for a in (NullAgent(), TailAgent(), ReferenceAgent(), PrepPIAgent())}


def run_baseline(difficulty: str, seed: int, agent_name: str,
                 n_per_stratum: int = 4, n_prep: int = 0) -> dict[str, Any]:
    from physim.engine import make_world
    world = make_world(difficulty, seed)
    session = PhysimSession(world, contract_seed=seed, n_per_stratum=n_per_stratum,
                            n_prep=n_prep)
    answer = AGENTS[agent_name].play(session)
    result = session.score(answer)
    result["agent"] = agent_name
    result["difficulty"] = difficulty
    result["seed"] = seed
    return result
