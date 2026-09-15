"""No-inference regression for the BLOB2v2r2 native verifier lifecycle.

Run from the repo root:
  .venv/bin/python -B environments/physim/tools/test_blob_round5_resources_native.py

Only a loopback interception server runs. No provider client, model, tool-server
process, sandbox, simulation, truth cache, or artifact filesystem is used.
The native state codec, HTTP routes, stop dispatch, Rollout.close, error record,
and retry predicates remain real. Task construction and artifacts use fixtures.
"""
from __future__ import annotations

import asyncio
from contextlib import ExitStack
import io
import json
from pathlib import Path
import sys
import tarfile
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import httpx
from pydantic import TypeAdapter

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "environments" / "physim"))

import verifiers.v1 as vf
from verifiers.v1.interception.server import InterceptionServer
from verifiers.v1.rollout import Rollout, RolloutTimeouts
from verifiers.v1.session import RolloutLimits
from verifiers.v1.utils.retries import episode_should_retry, trace_should_retry

from physim import blobcore as B
from physim import blobround5 as R5
from physim.blobstate import BlobToolState, ResourceSafetyError
from physim.servers import blob as S
from physim.taskset import PhysimConfig, PhysimEnv, PhysimEnvConfig, _blob5_task


STOP = {"reason": "native_gate", "meter": "sim_tu", "limit": 10.0,
        "current": 9.0, "requested": 2.0}
NOTE = "native resource gate: artifact survives an unscored safety stop\n"
TINY_LOG_CAP = 3  # one inject adds two entries; the second must stop before growth


def _forbidden(*args, **kwargs):
    raise AssertionError("native resource gate attempted real runtime/science work")


class _NoProvider:
    def __init__(self):
        self.calls = 0

    async def get_response(self, *args, **kwargs):
        self.calls += 1
        raise AssertionError("native resource gate attempted inference")

    relay = get_response
    relay_aux = get_response


class _Runtime:
    """Borrowed, inert runtime: even accidental artifact commands fail closed."""
    name = "native-resource-gate"
    stopped = False
    config = SimpleNamespace(type="subprocess", workdir="/native-resource-gate")

    async def run(self, *args, **kwargs):
        _forbidden()

    start = run
    read = run
    write = run
    stop = run


class _Harness:
    def __init__(self):
        self.score = AsyncMock(side_effect=_forbidden)
        self.cleanup = AsyncMock()


class _LatchTool(vf.Toolset[vf.ToolsetConfig, BlobToolState]):
    """Exercise the same native wrapper used by registered BLOB tools."""
    async def latch_then_raise(self):
        self.state.r5_resource_stop = dict(STOP)
        raise ResourceSafetyError("synthetic tool failure: state must not commit")


def _artifacts():
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as archive:
        content = NOTE.encode()
        member = tarfile.TarInfo("workspace/native_resource_gate.txt")
        member.size = len(content)
        archive.addfile(member, io.BytesIO(content))
    return {"/native-resource-gate": buf.getvalue()}


def _task():
    # The task prompt needs only these counts. No base cache or truth is opened.
    with patch.object(B, "contracts", return_value={
        "private": {"kA": 4, "kB": 4, "nf": 3}
    }), patch.object(R5, "syllabus5", return_value="synthetic native gate syllabus"):
        return _blob5_task(PhysimConfig(
            id="physim", difficulty="BLOB2v2r2-E1", tier="tools"), 0)


async def _rollout():
    task = _task()
    runtime, harness = _Runtime(), _Harness()
    ctx = vf.ModelContext(
        model="native-resource-gate-no-inference",
        client=vf.EvalClientConfig(
            base_url="http://127.0.0.1:1",
            api_key_var="NATIVE_RESOURCE_GATE_UNUSED_KEY",
        ),
    )
    rollout = Rollout(
        task=task, agent_config=vf.AgentConfig(), harness=harness, ctx=ctx,
        runtime_config=vf.SubprocessConfig(), runtime=runtime,
        timeouts=RolloutTimeouts(finalize=2.0, scoring=2.0),
        limits=RolloutLimits(),
    )
    # Deliberately skip open(): it provisions resources. Only task setup and the
    # native stop/close stages are under test, with an inert borrowed runtime.
    rollout._opened = True
    await task.setup(rollout.trace, runtime)
    assert rollout.trace.state.r5_resource_policy == "v2r2"
    assert not rollout.trace.state.r5_resource_stop
    return rollout


async def _state_and_stop(rollout, *, request_model=True):
    trace, session = rollout.trace, rollout._session
    # This is an initialized logical fork only: there is no resident simulator.
    fid = "native-log-fork"
    st = trace.state
    st.r5_nonce = trace.id
    st.r5_fork_seq = 1
    st.r5_forks = {fid: {
        "src": ["base", 0], "salt_idx": 1, "steps": 0, "open": True,
        "anchor_abs": 0.0, "poses": [[0.0, 0.0, 1.0], [1.0, 1.0, 1.0]],
        "poses0": [[0.0, 0.0, 1.0], [1.0, 1.0, 1.0]],
        "log": [], "emissions": [],
    }}
    provider = _NoProvider()
    server = InterceptionServer(requires_tunnel=False)
    with patch.object(server, "_client", return_value=provider):
        async with server:
            async with server.acquire(session) as (base, model_secret, state_secret):
                async with httpx.AsyncClient(timeout=2.0, trust_env=False) as http:
                    tool = _LatchTool(vf.ToolsetConfig())
                    tool._state_client = http
                    with patch.object(tool, "_state_channel", return_value=(
                        base + "/state", state_secret, None
                    )):
                        # A server-side exception is NOT a terminal host error:
                        # _with_state only PUTs after a normal tool return.
                        try:
                            await tool._with_state(tool.latch_then_raise)()
                        except ResourceSafetyError:
                            pass
                        else:
                            raise AssertionError("synthetic tool exception was swallowed")
                        assert not trace.state.r5_resource_stop
                        assert not trace.errors
                        assert session.error is None

                    # Exercise the REAL BLOB tool, with only secrets/counts
                    # supplied as fixtures. Even a zero-amp emission whose
                    # positive duration rounds to zero substeps must retain its
                    # two entries, and must trip the aggregate log guard.
                    blob = rollout.task.toolsets(rollout.task.config)[0]
                    assert isinstance(blob, S.BlobToolset)
                    blob._state_client = http
                    dur = R5.SIM_DT / 10.0
                    assert int(round(dur / R5.SIM_DT)) == 0
                    with patch.object(blob, "_state_channel", return_value=(
                        base + "/state", state_secret, None
                    )), patch.object(B, "n_ports", return_value=3), patch.object(
                        B, "get_secrets", return_value={
                            "devices": [{"center": [0.0, 0.0]},
                                        {"center": [1.0, 1.0]}],
                            "port_perm": [0, 1, 2],
                        }
                    ):
                        call = blob._with_state(blob.inject5)
                        accepted = json.loads(await call(ctx=fid, port=0, amp=0.0, dur=dur))
                        assert accepted.get("ok") is True, accepted
                        kept_fork = trace.state.r5_forks[fid]
                        assert kept_fork["emissions"] == [[0, 0.0, 0, 0]]
                        assert kept_fork["log"] == [["inj", 0, 0.0, dur]]
                        retained = json.loads(json.dumps(kept_fork))
                        assert not trace.state.r5_resource_stop

                        refused = json.loads(await call(ctx=fid, port=0, amp=0.0, dur=dur))
                        assert refused == {"error": R5.RESOURCE_STOP_MSG5, "terminal": True}
                        stopped = dict(trace.state.r5_resource_stop)
                        assert stopped["meter"] == "log_entries", stopped
                        assert stopped["current"] == 2, stopped
                        assert stopped["requested"] == 2, stopped
                        assert stopped["limit"] == TINY_LOG_CAP, stopped
                        assert trace.state.r5_forks[fid] == retained, "cap did not preflight"
                        assert trace.state.r5_cap_hits["log_entries"] == 1
                        assert trace.state.r5_meters["injection"] == 0
                        assert trace.state.r5_meters["sim_tu"] == 0
                        assert trace.state.r5_phase != "revealed"
                        assert not trace.state.r5_subs

                        # The latch prevents further growth, not an ordinary
                        # recoverable refusal that the model can work around.
                        again = json.loads(await call(ctx=fid, port=0, amp=0.0, dur=dur))
                        assert again == refused
                        assert trace.state.r5_resource_stop == stopped
                        assert trace.state.r5_forks[fid] == retained
                        assert trace.state.r5_cap_hits["log_entries"] == 1
                    assert trace.stop_condition is None, "PUT itself must not stop a trace"

                    # A native @stop must refuse both dialect paths before any
                    # provider call. These are LOCAL HTTP requests, not inference.
                    statuses = []
                    for stream in ((False, True) if request_model else ()):
                        response = await http.post(
                            base + "/v1/chat/completions",
                            headers={"Authorization": "Bearer " + model_secret},
                            json={"model": "native-resource-gate-no-inference",
                                  "messages": [{"role": "user", "content": "gate"}],
                                  "stream": stream},
                        )
                        statuses.append(response.status_code)
                        assert response.status_code == 400, response.text
                        assert "resource_safety_stop" in response.text, response.text
                    assert provider.calls == 0
                    if request_model:
                        assert trace.stop_condition == "resource_safety_stop"
                        assert trace.is_completed
                    else:
                        assert trace.stop_condition is None and not trace.is_completed
                    assert session.error is None, "returning True is a clean native stop"
                    assert not trace.nodes and not trace.calls
    return statuses, {"tool": "BlobToolset.inject5", "amp": 0.0, "dur": dur,
                      "simulation_substeps": 0, "retained_log_entries": 1,
                      "retained_emission_entries": 1, "resource_stop": stopped}


def _assert_unscored(trace, expected_stop):
    assert trace.is_completed and not trace.ok
    assert trace.last_error is not None
    assert trace.last_error.type == "ResourceSafetyError", trace.errors
    assert not any(value is not None for value in trace.rewards.values()), trace.rewards
    info = trace.info.get("physim", {})
    assert info.get("resource_truncated") is True, info
    assert info.get("score_status") == "not_scored_resource_limit", info
    assert info.get("resource_stop") == expected_stop, info
    assert info.get("resource_policy") == R5.resource_metadata5("v2r2"), info
    assert "log_entries" in info["resource_policy"]["caps"], info
    # Trace.state is intentionally absent from the native wire record. The task
    # must copy the terminal record and collected workspace into trace.info.
    assert "state" not in trace.model_dump()
    wire_bytes = TypeAdapter(type(vf.Episode.of(trace))).dump_json(
        vf.Episode.of(trace), exclude_none=True)
    wire = vf.WireEpisode.model_validate_json(wire_bytes)
    saved = wire.traces[0]
    assert not wire.ok and not saved.ok
    assert saved.last_error.type == "ResourceSafetyError"
    assert not any(value is not None for value in saved.rewards.values())
    assert saved.info["physim"]["resource_stop"] == expected_stop, saved.info
    assert NOTE.strip() in json.dumps(saved.info), "collected workspace was lost"
    return wire


async def _close_unscored(rollout, artifacts, expected_stop):
    collector = AsyncMock(return_value=artifacts)
    task_score = AsyncMock(wraps=rollout.task.score)
    with patch("verifiers.v1.utils.artifacts.collect", collector), \
         patch("verifiers.v1.collect", collector), \
         patch.object(rollout.task, "score", task_score):
        result = await rollout.close()
        assert await rollout.close() is result  # close is idempotent
    collector.assert_awaited_once()
    task_score.assert_not_awaited()
    rollout.harness.score.assert_not_awaited()
    rollout.harness.cleanup.assert_awaited_once()
    assert result.state.artifacts == artifacts
    wire = _assert_unscored(result, expected_stop)
    return result, wire


def _config(difficulty="BLOB2v2r2-E1", exclusions=()):
    return PhysimEnvConfig.model_validate({
        "taskset": {"id": "physim", "difficulty": difficulty, "tier": "tools"},
        "retries": {"max_retries": 3, "exclude": list(exclusions)},
        "scientist": {"retries": {"max_retries": 3, "exclude": list(exclusions)}},
    })


async def _enforced_retry_and_resume(task, wire, ctx):
    # Even an explicit positive retry count and empty exclusions must normalize
    # to the r2 cohort policy. Per-call SDK retries are outside these two knobs.
    cfg = _config()
    for retry in (cfg.retries, cfg.scientist.retries):
        assert retry.max_retries == 0
        assert retry.exclude == ["ResourceSafetyError"]
    copied = PhysimEnvConfig.model_validate_json(cfg.model_dump_json())
    for retry in (copied.retries, copied.scientist.retries):
        assert retry.max_retries == 0
        assert retry.exclude == ["ResourceSafetyError"]
    kept = _config(exclusions=("SandboxError",))
    for retry in (kept.retries, kept.scientist.retries):
        assert retry.max_retries == 0
        assert retry.exclude == ["SandboxError", "ResourceSafetyError"]
    legacy = _config(difficulty="BLOB2v2-E1")
    for retry in (legacy.retries, legacy.scientist.retries):
        assert retry.max_retries == 3
        assert retry.exclude == []

    # Exact-name exclusion alone is not a terminal override. Native predicates
    # inspect ALL errors, including a recovered provider attempt prepended to a
    # final safety-stop trace. This is why the cohort enforces both retry counts.
    with_history = wire.model_copy(deep=True)
    with_history.traces[0].errors.insert(0, vf.Error(
        type="ProviderError", message="recovered earlier provider attempt"))
    exclude_only = vf.RetryConfig(max_retries=3, exclude=["ResourceSafetyError"])
    assert trace_should_retry(with_history.traces[0], exclude_only)
    assert episode_should_retry(with_history, exclude_only)

    # Exercise the real native retry loops, but inject completed synthetic
    # attempts. __new__ intentionally skips harness/taskset construction.
    attempts = {}
    for label, episode in (("terminal_only", wire),
                           ("prior_provider_then_terminal", with_history)):
        agent = vf.Agent.__new__(vf.Agent)
        agent.config, agent._closed = cfg.scientist, False
        agent._run_once = AsyncMock(return_value=episode.traces[0])
        env = PhysimEnv.__new__(PhysimEnv)
        env.config = cfg
        env.run_episode = AsyncMock(return_value=episode)
        slot = env.slots(task)[0]
        with patch("verifiers.v1.utils.retries.asyncio.sleep", new=AsyncMock(
            side_effect=AssertionError("resource safety error entered retry backoff")
        )), patch("verifiers.v1.env.trim_memory_periodically", new=AsyncMock()):
            assert await agent.run(task) is episode.traces[0]
            assert await env.run_slot(slot, ctx) is episode
        agent._run_once.assert_awaited_once()
        env.run_episode.assert_awaited_once()
        assert slot.done and slot.episode is episode
        attempts[label] = {"agent": agent._run_once.await_count,
                           "episode": env.run_episode.await_count}
    assert [error.type for error in with_history.traces[0].errors] == [
        "ProviderError", "ResourceSafetyError"], "do not discard error history"

    # --resume is a distinct decision from retry. Test the exact env predicate
    # consumed by the native in-process resume loader, with a wire-decoded row.
    assert env.complete(wire)
    assert env.complete(with_history)
    assert not wire.ok and not wire.traces[0].ok, "resume must not forge success"
    successful = wire.model_copy(deep=True)
    successful.ok = True
    assert env.complete(successful)
    outer_error = wire.model_copy(deep=True)
    outer_error.errors.append(vf.Error(type="EnvError", message="unrelated failure"))
    assert not env.complete(outer_error)
    other_error = wire.model_copy(deep=True)
    other_error.traces[0].errors = [vf.Error(type="ProviderError", message="failed")]
    assert not env.complete(other_error)
    old_tag = wire.model_copy(deep=True)
    old_tag.traces[0].task.data = old_tag.traces[0].task.data.model_copy(
        update={"difficulty": "BLOB2v2-E1"})
    assert not env.complete(old_tag)
    no_marker = wire.model_copy(deep=True)
    no_marker.traces[0].info["physim"]["resource_truncated"] = False
    assert not env.complete(no_marker)
    wrong_policy = wire.model_copy(deep=True)
    wrong_policy.traces[0].info["physim"]["resource_policy"]["id"] = "v2"
    assert not env.complete(wrong_policy)
    multiple = wire.model_copy(deep=True)
    multiple.traces.append(multiple.traces[0].model_copy(deep=True))
    assert not env.complete(multiple)
    return attempts


async def run_gate():
    """Run the native lifecycle gate; safe to await from the main resource suite."""
    assert issubclass(ResourceSafetyError, vf.TaskError)
    artifacts = _artifacts()
    assert R5.CAPS5_R2["log_entries"] == 1_000_000
    with ExitStack() as guards:
        guards.enter_context(patch.dict(R5.CAPS5_R2, {"log_entries": TINY_LOG_CAP}))
        bombs = []
        for owner, name in ((B, "get_cached"), (R5, "score_episode5"),
                            (R5, "load_truth"), (R5, "build_anchors"),
                            (R5, "run_member_chunk"), (R5, "assemble_truth"),
                            (S, "_template5"), (S.Blob5Mixin, "_advance_sim"),
                            (B.agdev, "step_chunk")):
            bombs.append(guards.enter_context(patch.object(
                owner, name, side_effect=_forbidden)))

        rollout = await _rollout()
        statuses, log_proof = await _state_and_stop(rollout)
        trace, wire = await _close_unscored(
            rollout, artifacts, log_proof["resource_stop"])
        assert trace.stop_condition == "resource_safety_stop"
        retry_attempts = await _enforced_retry_and_resume(
            rollout.task, wire, rollout.ctx)

        # Also cover a final tool with no following model request. finalize must
        # independently detect the latch; relying on @stop alone would score -1.
        last_tool = await _rollout()
        no_requests, final_log_proof = await _state_and_stop(
            last_tool, request_model=False)
        assert no_requests == []
        no_next_model, _ = await _close_unscored(
            last_tool, artifacts, final_log_proof["resource_stop"])

        # Replay/offline task.score must guard before loading or building truth.
        offline = await _rollout()
        offline.trace.state.r5_resource_stop = dict(log_proof["resource_stop"])
        try:
            await offline.task.score(offline.trace)
        except ResourceSafetyError:
            pass
        else:
            raise AssertionError("offline score did not reject a resource-stopped trace")
        assert not any(value is not None for value in offline.trace.rewards.values())
        for bomb in bombs:
            bomb.assert_not_called()

    # There is no intrinsic retryable flag. Both native levels match the exact
    # serialized class name; exclude beats include, not an inherited class name.
    retry_any = vf.RetryConfig(max_retries=1)
    exclude = vf.RetryConfig(max_retries=1, include=["ResourceSafetyError"],
                             exclude=["ResourceSafetyError"])
    base_only = vf.RetryConfig(max_retries=1, exclude=["TaskError"])
    for predicate, value in ((trace_should_retry, wire.traces[0]),
                             (episode_should_retry, wire)):
        assert predicate(value, retry_any)
        assert not predicate(value, exclude)
        assert predicate(value, base_only), "retry matching unexpectedly uses inheritance"

    return {
        "gate": "BLOB2v2r2 native resource lifecycle", "pass": True,
        "http_stop_statuses": statuses, "provider_calls": 0,
        "real_inject_log_guard": log_proof,
        "synthetic_log_entries_cap": TINY_LOG_CAP,
        "simulation_or_truth_calls": 0, "resource_error": trace.last_error.type,
        "science_reward_recorded": False,
        "next_model_stop_condition": trace.stop_condition,
        "final_tool_stop_condition": no_next_model.stop_condition,
        "artifact_and_error_wire_roundtrip": True,
        "retry_exclusions_checked": ["agent", "episode"],
        "requested_whole_retry_count": 3,
        "enforced_whole_retry_count": 0,
        "native_retry_loop_attempts": retry_attempts,
        "prior_provider_error_history_preserved": True,
        "in_process_resume_terminal": True,
        "native_is_truncated": trace.is_truncated,
    }


if __name__ == "__main__":
    print(json.dumps(asyncio.run(run_gate()), indent=2))
