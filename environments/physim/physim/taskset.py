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

WORKSPACE_TEXT_EXTS = {".md", ".txt", ".py", ".json", ".csv", ".yaml", ".yml", ".toml"}
WORKSPACE_FILE_CAP = 120_000       # chars per file
WORKSPACE_TOTAL_CAP = 600_000      # chars per rollout


def _extract_workspace(artifacts: dict | None) -> dict:
    """Text files from collected workspace tars -> {path: content}, capped."""
    if not artifacts:
        return {}
    import io
    import tarfile
    from pathlib import PurePosixPath

    out: dict[str, str] = {}
    total = 0
    for source, blob in artifacts.items():
        if not blob:
            continue
        try:
            tar = tarfile.open(fileobj=io.BytesIO(blob))
        except tarfile.TarError:
            continue
        with tar:
            for member in tar.getmembers():
                if not member.isfile() or member.size > 2_000_000:
                    continue
                if PurePosixPath(member.name).suffix.lower() not in WORKSPACE_TEXT_EXTS:
                    continue
                fh = tar.extractfile(member)
                if fh is None:
                    continue
                try:
                    text = fh.read().decode("utf-8", errors="replace")
                except Exception:
                    continue
                text = text[:WORKSPACE_FILE_CAP]
                if total + len(text) > WORKSPACE_TOTAL_CAP:
                    break
                out[member.name] = text
                total += len(text)
    return out

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
After exploration ends (you send "ready", or you run out of budget/turns), you receive prediction contracts. Each specifies an input protocol applied to a FRESH draw of this same system (same laws, new initial conditions) and asks for one statistic of one output channel — the mean over the final {tail} ticks, or on some worlds the standard deviation over a ~200-tick window, or the count of upward threshold crossings (event rate; threshold = channel median + 1 sd) — the contract says which. You answer each with a point prediction and an interval:
  {{"op":"answer","answers":[{{"id":0,"mean":0.42,"low":0.1,"high":0.7}}, ...]}}
Scoring: a proper distributional score (CRPS against the repetition ensemble; reduces to exp(-|error|/(3*ensemble_sd)) for point answers on deterministic contracts). You MAY add "quantiles":{{"0.1":..,"0.25":..,"0.5":..,"0.75":..,"0.9":..}} to any answer — where the system is stochastic or has multiple possible regimes, reporting your honest distribution scores strictly better than any single point. Your interval should cover the true ensemble mean (calibration is also measured). Unanswered contracts score 0.

ADVICE
- First learn your senses: measure the noise floor (zero input), find dead/live sensors, and each sensor's response direction.
- Then characterize the dynamics: response to steps of different sizes and signs, relaxation after release, dependence on history (path dependence / hysteresis), per-port differences.
- Contracts include held-out regimes: strong drives followed by release, weak pushes, long autonomous evolution, and multi-stage sequences with long settling periods. Understand state memory and any slow drift before answering.
- Contracts are evaluated on FRESH initial draws, not on your current world state. Use reset to study how fresh states behave (relaxation, weak pushes of both signs) before answering.
- Budget your ticks: reserve enough exploration for release/memory behavior, not just steady states.
- Think between commands, but always end each message with exactly one JSON command."""


class PhysimData(vf.TaskData):
    difficulty: Literal["D0", "D1", "D2", "D3", "D4", "C0", "C1", "C2", "C3", "C4", "B0", "B0a", "B0b", "B1", "B2", "E0", "E1", "E2"] = "D0"
    world_seed: int = 0
    max_turns: int = MAX_TURNS_DEFAULT
    n_per_stratum: int = 4
    n_prep: int = 0
    calibration_weight: float = 0.0
    tier: Literal["chat", "tools"] = "chat"


TOOLS_SYSTEM_PROMPT = """You are a scientist studying an unknown dynamical system through a fixed tool interface. Nothing about the system's internal laws is documented. Everything must be discovered by experiment.

INTERFACE (MCP tools)
- physim_run(segments, channels, series, max_numbers): advance the hidden system through an input program and observe sensors. segments = [{{"t": ticks, "u": [values]}}, ...] holds, or {{"t":.., "u_start":[..], "u_end":[..]}} ramps; values in [-1,1]; the system has {n_in} input ports and {n_out} output sensors with persistent internal state (one tick at a time, may retain memory of past inputs). Returns per-channel mean/sd over the final {tail} ticks; series=true adds downsampled traces (<=6 channels). segments MUST be a JSON array of objects, e.g. physim_run(segments=[{{"t": 100, "u": [0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0]}}], channels="all").
- physim_reset(): fresh initial conditions (costs 200 ticks). State otherwise PERSISTS between runs.
- physim_status(): budget and interface info.
- physim_ready(): end exploration, receive prediction contracts.
- physim_answer(answers): submit [{{"id":..,"mean":..,"low":..,"high":..}}, ...]. May be revised; last submission scores.
- physim_run_policy(code, t): closed-loop experiment — your code defines policy(t, y, mem) -> [{n_in} floats]; it runs tick-synchronously against the live system (y = current sensor readings). Use it to build feedback controllers (clamps) that hold states no open-loop input can reach. Sandboxed: math + np only, no imports/files.
- physim_answer_prep(id, code): submit a policy for a PREPARATION contract (steer a fresh draw into a stated sensor band; verified on 5 fresh draws after release).
- physim_submit_theory(code): OPTIONAL — submit an executable theory (init/step simulator of the sensors); scored separately after the rollout.
- Tick budget for all experiments: {budget}. Unspent budget is not rewarded.

TASK
After physim_ready() you receive contracts: each specifies an input protocol applied to a FRESH draw of this same system (same laws, new initial conditions) and asks for one statistic of one sensor: its mean over the final {tail} ticks, or (on some worlds) its standard deviation over a ~200-tick window, or the COUNT of upward threshold crossings in that window (a pulse/event rate) — the contract says which. Score per contract: a proper distributional score (CRPS against the repetition ensemble; for a point answer on a deterministic contract this reduces to exp(-|error|/scale)). OPTIONAL "quantiles" per answer (see physim_answer) — where the system is stochastic or has multiple regimes, an honest full distribution scores strictly better than any point. An interval score also rewards NARROW intervals that contain the truth and heavily penalizes misses (honest width = your real uncertainty). Give calibrated [low,high] intervals. Unanswered contracts score 0.

STRATEGY
You have a full coding environment: write files and scripts to record every experiment result, fit response curves offline (per-port gains, signs, time constants, saturation, hysteresis branches, drift/adaptation over hundreds of ticks), and simulate your fitted model to predict each contract protocol. Contracts include held-out regimes: weak pushes + relaxation, steady drives, strong drive + release (branch memory), and multi-stage sequences with long settling windows -- systems like this can show duration-dependent effects and slow internal drift; design experiments that measure them. Characterize both the LEVELS and the VARIABILITY of every responsive channel — some contracts ask for fluctuation (sd) rather than mean. Use the tick budget generously; reserve turns to answer ALL contracts. Call physim_answer before finishing."""


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

    async def finalize(self, trace: vf.Trace, runtime) -> None:
        if self.data.tier != "tools":
            return
        try:
            from verifiers.v1.utils.artifacts import collect
            trace.state.artifacts = await collect(runtime, self.data.artifacts)
        except Exception as e:  # collection must never fail the rollout
            trace.info.setdefault("physim_artifact_error", str(e))

    async def setup(self, trace: vf.Trace, runtime) -> None:
        # Host-side state init: the tool server pulls trace.state through the
        # state channel on every call (server-side setup_task mutations would
        # only hit its inert fallback state).
        st = trace.state
        st.difficulty = self.data.difficulty
        st.world_seed = self.data.world_seed
        st.n_per_stratum = self.data.n_per_stratum
        st.n_prep = self.data.n_prep

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
                                n_per_stratum=self.data.n_per_stratum,
                                n_prep=self.data.n_prep)
        session.prep_answers = dict(getattr(st, "prep_answers", {}) or {})
        session.theory_code = getattr(st, "theory_code", "") or ""
        cache = getattr(st, "contracts_cache", "") or ""
        if cache:
            import json as _json
            from physim.session import Contract, PrepContract
            session.contracts = [Contract(**d) for d in _json.loads(cache)]
            session.prep_contracts = [
                PrepContract(**d)
                for d in _json.loads(getattr(st, "preps_cache", "") or "[]")]
        elif session.n_prep or session.theory_code:
            session.issue_contracts()
        result = session.score(getattr(st, "answers_json", "") or None)
        trace.record_reward("calibration", result.get("reward_calibration", 0.0),
                            float(self.data.calibration_weight))
        if "reward_preparation" in result:
            trace.record_reward("preparation", result["reward_preparation"], 1.0)
            trace.record_metric("prep_n", float(len(result.get("prep_detail", []))))
        if "theory" in result:
            th = result["theory"]
            trace.record_reward("theory", th["theory_accuracy"], 0.0)  # report-only weight
            trace.record_metric("theory_code_chars", float(th["code_chars"]))
            for stratum, acc in th["per_stratum"].items():
                trace.record_metric(f"theory_acc_{stratum}", acc)
        trace.record_metric("coverage", result["coverage"])
        trace.record_metric("replication_ref", result["replication_ref"])
        if "reward_accuracy_legacy" in result:
            trace.record_metric("accuracy_legacy", result["reward_accuracy_legacy"])
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
                for k, v in w2.conduct_metrics().items():
                    trace.record_metric(k, v)
            except Exception:
                pass
        trace.info["physim"] = {
            "difficulty": self.data.difficulty,
            "world_seed": self.data.world_seed,
            "tier": "tools",
            "detail": result["detail"],
            "parse_error": result.get("parse_error"),
            "workspace": _extract_workspace(getattr(st, "artifacts", None)),
            "prep_detail": result.get("prep_detail"),
            "theory": {k: v for k, v in (result.get("theory") or {}).items()
                       if k != "detail"} or None,
            "theory_detail": (result.get("theory") or {}).get("detail"),
        }
        return float(result["reward_accuracy"])


class PhysimConfig(vf.TasksetConfig):
    difficulty: Literal["D0", "D1", "D2", "D3", "D4", "C0", "C1", "C2", "C3", "C4", "B0", "B0a", "B0b", "B1", "B2", "E0", "E1", "E2", "BLOB-E1", "BLOB-E1r2", "BLOB-E2", "BLOB-E3"] = "D0"
    """World difficulty preset (port opacity + macro complexity + budget).
    BLOB-* = Track A probe-device episodes on evolved worlds (tools tier
    only; E2/E3 registered but gated for round 1 — see physim/blobcore.py)."""
    tier: Literal["chat", "tools"] = "chat"
    """chat: JSON-over-messages loop (PhysimEnv drives). tools: per-rollout MCP
    world server for coding harnesses (codex/claude_code); scoring in Task."""
    seed0: int = 0
    """First world seed; task i uses seed0 + i."""
    max_turns: int = MAX_TURNS_DEFAULT
    """Max agent messages before contracts are forced."""
    n_per_stratum: int = 4
    """Contracts per stratum (S1 relax / S2 interpolation / S3 memory)."""
    n_prep: int = 0
    """Preparation contracts (M2): submit-a-policy steering tasks. 0 = off."""
    calibration_weight: float = 0.0
    """Weight for the interval-calibration reward (Winkler-based). 0 = report-only."""
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
                                n_per_stratum=data.n_per_stratum,
                                n_prep=data.n_prep)
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
            trace.record_reward("calibration_chat", result.get("reward_calibration", 0.0), 0.0)
            trace.record_metric("coverage", result["coverage"])
            trace.record_metric("replication_ref", result["replication_ref"])
            trace.record_metric("n_answered", result["n_answered"])
            trace.record_metric("budget_used_frac", result["budget_used_frac"])
            trace.record_metric("turns_used", float(session.turns))
            for k, v in session.world.conduct_metrics().items():
                trace.record_metric(k, v)
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




# ============================================================ BLOB family
# Track A round 1: probe-device episodes on evolved blob worlds. Additive
# to the file: its own Data/Task classes + a branch in PhysimTaskset.load.
# Design + scoring live in physim/blobcore.py; the agent-facing MCP surface
# in physim/servers/blob.py. Tools tier ONLY (coding harnesses drive the
# probe_* toolset; there is no chat-tier BLOB loop).

BLOB_SYSTEM_PROMPT = """You are a scientist studying an unknown spatial dynamical system through two remote sensor devices. Nothing about the system, the devices' structure, or their relation to it is documented. Everything must be discovered by experiment.

INTERFACE (MCP tools, prefix probe_)
- Two devices, ids 0 and 1. Each device is a fixed rigid cluster of point sensors: device 0 has {k0} sensor slots, device 1 has {k1}. Every slot reports {n_ports} scalar channels ("ports") — the same anonymous physical quantities sampled by that slot. Slot order and port order are fixed all episode but carry no disclosed meaning. You also get free per-port global mean/variance of the whole (unobserved) medium: a weather report, not a map.
- probe_status(): time, budgets, costs, caps, the contracts, lock state.
- probe_read_streams(window, devices, ports, stride): advance the world up to `window` 5tu steps, reading sensors each `stride`-th step. Sensor cost = slots x 5 per read step per device.
- probe_wait(steps): advance without reading. Free.
- probe_adjust(device, u1, u2, u3, steps, read): apply a 3-channel actuator to one device; each u in [-1, 1], cost |u1|+|u2|+|u3| per step. What the channels do to the device is fixed all episode but undisclosed — the effect of each channel, their interactions, and any limits are yours to discover from the streams. Cost is charged on the commanded u, whatever the effect.
- probe_inject(port, amp, dur, lags, devices, ports): ONLY after the span ends. Forks an independent replica of the world from the span's final instant, drives a FIXED emission channel with (port, amp) for dur tu, and returns reads at your lags. Where and what the emission channel couples to is undisclosed. amp <= 1.0 with steeply convex pricing above 0.5; amp=0 = control replica. Replicas share the same start state and noise stream: differences between replicas are causal responses. The same channel carries the announced protocol.
- probe_submit(contract, payload): submit/revise contract predictions.

EPISODE
The world runs t = 0 to {t0} tu in 5tu steps (the SPAN), then hard-stops. What happens after t={t0} is never directly observable — it is exactly what the contracts ask you to predict. After the span you may run up to {max_replicas} replica experiments (probe_inject) to calibrate causal responses. Budgets (sensor {b_sensor:.0f}, adjust {b_adjust:.0f}, injection {b_injection:.0f}) cover the whole episode; unspent budget is not rewarded.

CONTRACTS (issued now; details via probe_status)
- P1 (weight {w1}): the streams of device 0 in its t=0 configuration at {p1_h} tu after the span ends, without injection. payload mean shape [{n_h}][{n_ports}][{k0}].
- P2 (weight {w2}): per consecutive {p2_win:.0f}tu window after the span (there are {p2_n}), the count of upward crossings of the announced (port, threshold, sign) summed over device 0's slots in its t=0 configuration, without injection. payload mean shape [{p2_n}].
- P3 (weight {w3}, flagship): the harness will run the ANNOUNCED emission (see probe_status: port, amp {ann_amp:g} — far above your cap — dur {ann_dur:g}tu) from the span end, through the same fixed emission channel you use. Predict device 1's streams in its t=0 configuration at the announced lags. payload mean shape [{n_lags}][{n_ports}][{k1}].
Contract truths are evaluated with each device as it was at t=0, as if you never adjusted it. P1 and P2 LOCK at your first probe_inject (they are forecasts from span information). P3 stays open until the episode ends.

SCORING
Each contract is scored by CRPS against truth, normalized against scripted reference baselines (persistence/climatology-grade): beat the references toward 0 CRPS for accuracy 1, match them for 0. Your "sigma" is your predictive sd — honest uncertainty strictly beats overconfidence. Unsubmitted contracts score 0.

STRATEGY
You have a full coding environment: record every read, build models offline. Suggested science: (1) learn the device's internal structure from stream correlations (which slots respond alike?); (2) calibrate the actuator channels one at a time and in combination, watching how the stream correlation structure responds; (3) characterize the medium — is it made of localized objects? what changes? what are the timescales per port?; (4) after the span: control replica first, then small-amp emissions on the announced port; find which device and ports respond, at what delay; fit how the response grows with amp and extrapolate to the announced amp. Watch the clock: the span is {t0} tu and only moves forward. Submit P1/P2 BEFORE your first inject. Always submit all three contracts — calibrated baselines with honest sigma are worth real points."""

BLOB_PROMPT = (
    "Begin your investigation using the probe_* tools. Start with "
    "probe_status. Explore the span, submit P1 and P2 before your first "
    "probe_inject, run replica experiments, then submit P3. Submit every "
    "contract before finishing.")


class BlobData(vf.TaskData):
    difficulty: str = "BLOB-E1r2"
    world: str = ""
    world_seed: int = 0
    max_turns: int = 80
    tier: str = "tools"                # BLOB is tools-tier only (PhysimEnv
    #                                    branches on data.tier)


class BlobTaskConfig(vf.TaskConfig):
    tools: vf.ToolsetConfig = vf.ToolsetConfig()


from physim.blobstate import BlobToolState  # noqa: E402  (state for BlobTask)


class BlobTask(vf.Task[BlobData, BlobToolState, BlobTaskConfig]):
    @classmethod
    def toolsets(cls, config: "BlobTaskConfig") -> list[vf.Toolset]:
        from physim.servers.blob import BlobToolset
        return [BlobToolset(config.tools)]

    async def setup(self, trace: vf.Trace, runtime) -> None:
        st = trace.state
        st.world = self.data.world
        st.seed = self.data.world_seed

    async def finalize(self, trace: vf.Trace, runtime) -> None:
        try:
            from verifiers.v1.utils.artifacts import collect
            trace.state.artifacts = await collect(runtime, self.data.artifacts)
        except Exception as e:  # collection must never fail the rollout
            trace.info.setdefault("physim_artifact_error", str(e))

    @vf.reward(weight=1.0)
    async def accuracy(self, trace: vf.Trace) -> float:
        from physim import blobcore as B
        st = trace.state
        world, seed = self.data.world, self.data.world_seed
        result = B.score_episode(world, seed, st.sub_p1 or "",
                                 st.sub_p2 or "", st.sub_p3 or "")
        for c, v in result["accs"].items():
            trace.record_metric(f"acc_{c}", float(v))
        for key in B.BUDGETS:
            spent = (st.spent or {}).get(key, 0.0)
            trace.record_metric(f"spend_{key}_frac",
                                float(spent / B.BUDGETS[key]))
        trace.record_metric("n_replicas", float(st.n_replicas))
        trace.record_metric("turns_used", float(st.turns))
        trace.record_metric("span_frac",
                            float(st.i_ctrl / B.N_STEPS_MAIN))
        trace.info["physim"] = {
            "difficulty": self.data.difficulty,
            "world": world,
            "world_seed": seed,
            "tier": "blob",
            "detail": result["detail"],
            "replica_log": list(st.replica_log or []),
            "workspace": _extract_workspace(getattr(st, "artifacts", None)),
        }
        return float(result["reward_accuracy"])


def _blob_task(config: "PhysimConfig", i: int) -> "BlobTask":
    from physim import blobcore as B
    ep = B.episode_cfg(config.difficulty, config.seed0 + i)
    world, seed = ep["world"], ep["seed"]
    cc = B.contracts(world, seed)["private"]
    system_prompt = BLOB_SYSTEM_PROMPT.format(
        k0=cc["kA"], k1=cc["kB"], n_ports=cc["nf"],
        t0=int(B.T0), max_replicas=B.MAX_REPLICAS,
        b_sensor=B.BUDGETS["sensor"], b_adjust=B.BUDGETS["adjust"],
        b_injection=B.BUDGETS["injection"],
        w1=B.W_P1, w2=B.W_P2, w3=B.W_P3,
        p1_h="/".join(str(int(h)) for h in B.P1_HORIZONS),
        n_h=len(B.P1_HORIZONS),
        p2_win=B.P2_WIN, p2_n=len(B.truth_p2(world, seed)),
        ann_amp=B.ANN_AMP, ann_dur=B.ANN_DUR, n_lags=len(B.P3_LAGS))
    artifacts = [vf.Artifact(
        source=".",
        exclude=["*.pyc", "__pycache__", ".git", "node_modules",
                 ".venv", "*.tar", "*.npz"],
        required=False,
    )]
    data = BlobData(
        idx=i,
        name=f"physim-{config.difficulty}#{seed}",
        prompt=BLOB_PROMPT,
        system_prompt=system_prompt,
        difficulty=config.difficulty,
        world=world,
        world_seed=seed,
        max_turns=config.max_turns,
        artifacts=artifacts,
    )
    return BlobTask(data, BlobTaskConfig(judges=list(config.task.judges),
                                         tools=config.task.tools))


def certified_seed(difficulty: str, seed0: int, index: int) -> int:
    """Deterministically map task index -> the (index+1)-th certified seed at
    or after seed0. Cheap for tanh worlds (always certified); GS worlds run a
    short health probe per candidate."""
    from physim.engine import make_world
    found = -1
    seed = seed0
    for _ in range(200):                     # hard cap on search
        if make_world(difficulty, seed).certify():
            found += 1
            if found == index:
                return seed
        seed += 1
    return seed0 + index                     # fallback: uncertified


class PhysimTaskset(vf.Taskset[PhysimTask, PhysimConfig]):
    INFINITE = True

    def load(self) -> Iterator[PhysimTask]:
        if self.config.difficulty.startswith("BLOB"):
            for i in itertools.count():
                yield _blob_task(self.config, i)
            return
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
            artifacts = []
            if tools_tier:
                artifacts = [vf.Artifact(
                    source=".",
                    exclude=["*.pyc", "__pycache__", ".git", "node_modules",
                             ".venv", "*.tar", "*.npz"],
                    required=False,
                )]
            data = PhysimData(
                idx=i,
                name=f"physim-{self.config.difficulty}#{self.config.seed0 + i}",
                prompt=prompt,
                system_prompt=system_prompt,
                difficulty=self.config.difficulty,
                world_seed=certified_seed(self.config.difficulty,
                                          self.config.seed0, i),
                max_turns=self.config.max_turns,
                n_per_stratum=self.config.n_per_stratum,
                n_prep=self.config.n_prep,
                calibration_weight=self.config.calibration_weight,
                tier="tools" if tools_tier else "chat",
                artifacts=artifacts,
            )
            task_config = self.config.task.model_copy(
                update={"tier": self.config.tier})
            yield PhysimTask(data, task_config)
