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
- Contracts include held-out regimes: strong drives followed by release, weak pushes, long autonomous evolution, and multi-stage sequences with long settling periods. Understand state memory and any slow drift before answering.
- Contracts are evaluated on FRESH initial draws, not on your current world state. Use reset to study how fresh states behave (relaxation, weak pushes of both signs) before answering.
- Budget your ticks: reserve enough exploration for release/memory behavior, not just steady states.
- Think between commands, but always end each message with exactly one JSON command."""


class PhysimData(vf.TaskData):
    difficulty: Literal["D0", "D1", "D2", "D3", "D4"] = "D0"
    world_seed: int = 0
    max_turns: int = MAX_TURNS_DEFAULT
    n_per_stratum: int = 4
    tier: Literal["chat", "tools"] = "chat"


TOOLS_SYSTEM_PROMPT = """You are a scientist studying an unknown dynamical system through a fixed tool interface. Nothing about the system's internal laws is documented. Everything must be discovered by experiment.

INTERFACE (MCP tools)
- physim_run(segments, channels, series, max_numbers): advance the hidden system through an input program and observe sensors. segments = [{{"t": ticks, "u": [values]}}, ...] holds, or {{"t":.., "u_start":[..], "u_end":[..]}} ramps; values in [-1,1]; the system has {n_in} input ports and {n_out} output sensors with persistent internal state (one tick at a time, may retain memory of past inputs). Returns per-channel mean/sd over the final {tail} ticks; series=true adds downsampled traces (<=6 channels). segments MUST be a JSON array of objects, e.g. physim_run(segments=[{{"t": 100, "u": [0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0]}}], channels="all").
- physim_reset(): fresh initial conditions (costs 200 ticks). State otherwise PERSISTS between runs.
- physim_status(): budget and interface info.
- physim_ready(): end exploration, receive prediction contracts.
- physim_answer(answers): submit [{{"id":..,"mean":..,"low":..,"high":..}}, ...]. May be revised; last submission scores.
- Tick budget for all experiments: {budget}. Unspent budget is not rewarded.

TASK
After physim_ready() you receive contracts: each specifies an input protocol applied to a FRESH draw of this same system (same laws, new initial conditions) and asks for the mean of one sensor over the final {tail} ticks. Score per contract: exp(-|error|/scale). Give calibrated [low,high] intervals. Unanswered contracts score 0.

STRATEGY
You have a full coding environment: write files and scripts to record every experiment result, fit response curves offline (per-port gains, signs, time constants, saturation, hysteresis branches, drift/adaptation over hundreds of ticks), and simulate your fitted model to predict each contract protocol. Contracts include held-out regimes: weak pushes + relaxation, steady drives, strong drive + release (branch memory), and multi-stage sequences with long settling windows -- systems like this can show duration-dependent effects and slow internal drift; design experiments that measure them. Use the tick budget generously; reserve turns to answer ALL contracts. Call physim_answer before finishing."""


class PhysimTaskConfig(vf.TaskConfig):
    tier: Literal["chat", "tools"] = "chat"
    tools: vf.ToolsetConfig = vf.ToolsetConfig()


from physim.servers.world import PhysimToolState


class PhysimTask(vf.Task[PhysimData, PhysimToolState, PhysimTaskConfig]):
    @classmethod
    def toolsets(cls, config: "PhysimTaskConfig") -> list[vf.Toolset]:
        if config.tier != "tools":
            return []
        from physim.servers.world import PhysimToolset
        return [PhysimToolset(config.tools)]

    async def setup(self, trace: vf.Trace, runtime) -> None:
        # Host-side state init: the tool server pulls trace.state through the
        # state channel on every call (server-side setup_task mutations would
        # only hit its inert fallback state).
        st = trace.state
        st.difficulty = self.data.difficulty
        st.world_seed = self.data.world_seed
        st.n_per_stratum = self.data.n_per_stratum

    """Chat tier: scoring happens in PhysimEnv. Tools tier: the toolset records
    the last answers + world snapshot in trace.state; score() replays them."""

    @vf.reward(weight=1.0)
    async def accuracy(self, trace: vf.Trace) -> float:
        if self.data.tier != "tools":
            # chat tier: PhysimEnv computed the score during the episode and
            # stashed it in trace.info (score() re-seeds trace.rewards, so the
            # env cannot record the reward directly).
            info = (trace.info or {}).get("physim") or {}
            return float(info.get("reward_accuracy") or 0.0)
        from physim.session import PhysimSession
        from physim.engine import make_world

        st = trace.state
        world = make_world(self.data.difficulty, self.data.world_seed)
        session = PhysimSession(world, contract_seed=self.data.world_seed,
                                n_per_stratum=self.data.n_per_stratum)
        result = session.score(getattr(st, "answers_json", "") or None)
        trace.record_metric("coverage", result["coverage"])
        trace.record_metric("replication_ref", result["replication_ref"])
        trace.record_metric("n_answered", result["n_answered"])
        for stratum, acc in result["per_stratum"].items():
            trace.record_metric(f"acc_{stratum}", acc)
        snap = getattr(st, "snapshot", "")
        if snap:
            try:
                from physim.servers.world import _restore
                w2 = make_world(self.data.difficulty, self.data.world_seed)
                _restore(w2, snap)
                trace.record_metric("budget_used_frac",
                                    w2.ticks_used / w2.p.max_ticks)
            except Exception:
                pass
        trace.info["physim"] = {
            "difficulty": self.data.difficulty,
            "world_seed": self.data.world_seed,
            "tier": "tools",
            "detail": result["detail"],
            "parse_error": result.get("parse_error"),
        }
        return float(result["reward_accuracy"])


class PhysimConfig(vf.TasksetConfig):
    difficulty: Literal["D0", "D1", "D2", "D3", "D4"] = "D0"
    """World difficulty preset (port opacity + macro complexity + budget)."""
    tier: Literal["chat", "tools"] = "chat"
    """chat: JSON-over-messages loop (PhysimEnv drives). tools: per-rollout MCP
    world server for coding harnesses (codex/claude_code); scoring in Task."""
    seed0: int = 0
    """First world seed; task i uses seed0 + i."""
    max_turns: int = MAX_TURNS_DEFAULT
    """Max agent messages before contracts are forced."""
    n_per_stratum: int = 4
    """Contracts per stratum (S1 relax / S2 interpolation / S3 memory)."""
    task: PhysimTaskConfig = PhysimTaskConfig()
    """Per-task config (tier is copied from the taskset-level field)."""


class PhysimEnvConfig(vf.EnvConfig):
    scientist: vf.AgentConfig = vf.AgentConfig()


class PhysimEnv(vf.Env[PhysimEnvConfig]):
    async def run(self, task, agents):
        data: PhysimData = task.data
        if data.tier == "tools":
            # coding-harness tier: the agent drives the MCP toolset itself;
            # scoring happens in PhysimTask.accuracy from trace.state.
            await agents.scientist.run(task)
            return
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
                "tier": "chat",
                "reward_accuracy": result["reward_accuracy"],
                "detail": result["detail"],
                "parse_error": result.get("parse_error"),
            }


class PhysimTaskset(vf.Taskset[PhysimTask, PhysimConfig]):
    INFINITE = True

    def load(self) -> Iterator[PhysimTask]:
        params = DIFFICULTY_PRESETS[self.config.difficulty]
        tools_tier = self.config.tier == "tools"
        for i in itertools.count():
            if tools_tier:
                prompt = (
                    "Begin your investigation of the system using the physim_* "
                    "tools. Explore, build a quantitative model in your workspace, "
                    "then call physim_ready and answer every contract with "
                    "physim_answer."
                )
                system_prompt = TOOLS_SYSTEM_PROMPT.format(
                    n_in=params.n_in, n_out=params.n_out,
                    tail=20, budget=params.max_ticks,
                )
            else:
                prompt = (
                    "Begin. Send your first JSON command to start exploring the "
                    "system. A good opening is a zero-input run to measure the "
                    "noise floor."
                )
                system_prompt = SYSTEM_PROMPT.format(
                    n_in=params.n_in, n_out=params.n_out,
                    tail=20, budget=params.max_ticks,
                )
            data = PhysimData(
                idx=i,
                name=f"physim-{self.config.difficulty}#{self.config.seed0 + i}",
                prompt=prompt,
                system_prompt=system_prompt,
                difficulty=self.config.difficulty,
                world_seed=self.config.seed0 + i,
                max_turns=self.config.max_turns,
                n_per_stratum=self.config.n_per_stratum,
                tier="tools" if tools_tier else "chat",
            )
            task_config = self.config.task.model_copy(
                update={"tier": self.config.tier})
            yield PhysimTask(data, task_config)
