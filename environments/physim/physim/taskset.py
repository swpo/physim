"""physim — hidden-law world discovery taskset (M0, chat tier).

The agent faces an anonymous-port world (DESIGN.md v0.1-v0.5): input ports,
output ports, a tick budget, no semantics. It explores by submitting JSON
open-loop protocols, then answers evaluator-issued prediction contracts,
scored against fresh truth ensembles of the same hidden world.

Difficulty is a task parameter (D0..D3): port opacity, macro complexity
(modules), noise, and budget scale together.
"""

from __future__ import annotations

import itertools
import json
from collections.abc import Iterator
from typing import Literal

import verifiers.v1 as vf

from physim.engine import DIFFICULTY_PRESETS, make_world
from physim.session import PhysimSession

MAX_TURNS_DEFAULT = 40

SYSTEM_PROMPT = """You are a scientist studying an unknown dynamical system through a fixed interface. Nothing about the system's internal laws is documented. Everything must be discovered by experiment.

INTERFACE
- The system has {n_in} input ports (values in [-1, 1]) and {n_out} output ports (real-valued sensors). Port meanings, locations, polarities, and reliability are all unknown. Some sensors may be dead. The system has persistent internal state that evolves one tick at a time and may retain memory of past inputs.
- You interact ONLY by sending one JSON command per message:
  {{"op":"run","segments":[{{"t":50,"u":[u1,...]}}, {{"t":80,"u_start":[...],"u_end":[...]}}],"observe":{{"channels":[0,1,2],"series":true}}}}
     Advances the world through your input program (segments concatenate; "u" holds a constant vector for t ticks, "u_start"/"u_end" ramps linearly). Returns per-channel mean/sd over the last {tail} ticks; "series":true additionally returns downsampled traces for up to 6 channels. "channels" may be "all".
  {{"op":"reset"}}  -> draw fresh initial conditions (costs 200 ticks). State otherwise PERSISTS between runs.
  {{"op":"status"}} -> budget and interface info.
  {{"op":"ready"}}  -> end exploration early and receive the prediction contracts.
- Tick budget for all experiments combined: {budget}. Unspent budget is not rewarded; use it.

TASK
After exploration ends (you send "ready", or you run out of budget/turns), you receive prediction contracts. Each specifies an input protocol applied to a FRESH draw of this same system (same laws, new initial conditions) and asks for one statistic of one output channel (mean over the final {tail} ticks). You answer each with a point prediction and an interval:
  {{"op":"answer","answers":[{{"id":0,"mean":0.42,"low":0.1,"high":0.7}}, ...]}}
Scoring: accuracy = exp(-|error| / (3*ensemble_sd)) per contract, averaged. Your interval should cover the true ensemble mean (calibration is also measured). Unanswered contracts score 0.

ADVICE
- First learn your senses: measure the noise floor (zero input), find dead/live sensors, and each sensor's response direction.
- Then characterize the dynamics: response to steps of different sizes and signs, relaxation after release, dependence on history (path dependence / hysteresis), per-port differences.
- Contracts include held-out regimes: strong drives followed by release, weak pushes, and long autonomous evolution. Understand state memory before answering.
- Contracts are evaluated on FRESH initial draws, not on your current world state. Use reset to study how fresh states behave (relaxation, weak pushes of both signs) before answering.
- Budget your ticks: reserve enough exploration for release/memory behavior, not just steady states.
- Think between commands, but always end each message with exactly one JSON command."""


class PhysimData(vf.TaskData):
    difficulty: Literal["D0", "D1", "D2", "D3"] = "D0"
    world_seed: int = 0
    max_turns: int = MAX_TURNS_DEFAULT
    n_per_stratum: int = 4


class PhysimTaskConfig(vf.TaskConfig):
    pass


class PhysimTask(vf.Task[PhysimData, vf.State, PhysimTaskConfig]):
    """Scoring happens in the env loop (engine-authoritative), recorded on the trace."""


class PhysimConfig(vf.TasksetConfig):
    difficulty: Literal["D0", "D1", "D2", "D3"] = "D0"
    """World difficulty preset (port opacity + macro complexity + budget)."""
    seed0: int = 0
    """First world seed; task i uses seed0 + i."""
    max_turns: int = MAX_TURNS_DEFAULT
    """Max agent messages before contracts are forced."""
    n_per_stratum: int = 4
    """Contracts per stratum (S1 relax / S2 interpolation / S3 memory)."""


class PhysimEnvConfig(vf.EnvConfig):
    scientist: vf.AgentConfig = vf.AgentConfig()


class PhysimEnv(vf.Env[PhysimEnvConfig]):
    async def run(self, task, agents):
        data: PhysimData = task.data
        world = make_world(data.difficulty, data.world_seed)
        session = PhysimSession(world, contract_seed=data.world_seed,
                                n_per_stratum=data.n_per_stratum)
        answer_text: str | None = None
        async with agents.scientist.interaction(task) as interaction:
            segment = await interaction.turn()  # prompted task speaks first
            for _ in range(data.max_turns):
                if segment.terminated:
                    break
                reply = segment.last_reply or ""
                if session.phase == "answer":
                    answer_text = reply
                    break
                response = session.handle(reply)
                if session.phase == "answer" and "contracts" not in response:
                    # ready was acknowledged elsewhere; make sure specs are shown
                    response = session.issue_contracts()
                segment = await interaction.turn(json.dumps(response))
            else:
                # turn limit reached during exploration: force contracts, one shot
                if session.phase != "answer" and not segment.terminated:
                    forced = session.issue_contracts()
                    segment = await interaction.turn(json.dumps(forced))
                    if not segment.terminated:
                        answer_text = segment.last_reply or ""
            if session.phase != "answer":
                session.issue_contracts()

            result = session.score(answer_text)
            trace = interaction.trace
            trace.record_reward("accuracy", result["reward_accuracy"], 1.0)
            trace.record_metric("coverage", result["coverage"])
            trace.record_metric("replication_ref", result["replication_ref"])
            trace.record_metric("n_answered", result["n_answered"])
            trace.record_metric("budget_used_frac", result["budget_used_frac"])
            trace.record_metric("turns_used", float(session.turns))
            for stratum, acc in result["per_stratum"].items():
                trace.record_metric(f"acc_{stratum}", acc)
            trace.info["physim"] = {
                "difficulty": data.difficulty,
                "world_seed": data.world_seed,
                "detail": result["detail"],
                "parse_error": result.get("parse_error"),
            }


class PhysimTaskset(vf.Taskset[PhysimTask, PhysimConfig]):
    INFINITE = True

    def load(self) -> Iterator[PhysimTask]:
        params = DIFFICULTY_PRESETS[self.config.difficulty]
        for i in itertools.count():
            data = PhysimData(
                idx=i,
                name=f"physim-{self.config.difficulty}#{self.config.seed0 + i}",
                prompt=(
                    "Begin. Send your first JSON command to start exploring the "
                    "system. A good opening is a zero-input run to measure the "
                    "noise floor."
                ),
                system_prompt=SYSTEM_PROMPT.format(
                    n_in=params.n_in, n_out=params.n_out,
                    tail=20, budget=params.max_ticks,
                ),
                difficulty=self.config.difficulty,
                world_seed=self.config.seed0 + i,
                max_turns=self.config.max_turns,
                n_per_stratum=self.config.n_per_stratum,
            )
            yield PhysimTask(data, self.config.task)
