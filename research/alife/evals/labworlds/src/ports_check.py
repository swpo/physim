"""Checks for LabOracleRunner (physim/labworld.py): actuators apart from observed ports.

    parity_lab     phase_membrane (runner_demo.py declaration): the pre-extension OracleRunner on
                   LabStepper, LabOracleRunner from oracle(), and LabOracleRunner.wrap(OracleRunner)
                   return bit-identical samples, also with a permuted port order and a non-trivial
                   adjustment map, raise identical protocol errors, and reproduce the demo's saved
                   forecast members
    parity_native  the same comparison on a native Blobkit world (packaged BF genome, init_soup,
                   devices.step_chunk), plus a short '-' pulse through genome.poke
    signed         fed vortices (vortex_demo.py declaration) with actuators (om,+), (om,-), (Y,+):
                   amp 3 for 50 tu at each device centre, every-1-tu readouts, finite and signed
    observe        an observe-only speed channel |u| riding in F: returned by every sensor, does not
                   perturb the dynamical channels, matches |u| recomputed from the state, and is
                   rejected as an inject target (declaration, runner and request level)

Usage: python ports_check.py CMD [--out DIR]   (OMP_NUM_THREADS=1 is set here; one command at a time)
"""

from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import copy
import dataclasses
import importlib.util
import json
import resource
import sys
import time
from pathlib import Path

import numpy as np

ENV = Path(__file__).resolve().parents[3] / "environments" / "physim"
sys.path.insert(0, str(ENV))
from physim import blobround6 as R6  # noqa: E402
from physim import labworld as LW  # noqa: E402
from physim.devices import ProbeDevice, step_chunk  # noqa: E402

EVALPILOT = Path("/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot")
SENSORS = ("device0", "device1", "global")


def demo(name):
    """The scratchpad demo module (its prepared states live next to it in out/)."""
    spec = importlib.util.spec_from_file_location(name, EVALPILOT / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def one_worker(module):
    if hasattr(module, "ops") and hasattr(module.ops, "WORKERS"):
        module.ops.WORKERS = 1


def cpu():
    r = resource.getrusage(resource.RUSAGE_SELF)
    return r.ru_utime + r.ru_stime


def identical(a, b):
    """Bitwise equality of two sample payloads (lists of float64 arrays)."""
    return len(a) == len(b) and all(
        x.shape == y.shape and x.dtype == y.dtype and x.tobytes() == y.tobytes() for x, y in zip(a, b)
    )


def max_abs(a, b):
    return float(max(np.abs(x - y).max() for x, y in zip(a, b)))


def errors(runner, requests):
    out = []
    for actions, queries in requests:
        try:
            runner.sample_truth(actions, queries, 1, truth_seed=0)
            out.append("accepted")
        except R6.ProtocolError as e:
            out.append(f"ProtocolError: {e}")
    return out


INVALID = [
    ([dict(t=0.0, kind="inject", device=0, port=4, amp=1.0, dur=1.0)], [dict(sensor="global", t=[1.0])]),
    ([dict(t=0.0, kind="inject", device=0, port=0, amp=-1.0, dur=1.0)], [dict(sensor="global", t=[1.0])]),
    ([dict(t=0.0, kind="inject", device=0, port=0, amp=1.0, dur=51.0)], [dict(sensor="global", t=[1.0])]),
    ([dict(t=0.01, kind="inject", device=0, port=0, amp=1.0, dur=1.0)], [dict(sensor="global", t=[1.0])]),
    (
        [
            dict(t=0.0, kind="inject", device=0, port=0, amp=1.0, dur=2.0),
            dict(t=1.0, kind="inject", device=0, port=1, amp=1.0, dur=1.0),
        ],
        [dict(sensor="global", t=[1.0])],
    ),
    ([dict(t=0.0, kind="inject", device=0, port=True, amp=1.0, dur=1.0)], [dict(sensor="global", t=[1.0])]),
    ([], [dict(sensor="device2", t=[1.0])]),
]


def rich_request(n_ports, horizon):
    """Pulses on every port at both devices, moves, a zero-amplitude (ineffective) pulse, equal-time
    actions in list order, a one-tick pulse, and readouts at t=0 and around pulse boundaries."""
    h = float(horizon)
    actions = [
        dict(t=0.0, kind="inject", device=0, port=0, amp=3.0, dur=0.2 * h),
        dict(t=0.0, kind="adjust", device=1, u=[0.5, -0.3, 0.2]),
        dict(t=0.1 * h, kind="inject", device=1, port=n_ports - 1, amp=1.5, dur=0.3 * h),
        dict(t=0.2 * h, kind="inject", device=0, port=min(2, n_ports - 1), amp=0.0, dur=0.1 * h),
        dict(t=0.25 * h, kind="adjust", device=0, u=[-1.0, 1.0, -0.5]),
        dict(t=0.3 * h, kind="inject", device=0, port=1 % n_ports, amp=2.0, dur=0.15 * h),
        dict(t=0.5 * h, kind="inject", device=1, port=0, amp=3.0, dur=0.5 * h),
        dict(t=0.5 * h, kind="adjust", device=1, u=[0.0, 0.7, 0.0]),
        dict(t=0.6 * h, kind="inject", device=0, port=n_ports - 1, amp=0.7, dur=0.02),
    ]
    edges = [0.0, 0.02, 0.2 * h - 0.02, 0.2 * h, 0.2 * h + 0.02, 0.5 * h, 0.6 * h + 0.02, h]
    queries = [
        dict(sensor="device0", t=[round(t, 2) for t in edges]),
        dict(sensor="device1", t=[0.0, 0.25 * h, 0.5 * h, h]),
        dict(sensor="global", t=[0.0, 0.125 * h, 0.375 * h, h]),
    ]
    return actions, queries


MIX = np.array([[0.8, -0.6, 0.1], [0.6, 0.8, -0.2], [0.0, 0.1, 0.5]])


# ----------------------------------------------------------------------------- (a) lab world


def parity_lab(args):
    rd = demo("runner_demo")
    s0, info = rd.prepared()
    fields = rd.FIELDS
    w = rd.world({f: 0.01 for f in fields}, None, 0.01)
    rows = {}

    def legacy(perm, mix):
        """The pre-extension labworld.oracle(): OracleRunner on LabStepper."""
        stepper = LW.LabStepper(w, dict(w.aux(s0), _grid=s0[fields[0]].shape))
        return R6.OracleRunner(
            _template=LW.template(w, s0),
            _devices=rd.devices(info),
            _port_perm=perm,
            _adjust_mix=mix,
            _stepper=stepper,
        )

    # 1. runner_demo's pulseK program, 50 tu, every 1 tu, identity ports: three runners and the saved forecast
    times = [float(t) for t in np.arange(1, 51)]
    q = [dict(sensor=s, t=times) for s in SENSORS]
    act = [dict(t=5.0, kind="inject", device=0, port=1, amp=3.0, dur=10.0)]
    base = legacy(np.arange(4), np.eye(3))
    runners = {
        "OracleRunner": base,
        "LabOracleRunner(oracle)": LW.oracle(w, s0, rd.devices(info)),
        "LabOracleRunner.wrap": LW.LabOracleRunner.wrap(base),
    }
    out, secs = {}, {}
    for name, r in runners.items():
        c0 = cpu()
        out[name] = r.sample_truth(act, q, args.members, truth_seed=101)["samples"]
        secs[name] = round(cpu() - c0, 1)
    z = np.load(EVALPILOT / "out" / "runner_demo_pulseK_samples.npz")
    saved = [z[f"forecast_{g}"][: args.members] for g in SENSORS]
    ref = out["OracleRunner"]
    rows["demo_pulseK_50tu"] = dict(
        members=args.members,
        cpu_s=secs,
        identical_to_OracleRunner={k: identical(ref, v) for k, v in out.items() if k != "OracleRunner"},
        OracleRunner_vs_saved_demo_forecast=dict(identical=identical(ref, saved), max_abs=max_abs(ref, saved)),
        LabOracleRunner_vs_saved_demo_forecast=identical(out["LabOracleRunner(oracle)"], saved),
        shapes=[list(a.shape) for a in ref],
    )
    print(json.dumps(rows["demo_pulseK_50tu"]), flush=True)

    # 2. rich program, permuted ports and a non-trivial adjustment map
    perm = np.array([2, 0, 3, 1])
    actions, queries = rich_request(4, args.horizon)
    base = legacy(perm, MIX)
    runners = {
        "OracleRunner": base,
        "LabOracleRunner(oracle)": LW.oracle(w, s0, rd.devices(info), port_perm=perm, adjust_mix=MIX),
        "LabOracleRunner.wrap": LW.LabOracleRunner.wrap(base),
    }
    out = {}
    for name, r in runners.items():
        out[name] = r.sample_truth(actions, queries, args.members + 1, truth_seed=9)["samples"]
    ref = out["OracleRunner"]
    rows["rich_permuted"] = dict(
        members=args.members + 1,
        horizon_tu=args.horizon,
        port_perm=perm.tolist(),
        identical_to_OracleRunner={k: identical(ref, v) for k, v in out.items() if k != "OracleRunner"},
        members_differ=bool(not np.array_equal(ref[0][0], ref[0][1])),
        actions=actions,
        queries=queries,
    )
    errs = {name: errors(r, INVALID) for name, r in runners.items()}
    rows["protocol_errors"] = dict(
        identical=all(e == errs["OracleRunner"] for e in errs.values()), messages=errs["OracleRunner"]
    )
    print(json.dumps({k: v for k, v in rows["rich_permuted"].items() if k not in ("actions", "queries")}), flush=True)
    print(json.dumps(rows["protocol_errors"]), flush=True)
    rows["cpu_s_total"] = round(cpu(), 1)
    (args.out / "parity_lab.json").write_text(json.dumps(rows, indent=1) + "\n")


# ----------------------------------------------------------------------------- (a) native Blobkit world


def native_runner(seed):
    """eval_preparation.make_oracle's native binding on a fresh BF soup (no hidden preparation)."""
    from blobkit import worlds
    from blobkit.soup import sim_cpu

    genome = worlds.load("bf")
    state = sim_cpu.init_soup(genome, L=128.0, seed=seed, workers=1, noise=0.002)
    y, x = np.unravel_index(np.argmax(state["F"][0]), state["F"][0].shape)
    center = (np.array([y, x]) + 0.5) * 0.5
    rng = np.random.default_rng(41001)
    devices = [
        ProbeDevice(i, lattice, 3, spacing, center + 12.0 * i, 128.0, 0.0, False, 0.0, False, rng.permutation(k))
        for i, (lattice, spacing, k) in enumerate((("square", 3.0, 13), ("hex", 6.0, 19)))
    ]
    return R6.OracleRunner(
        _template=state, _devices=devices, _port_perm=[2, 0, 3, 1], _adjust_mix=MIX, _stepper=step_chunk
    ), genome


def parity_native(args):
    rows = {}
    try:
        R6._native_oracle("bf", 0)
        rows["blobround6._native_oracle"] = "ran"
    except ImportError as e:
        rows["blobround6._native_oracle"] = f"unavailable: {type(e).__name__}: {e}"
    base, genome = native_runner(args.seed)
    n = len(base._perm)
    rows["world"] = dict(genome=genome.get("id", "bf"), n_ports=n, grid=list(base._template["F"].shape))
    actions, queries = rich_request(n, args.horizon)
    runners = {
        "OracleRunner": base,
        "LabOracleRunner.wrap": LW.LabOracleRunner.wrap(base),
        "LabOracleRunner(direct)": LW.LabOracleRunner(
            _template=base._template,
            _devices=base._devices,
            _port_perm=[2, 0, 3, 1],
            _adjust_mix=MIX,
            _stepper=step_chunk,
        ),
    }
    out, secs = {}, {}
    for name, r in runners.items():
        c0 = cpu()
        out[name] = r.sample_truth(actions, queries, args.members, truth_seed=11)["samples"]
        secs[name] = round(cpu() - c0, 1)
    ref = out["OracleRunner"]
    rows["rich_permuted"] = dict(
        members=args.members,
        horizon_tu=args.horizon,
        cpu_s=secs,
        identical_to_OracleRunner={k: identical(ref, v) for k, v in out.items() if k != "OracleRunner"},
        members_differ=bool(not np.array_equal(ref[0][0], ref[0][1])),
    )
    print(json.dumps(rows["rich_permuted"]), flush=True)
    errs = {name: errors(r, INVALID) for name, r in runners.items()}
    rows["protocol_errors"] = dict(identical=all(e == errs["OracleRunner"] for e in errs.values()))
    # a '-' actuator on activator row 0 through genome.poke (not part of the identity check)
    signed = LW.LabOracleRunner.wrap(base, actuators=[(0, 1), (0, -1)])
    q = [dict(sensor="global", t=[0.0, 2.0])]
    res = {}
    for label, act in (
        ("sham", []),
        ("plus", [dict(t=0.0, kind="inject", device=0, port=0, amp=3.0, dur=2.0)]),
        ("minus", [dict(t=0.0, kind="inject", device=0, port=1, amp=3.0, dur=2.0)]),
    ):
        res[label] = signed.sample_truth(act, q, 1, truth_seed=3)["samples"][0][0, 1, :, 0]
    row0 = int(np.where(np.asarray(base._perm) == 0)[0][0])  # public observed port that reads F row 0
    rows["native_signed_row0_global_mean_delta_at_2tu"] = dict(
        observed_port=row0,
        plus=float(res["plus"][row0] - res["sham"][row0]),
        minus=float(res["minus"][row0] - res["sham"][row0]),
        expected_first_order=float(3.0 * 2.0 * 2 * np.pi * 2.0**2 / 128.0**2),
    )
    print(json.dumps(rows["native_signed_row0_global_mean_delta_at_2tu"]), flush=True)
    rows["cpu_s_total"] = round(cpu(), 1)
    (args.out / "parity_native.json").write_text(json.dumps(rows, indent=1) + "\n")


# ----------------------------------------------------------------------------- (b) signed vorticity


def vortex(actuators=None, derived=()):
    vd = demo("vortex_demo")
    s, info = vd.prepared()
    w = dataclasses.replace(
        vd.world({"om": 0.01, "Y": 0.1}, None, noise=0.003), actuators=actuators, derived=tuple(derived)
    )
    o = LW.oracle(w, s, vd.devices(info))
    one_worker(o._stepper.module)
    return o, w, s, info


PM = (LW.Actuator("om", 1), LW.Actuator("om", -1), LW.Actuator("Y", 1))


def signed(args):
    o, w, s, info = vortex(PM)
    default, *_ = vortex(None)
    rows = dict(actuators=[dataclasses.asdict(a) for a in PM], gain=w.ports["om"].gain, noise=w.noise)
    times = [0.02] + [float(t) for t in np.arange(1, 51)]
    q = [dict(sensor=x, t=times) for x in SENSORS]
    c0 = cpu()
    sham = o.sample_truth([], q, 1, truth_seed=5)["samples"]
    # parity of the +/- roster's sham with the default-roster oracle and with the saved demo forecast
    vz = np.load(EVALPILOT / "out" / "vortex_demo_sham_samples.npz")
    saved = [vz[f"forecast_{g}"][:1] for g in SENSORS]
    fc = o.sample_truth(
        [], [dict(sensor=x, t=[float(t) for t in np.arange(1, 51)]) for x in SENSORS], 1, truth_seed=101
    )
    rows["sham_vs_saved_demo_forecast_member0"] = identical(fc["samples"], saved)
    for dev in (0, 1):
        res = {}
        for label, port in (("plus", 0), ("minus", 1)):
            act = [dict(t=0.0, kind="inject", device=dev, port=port, amp=3.0, dur=50.0)]
            res[label] = o.sample_truth(act, q, 1, truth_seed=5)["samples"]
        old = default.sample_truth(
            [dict(t=0.0, kind="inject", device=dev, port=0, amp=3.0, dur=50.0)], q, 1, truth_seed=5
        )
        d = f"device{dev}"
        g = SENSORS.index(d)
        centre = {
            k: v[g][0, :, 0, 0] for k, v in dict(sham=sham, **res).items()
        }  # node 0 = ring 0 (identity node_perm)
        probe_om = {k: v[g][0, :, 0, :] for k, v in dict(sham=sham, **res).items()}
        gmean = {k: v[2][0, :, 0, 0] for k, v in dict(sham=sham, **res).items()}
        gvar = {k: v[2][0, :, 0, 1] for k, v in dict(sham=sham, **res).items()}
        tick1 = {k: float(centre[k][0] - centre["sham"][0]) for k in ("plus", "minus")}
        rows[f"pulse_at_{d}"] = dict(
            finite_all_readouts=bool(all(np.isfinite(a).all() for v in res.values() for a in v)),
            plus_identical_to_default_roster_port0=identical(res["plus"], old["samples"]),
            centre_om_at=dict(
                t=[times[i] for i in (0, 10, 25, 50)],
                **{k: [round(float(centre[k][i]), 4) for i in (0, 10, 25, 50)] for k in centre},
            ),
            first_tick_centre_delta=dict(tick1, ratio_minus_over_plus=tick1["minus"] / tick1["plus"]),
            expected_first_tick_delta=0.01 * 3.0 * 0.02,
            probe_om_min_max={k: [round(float(v.min()), 4), round(float(v.max()), 4)] for k, v in probe_om.items()},
            global_mean_om_delta_at=dict(
                t=[times[i] for i in (10, 25, 50)],
                **{k: [float(gmean[k][i] - gmean["sham"][i]) for i in (10, 25, 50)] for k in ("plus", "minus")},
            ),
            global_var_om_at_50={k: round(float(v[-1]), 5) for k, v in gvar.items()},
        )
        print(json.dumps(rows[f"pulse_at_{d}"]), flush=True)
        np.savez_compressed(
            args.out / f"signed_{d}.npz",
            times=np.array(times),
            **{f"{k}_{x}": v[i] for k, v in dict(sham=sham, **res).items() for i, x in enumerate(SENSORS)},
        )
    # the fields themselves after 50 tu of the '-' pulse at device0 (stepper driven exactly as the runner does)
    c = o._devices[0].center
    snaps = {}
    for label, amp in (("sham", 0.0), ("minus", -3.0)):
        sim = R6._clone_sim(o._template)
        sim["rng"] = np.random.default_rng(R6._truth_member_seed(5, 0))
        inj = [dict(field=0, y=float(c[0]), x=float(c[1]), amp=amp)] if amp else []
        o._stepper(sim, 2500, injections=inj)
        snaps[label] = sim["F"]
    readout = o._sample(dict(F=snaps["minus"], dx=1.0), o._devices, "device0")
    runner = np.load(args.out / "signed_device0.npz")["minus_device0"][0, -1]
    rows["direct_stepper_snapshot_matches_runner_readout_at_50"] = bool(np.array_equal(readout, runner))
    np.savez_compressed(args.out / "signed_fields_50tu.npz", centre=c, **{k: v[0] for k, v in snaps.items()})
    rows["field_om_min_max_50tu"] = {k: [float(v[0].min()), float(v[0].max())] for k, v in snaps.items()}
    rows["cpu_s_total"] = round(cpu() - c0, 1)
    (args.out / "signed.json").write_text(json.dumps(rows, indent=1) + "\n")


# ----------------------------------------------------------------------------- (c) observe-only channel


def vortex_speed(module, state):
    """|u| of the flow the module advects with (zero when adv=0)."""
    uy, ux = module._vel(state)
    return state["par"]["adv"] * np.hypot(uy, ux)


def observe(args):
    speed = LW.Derived("speed", vortex_speed)
    o, w, s, info = vortex(PM, (speed,))
    plain, *_ = vortex(PM)
    rows = dict(
        observed=list(w.observed),
        n_observed=o.n_observed,
        n_actuators=o.n_actuators,
        declaration_derived=w.declaration()["derived"],
    )
    c0 = cpu()
    q = [dict(sensor=x, t=[0.0, 1.0, 5.0, 10.0]) for x in SENSORS]
    act = [dict(t=0.0, kind="inject", device=0, port=1, amp=3.0, dur=5.0)]
    with_speed = o.sample_truth(act, q, 2, truth_seed=7)["samples"]
    without = plain.sample_truth(act, q, 2, truth_seed=7)["samples"]
    rows["shapes"] = [list(a.shape) for a in with_speed]
    rows["dynamical_channels_identical_without_derived"] = identical([a[:, :, :2] for a in with_speed], without)
    sp = [a[:, :, 2] for a in with_speed]
    rows["speed_channel"] = dict(
        finite=bool(all(np.isfinite(a).all() for a in sp)),
        nonnegative_probe_values=bool((sp[0] >= 0).all() and (sp[1] >= 0).all()),
        device0_centre_member0=[round(float(v), 5) for v in sp[0][0, :, 0]],
        global_mean_member0=[round(float(v), 5) for v in sp[2][0, :, 0]],
        global_var_member0=[round(float(v), 7) for v in sp[2][0, :, 1]],
    )
    # t=0: the template's speed row equals |u| from the prepared state; after 50 ticks it equals |u| from the
    # stepper's state (fields from F, the rest from the per-member aux)
    module = o._stepper.module
    st0 = dict(copy.deepcopy(s))
    rows["t0_speed_row_equals_prepared_state_speed"] = bool(
        np.array_equal(o._template["F"][2], vortex_speed(module, st0))
    )
    sim = R6._clone_sim(o._template)
    sim["rng"] = np.random.default_rng(1)
    o._stepper(sim, 50)
    state = dict(sim["_lab_aux"], om=sim["F"][0], Y=sim["F"][1])
    rows["t1_speed_row_equals_recomputed_speed"] = bool(np.array_equal(sim["F"][2], vortex_speed(module, state)))
    rows["t1_speed_field_mean_max"] = [float(sim["F"][2].mean()), float(sim["F"][2].max())]
    # rejection as an inject target
    rej = {}
    try:
        dataclasses.replace(w, actuators=(LW.Actuator("speed", 1),))
        rej["declaration Actuator('speed')"] = "accepted"
    except ValueError as e:
        rej["declaration Actuator('speed')"] = f"ValueError: {e}"
    try:
        LW.LabOracleRunner.wrap(o, actuators=[(2, 1)], observe_only=[2])
        rej["runner _actuators=[(2, +1)] with row 2 observe-only"] = "accepted"
    except ValueError as e:
        rej["runner _actuators=[(2, +1)] with row 2 observe-only"] = f"ValueError: {e}"
    gq = [dict(sensor="global", t=[1.0])]
    rej["request port 3 on roster (om+, om-, Y+)"] = errors(
        o, [([dict(t=0.0, kind="inject", device=0, port=3, amp=1.0, dur=1.0)], gq)]
    )[0]
    try:
        vortex(None, (speed,))
        rej["default roster with an observe-only row"] = "accepted"
    except ValueError as e:
        rej["default roster with an observe-only row"] = f"ValueError: {e}"
    rows["rejections"] = rej
    rows["cpu_s_total"] = round(cpu() - c0, 1)
    print(json.dumps(rows, indent=1), flush=True)
    (args.out / "observe.json").write_text(json.dumps(rows, indent=1) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["parity_lab", "parity_native", "signed", "observe"])
    ap.add_argument("--out", type=Path, default=EVALPILOT / "ports")
    ap.add_argument("--members", type=int, default=2)
    ap.add_argument("--horizon", type=float, default=20.0)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    {"parity_lab": parity_lab, "parity_native": parity_native, "signed": signed, "observe": observe}[a.cmd](a)
    print(f"{a.cmd}: wall {time.time() - t0:.1f} s, cpu {cpu():.1f} s", flush=True)
