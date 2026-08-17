"""physim.servers.world — the world as an MCP tool server (coding-harness tier).

One shared server per environment worker; per-rollout worlds are isolated via
`self.state` (serialized engine snapshots ride the framework's state channel).
The tools mirror the chat-tier JSON ops 1:1 so results are comparable:

  physim_run(segments, channels, series, max_numbers) -> observation JSON
  physim_reset()   fresh initial conditions (costed)
  physim_status()  budget + interface card
  physim_ready()   freeze exploration, receive contracts
  physim_answer(answers) -> receipt (scored evaluator-side after the rollout)

The hidden world state itself never crosses to the agent: state carries a
compressed snapshot of (x, a, noise rng, ticks); wiring is rebuilt
deterministically from (difficulty, seed).
"""

from __future__ import annotations

import base64
import io
import json

import numpy as np

import verifiers.v1 as vf

from physim.engine import World, make_world
from physim.session import PhysimSession


def _snapshot(world: World) -> str:
    buf = io.BytesIO()
    rng_state = json.dumps(world._noise.bit_generator.state).encode()
    arrays = dict(
        ticks=np.array([world.ticks_used, world.n_resets]),
        rng=np.frombuffer(rng_state, dtype=np.uint8),
        port_energy=world.port_energy,
    )
    if world.p.reaction in ("grayscott", "grayscott2"):
        arrays.update(U=world.U, V=world.V)
        if world.p.reaction == "grayscott2":
            arrays.update(U2=world.U2, V2=world.V2)
    elif world.p.reaction == "excitable":
        arrays.update(eu=world.eu, ev=world.ev,
                      ext=np.array([world._ex_t]))
    elif world.p.reaction == "ecology":
        arrays.update(U1e=world.U1e, V1e=world.V1e,
                      U2e=world.U2e, V2e=world.V2e, Re=world.Re)
    elif world.p.reaction == "ecowave":
        arrays.update(U1e=world.U1e, V1e=world.V1e, Re=world.Re,
                      eu=world.eu, ev=world.ev, ext=np.array([world._ex_t]))
    elif world.p.reaction == "ecowave2":
        arrays.update(U1e=world.U1e, V1e=world.V1e, U2e=world.U2e,
                      V2e=world.V2e, Re=world.Re,
                      eu=world.eu, ev=world.ev, ext=np.array([world._ex_t]))
    elif world.p.reaction == "evo":
        arrays.update(U1e=world.U1e, V1e=world.V1e, Re=world.Re, Ge=world.Ge,
                      evt=np.array([getattr(world, "_evo_tick", 0)]))
    elif world.p.reaction == "enzyme":
        arrays.update(V1e=world.V1e, Ee=world.Ee, Re=world.Re, Ge=world.Ge,
                      evt=np.array([getattr(world, "_evo_tick", 0)]))
    else:
        arrays.update(x=world.x, a=world.a)
    if world.app_pos is not None:
        arrays.update(app_pos=world.app_pos,
                      app_gain=world.app_gain_mult,
                      app_en=world.app_enabled.astype(np.uint8),
                      app_acc=getattr(world, "_app_enable_acc",
                                      np.zeros(len(world.app_enabled))))
    np.savez_compressed(buf, **arrays)
    return base64.b64encode(buf.getvalue()).decode()


def _restore(world: World, snap: str) -> None:
    buf = io.BytesIO(base64.b64decode(snap))
    z = np.load(buf)
    if world.p.reaction in ("grayscott", "grayscott2"):
        world.U = z["U"]
        world.V = z["V"]
        if world.p.reaction == "grayscott2":
            world.U2 = z["U2"]
            world.V2 = z["V2"]
    elif world.p.reaction == "excitable":
        world.eu = z["eu"]
        world.ev = z["ev"]
        world._ex_t = int(z["ext"][0])
    elif world.p.reaction == "ecology":
        world.U1e = z["U1e"]; world.V1e = z["V1e"]
        world.U2e = z["U2e"]; world.V2e = z["V2e"]
        world.Re = z["Re"]
    elif world.p.reaction == "ecowave":
        world.U1e = z["U1e"]; world.V1e = z["V1e"]; world.Re = z["Re"]
        world.eu = z["eu"]; world.ev = z["ev"]; world._ex_t = int(z["ext"][0])
    elif world.p.reaction == "ecowave2":
        world.U1e = z["U1e"]; world.V1e = z["V1e"]
        world.U2e = z["U2e"]; world.V2e = z["V2e"]; world.Re = z["Re"]
        world.eu = z["eu"]; world.ev = z["ev"]; world._ex_t = int(z["ext"][0])
    elif world.p.reaction == "evo":
        world.U1e = z["U1e"]; world.V1e = z["V1e"]; world.Re = z["Re"]
        world.Ge = z["Ge"]; world._evo_tick = int(z["evt"][0])
    elif world.p.reaction == "enzyme":
        world.V1e = z["V1e"]; world.Ee = z["Ee"]; world.Re = z["Re"]
        world.Ge = z["Ge"]; world._evo_tick = int(z["evt"][0])
    else:
        world.x = z["x"]
        world.a = z["a"]
    if "app_pos" in z.files and world.app_pos is not None:
        world.app_pos = z["app_pos"]
        world.app_gain_mult = z["app_gain"]
        world.app_enabled = z["app_en"].astype(bool)
        world._app_enable_acc = z["app_acc"]
    world.ticks_used = int(z["ticks"][0])
    world.n_resets = int(z["ticks"][1])
    if "port_energy" in z.files:
        world.port_energy = z["port_energy"]
    world._noise.bit_generator.state = json.loads(bytes(z["rng"]).decode())


class PhysimToolState(vf.State):
    difficulty: str = ""
    world_seed: int = 0
    n_per_stratum: int = 4
    n_prep: int = 0
    snapshot: str = ""
    phase: str = "explore"
    answers_json: str = ""      # last submitted answers (evaluator scores post-hoc)
    prep_answers: dict[int, str] = {}   # prep contract id -> policy code
    theory_code: str = ""
    contracts_cache: str = ""   # JSON [Contract fields] — sampled once at ready()
    preps_cache: str = ""       # JSON [PrepContract fields]
    turns: int = 0


class PhysimToolsetConfig(vf.ToolsetConfig):
    pass


class PhysimToolset(vf.Toolset[vf.ToolsetConfig, PhysimToolState]):
    TOOL_PREFIX = "physim"

    # ---- internals ----
    def _session(self) -> PhysimSession:
        st = self.state
        world = make_world(st.difficulty or "D0", st.world_seed)
        if st.snapshot:
            _restore(world, st.snapshot)
        s = PhysimSession(world, contract_seed=st.world_seed,
                          n_per_stratum=st.n_per_stratum,
                          n_prep=st.n_prep)
        s.phase = st.phase or "explore"
        s.prep_answers = dict(st.prep_answers or {})
        s.theory_code = st.theory_code or ""
        if st.contracts_cache:
            from physim.session import Contract, PrepContract
            s.contracts = [Contract(**d) for d in json.loads(st.contracts_cache)]
            s.prep_contracts = [PrepContract(**d)
                                for d in json.loads(st.preps_cache or "[]")]
        return s

    def _save(self, s: PhysimSession) -> None:
        self.state.snapshot = _snapshot(s.world)
        self.state.phase = s.phase
        self.state.prep_answers = dict(s.prep_answers)
        self.state.theory_code = s.theory_code
        if s.contracts and not self.state.contracts_cache:
            from dataclasses import asdict
            self.state.contracts_cache = json.dumps([asdict(c) for c in s.contracts])
            self.state.preps_cache = json.dumps([asdict(c) for c in s.prep_contracts])
        self.state.turns += 1

    def _dispatch(self, cmd: dict) -> str:
        st = self.state
        if not st.difficulty:
            return json.dumps({"error": "world not initialized; retry in a moment"})
        s = self._session()
        out = s.handle(json.dumps(cmd))
        self._save(s)
        return json.dumps(out)

    # ---- tools ----
    @vf.tool(name="run")
    async def run_experiment(self, segments: list, channels: list | str = "all",
                  series: bool = False, max_numbers: int = 360,
                  stride: int = 0) -> str:
        """Advance the hidden system through an input program and observe sensors.

        segments: list of {"t": ticks, "u": [values]} holds or
        {"t": ticks, "u_start": [...], "u_end": [...]} linear ramps, executed in
        order against the persistent system state (values clipped to [-1, 1]).
        channels: "all" or a list of sensor indices to report.
        series=True additionally returns downsampled per-tick traces for up to
        6 channels (at most max_numbers values total; optional stride).
        Returns JSON: per-channel mean/sd over the final 20 ticks, budget left,
        and the series if requested."""
        # Some MCP clients deliver structured args as JSON strings (sometimes
        # double-encoded, sometimes per-element); normalize aggressively.
        def _decode(v, depth=3):
            while isinstance(v, str) and depth > 0:
                try:
                    v = json.loads(v)
                except json.JSONDecodeError:
                    break
                depth -= 1
            return v

        segments = _decode(segments)
        if isinstance(segments, dict):
            segments = [segments]
        if isinstance(segments, list):
            segments = [_decode(seg) for seg in segments]
        if not (isinstance(segments, list)
                and all(isinstance(seg, dict) for seg in segments)):
            return json.dumps({"error": (
                "segments must be a JSON array of objects like "
                '[{"t": 100, "u": [0.5, 0, ...]}] — got '
                f"{type(segments).__name__}"
                + (f" of {type(segments[0]).__name__}" if isinstance(segments, list) and segments else ""))})
        if isinstance(channels, str) and channels != "all":
            try:
                channels = json.loads(channels)
            except json.JSONDecodeError:
                pass
        obs = {"channels": channels, "series": bool(series),
               "max_numbers": int(max_numbers)}
        if stride:
            obs["stride"] = int(stride)
        return self._dispatch({"op": "run", "segments": segments, "observe": obs})

    @vf.tool(name="run_policy")
    async def run_policy(self, code: str, t: int, channels: list | str = "all",
                         series: bool = False, max_numbers: int = 360) -> str:
        """Closed-loop experiment: your code defines policy(t, y, mem) -> list of
        n_in floats in [-1,1]; it is executed tick-synchronously against the live
        system for t ticks (y = current sensor readings, mem = a persistent dict).
        Sandboxed: math and np (numpy, no file IO) available; no imports.
        Costs t ticks of budget. Returns the same observation format as run."""
        obs = {"channels": channels, "series": bool(series),
               "max_numbers": int(max_numbers)}
        return self._dispatch({"op": "run_policy", "code": code, "t": int(t),
                               "observe": obs})

    @vf.tool(name="answer_prep")
    async def answer_prep(self, id: int, code: str) -> str:
        """Submit a preparation-contract policy: code defining policy(t, y, mem)
        that steers a FRESH draw of the system into the contract's band within
        its tick budget (the band is then checked on a free run after release).
        May be resubmitted; the last submission per contract id is scored."""
        return self._dispatch({"op": "answer_prep", "id": int(id), "code": code})

    @vf.tool(name="submit_theory")
    async def submit_theory(self, code: str) -> str:
        """OPTIONAL bonus: submit an executable theory of the system — code
        defining init(y_history) -> state and step(state, a) -> (state, y_pred)
        where a is the input vector and y_pred the predicted next sensor
        readings (length n_out). Scored after the rollout by simulating every
        prediction-contract protocol; adds a separate theory reward. Sandboxed
        like run_policy (math + np, no imports/files). Resubmission replaces."""
        return self._dispatch({"op": "submit_theory", "code": code})

    @vf.tool(name="reset")
    async def reset_world(self) -> str:
        """Draw fresh initial conditions for the system (costs 200 ticks of budget).
        The system's hidden laws stay the same; only the state re-randomizes."""
        return self._dispatch({"op": "reset"})

    @vf.tool
    async def status(self) -> str:
        """Report exploration phase, remaining tick budget, and the interface card."""
        return self._dispatch({"op": "status"})

    @vf.tool
    async def ready(self, confirm: bool = False) -> str:
        """End exploration and receive the prediction contracts to answer.
        If less than 5% of the tick budget has been used, requires confirm=true
        (ending exploration that early is almost always an accident)."""
        return self._dispatch({"op": "ready", "confirm": bool(confirm)})

    @vf.tool
    async def answer(self, answers: list) -> str:
        """Submit final answers: a list of {"id": int, "mean": float, "low": float,
        "high": float}, one per contract. OPTIONAL: add "quantiles":
        {"0.1": v, "0.25": v, "0.5": v, "0.75": v, "0.9": v} — scoring is a
        proper distributional score (CRPS), so where the system is stochastic
        or has multiple regimes, reporting your honest full distribution
        (including spread and multimodality) scores strictly better than any
        single point. May be called again to revise; the last submission is
        scored."""
        st = self.state
        if st.phase != "answer":
            return json.dumps({"error": (
                "exploration is still active; call physim_ready first to "
                "receive the contracts, then submit answers")})
        norm = []
        bad = 0
        items = answers if isinstance(answers, list) else [answers]
        for a in items:
            if isinstance(a, str):
                try:
                    a = json.loads(a)
                except json.JSONDecodeError:
                    bad += 1
                    continue
            if isinstance(a, dict) and "id" in a:
                try:
                    entry = {"id": int(a["id"]),
                             "mean": float(a.get("mean", 0.0)),
                             "low": float(a.get("low", a.get("mean", 0.0))),
                             "high": float(a.get("high", a.get("mean", 0.0)))}
                    qs = a.get("quantiles")
                    if isinstance(qs, dict) and qs:
                        try:
                            entry["quantiles"] = {
                                str(float(k)): float(v) for k, v in qs.items()}
                        except (TypeError, ValueError):
                            pass
                    norm.append(entry)
                except (TypeError, ValueError):
                    bad += 1
            else:
                bad += 1
        st.answers_json = json.dumps({"op": "answer", "answers": norm})
        note = "answers recorded; they are scored after the rollout ends"
        if bad:
            note += f" ({bad} entries were malformed and dropped)"
        return json.dumps({"ok": True, "received": len(norm), "rejected": bad,
                           "note": note})


if __name__ == "__main__":
    PhysimToolset.run()
