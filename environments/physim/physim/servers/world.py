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
    np.savez_compressed(
        buf, x=world.x, a=world.a,
        ticks=np.array([world.ticks_used, world.n_resets]),
        rng=np.frombuffer(rng_state, dtype=np.uint8),
    )
    return base64.b64encode(buf.getvalue()).decode()


def _restore(world: World, snap: str) -> None:
    buf = io.BytesIO(base64.b64decode(snap))
    z = np.load(buf)
    world.x = z["x"]
    world.a = z["a"]
    world.ticks_used = int(z["ticks"][0])
    world.n_resets = int(z["ticks"][1])
    world._noise.bit_generator.state = json.loads(bytes(z["rng"]).decode())


class PhysimToolState(vf.State):
    difficulty: str = ""
    world_seed: int = 0
    n_per_stratum: int = 4
    snapshot: str = ""
    phase: str = "explore"
    answers_json: str = ""      # last submitted answers (evaluator scores post-hoc)
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
                          n_per_stratum=st.n_per_stratum)
        s.phase = st.phase or "explore"
        if s.phase == "answer":
            s.contracts = s.contracts or []
        return s

    def _save(self, s: PhysimSession) -> None:
        self.state.snapshot = _snapshot(s.world)
        self.state.phase = s.phase
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
        obs = {"channels": channels, "series": bool(series),
               "max_numbers": int(max_numbers)}
        if stride:
            obs["stride"] = int(stride)
        return self._dispatch({"op": "run", "segments": segments, "observe": obs})

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
    async def ready(self) -> str:
        """End exploration and receive the prediction contracts to answer."""
        return self._dispatch({"op": "ready"})

    @vf.tool
    async def answer(self, answers: list) -> str:
        """Submit final answers: a list of {"id": int, "mean": float, "low": float,
        "high": float}, one per contract. May be called again to revise before the
        rollout ends; the last submission is scored."""
        st = self.state
        if st.phase != "answer":
            s = self._session()
            s.issue_contracts()
            self._save(s)
        st.answers_json = json.dumps({"op": "answer", "answers": answers})
        n = len(answers) if isinstance(answers, list) else 0
        return json.dumps({"ok": True, "received": n,
                           "note": "answers recorded; they are scored after the rollout ends"})


if __name__ == "__main__":
    PhysimToolset.run()
