"""BLOB2v2r2 resource-policy gates. No inference or truth construction.

Run from the repo root with the project interpreter:
  .venv/bin/python environments/physim/tools/test_blob_round5_resources.py
  ... --gates config synthetic --json-out /tmp/r2-fast.json
  ... --gates physics --json-out /tmp/r2-physics.json

High-count tests use small synthetic fields but the REAL fork registry,
operation log, salted RNG, apparatus checks, policy gates, and tool methods.
The physics gate uses the existing E1 cache and the actual step_chunk engine.
The native gate uses real loopback state/interception and native close/retry.
"""
from __future__ import annotations

import argparse
import asyncio
from contextlib import contextmanager, ExitStack
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
from pydantic import ValidationError

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "environments" / "physim"))

from physim import blobcore as B
from physim import blobround5 as R5
from physim.blobstate import BlobToolState
from physim.servers import blob as S
from physim.taskset import Blob5TaskConfig, PhysimConfig, _blob5_task

WORLD, SEED, MENU = "p4g2_044", 928, "E1"
EXPECTED_LEGACY = dict(sensor=1_000_000.0, adjust=30_000.0,
                       injection=3_000.0, fork_spawns=400,
                       open_forks=8, sim_tu=100_000.0)
EXPECTED_R2 = dict(sensor=1_000_000_000.0, adjust=10_000_000.0,
                  injection=1_000_000.0, fork_spawns=100_000,
                  open_forks=10_000, sim_tu=10_000_000.0,
                  log_entries=1_000_000)


def make_ts(policy="v2r2", nonce="resource-gate", world=WORLD,
            seed=SEED, menu=MENU):
    ts = S.BlobToolset(S.BlobToolsetConfig(
        r5_mode=True, r5_resource_policy=policy))
    ts._inert_state = BlobToolState(world=world, seed=seed, round5=menu,
                                   r5_nonce=nonce)
    return ts


def no_cap_hits(ts):
    assert not any(ts.state.r5_cap_hits.values()), ts.state.r5_cap_hits
    assert not ts.state.r5_resource_stop, ts.state.r5_resource_stop


def resident_bound(ts):
    assert len(S._LIVE5) <= R5.RESIDENT_FORKS5, len(S._LIVE5)
    assert ts.state.r5_resident_peak <= R5.RESIDENT_FORKS5


def private_free(text):
    low = text.lower()
    for key in ("resource_policy", "r5_", "cap_hits", "resident_", "meter_",
                '"caps"', '"budget"', "be efficient"):
        assert key not in low, (key, text)
    for pattern in (r"\bbudget", r"\bcost", r"\bpric", r"\bspend",
                    r"\bspent\b", r"\bremaining\b", r"\bafford"):
        assert not re.search(pattern, low), (pattern, text)
    for number in ("1000000000", "10000000", "100000", "1000000"):
        assert number not in text, (number, text)


class _ToyCached:
    meta = {"L": 16.0, "dx": 0.5}

    def fields_at(self, index):
        return np.full((2, 4, 4), index * 0.001, np.float32)


class _ToyDevice:
    def __init__(self, index, center=None, dilation=1.0):
        self.k = (13, 19)[index]
        self.center = center if center is not None else (index + 1., 2.)
        self.dilation = dilation

    def sample(self, fields, dx):
        offset = float(sum(self.center)) * 0.01
        value = fields.mean(axis=(1, 2)) + offset
        return value[:, None] + np.arange(self.k)[None, :] * self.dilation * 0.001


def _toy_step(state, n, injections=()):
    # Same calls/cuts/order on warm and cold paths; consume real salted RNG.
    noise = state["rng"].standard_normal((n, *state["F"].shape), dtype=np.float32)
    state["F"] = state["F"] + noise.sum(axis=0) * np.float32(1e-4)
    for inj in injections:
        state["F"][inj["field"]] += np.float32(inj["amp"] * n * 1e-5)
    state["t_step"] += n


@contextmanager
def synthetic_world():
    cached = _ToyCached()
    secrets = dict(port_perm=[1, 0], devices=[dict(center=[1., 2.]),
                                            dict(center=[3., 4.])])
    template = dict(F=cached.fields_at(0), t_step=0)
    private = dict(nf=2, kA=13, kB=19, p2_port=0, p2_sign=1,
                   p2_thr=0.1)

    def make_device(world, seed, index, center=None, dilation=1.0):
        return _ToyDevice(index, center, dilation)

    def sample_at(world, seed, index, device):
        return device.sample(cached.fields_at(index), 0.5)

    def stats(world, seed, index):
        f = cached.fields_at(index)
        return np.stack([f.mean(axis=(1, 2)), f.var(axis=(1, 2))], axis=1)

    with ExitStack() as stack:
        for name, value in (("get_cached", lambda *a: cached),
                            ("get_secrets", lambda *a: secrets),
                            ("n_ports", lambda *a: 2),
                            ("make_device", make_device),
                            ("sample_at", sample_at),
                            ("global_stats", stats),
                            ("contracts", lambda *a: {"private": private})):
            stack.enter_context(patch.object(B, name, value))
        stack.enter_context(patch.object(S, "_template5", lambda *a: template))
        stack.enter_context(patch.object(B.agdev, "step_chunk", _toy_step))
        # Cached category facts must not leak between fixture/real gates.
        R5.syllabus5.cache_clear()
        R5.instances5.cache_clear()
        S._LIVE5.clear()
        try:
            yield
        finally:
            S._LIVE5.clear()
            R5.syllabus5.cache_clear()
            R5.instances5.cache_clear()


async def config_gate():
    assert R5.CAPS5 == EXPECTED_LEGACY
    assert R5.CAPS5_R2 == EXPECTED_R2
    assert R5.RESIDENT_FORKS5 == 8
    assert "r5_resource_policy" in S.BlobToolsetConfig.model_fields
    assert "r5_mode" in S.BlobToolsetConfig.model_fields
    rows = []
    with synthetic_world():
        for menu in ("E1", "E2"):
            old = _blob5_task(PhysimConfig(id="physim", tier="tools",
                                          difficulty=f"BLOB2v2-{menu}"), 0)
            new = _blob5_task(PhysimConfig(id="physim", tier="tools",
                                          difficulty=f"BLOB2v2r2-{menu}"), 0)
            assert old.data.world == new.data.world
            assert old.data.world_seed == new.data.world_seed
            assert old.data.menu == new.data.menu
            assert old.data.prompt == new.data.prompt
            assert old.data.system_prompt == new.data.system_prompt.replace(
                "BLOB2v2r2-", "BLOB2v2-")
            for i in range(6):
                assert R5.episode_cfg5(f"BLOB2v2-{menu}", i) == \
                    R5.episode_cfg5(f"BLOB2v2r2-{menu}", i)
            for task, expected in ((old, "v2"), (new, "v2r2")):
                restored = Blob5TaskConfig.model_validate_json(
                    task.config.model_dump_json())
                toolset = task.toolsets(restored)[0]
                wire = toolset.config.model_dump_json()
                encoded = json.loads(wire)
                assert encoded["r5_mode"] is True
                assert encoded["r5_resource_policy"] == expected
                captured = []

                def fake_serve(server):
                    # Native ServerBase.run has parsed VF_CONFIG. Neither
                    # setup_task nor host state exists yet: registration
                    # must already choose the correct surface and policy.
                    assert server.state.world == ""
                    assert server.config.r5_resource_policy == expected
                    tools = {}
                    mcp = SimpleNamespace(add_tool=lambda fn, name, **kw:
                                          tools.__setitem__(name, fn))
                    server.register(mcp)
                    assert set(tools) == set(S.V2_TOOL_NAMES), set(tools)
                    captured.append(server)

                with patch.dict(os.environ, {"VF_CONFIG": wire}), \
                        patch.object(S.BlobToolset, "_serve", fake_serve):
                    S.BlobToolset.run()  # actual native config entry point
                assert len(captured) == 1
                ts = captured[0]
                ts._inert_state = BlobToolState(world=task.data.world,
                    seed=task.data.world_seed, round5=menu, r5_nonce="config-gate")
                status = await ts.status5()
                assert json.loads(status)["syllabus"].startswith(
                    f"SYLLABUS — {task.data.difficulty}")
                private_free(status)
                private_free(task.data.system_prompt)
                rows.append(dict(cohort=task.data.difficulty, policy=expected,
                                 vf_config=json.loads(wire)))
        try:
            S.BlobToolsetConfig(r5_mode=True, r5_resource_policy="unknown")
        except ValidationError:
            pass
        else:
            raise AssertionError("unknown serialized policy was accepted")
        # A wire/config mismatch must fail closed, not silently select v1.
        ts = make_ts()
        ts.state.r5_resource_policy = "v2"
        try:
            await ts.status5()
        except ValueError as exc:
            assert "policy/state mismatch" in str(exc)
        else:
            raise AssertionError("policy mismatch accepted")
    return dict(pass_=True, cohorts=rows, native_vf_config_entrypoint=True,
                contracts_identical_except_label=True,
                legacy_caps=EXPECTED_LEGACY, new_caps=EXPECTED_R2)


async def handle_gate():
    nonce = "resource-collision-audit"
    first, second = 5_931, 67_233
    short = [hashlib.sha256(f"{nonce}|{i}".encode()).hexdigest()[:8]
             for i in (first, second)]
    assert short[0] == short[1] == "39ff6e0a"  # genuine 32-bit collision
    with synthetic_world():
        ts = make_ts(nonce=nonce)
        ts._ensure5()
        ts.state.r5_fork_seq = first - 1
        a = json.loads(await ts.fork5(t=0))["fork"]
        saved = copy.deepcopy(ts.state.r5_forks[a])
        ts.state.r5_fork_seq = second - 1
        b = json.loads(await ts.fork5(t=50))["fork"]
        assert len(a) == len(b) == 33 and a != b
        assert a[:9] == b[:9] == "f39ff6e0a"
        assert ts.state.r5_forks[a] == saved
        assert len(ts._open_forks()) == 2
        no_cap_hits(ts)
        old = make_ts(policy="v2", nonce="legacy-id")
        legacy_id = json.loads(await old.fork5(t=0))["fork"]
        assert len(legacy_id) == 9
        assert legacy_id == "f" + hashlib.sha256(b"legacy-id|1").hexdigest()[:8]
    return dict(pass_=True, r2_handle_bits=128, legacy_handle_bits=32,
                known_legacy_hash_collision_counters=[first, second],
                occupied_record_preserved=True)


async def count_gate():
    with synthetic_world():
        ts = make_ts(nonce="high-count")
        for i in range(512):
            out = json.loads(await ts.fork5(t=(i % 501) * 5))
            assert "fork" in out, (i, out)
            reset = json.loads(await ts.reset5(fork=out["fork"]))
            assert reset["ok"]
            resident_bound(ts)
        assert ts.state.r5_fork_seq == ts.state.r5_n_resets == 512
        no_cap_hits(ts)
        ids = []
        for i in range(64):
            out = json.loads(await ts.fork5(t=i * 5))
            assert "fork" in out, (i, out)
            ids.append(out["fork"])
            assert len(ts._open_forks()) == i + 1
            resident_bound(ts)
        assert (ts.state.r5_nonce, ids[0]) not in S._LIVE5
        assert ts.state.r5_open_peak == 64
        resident_bytes_peak = sum(e["S"]["F"].nbytes for e in S._LIVE5.values())
        # All 64 handles remain readable despite only 8 resident states.
        for fid in ids:
            out = json.loads(await ts.read5(ctx=fid, window=0))
            assert out["ctx"] == fid and "error" not in out
            resident_bound(ts)
        # Exceed the actual completed Fable demand with nontrivial toy
        # forward integration and real sensor metering, no fixtures on caps.
        for _ in range(17):
            out = json.loads(await ts.read5(ctx=ids[0], window=200, ports=[0]))
            assert len(out["steps"]) == 200
            resident_bound(ts)
        assert ts.state.r5_meters["sim_tu"] == 17_000
        assert ts.state.r5_meters["sensor"] > 536_360
        no_cap_hits(ts)
        # Safety resource totals have no per-fork deadline. A cheap sim
        # stub isolates this control-flow gate from multi-day integration.
        def fast_advance(state, fk, start, n):
            state["F"] = state["F"] + np.float32(n * 1e-5)
            state["t_step"] += n * R5.SPC
        with patch.object(ts, "_advance_sim", fast_advance):
            out = json.loads(await ts.wait5(ctx=ids[0], steps=20_001))
        assert "error" not in out
        assert ts.state.r5_forks[ids[0]]["steps"] * B.CTRL_TU > 100_000
        assert ts.state.r5_phase != "revealed"
        no_cap_hits(ts)
        return dict(pass_=True, spawn_reset_cycles=512,
                    cumulative_spawns=ts.state.r5_fork_seq,
                    logical_open=64, resident_peak=ts.state.r5_resident_peak,
                    resident_fixture_field_bytes_peak=resident_bytes_peak,
                    cache_evictions=ts.state.r5_cache_evictions,
                    meters=dict(ts.state.r5_meters),
                    cap_hits=dict(ts.state.r5_cap_hits),
                    no_per_fork_duration_ceiling=True)


async def branch_program(cold=False, evict=True, nonce="branch-parity"):
    S._LIVE5.clear()
    ts = make_ts(nonce=nonce)
    outputs = []
    resident_bytes_peak = 0

    async def call(name, **kwargs):
        nonlocal resident_bytes_peak
        if cold:
            # Exercise both a completely cold server registry AND the
            # serializable state representation used by the state channel.
            ts._inert_state = BlobToolState.model_validate_json(
                ts.state.model_dump_json())
            S._LIVE5.clear()
        out = await getattr(ts, name)(**kwargs)
        result = json.loads(out)
        assert "error" not in result, (name, result)
        outputs.append(out)
        resident_bound(ts)
        resident_bytes_peak = max(resident_bytes_peak, sum(
            e["S"]["F"].nbytes for e in S._LIVE5.values()))
        return result

    await call("status5")
    await call("adjust5", ctx="base", device=0, u1=0.2, u2=-0.1,
               u3=0.1, steps=1, read=True)
    parent = (await call("fork5", t=700))["fork"]
    await call("inject5", ctx=parent, port=0, amp=0.6, dur=7.5)
    await call("read5", ctx=parent, window=1)
    # Parent emission is still pending at spawn; child inherits fields and
    # device poses, but uses its own fresh stream and its own emissions.
    child = (await call("fork5", fork=parent))["fork"]
    assert ts.state.r5_forks[child]["emissions"] == []
    inherited = copy.deepcopy(ts.state.r5_forks[child]["poses"])
    await call("adjust5", ctx=parent, device=0, u1=0.3, u2=0.1,
               u3=-0.1, steps=1)
    assert ts.state.r5_forks[child]["poses"] == inherited
    # Alter parent after spawn; reconstruction must use historical fields.
    await call("inject5", ctx=parent, port=1, amp=0.4, dur=2.3)
    await call("wait5", ctx=parent, steps=1)
    if evict:
        for i in range(9):
            await call("fork5", t=i * 5)
        assert (ts.state.r5_nonce, parent) not in S._LIVE5
        assert (ts.state.r5_nonce, child) not in S._LIVE5
    # Branch directly from an evicted parent's CURRENT (post-child) state.
    branch = (await call("fork5", fork=parent))["fork"]
    assert ts.state.r5_forks[branch]["poses0"] == \
        ts.state.r5_forks[parent]["poses"]
    await call("reset5", fork=parent)
    await call("read5", ctx=child, window=0)  # reset parent, surviving child
    await call("inject5", ctx=child, port=1, amp=0.3, dur=6.6)
    await call("read5", ctx=child, window=1)
    await call("adjust5", ctx=child, device=1, u1=-0.2, u2=0.15,
               u3=0.05, steps=1)
    grandchild = (await call("fork5", fork=child))["fork"]
    await call("reset5", fork=child)
    await call("read5", ctx=grandchild, window=1)
    await call("read5", ctx=branch, window=1)
    await call("status5")
    snapshots = {}
    for fid in (parent, child, branch, grandchild):
        if cold:
            S._LIVE5.clear()
        state = ts._fork_sim(fid)
        snapshots[fid] = dict(
            fields=hashlib.sha256(state["F"].tobytes()).hexdigest(),
            rng=copy.deepcopy(state["rng"].bit_generator.state),
            t_step=state["t_step"])
        resident_bound(ts)
    no_cap_hits(ts)
    return dict(transcript=outputs, snapshots=snapshots,
                records=copy.deepcopy(ts.state.r5_forks),
                meters=dict(ts.state.r5_meters),
                resident_peak=ts.state.r5_resident_peak,
                resident_field_bytes_peak=resident_bytes_peak,
                evictions=ts.state.r5_cache_evictions,
                rebuilds=ts.state.r5_cache_rebuilds)


async def parity_gate(real=False):
    if real:
        warm = await branch_program(cold=False)
        cold = await branch_program(cold=True)
    else:
        with synthetic_world():
            warm = await branch_program(cold=False)
            cold = await branch_program(cold=True)
    for key in ("transcript", "snapshots", "records", "meters"):
        assert warm[key] == cold[key], ("warm/cold mismatch", key)
    for text in warm["transcript"]:
        private_free(text)
    return dict(pass_=True, physics="actual step_chunk" if real else "synthetic",
                exact_fields_rng_poses_emissions_logs=True,
                evicted_parent_branch_and_reset_ancestor=True,
                transcript_responses=len(warm["transcript"]),
                warm_resident_peak=warm["resident_peak"],
                warm_resident_field_bytes_peak=warm["resident_field_bytes_peak"],
                warm_cache_evictions=warm["evictions"],
                warm_rebuilds=warm["rebuilds"], cold_rebuilds=cold["rebuilds"],
                snapshots=warm["snapshots"], meters=warm["meters"])


async def deep_chain_gate():
    with synthetic_world():
        ts = make_ts(nonce="deep-chain")
        root_id = json.loads(await ts.fork5(t=100))["fork"]
        last = root_id
        for _ in range(1_100):
            out = json.loads(await ts.fork5(fork=last))
            assert "fork" in out, out
            last = out["fork"]
            resident_bound(ts)
        warm = ts._fork_sim(last)["F"].copy()
        # Iterative replay must work past Python's normal recursion depth.
        await ts.reset5(fork=root_id)
        S._LIVE5.clear()
        cold = ts._fork_sim(last)["F"]
        assert np.array_equal(warm, cold)
        no_cap_hits(ts)
        return dict(pass_=True, ancestry_depth=1_101,
                    logical_open=len(ts._open_forks()),
                    resident_peak=ts.state.r5_resident_peak,
                    cap_hits=dict(ts.state.r5_cap_hits))


def persisted_entries(ts):
    return sum(len(f["log"]) + len(f["emissions"])
               for f in ts.state.r5_forks.values())


async def metadata_entries_gate():
    with synthetic_world():
        cases = [(0.0, 7.5), (0.0, 0.001), (0.5, 0.001)]
        results = []
        for amp, dur in cases:
            ts = make_ts(nonce=f"metadata-{amp}-{dur}")
            fid = json.loads(await ts.fork5(t=0))["fork"]
            tiny = {**EXPECTED_R2, "log_entries": 4}
            with patch.object(R5, "CAPS5_R2", tiny):
                for _ in range(2):
                    out = json.loads(await ts.inject5(ctx=fid, port=0, amp=amp, dur=dur))
                    assert out["ok"], out
                fk = ts.state.r5_forks[fid]
                assert len(fk["log"]) == len(fk["emissions"]) == 2
                assert ts.state.r5_meters["log_entries"] == persisted_entries(ts) == 4
                assert ts.state.r5_meters["injection"] == 2 * B.inj_price(amp) * dur
                if dur == 0.001:
                    assert all(e[2] == e[3] for e in fk["emissions"])
                assert ts.state.r5_forks[fid]["steps"] == 0
                no_cap_hits(ts)
                ts._inert_state = BlobToolState.model_validate_json(ts.state.model_dump_json())
                before_forks = copy.deepcopy(ts.state.r5_forks)
                before_meters = dict(ts.state.r5_meters)
                out = json.loads(await ts.inject5(ctx=fid, port=0, amp=amp, dur=dur))
                assert out.get("terminal") is True
                assert ts.state.r5_forks == before_forks
                assert ts.state.r5_meters == before_meters
                stop = ts.state.r5_resource_stop
                assert stop["meter"] == "log_entries"
                assert stop["current"] == stop["limit"] == 4
                assert stop["requested"] == 2
                assert sum(ts.state.r5_cap_hits.values()) == 1
                assert ts.state.r5_phase != "revealed"
                results.append(dict(amp=amp, dur=dur, accepted=2,
                                    persisted_entries=4, terminal_before_third_append=True))
        # Every metadata-growing tool checks before simulation or mutation.
        paths = [("read5", dict(window=1)), ("wait5", dict(steps=1)),
                 ("adjust5", dict(device=0, u1=0.1, u2=0, u3=0, read=False)),
                 ("inject5", dict(port=0, amp=0, dur=0.001))]
        for name, kw in paths:
            ts = make_ts(nonce=f"metadata-preflight-{name}")
            fid = json.loads(await ts.fork5(t=0))["fork"]
            before = copy.deepcopy(ts.state.r5_forks)
            with patch.object(R5, "CAPS5_R2", {**EXPECTED_R2, "log_entries": 0}), \
                    patch.object(ts, "_advance_sim", side_effect=AssertionError("advanced before metadata gate")):
                out = json.loads(await getattr(ts, name)(ctx=fid, **kw))
            assert out.get("terminal") is True, (name, out)
            assert ts.state.r5_resource_stop["meter"] == "log_entries"
            assert ts.state.r5_forks == before
            assert persisted_entries(ts) == ts.state.r5_meters["log_entries"] == 0
        # Normal operations count actual persisted records, not read steps.
        ts = make_ts(nonce="metadata-accounting")
        fid = json.loads(await ts.fork5(t=0))["fork"]
        await ts.read5(ctx=fid, window=3)
        await ts.wait5(ctx=fid, steps=2)
        await ts.adjust5(ctx=fid, device=0, u1=0.1, u2=0, u3=0,
                         steps=2, read=False)
        await ts.inject5(ctx=fid, port=0, amp=0, dur=0.001)
        assert persisted_entries(ts) == ts.state.r5_meters["log_entries"] == 5
        # A rejected first step adds no history and must not trip a full
        # metadata guard. A zero-window read similarly adds no history.
        ts.state.r5_forks[fid]["poses"][0][2] = 3.0
        with patch.object(R5, "CAPS5_R2", {**EXPECTED_R2, "log_entries": 5}):
            out = json.loads(await ts.adjust5(ctx=fid, device=0, u1=0, u2=0,
                                              u3=1, steps=1, read=False))
            assert out["result"] == "adjust_rejected" and out["steps_applied"] == 0
            assert "error" not in json.loads(await ts.read5(ctx=fid, window=0))
        assert persisted_entries(ts) == ts.state.r5_meters["log_entries"] == 5
        no_cap_hits(ts)
        # Old cohorts still retain accepted no-op history without this guard.
        old = make_ts(policy="v2", nonce="metadata-legacy")
        fid = json.loads(await old.fork5(t=0))["fork"]
        with patch.object(R5, "CAPS5_R2", {**EXPECTED_R2, "log_entries": 0}):
            assert json.loads(await old.inject5(ctx=fid, port=0, amp=0, dur=0.001))["ok"]
        assert persisted_entries(old) == 2
        assert "log_entries" not in old.state.r5_meters
        assert "log_entries" not in old.state.r5_cap_hits
        no_cap_hits(old)
        return dict(pass_=True, guard=1_000_000,
                    counter="persisted operation-log plus emission-list entries",
                    noop_entries_preserved=results,
                    preflight_before_physics_paths=[n for n, _ in paths],
                    actual_entry_accounting=True, legacy_unchanged=True)


async def response_memory_gate():
    with synthetic_world():
        ts = make_ts(nonce="response-memory")
        fid = json.loads(await ts.fork5(t=0))["fork"]
        before = copy.deepcopy(ts.state.r5_meters)
        # A billion-step dense read must reject its output envelope without
        # constructing a billion-item list or starting any simulation.
        with patch.object(ts, "_advance_sim", side_effect=AssertionError("advanced")):
            out = json.loads(await ts.read5(ctx=fid, window=1_000_000_000))
            assert out["error"].startswith("response too large")
            assert not out.get("terminal")
            out = json.loads(await ts.adjust5(ctx=fid, device=0, u1=0,
                u2=0, u3=0, steps=1_000_000, read=True))
            assert out["error"].startswith("response too large")
            assert not out.get("terminal")
        assert ts.state.r5_meters == before
        no_cap_hits(ts)
        # read=False does NOT introduce a per-call/fork duration limit.
        def fast_advance(state, fk, start, n):
            state["t_step"] += n * R5.SPC
        with patch.object(ts, "_advance_sim", fast_advance):
            out = json.loads(await ts.adjust5(ctx=fid, device=0, u1=0,
                u2=0, u3=0, steps=2_500, read=False))
        assert out["steps_applied"] == 2_500 and not out["steps_read"]
        no_cap_hits(ts)
        # A sparse giant read has a small response but exceeds the genuine
        # aggregate guard. It must latch stop before physics, not allocate.
        with patch.object(ts, "_advance_sim", side_effect=AssertionError("advanced")):
            out = json.loads(await ts.read5(ctx=fid, window=1_000_000_000,
                                           stride=1_000_000_000))
        assert out.get("terminal") is True
        assert ts.state.r5_resource_stop["meter"] == "sim_tu"
        assert sum(ts.state.r5_cap_hits.values()) == 1
        return dict(pass_=True, lazy_billion_step_read=True,
                    bounded_adjust_read_response=True,
                    long_adjust_read_false_steps=2_500,
                    sparse_oversized_read_stops_before_physics=True)


async def phase_and_caps_gate():
    with synthetic_world():
        ts = make_ts(nonce="phase")
        fid = json.loads(await ts.fork5(t=50))["fork"]
        await ts.inject5(ctx=fid, port=0, amp=0.3, dur=6.6)
        before = copy.deepcopy(ts.state.r5_meters)
        ready = await ts.ready5()
        private_free(ready)
        assert ts.state.r5_phase == "revealed"
        assert not S._LIVE5
        tools = [("read5", dict(ctx=fid, window=1)),
                 ("read5", dict(ctx="base", window=0)),
                 ("wait5", dict(ctx=fid, steps=1)),
                 ("adjust5", dict(ctx="base", device=0, u1=0, u2=0, u3=0)),
                 ("fork5", dict(t=100)), ("fork5", dict(fork=fid)),
                 ("reset5", dict(fork=fid)),
                 ("inject5", dict(ctx=fid, port=0, amp=0.5, dur=5)),
                 ("ready5", {})]
        for name, kw in tools:
            out = json.loads(await getattr(ts, name)(**kw))
            assert out == {"error": S._PHASE_ERR}, (name, out)
        assert ts.state.r5_meters == before
        status = await ts.status5()
        private_free(status)
        assert json.loads(status)["phase"] == "revealed"
        shape = R5.payload_shapes5(WORLD, SEED, MENU)["L2"]
        payload = dict(mean=np.zeros(shape).tolist(), sigma=1.0)
        accepted = json.loads(await ts.submit5(instance="L2", payload=payload))
        assert accepted["ok"]
        no_cap_hits(ts)

        # Apparatus bounds are task definition, not revised resource policy.
        apparatus = make_ts(nonce="apparatus")
        af = json.loads(await apparatus.fork5(t=0))["fork"]
        for args in (dict(port=0, amp=1.01, dur=5),
                     dict(port=0, amp=0.5, dur=50.01),
                     dict(port=0, amp=0.5, dur=0),
                     dict(port=0, amp=0.01, dur=5)):
            out = json.loads(await apparatus.inject5(ctx=af, **args))
            assert "error" in out and not out.get("terminal"), out
        adjusted = json.loads(await apparatus.adjust5(ctx=af, device=0,
            u1=7, u2=-7, u3=0, steps=1, read=False))
        assert adjusted["applied"] == [1.0, -1.0, 0.0]
        no_cap_hits(apparatus)
        S._LIVE5.clear()

        # Each private cap has a separate tiny fixture. A trip latches ONCE,
        # every tool then returns terminal without additional cap counters,
        # world mutations, reveal, or a loop of generic saturated errors.
        trips = {}
        for meter in EXPECTED_R2:
            ts = make_ts(nonce=f"cap-{meter}")
            fid = json.loads(await ts.fork5(t=0))["fork"]
            tiny = {**EXPECTED_R2, meter: 0}
            if meter == "fork_spawns":
                tiny[meter] = 1
            if meter == "open_forks":
                tiny[meter] = 1
            with patch.object(R5, "CAPS5_R2", tiny):
                calls = {
                    "sensor": ("read5", dict(ctx="base", window=0)),
                    "sim_tu": ("wait5", dict(ctx=fid, steps=1)),
                    "adjust": ("adjust5", dict(device=0, u1=0.1, u2=0,
                                               u3=0, ctx=fid, read=False)),
                    "injection": ("inject5", dict(ctx=fid, port=0, amp=0.5, dur=5)),
                    "fork_spawns": ("fork5", dict(t=10)),
                    "open_forks": ("fork5", dict(t=10)),
                    "log_entries": ("inject5", dict(ctx=fid, port=0, amp=0, dur=0.001)),
                }
                name, kw = calls[meter]
                first = json.loads(await getattr(ts, name)(**kw))
                assert first == {"error": R5.RESOURCE_STOP_MSG5, "terminal": True}
                assert ts.state.r5_resource_stop["kind"] == "resource_limit"
                assert ts.state.r5_resource_stop["meter"] == meter
                assert sum(ts.state.r5_cap_hits.values()) == 1
                assert not S._LIVE5
                frozen = copy.deepcopy(ts.state.r5_meters)
                forks = copy.deepcopy(ts.state.r5_forks)
                for _ in range(3):
                    for next_name, next_kw in [*tools, ("status5", {}),
                                               ("submit5", dict(instance="L2", payload=payload))]:
                        out = json.loads(await getattr(ts, next_name)(**next_kw))
                        assert out == first, (next_name, out)
                assert sum(ts.state.r5_cap_hits.values()) == 1
                assert ts.state.r5_meters == frozen
                assert ts.state.r5_forks == forks
                assert ts.state.r5_phase != "revealed"
                assert ts.state.r5_t_ready_sim == -1
                private_free(json.dumps(first))
                trips[meter] = copy.deepcopy(ts.state.r5_resource_stop)

        # Legacy cap semantics remain generic and do NOT latch a halt.
        old = make_ts(policy="v2", nonce="old-caps")
        old._ensure5()
        old.state.r5_fork_seq = 400
        refused = json.loads(await old.fork5(t=0))
        assert refused == {"error": R5.CAP_MSG}
        assert old.state.r5_cap_hits["fork_spawns"] == 1
        assert not old.state.r5_resource_stop
        # Legacy 8-open ceiling is still a refusal (not LRU admission).
        old = make_ts(policy="v2", nonce="old-open")
        for i in range(8):
            assert "fork" in json.loads(await old.fork5(t=i * 5))
        refused = json.loads(await old.fork5(t=50))
        assert refused == {"error": R5.CAP_MSG}
        assert old.state.r5_cap_hits["open_forks"] == 1
        assert not old.state.r5_resource_stop
        return dict(pass_=True, post_ready_world_tools_closed=len(tools),
                    apparatus_bounds_unchanged=True, private_surface_clean=True,
                    synthetic_resource_trips=trips,
                    legacy_refusals_unchanged=True)


async def main(args):
    gates = args.gates
    result = dict(cohort="BLOB2v2r2", command=" ".join(sys.argv), gates={})
    started = time.monotonic()
    if "all" in gates:
        gates = ["config", "synthetic", "physics", "native"]
    async def run(label, fn):
        before = time.monotonic()
        row = await fn()
        row["duration_s"] = round(time.monotonic() - before, 3)
        result["gates"][label] = row
        print(f"PASS {label} ({row['duration_s']:.3f}s)", flush=True)
    if "config" in gates:
        await run("config", config_gate)
    if "synthetic" in gates:
        await run("handle_collision", handle_gate)
        await run("high_count", count_gate)
        await run("synthetic_parity", parity_gate)
        await run("deep_chain", deep_chain_gate)
        await run("metadata_entries", metadata_entries_gate)
        await run("response_memory", response_memory_gate)
        await run("phase_and_caps", phase_and_caps_gate)
    if "physics" in gates:
        await run("physics_parity", lambda: parity_gate(real=True))
    if "native" in gates:
        from test_blob_round5_resources_native import run_gate
        await run("native_lifecycle", run_gate)
    result["pass"] = True
    result["duration_s"] = round(time.monotonic() - started, 3)
    if args.json_out:
        path = Path(args.json_out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gates", nargs="+", default=["all"],
                        choices=["all", "config", "synthetic", "physics", "native"])
    parser.add_argument("--json-out")
    asyncio.run(main(parser.parse_args()))
