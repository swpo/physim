"""R6 scheduler gates. Local-only; no inference, cache replay, or truth creation.

From the repo root:
  .venv/bin/python environments/physim/tools/test_blob_round6.py --gates toy
  .venv/bin/python environments/physim/tools/test_blob_round6.py --gates native
  ... --gates toy native --json-out probes/blobs/agentenv/round6/runner/validation.json

The native gate initializes only the existing E1/928 case and takes at most six
native substeps per trajectory. Toy fixtures are exact test laws, not new worlds.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import replace
import json
import os
from pathlib import Path
import pickle
import resource
import sys
import time
import unittest
from unittest.mock import patch

for _key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_key] = "1"

import numpy as np

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "environments" / "physim"))
from physim import blobround6 as R6

NATIVE_REPORT = {}


class _ToyDevice:
    def __init__(self, index, dilation=1.0):
        self.k = (2, 3)[index]
        self.center = np.array((15.5, 15.5) if index == 0 else (2.0, 3.0))
        self.dilation = dilation
        self.dil_bounds = (0.5, 3.0)
        self.L = 16.0

    def sample(self, fields, dx):
        # Perfect known-state observation law. It has no RNG or side effects.
        return (fields.mean(axis=(1, 2))[:, None]
                + self.center[0] + 2 * self.center[1]
                + self.dilation * np.arange(self.k)[None, :])


def _toy_step(sim, n_steps, injections=None):
    # Fixed per-substep operation order, even when queries cut a chunk.
    for _ in range(n_steps):
        for inj in injections or ():
            sim["F"][inj["field"]] += inj["amp"] * R6.SIM_DT
        sim["F"] = sim["F"] + np.array((0.25, 0.5))[:, None, None]
        if sim["noise"]:
            sim["F"] += sim["rng"].standard_normal(sim["F"].shape) * 0.01
        sim["t_step"] += 1


def _toy(noise=False, dilation=1.0):
    template = dict(F=np.arange(8, dtype=np.float64).reshape(2, 2, 2),
                    rng=np.random.default_rng(2024), t_step=0, dt=R6.SIM_DT,
                    dx=1.0, noise=noise)
    devices = [_ToyDevice(0, dilation), _ToyDevice(1)]
    calls = []

    def step(sim, n_steps, injections=None):
        calls.append((sim["t_step"], n_steps, deepcopy(injections)))
        _toy_step(sim, n_steps, injections)

    predictor = R6.OracleRunner(
        _template=template, _devices=devices, _port_perm=[1, 0],
        _adjust_mix=np.array(((0, 1.5, 0), (1.5, 0, 0), (0, 0, 1.0))),
        _emitter_yx=[15.5, 15.5], _stepper=step)
    return predictor, calls, template, devices


def _inj(t=0.04, amp=0.5, dur=0.04, port=0):
    return dict(t=t, kind="inject", port=port, amp=amp, dur=dur)


def _adj(t=0.04, u=None, device=0):
    return dict(t=t, kind="adjust", device=device, u=[0.2, 0.1, 0.1] if u is None else u)


def _query(times=None, sensor="global"):
    return dict(sensor=sensor, t=[0, 0.02, 0.04, 0.06, 0.1] if times is None else times)


def _samples(predictor, actions=None, queries=None, n=4, truth_seed=17):
    return predictor.sample_truth([] if actions is None else actions,
                             [_query()] if queries is None else queries,
                             n_samples=n, truth_seed=truth_seed)["samples"]


class _ArrayCase(unittest.TestCase):
    def arrays_equal(self, left, right):
        self.assertEqual(len(left), len(right))
        for a, b in zip(left, right):
            np.testing.assert_array_equal(a, b)


class ValidationTests(_ArrayCase):
    def setUp(self):
        self.p, self.calls, _, _ = _toy()

    def bad(self, actions=None, queries=None, **kwargs):
        with self.assertRaises(R6.ProtocolError):
            self.p.sample_truth([] if actions is None else actions,
                                [_query()] if queries is None else queries,
                                **dict({"truth_seed": 17}, **kwargs))
        self.assertEqual(self.calls, [], "validation must precede all physics")

    def test_container_types_and_unknown_actions(self):
        for field in ("actions", "queries"):
            for value in (None, (), {}, "[]", True, 0):
                with self.subTest(field=field, value=value):
                    request = dict(actions=[], queries=[], truth_seed=17)
                    request[field] = value
                    with self.assertRaises(R6.ProtocolError):
                        self.p.sample_truth(**request)
        for value in (None, [], 3, "adjust"):
            with self.subTest(action=value):
                self.bad(actions=[value])
        for kind in (None, True, [], "wait", "read", "fork", "reset"):
            with self.subTest(kind=kind):
                self.bad(actions=[dict(t=0, kind=kind)])

    def test_exact_action_keys(self):
        for base in (_inj(), _adj()):
            for key in base:
                obj = dict(base)
                del obj[key]
                with self.subTest(missing=key, kind=base["kind"]):
                    self.bad(actions=[obj])
            for key in ("history", "anchor_t", "seed", "x", "pose", "steps", "read"):
                with self.subTest(extra=key, kind=base["kind"]):
                    self.bad(actions=[dict(base, **{key: 0})])

    def test_exact_query_keys_and_shapes(self):
        for query in (None, [], "device0", {}, dict(sensor="global"),
                      dict(t=[0]), dict(sensor="global", t=[0], history=[])):
            with self.subTest(query=query):
                self.bad(queries=[query])
        for sensor in (None, True, 0, [], "device2", "Device0", "device00", "hidden"):
            with self.subTest(sensor=sensor):
                self.bad(queries=[dict(sensor=sensor, t=[0])])
        for times in (None, 0, 0.02, (0,), "[0]", {}, True):
            with self.subTest(times=times):
                self.bad(queries=[dict(sensor="global", t=times)])

    def test_boolean_string_and_nonfinite_numbers(self):
        values = (True, False, "0.02", None, [], float("nan"), float("inf"),
                  -float("inf"), 10**400)
        for value in values:
            for key in ("t", "amp", "dur"):
                with self.subTest(value=repr(value), key=key):
                    obj = _inj()
                    obj[key] = value
                    self.bad(actions=[obj])
            with self.subTest(value=repr(value), key="u"):
                self.bad(actions=[_adj(u=[0, value, 0])])
            with self.subTest(value=repr(value), key="query t"):
                self.bad(queries=[_query([value])])

    def test_integer_ids_counts_seeds_and_ranges(self):
        for value in (-1, 2, 0.0, True, "0", [], None):
            with self.subTest(device=value):
                self.bad(actions=[_adj(device=value)])
        for value in (-1, 2, 0.0, True, "0", [], None):
            with self.subTest(port=value):
                self.bad(actions=[_inj(port=value)])
        for value in (0, -1, 1.0, True, "1", None, 2**64):
            with self.subTest(n_samples=value):
                self.bad(n_samples=value)
        for value in (-1, 0.0, True, "0", None, R6.MAX_SEED + 1):
            with self.subTest(truth_seed=value):
                self.bad(truth_seed=value)
        for value in (-0.01, 3.000001):
            self.bad(actions=[_inj(amp=value)])
        for value in (0, -0.02, 50.02, 1e-11):
            self.bad(actions=[_inj(dur=value)])
        for u in ([], [0], [0, 0], [0, 0, 0, 0], (0, 0, 0),
                  [[0], 0, 0], [1.0001, 0, 0], [0, -1.0001, 0]):
            with self.subTest(u=u):
                self.bad(actions=[_adj(u=u)])

    def test_time_grid_and_float_tolerance(self):
        for t in (-1e-12, -0.02, 0.01, 0.03, 0.020000002):
            with self.subTest(t=t):
                self.bad(actions=[_inj(t=t)])
                self.bad(queries=[_query([t])])
        self.bad(actions=[_inj(dur=0.03)])
        self.bad(queries=[_query([1e300])])
        self.bad(actions=[_adj(t=R6.MAX_EXACT_TICK * R6.SIM_DT)])
        exact = _samples(self.p, queries=[_query([0.3, 0.32])], n=1)
        tolerant = _samples(self.p, queries=[_query([0.1 + 0.2, 0.3200000001])], n=1)
        self.arrays_equal(exact, tolerant)

    def test_unsorted_simultaneous_and_overlapping_actions(self):
        cases = [
            [_inj(0.1), _inj(0.02)],
            [_inj(0, dur=0.02), _adj(0)],
            [_adj(0), _inj(0, amp=0)],
            [_inj(0, dur=0.06), _inj(0.04, port=1)],
            [_adj(0), _adj(4.98, device=1)],
            [_adj(0, u=[0, 0, 0]), _adj(0.02, device=1)],
            [_inj(0.3, dur=0.02), _inj(0.3000000001, dur=0.02)],
        ]
        for actions in cases:
            with self.subTest(actions=actions):
                self.bad(actions=actions)

    def test_empty_outputs_validate_all_actions_but_never_step(self):
        self.assertEqual(self.p.sample_truth([_adj(0)], [], 1, truth_seed=17), {"samples": []})
        arrays = self.p.sample_truth([_inj(0)], [_query([], "device0"), _query([])], 3, truth_seed=17)["samples"]
        self.assertEqual([a.shape for a in arrays], [(3, 0, 2, 2), (3, 0, 2, 2)])
        self.bad(actions=[_inj(20, amp=99)], queries=[])
        self.bad(actions=[_adj(0), _adj(1)], queries=[_query([])])
        self.assertEqual(self.calls, [])

    def test_supported_boundaries_and_cross_lane_overlap(self):
        schedules = [
            [_inj(0, amp=0, dur=50)],
            [_inj(0, amp=3, dur=0.02)],
            [_adj(0, [-1, 1, -1])],
            [_adj(0), _adj(5, device=1)],
            [_inj(0, dur=0.06), _inj(0.06, dur=0.02)],
            [_inj(0, dur=10.5), _adj(5)],
            [_adj(0), _inj(0.02, dur=0.02)],
        ]
        for actions in schedules:
            with self.subTest(actions=actions):
                _samples(self.p, actions, [_query([0])], n=1, truth_seed=R6.MAX_SEED)
        self.assertEqual(self.calls, [], "occupied durations never extend last query")


class SchedulerTests(_ArrayCase):
    def test_predictor_sampling_seed_is_not_an_oracle_truth_input(self):
        class SubmittedToyPredictor:
            # Only an interface fixture; not a physics model or scorer.
            def predict(self, actions, queries, n_samples=64, seed=0):
                rng = np.random.default_rng(seed)
                return {"samples": [rng.standard_normal((n_samples, len(q["t"]), 2, 2))
                                    for q in queries]}

        p, _, _, _ = _toy(noise=True)
        truth_request = dict(actions=[_inj()], queries=[_query()],
                             n_samples=4, truth_seed=41)
        saved_request = deepcopy(truth_request)
        original = p.sample_truth(**truth_request)["samples"]
        submitted = SubmittedToyPredictor()
        previous_prediction = None
        for predictor_seed in (11, 12):
            public_request = {k: deepcopy(v) for k, v in truth_request.items()
                              if k != "truth_seed"}
            public_request["seed"] = predictor_seed
            prediction = submitted.predict(**public_request)["samples"]
            self.arrays_equal(original, p.sample_truth(**truth_request)["samples"])
            self.assertEqual(truth_request, saved_request)
            with self.assertRaises(TypeError):
                p.sample_truth(**public_request)   # no accidental seed alias
            if previous_prediction is not None:
                self.assertFalse(np.array_equal(prediction[0], previous_prediction[0]))
            previous_prediction = prediction
        self.assertFalse(hasattr(p, "predict"))
        with self.assertRaises(TypeError):
            p.sample_truth([], [])  # truth seed is required, even for empty output

    def test_perfect_known_state_deterministic_law(self):
        p, _, _, _ = _toy()
        times = [0, 0.02, 0.04, 0.06, 0.1]
        out = _samples(p, queries=[_query(times), _query(times, "device1")], n=3)
        means = np.array([5.5, 1.5])[None, :] + np.arange(0, 6)[[0, 1, 2, 3, 5], None] * [0.5, 0.25]
        for member in range(3):
            np.testing.assert_array_equal(out[0][member, :, :, 0], means)
            np.testing.assert_array_equal(out[0][member, :, :, 1], np.full_like(means, 1.25))
            expected = means[:, :, None] + 8.0 + np.arange(3)[None, None, :]
            np.testing.assert_array_equal(out[1][member], expected)
        self.assertEqual(out[0].dtype, np.float64)

    def test_source_half_open_boundaries_and_amplitude_duration(self):
        p, calls, _, _ = _toy()
        times = [0.02, 0.04, 0.06, 0.08, 0.1, 0.12]
        actions = [_inj(0.04, amp=2.8, dur=0.06), _inj(0.1, amp=1, dur=0.02)]
        out = _samples(p, actions, [_query(times)], n=1)[0][0]
        ticks = np.array([1, 2, 3, 4, 5, 6])
        means = [5.5, 1.5] + ticks[:, None] * [0.5, 0.25]
        means[:, 0] += np.array([0, 0, 1, 2, 3, 3]) * 2.8 * 0.02
        means[:, 0] += np.array([0, 0, 0, 0, 0, 1]) * 0.02
        np.testing.assert_allclose(out[:, :, 0], means, atol=1e-13, rtol=0)
        np.testing.assert_allclose(out[:, :, 1], 1.25, atol=1e-13, rtol=0)
        # Original fixed emitter, not adjusted device location or query layout.
        emitted = [inj[0] for _, _, inj in calls if inj]
        self.assertTrue(emitted)
        self.assertTrue(all(j["field"] == 1 and (j["y"], j["x"]) == (15.5, 15.5)
                            for j in emitted))

    def test_adjust_is_immediate_and_occupies_five_tu(self):
        p, _, _, _ = _toy()
        times = [0, 0.02, 4.98, 5, 5.02, 10]
        actions = [_adj(0, [1, 1, 1]), _adj(5, [0, 0, 1]), _adj(10, [0, 0, -1])]
        arrays = _samples(p, actions, [_query(times), _query(times, "device0")], n=1)
        device = arrays[1][0]
        means = arrays[0][0, :, :, 0]
        expected_dilation = [np.e, np.e, np.e, 3.0, 3.0, 3 * np.exp(-1)]
        for i, dilation in enumerate(expected_dilation):
            expected = means[i, :, None] + 3.0 + dilation * np.arange(2)[None, :]
            np.testing.assert_allclose(device[i], expected, atol=1e-12, rtol=0)
        # Query at command start is not silently moved to t+5.
        np.testing.assert_array_equal(arrays[0][0, 0, :, 0], [5.5, 1.5])

    def test_lower_dilation_clip_and_second_device_independence(self):
        p, _, _, _ = _toy()
        actions = [_adj(0, [0, 0, -1]), _adj(5, [0, 0, -1])]
        arrays = _samples(p, actions, [_query([0, 5], "device0"),
                                      _query([0, 5], "device1")], n=1)
        np.testing.assert_allclose(arrays[0][0, :, :, 1] - arrays[0][0, :, :, 0], 0.5)
        np.testing.assert_allclose(arrays[1][0, :, :, 1] - arrays[1][0, :, :, 0], 1.0)

    def test_query_invariance_order_duplicates_and_no_mutation(self):
        p, _, _, _ = _toy(noise=True)
        actions = [_inj(0.04)]
        original = deepcopy(actions)
        sparse_queries = [_query([0.1, 0.04, 0.06], "device1")]
        original_queries = deepcopy(sparse_queries)
        sparse = _samples(p, actions, sparse_queries, n=6)[0]
        dense = _samples(p, actions, [_query([0.1, 0.06, 0, 0.1], "device1"),
                                     _query([0.04, 0.08, 0.02]),
                                     _query([0.04, 0.06, 0.1], "device1")], n=6)
        np.testing.assert_array_equal(sparse[:, [1, 2, 0]], dense[2])
        np.testing.assert_array_equal(dense[0][:, 0], dense[0][:, 3])
        self.assertEqual(actions, original)
        self.assertEqual(sparse_queries, original_queries)
        state = R6._clone_sim(p._template)
        rng_before = pickle.dumps(state["rng"].bit_generator.state)
        fields_before = state["F"].copy()
        poses_before = pickle.dumps(p._devices)
        for sensor in ("device0", "global", "device1"):
            p._sample(state, p._devices, sensor)
        self.assertEqual(pickle.dumps(state["rng"].bit_generator.state), rng_before)
        np.testing.assert_array_equal(state["F"], fields_before)
        self.assertEqual(pickle.dumps(p._devices), poses_before)

    def test_future_action_suffix_cannot_change_past_queries(self):
        p, _, _, _ = _toy(noise=True)
        queries = [_query([0, 0.02, 0.04, 0.06, 0.08])]
        prefix = [_inj(0.04, dur=0.04)]
        self.arrays_equal(_samples(p, prefix, queries),
                          _samples(p, prefix + [_inj(0.12), _adj(0.18)], queries))
        self.arrays_equal(_samples(p, [], queries),
                          _samples(p, [_adj(0.1)], queries))

    def test_base_replay_and_noops_ignore_truth_seed(self):
        p, _, _, _ = _toy(noise=True)
        plain = _samples(p, truth_seed=1)
        self.arrays_equal(plain, _samples(p, truth_seed=R6.MAX_SEED))
        for m in range(1, 4):
            np.testing.assert_array_equal(plain[0][0], plain[0][m])
        self.arrays_equal(plain, _samples(p, [_inj(0, amp=0, dur=0.02),
                                            _adj(0.02, [0, 0, 0])], truth_seed=55))
        clipped, _, _, _ = _toy(noise=True, dilation=3.0)
        self.arrays_equal(_samples(clipped, truth_seed=1),
                          _samples(clipped, [_adj(0, [0, 0, 1])], truth_seed=99))

    def test_noops_do_not_move_first_branch_or_reseed(self):
        p, _, _, _ = _toy(noise=True, dilation=3.0)
        action = _inj(0.04, dur=0.02)
        baseline = _samples(p, [action])
        self.arrays_equal(baseline, _samples(p, [_adj(0, [0, 0, 1]), action]))
        self.arrays_equal(baseline, _samples(p, [action, _inj(0.08, amp=0)]))
        self.arrays_equal(baseline, _samples(p, [_inj(0, amp=0, dur=0.02), action]))

    def test_branch_at_pose_change_and_only_once_across_multiple_actions(self):
        p, _, template, devices = _toy(noise=True)
        actions = [_adj(0.02, [0.2, 0.1, 0]), _inj(0.04, dur=0.02), _inj(0.08, dur=0.02)]
        times = [0, 0.02, 0.04, 0.06, 0.08, 0.1]
        got = _samples(p, actions, [_query(times)], n=3, truth_seed=4)[0]
        base = R6._clone_sim(template)
        _toy_step(base, 1)
        # Manual known-state reference switches exactly once at tick 1.
        for member in range(3):
            ref = R6._clone_sim(base)
            ref["rng"] = np.random.default_rng(R6._truth_member_seed(4, member))
            np.testing.assert_array_equal(got[member, 1, :, 0], ref["F"][[1, 0]].mean(axis=(1, 2)))
            for tick in range(1, 5):
                active = [dict(field=1, amp=0.5)] if tick in (2, 4) else []
                _toy_step(ref, 1, active)
                f = ref["F"][[1, 0]]
                expected = np.stack((f.mean(axis=(1, 2)), f.var(axis=(1, 2))), axis=1)
                np.testing.assert_array_equal(got[member, tick + 1], expected)
        np.testing.assert_array_equal(got[0, :2], got[1, :2])
        self.assertFalse(np.array_equal(got[0, 2:], got[1, 2:]))

    def test_member_prefix_distinct_streams_and_cross_sensor_coherence(self):
        p, _, _, _ = _toy(noise=True)
        queries = [_query(), _query(sensor="device0"), _query(sensor="device1")]
        small = _samples(p, [_inj()], queries, n=3, truth_seed=9)
        large = _samples(p, [_inj()], queries, n=7, truth_seed=9)
        self.arrays_equal(small, [a[:3] for a in large])
        self.assertEqual(len({R6._truth_member_seed(9, m) for m in range(64)}), 64)
        self.assertEqual(len({tuple(large[0][m, -1].ravel()) for m in range(7)}), 7)
        for di, offset in ((1, 46.5), (2, 8.0)):
            expected = large[0][:, :, :, 0, None] + offset + np.arange(di + 1)
            np.testing.assert_allclose(large[di], expected, rtol=0, atol=1e-12)
        changed_seed = _samples(p, [_inj()], queries, n=3, truth_seed=10)
        for a, b in zip(small, changed_seed):
            np.testing.assert_array_equal(a[:, :3], b[:, :3])
        self.assertFalse(np.array_equal(small[0][:, 3:], changed_seed[0][:, 3:]))

    def test_reset_repeat_and_output_ownership(self):
        p, _, template, devices = _toy(noise=True)
        before_fields = template["F"].copy()
        before_rng = pickle.dumps(template["rng"].bit_generator.state)
        before_devices = pickle.dumps(devices)
        original = _samples(p, [_inj()], truth_seed=3)
        _samples(p, [_adj(0), _inj(0.04)], n=7, truth_seed=7)
        _samples(p, queries=[_query([0.4])], truth_seed=55)
        repeated = _samples(p, [_inj()], truth_seed=3)
        self.arrays_equal(original, repeated)
        repeated[0].fill(999)
        self.arrays_equal(original, _samples(p, [_inj()], truth_seed=3))
        np.testing.assert_array_equal(template["F"], before_fields)
        self.assertEqual(pickle.dumps(template["rng"].bit_generator.state), before_rng)
        self.assertEqual(pickle.dumps(devices), before_devices)


class CheckpointTests(_ArrayCase):
    def test_exact_checkpoint_reuse_preserves_rng_and_saves_steps(self):
        p, calls, template, _ = _toy(noise=True)
        _samples(p, queries=[_query([0.06])])
        cp = p._base_checkpoints[3]
        ref = R6._clone_sim(template)
        _toy_step(ref, 3)
        np.testing.assert_array_equal(cp.fields, ref["F"])
        self.assertEqual(pickle.dumps(cp.rng_state), pickle.dumps(ref["rng"].bit_generator.state))
        self.assertEqual(cp.fields.dtype, np.float64)
        self.assertFalse(cp.fields.flags.writeable)
        calls.clear()
        warm = _samples(p, queries=[_query([0.1])])
        self.assertEqual([(k, n) for k, n, _ in calls], [(3, 2)])
        cold, _, _, _ = _toy(noise=True)
        self.arrays_equal(warm, _samples(cold, queries=[_query([0.1])]))
        self.assertLessEqual(len(p._base_checkpoints), 2)

    def test_checkpoint_never_skips_earlier_query_or_intervention(self):
        p, calls, _, _ = _toy(noise=True)
        _samples(p, queries=[_query([0.2])])
        calls.clear()
        request = [_inj(0.02)]
        warm = _samples(p, request, [_query([0, 0.1])])
        cold, _, _, _ = _toy(noise=True)
        self.arrays_equal(warm, _samples(cold, request, [_query([0, 0.1])]))
        self.assertEqual(calls[0][:2], (0, 1))

    def test_checkpoint_provenance_dtype_and_tamper_rejection(self):
        p, _, _, _ = _toy()
        other, _, _, _ = _toy()
        cp = p._base_checkpoints[0]
        with self.assertRaisesRegex(ValueError, "provenance"):
            p._restore_base(other._base_checkpoints[0])
        bad_rng = deepcopy(cp.rng_state)
        bad_rng["state"]["state"] += 1
        cases = [replace(cp, fields=cp.fields.astype(np.float16)),
                 replace(cp, fields=cp.fields[:, :1, :1]),
                 replace(cp, tick=1), replace(cp, rng_state=bad_rng)]
        for bad in cases:
            with self.subTest(dtype=bad.fields.dtype, tick=bad.tick):
                with self.assertRaisesRegex(ValueError, "integrity"):
                    p._restore_base(bad)
        sim = R6._clone_sim(p._template)
        sim["F"] = sim["F"].astype(np.float16)
        with self.assertRaisesRegex(ValueError, "precision"):
            p._remember_base(sim)

    def test_private_template_is_owned_full_precision_t0(self):
        p, _, template, devices = _toy(noise=True)
        baseline = _samples(p)
        template["F"].fill(0)
        template["rng"].standard_normal(25)
        devices[0].center.fill(0)
        self.arrays_equal(baseline, _samples(p))
        for change in ({"F": np.zeros((2, 2, 2), np.float16)},
                       {"t_step": 1}, {"dt": 0.01},
                       {"F": np.full((2, 2, 2), np.nan)}):
            with self.subTest(change=list(change)):
                broken = dict(p._template, **change)
                with self.assertRaises(ValueError):
                    R6.OracleRunner(_template=broken, _devices=p._devices,
                                 _port_perm=[1, 0], _adjust_mix=p._mix,
                                 _emitter_yx=p._emitter, _stepper=_toy_step)
        self.assertFalse(p._template["F"].flags.writeable)
        self.assertTrue(R6._clone_sim(p._template)["F"].flags.writeable)


class NativeTests(_ArrayCase):
    @classmethod
    def setUpClass(cls):
        from physim import blobcore as B
        from physim import blobround5 as R5
        cls.B, cls.R5 = B, R5
        started = time.perf_counter()
        cls.origin = R6._native_oracle("p4g2_044", 928, workers=1)
        NATIVE_REPORT.update(world="p4g2_044", hidden_seed=928,
                             initialization_seconds=time.perf_counter() - started,
                             field_shape=list(cls.origin._template["F"].shape),
                             field_dtype=str(cls.origin._template["F"].dtype),
                             field_bytes=cls.origin._template["F"].nbytes,
                             maximum_trajectory_substeps=6,
                             old_truth_parity="not run; primitive/state parity only")

    def fresh(self):
        p = self.origin
        return R6.OracleRunner(_template=p._template, _devices=p._devices,
                            _port_perm=p._perm, _adjust_mix=p._mix,
                            _emitter_yx=p._emitter, _stepper=self.B.agdev.step_chunk)

    def ref_sample(self, sim, devices, sensor):
        fields = sim["F"][self.origin._perm]
        if sensor == "global":
            return np.stack((fields.mean(axis=(1, 2)), fields.var(axis=(1, 2))), axis=1)
        return devices[int(sensor[-1])].sample(fields, sim["dx"])

    def test_native_base_replay_direct_stepper_exact(self):
        p = self.fresh()
        times = [0, 0.02, 0.04, 0.06]
        queries = [_query(times, sensor) for sensor in ("device0", "device1", "global")]
        got = _samples(p, queries=queries, n=3)
        self.assertEqual([a.shape for a in got],
                         [(3, 4, len(p._perm), 13), (3, 4, len(p._perm), 19),
                          (3, 4, len(p._perm), 2)])
        ref = R6._clone_sim(p._template)
        for ti in range(4):
            if ti:
                self.B.agdev.step_chunk(ref, 1)
            for qi, query in enumerate(queries):
                expected = self.ref_sample(ref, p._devices, query["sensor"])
                for member in range(3):
                    np.testing.assert_array_equal(got[qi][member, ti], expected)

    def test_native_query_cuts_do_not_change_rng_or_fields(self):
        dense, sparse = self.fresh(), self.fresh()
        a = _samples(dense, queries=[_query([0, 0.02, 0.04, 0.06], "device1")])
        b = _samples(sparse, queries=[_query([0.06], "device1")])
        np.testing.assert_array_equal(a[0][:, -1:], b[0])
        ca, cb = dense._base_checkpoints[3], sparse._base_checkpoints[3]
        np.testing.assert_array_equal(ca.fields, cb.fields)
        self.assertEqual(pickle.dumps(ca.rng_state), pickle.dumps(cb.rng_state))

    def test_native_injection_matches_r5_member_state_and_source_primitive(self):
        p = self.fresh()
        truth_seed = 7
        actions = [_inj(0.02, amp=2.8, dur=0.02, port=0)]
        times = [0.02, 0.04, 0.06]
        queries = [_query(times, "device1"), _query(times)]
        got = _samples(p, actions, queries, n=2, truth_seed=truth_seed)
        base = R6._clone_sim(p._template)
        self.B.agdev.step_chunk(base, 1)
        inj = dict(field=int(p._perm[0]), y=p._emitter[0], x=p._emitter[1], amp=2.8)
        for member in range(2):
            # R5's exact state constructor is semantically matched at this
            # first source. This is NOT a full old truth-instance parity test.
            ref = self.R5._member_state(p._template, base["F"],
                                        R6._truth_member_seed(truth_seed, member), 1)
            for ti in range(3):
                if ti:
                    self.B.agdev.step_chunk(ref, 1, injections=[inj] if ti == 1 else [])
                for qi, query in enumerate(queries):
                    np.testing.assert_array_equal(got[qi][member, ti],
                                                  self.ref_sample(ref, p._devices, query["sensor"]))
        self.assertFalse(np.array_equal(got[0][0, -1], got[0][1, -1]))

    def test_native_multiple_actions_fixed_emitter_and_pose(self):
        p = self.fresh()
        actions = [_inj(0.02, dur=0.02), _adj(0.04), _inj(0.06, dur=0.02, port=1)]
        times = [0.02, 0.04, 0.06, 0.08, 0.1]
        queries = [_query(times, "device0"), _query(times, "global")]
        got = _samples(p, actions, queries, n=2, truth_seed=3)
        base = R6._clone_sim(p._template)
        self.B.agdev.step_chunk(base, 1)
        for member in range(2):
            ref = self.R5._member_state(p._template, base["F"], R6._truth_member_seed(3, member), 1)
            devices = deepcopy(p._devices)
            for tick in range(1, 6):
                if tick > 1:
                    port = {2: 0, 4: 1}.get(tick)
                    inj = [] if port is None else [dict(
                        field=int(p._perm[port]), y=p._emitter[0], x=p._emitter[1], amp=0.5)]
                    self.B.agdev.step_chunk(ref, 1, injections=inj)
                if tick == 2:
                    delta = self.B.adjust_mix("unused") @ np.array(actions[1]["u"])
                    devices[0].center = (devices[0].center + delta[:2]) % devices[0].L
                    devices[0].dilation = float(np.clip(
                        devices[0].dilation * np.exp(delta[2]), *devices[0].dil_bounds))
                for qi, query in enumerate(queries):
                    np.testing.assert_array_equal(got[qi][member, tick - 1],
                                                  self.ref_sample(ref, devices, query["sensor"]))

    def test_native_private_checkpoint_continuation_exact(self):
        warm, cold = self.fresh(), self.fresh()
        _samples(warm, queries=[_query([0.08])])
        a = _samples(warm, queries=[_query([0.12])])
        b = _samples(cold, queries=[_query([0.12])])
        self.arrays_equal(a, b)
        cp = warm._base_checkpoints[6]
        self.assertEqual(cp.fields.dtype, np.float32)
        np.testing.assert_array_equal(cp.fields, cold._base_checkpoints[6].fields)
        self.assertEqual(pickle.dumps(cp.rng_state), pickle.dumps(cold._base_checkpoints[6].rng_state))

    def test_native_pose_helper_matches_r5_truth_not_transport(self):
        p = self.fresh()
        seq = [[1, 1, 1], [0, 0, 1], [-1, -1, -1], [0, 0, -1]]
        dev = deepcopy(p._devices[0])
        for u in seq:
            R6._adjust_pose(dev, u, p._mix)
        # Do not call B.make_device's heavy frame cache just to build a pose.
        with patch.object(self.B, "make_device", return_value=deepcopy(p._devices[0])):
            expected = self.R5._walked_device_l1("p4g2_044", 928, seq)
        np.testing.assert_array_equal(dev.center, expected.center)
        self.assertEqual(dev.dilation, expected.dilation)


class _TimedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timings = []

    def startTest(self, test):
        self._started = time.perf_counter()
        super().startTest(test)

    def stopTest(self, test):
        self.timings.append(dict(test=test.id(), seconds=time.perf_counter() - self._started))
        super().stopTest(test)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gates", nargs="+", choices=("toy", "native"), default=["toy"])
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    classes = []
    if "toy" in args.gates:
        classes.extend((ValidationTests, SchedulerTests, CheckpointTests))
    if "native" in args.gates:
        classes.append(NativeTests)
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in classes)
    started = time.perf_counter()
    result = unittest.TextTestRunner(verbosity=2, resultclass=_TimedResult).run(suite)
    elapsed = time.perf_counter() - started
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_bytes = int(rss if sys.platform == "darwin" else rss * 1024)
    report = dict(status="passed" if result.wasSuccessful() else "failed",
                  gates=args.gates, tests_run=result.testsRun,
                  failures=[dict(test=t.id(), traceback=tb) for t, tb in result.failures],
                  errors=[dict(test=t.id(), traceback=tb) for t, tb in result.errors],
                  skipped=[dict(test=t.id(), reason=why) for t, why in result.skipped],
                  wall_seconds=elapsed, peak_rss_bytes=peak_bytes,
                  interpreter=sys.executable, numpy_version=np.__version__,
                  thread_env={k: os.environ[k] for k in
                              ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")},
                  tests=result.timings, native=NATIVE_REPORT,
                  limitations=["No old truth-instance parity or full base replay was run.",
                               "No scorer, untrusted-code sandbox, transport or exploration parity.",
                               "No final horizon/member/output resource budgets; trusted small requests only."])
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "tests_run", "wall_seconds", "peak_rss_bytes")}))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
