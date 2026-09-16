"""Centered-source protocol tests using small, exact Gaussian-deposition fixtures."""

from copy import deepcopy
from dataclasses import replace

import numpy as np
import pytest
from physim import blobround6 as R6
from physim import blobround6_eval as scoring
from physim import evaluation, taskset
from physim.blobround6_explore import ExperimentService
from physim.devices import ProbeDevice


def pulse(t=0, device=0, port=0, amp=1.0, dur=0.04):
    return dict(t=t, kind="inject", device=device, port=port, amp=amp, dur=dur)


def move(t=0, device=0, u=(1, 0, 0)):
    return dict(t=t, kind="adjust", device=device, u=list(u))


def toy(noise=False):
    devices = [
        ProbeDevice(i, lattice, 3, 1, center, 16, 0, False, 0, False, np.arange(slots))
        for i, (lattice, center, slots) in enumerate((("square", [8.5, 8.5], 13), ("hex", [3.5, 3.5], 19)))
    ]
    state = dict(F=np.zeros((2, 16, 16)), t_step=0, dt=0.02, dx=1.0, rng=np.random.default_rng(42))
    calls = []
    yy, xx = np.mgrid[:16, :16] + 0.5

    def step(sim, count, injections):
        calls.append((sim["t_step"], count, deepcopy(injections)))
        for _ in range(count):
            for source in injections:
                dy = (yy - source["y"] + 8) % 16 - 8
                dx = (xx - source["x"] + 8) % 16 - 8
                sim["F"][source["field"]] += source["amp"] * 0.02 * np.exp(-(dx**2 + dy**2) / 8)
            if noise:
                sim["F"] += sim["rng"].normal(0, 0.001, sim["F"].shape)
            sim["t_step"] += 1

    oracle = R6.OracleRunner(_template=state, _devices=devices, _port_perm=[1, 0], _adjust_mix=np.eye(3), _stepper=step)
    return oracle, calls


def observe(oracle, actions, times=(0, 0.02, 0.04), n=1):
    return oracle.sample_truth(
        actions,
        [dict(sensor="device0", t=list(times)), dict(sensor="device1", t=list(times))],
        n_samples=n,
        truth_seed=17,
    )["samples"]


def emitted(calls):
    return [source for _, _, sources in calls for source in sources]


@pytest.mark.parametrize("device,center", [(0, [8.5, 8.5]), (1, [3.5, 3.5])])
def test_each_source_is_at_its_sensor_center(device, center):
    oracle, calls = toy()
    arrays = observe(oracle, [pulse(device=device)])
    assert all([s["y"], s["x"]] == center for s in emitted(calls))
    # Slot zero is the center in this fixture; native interpolation samples that cell.
    assert arrays[device][0, 1, 0, 0] == pytest.approx(0.02)
    assert arrays[device][0, 2, 0, 0] == pytest.approx(0.04)
    assert np.max(arrays[device][0, 2, 0]) == pytest.approx(0.04)
    assert np.all(arrays[device][:, :, 1] == 0)  # only the selected anonymous port


def test_move_mid_pulse_does_not_drag_forcing_and_next_pulse_uses_new_center():
    oracle, calls = toy()
    observe(oracle, [pulse(dur=0.08), move(t=0.02), pulse(t=0.08)], times=(0.02, 0.04, 0.08, 0.1))
    old = [s for tick, _, sources in calls if tick < 4 for s in sources]
    new = [s for tick, _, sources in calls if tick >= 4 for s in sources]
    assert old and new
    assert all([s["y"], s["x"]] == [8.5, 8.5] for s in old)
    assert all([s["y"], s["x"]] == [9.5, 8.5] for s in new)


@pytest.mark.parametrize("move_first,center", [(False, [8.5, 8.5]), (True, [9.5, 8.5])])
def test_equal_time_order_selects_launch_location(move_first, center):
    oracle, calls = toy()
    actions = [move(), pulse()] if move_first else [pulse(), move()]
    arrays = observe(oracle, actions)
    assert all([s["y"], s["x"]] == center for s in emitted(calls))
    assert np.all(arrays[0][:, 0] == 0)  # launch precedes the next field update


def test_both_instruments_can_move_and_inject_simultaneously():
    oracle, calls = toy()
    observe(oracle, [move(), move(device=1), pulse(), pulse(device=1, port=1, dur=0.02)])
    assert len(calls[0][2]) == 2
    assert [(s["y"], s["x"]) for s in calls[0][2]] == [(9.5, 8.5), (4.5, 3.5)]
    assert len(calls[1][2]) == 1  # device1's pulse ended, device0 continues
    assert calls[1][2][0]["field"] == 1


@pytest.mark.parametrize(
    "actions",
    [
        [pulse(), pulse(t=0.02)],
        [move(), move(t=0.02)],
        [pulse(amp=0), pulse(t=0.02)],
        [move(u=(0, 0, 0)), move(t=0.02)],
    ],
)
def test_same_component_conflicts_reject_before_physics(actions):
    oracle, calls = toy()
    with pytest.raises(R6.ProtocolError, match="overlapping"):
        observe(oracle, actions)
    assert calls == []


def test_adjacent_pulses_replace_cleanly_at_half_open_endpoint():
    oracle, calls = toy()
    arrays = observe(oracle, [pulse(dur=0.02), pulse(t=0.02, amp=2, dur=0.02)])
    assert arrays[0][0, 1, 0, 0] == pytest.approx(0.02)
    assert arrays[0][0, 2, 0, 0] == pytest.approx(0.06)
    assert [source["amp"] for source in emitted(calls)] == [1, 2]


def test_dilation_preserves_source_center_and_move_wraps_periodically():
    oracle, calls = toy()
    oracle._devices[0].center[:] = [15.5, 8.5]
    observe(oracle, [move(u=(1, 0, 1)), pulse()])
    assert all([s["y"], s["x"]] == [0.5, 8.5] for s in emitted(calls))


def test_query_partition_and_future_actions_preserve_noise_and_prefix():
    oracle, _ = toy(noise=True)
    base = observe(oracle, [pulse(), move(t=0.02)], times=(0, 0.04), n=2)
    extra = observe(oracle, [pulse(), move(t=0.02), pulse(t=0.06, device=1)], times=(0, 0.02, 0.04, 0.08), n=3)
    for a, b in zip(base, extra):
        np.testing.assert_array_equal(a, b[:2, [0, 2]])
    for a, b in zip(base, observe(oracle, [pulse(), move(t=0.02)], times=(0, 0.04), n=2)):
        np.testing.assert_array_equal(a, b)


@pytest.mark.parametrize("device", [None, True, -1, 2, 0.0])
def test_device_selection_is_explicit_and_strict(device):
    oracle, calls = toy()
    action = pulse(device=device)
    if device is None:
        del action["device"]
    with pytest.raises(R6.ProtocolError):
        observe(oracle, [action])
    assert calls == []


def test_public_service_and_validation_share_new_grammar_and_limits():
    oracle, _ = toy()
    roster = scoring.PublicRoster(n_ports=2)
    service = ExperimentService(oracle, roster=roster)
    actions = [pulse(), move(), pulse(device=1), move(device=1)]
    assert service.experiment(actions, [dict(sensor="device0", t=[0, 0.04])])["samples"][0].shape == (1, 2, 2, 13)
    usage = service.usage()
    for invalid in ([pulse(), pulse(t=0.02)], [move(t=48)], [pulse(t=1), pulse(t=0, device=1)]):
        with pytest.raises(scoring.EvaluationError):
            service.experiment(invalid, [dict(sensor="device0", t=[0.04])])
    assert service.usage() == usage
    for case in evaluation.public_validation_cases():
        scoring.validate_case(
            dict(id=case["name"], actions=case["actions"], queries=case["queries"]),
            roster=roster,
            limits=replace(scoring.DEFAULT_LIMITS, max_horizon_tu=50),
            allow_empty=True,
        )


def test_old_and_new_specs_and_validation_cases_do_not_mix():
    from unittest.mock import patch

    for protocol, text in [(R6.LEGACY_PROTOCOL, "fixed source location"), (R6.APPARATUS_PROTOCOL, "center")]:
        roster = scoring.PublicRoster(protocol=protocol)
        with patch.object(taskset, "public_roster", return_value=roster):
            assert text in taskset.public_prompt(taskset.R6ToolsConfig())
        cases = evaluation.public_validation_cases(protocol)
        for case in cases:
            scoring.validate_case(
                dict(id=case["name"], actions=case["actions"], queries=case["queries"]), roster=roster, allow_empty=True
            )
        other = scoring.PublicRoster(
            protocol=R6.APPARATUS_PROTOCOL if protocol == R6.LEGACY_PROTOCOL else R6.LEGACY_PROTOCOL
        )
        with pytest.raises(scoring.EvaluationError):
            scoring.validate_case(
                dict(id="wrong", actions=cases[5]["actions"], queries=cases[5]["queries"]), roster=other
            )


def test_native_step_receives_two_centered_sources_before_field_evolution():
    """One 0.02-tu integration step on a tiny grid; not a science rollout."""
    from blobkit import genome
    from blobkit.soup import sim_cpu
    from physim.devices import INJ_SIGMA, step_chunk

    state = sim_cpu.init_soup(genome.ref_BFIELD(), L=8, n_soup=0, seed=1, noise=0, workers=1)
    devices = [
        ProbeDevice(i, lattice, 3, 0.5, center, 8, 0, False, 0, False, np.arange(slots))
        for i, (lattice, center, slots) in enumerate((("square", [2.25, 2.25], 13), ("hex", [5.25, 5.25], 19)))
    ]
    perm = [2, 0, 3, 1]
    oracle = R6.OracleRunner(
        _template=state, _devices=devices, _port_perm=perm, _adjust_mix=np.eye(3), _stepper=step_chunk
    )
    actions = [pulse(port=1, amp=0.2, dur=0.02), move(), pulse(device=1, port=2, amp=0.1, dur=0.02)]
    actual = oracle.sample_truth(actions, [dict(sensor="global", t=[0.02])], n_samples=1, truth_seed=4)["samples"][0]
    expected = deepcopy(state)
    # Directly deposit the known pulses at their launch positions, then evolve once.
    # device0 moves after launching, so its expected deposit remains at 2.25.
    for field, center, amp in [(0, 2.25, 0.2), (3, 5.25, 0.1)]:
        expected["F"] = genome.poke(
            expected["F"], expected["g"], field, center, center, amp * 0.02, INJ_SIGMA, expected["dx"]
        )
    step_chunk(expected, 1)
    fields = expected["F"][perm]
    np.testing.assert_array_equal(actual[0, 0], np.stack((fields.mean((1, 2)), fields.var((1, 2))), axis=1))
