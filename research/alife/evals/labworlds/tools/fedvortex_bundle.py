"""c53's fed vortices as a PhySim lab bundle: preparation, frozen suite, truths, controls and checks.

    python fedvortex_bundle.py build    --out BUNDLE [--work WORK]   inputs, calibration, frozen suite, truths, manifest
    python fedvortex_bundle.py controls --out BUNDLE --work WORK --worker K --workers N   (cached; resumable)
    python fedvortex_bundle.py report   --out BUNDLE --work WORK      per-case and aggregate ratios, reward

World: collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py (copied verbatim with labkit's
modules into the bundle). Declaration: 128^2, dx 1, native dt 0.02, one native step per public tick;
dynamics noise by intensity 0.003 with a 2-world-unit correlation length (vorticity additive, fuel
proportional). Observed ports: vorticity, fuel, eating rate and flow speed (the last two observe-only).
Actuators: (om,+), (om,-), (Y,+), (Y,-); gains 0.01 (om) and 0.1 (Y, clipped at 0) from the envelope
test (amp 3 for 50 tu at the worst site: om within [-0.33, 0.40], Y within [0, 2.4], finite).

Preparation: init(31) run to t=580 under the declared noise (generator seeded [7331, 31]). Device 0
(square, 13 nodes) sits on the neck of a vortex rod that pinches into two same-sign daughters at about
t=23 of the window; device 1 (hex, 19 nodes) on a round positive vortex that drifts about 12 world units
in 50 tu. Adjustment matrix diag(3, 3, 1): one unit of u moves a device 3 world units.

Suite: 15 programs (8 PhySim-style generic, 7 mechanism-targeted), queries at PhySim's 15 times on both
devices and the global sensor; one score group per (sensor, observed port) with scales frozen from a
calibration ensemble (seeds 51000 + k) before any truth; 2 truths per case (71000 + i).
Controls (privileged, outside the bundle): a 64-member native reference (81000 + i; 16 independent
4-member slices give the native band), ignore actions, wrong probe geometry, initial persistence,
mechanism ablations and the dt-halved numerical null (82000 + i).
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import dataclasses
import json
import shutil
import sys
import time
from pathlib import Path

import numpy as np

ENV = Path(__file__).resolve().parents[3] / "environments" / "physim"
sys.path.insert(0, str(ENV))
from physim import blobround6 as R6  # noqa: E402
from physim import blobround6_eval as scoring  # noqa: E402
from physim import labbundle as LB  # noqa: E402
from physim import labworld as LW  # noqa: E402
from physim.bundles import digest, identified  # noqa: E402
from physim.devices import ProbeDevice  # noqa: E402

HERE = Path(__file__).resolve().parent
LAB = Path("/home/user/physim/research/alife")
WORLD_SRC = LAB / "collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py"
LABKIT_SRC = [LAB / "labkit" / n for n in ("__init__.py", "ops.py", "world.py")]
OBS_SRC = HERE / "fedvortex" / "observables.py"
ABLATIONS = HERE / "fedvortex" / "ablations.py"

PREP = dict(seed=31, noise_seed=7331, T=580.0)
SITES = dict(device0=[91.4, 122.1], device1=[112.0, 79.3])
PORT_PERMUTATION = [2, 0, 3, 1]                       # observed port p reads F row perm[p]: eat, om, speed, Y
ACTUATORS = [("om", -1), ("Y", 1), ("om", 1), ("Y", -1)]   # public inject ports 0..3
ACT = {"om-": 0, "Y+": 1, "om+": 2, "Y-": 3}
ROWS = ["om", "Y", "eat", "speed"]
MIX = [[3.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 1.0]]
TIMES = [0, 2, 5, 8, 10, 12, 15, 20, 22, 25, 30, 35, 40, 45, 50]
SCORE_TIMES = [2, 5, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50]
SENSORS = ("device0", "device1", "global")
FLOOR_FRAC = 0.02
CAL_SEED, TRUTH_SEED, FORECAST_SEED, IGNORE_SEED, NULL_SEED = 51000, 71000, 81000, 80999, 82000
REF_MEMBERS, CONTROL_MEMBERS, SLICE = 64, 4, 4
# Device-1 vortex path in the native sham (world units, every 5 tu); the follow program tracks it.
FOLLOW_PATH = [[112.0, 79.3], [110.9, 79.9], [109.9, 80.5], [108.9, 81.3], [108.2, 82.1], [107.3, 83.1],
               [106.5, 83.8], [105.8, 84.7], [105.0, 85.7], [104.4, 86.7], [103.9, 87.8]]


def declaration():
    return dict(
        name="c53-fed-vortices", world_file="world.py", fields=["om", "Y"], grid=[128, 128],
        steps_per_tick=1, native_dt=0.02,
        ports={"om": dict(gain=0.01, clip=[None, None]), "Y": dict(gain=0.1, clip=[0.0, None])},
        noise={"om": ["additive", 0.003], "Y": ["proportional", 0.003]},
        noise_corr={"om": 2.0, "Y": 2.0}, noise_intensity=["om", "Y"], overrides={}, dx=1.0, carry=["t"],
        actuators=[dict(field=f, sign=s) for f, s in ACTUATORS],
        derived=[dict(name="eat", source="observables.py", function="eat"),
                 dict(name="speed", source="observables.py", function="speed")],
        fft_workers=1,
    )


def apparatus():
    rng = np.random.default_rng(41031)
    devices = []
    for i, (lattice, ds, rot, k) in enumerate((("square", 3.0, 0.3, 13), ("hex", 6.0, 1.1, 19))):
        perm = rng.permutation(k).tolist()
        d = ProbeDevice(i, lattice, 3, ds, SITES[f"device{i}"], 128.0, rot, False, 0.0, False, perm)
        devices.append(dict(parameters=dict(dev_id=i, lattice=lattice, n_rings=3, base_ds=ds, center=SITES[f"device{i}"],
                                            L=128.0, secret_rot=rot, reflect=False, motion_theta=0.0, motion_reflect=False,
                                            node_perm=perm, dil_bounds=list(d.dil_bounds)),
                            dilation=1.0, motion_basis=d.Bm.tolist()))
    return dict(devices=devices, device_slots=[13, 19], port_permutation=PORT_PERMUTATION, adjustment_matrix=MIX,
                protocol=R6.APPARATUS_PROTOCOL)


# ----------------------------------------------------------------------------- programs

def _inject(t, device, act, amp, dur):
    return dict(t=t, kind="inject", device=device, port=ACT[act], amp=amp, dur=dur)


def _adjust(t, device, u):
    return dict(t=t, kind="adjust", device=device, u=[round(float(x), 3) for x in u])


def follow_actions():
    p = np.asarray(FOLLOW_PATH)
    u = [(p[1] - p[0]) / 6] + [(p[k + 1] - p[k - 1]) / 6 for k in range(1, 10)]
    return [_adjust(5 * k, 1, [u[k][0], u[k][1], 0.0]) for k in range(10)]


def programs():
    """(id, actions, kind, mechanism). Generic programs follow eval_preparation's BF/XV families."""
    pulse = _inject(0, 0, "om+", 3.0, 5.0)
    move = _adjust(0, 0, [1, 0, 0])
    arms = [
        ("sham", [], "generic", "natural pinch of the device-0 rod at ~23 tu; drift of the device-1 vortex"),
        ("probe_shift", [_adjust(0, 0, [1, 0, 0])], "generic", ""),
        ("probe_wide", [_adjust(0, 1, [0, 0, 1])], "generic", ""),
        ("pulse_then_move", [pulse, move], "generic", ""),
        ("move_then_pulse", [move, pulse], "generic", ""),
        ("two_sources", [pulse, _adjust(0, 1, [0, 1, 0]), dict(pulse, device=1)], "generic", ""),
        ("move_during_pulse", [pulse, dict(move, t=2)], "generic", ""),
        ("delayed_feed", [_inject(20, 0, "Y+", 3.0, 10.0)], "generic", "late feeding of the neck"),
        ("feed_neck", [_inject(0, 0, "Y+", 3.0, 20.0)], "targeted", "division: feeding the neck suppresses the pinch"),
        ("starve_neck", [_inject(0, 0, "Y-", 2.0, 6.0)], "targeted", "division/decay: starving the neck pinches it at ~8 tu"),
        ("feed_vortex", [_inject(0, 1, "Y+", 3.0, 25.0)], "targeted", "eating grows vorticity: circulation doubles"),
        ("starve_vortex", [_inject(0, 1, "Y-", 3.0, 10.0)], "targeted", "weak vorticity decays without fuel: vortex dies by ~25 tu"),
        ("stir_cut", [_inject(0, 1, "om-", 2.0, 8.0)], "targeted", "signed stir: partial cancellation, the remnant regrows by eating"),
        ("follow_vortex", follow_actions(), "targeted", "mutual advection: device 1 tracks its drifting vortex"),
        ("feed_and_follow", [_inject(0, 1, "Y+", 3.0, 15.0)] + follow_actions(), "targeted",
         "growth and motion together: a fed vortex tracked while it drifts"),
    ]
    return arms


def queries():
    return [dict(sensor=s, t=list(TIMES)) for s in SENSORS]


def calibration_plan():
    plan = [("sham", [], 4)]
    for device in (0, 1):
        for name in ACT:
            plan.append((f"cal_d{device}_{name}", [_inject(0, device, name, 3.0, 10.0)], 1))
    return plan


# ----------------------------------------------------------------------------- preparation

def prepare(work: Path):
    """init(seed) to T under the declared noise (generator [noise_seed, seed]); returns fields + carry."""
    path = work / "prepared_state.npz"
    if path.exists():
        with np.load(path) as z:
            return {k: z[k].copy() for k in z.files}
    decl = declaration()
    world = LW.LabWorld(path=str(WORLD_SRC), fields=("om", "Y"), steps_per_tick=1, native_dt=0.02,
                        noise={f: tuple(v) for f, v in decl["noise"].items()}, noise_corr=decl["noise_corr"],
                        noise_intensity=tuple(decl["noise_intensity"]), dx=1.0, sys_path=(str(LAB),))
    st = LW.LabStepper(world, {})
    m = st.module
    m.ops.WORKERS = 1
    s = m.init(PREP["seed"], (128, 128))
    rng = np.random.default_rng([PREP["noise_seed"], PREP["seed"]])
    for _ in range(int(round(PREP["T"] / world.native_dt))):
        s = st.add_noise(s, rng, world.native_dt)
        s = m.step(s)
    arrays = dict(om=np.asarray(s["om"], np.float64), Y=np.asarray(s["Y"], np.float64), t=np.asarray(float(s["t"])))
    np.savez_compressed(path, **arrays)
    return arrays


# ----------------------------------------------------------------------------- build

def write_json(path, value, compact=False):
    text = json.dumps(value, separators=(",", ":"), allow_nan=False) if compact else json.dumps(value, indent=1, allow_nan=False)
    Path(path).write_text(text + "\n")


def _sig(x, digits=6):
    return float(f"{x:.{digits}g}")


def _jsonable(x):
    return json.loads(json.dumps(x, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))


def oracle_from_dir(out: Path, *, world=None, devices=None):
    decl = json.loads((out / "labworld.json").read_text())
    app = json.loads((out / "apparatus.json").read_text())
    state = LB.read_state(out / "preparation.npz", decl)
    return LB.build_oracle(out, decl, app, state, world=world, devices=devices)


def ensemble(path: Path, compute, meta):
    meta = _jsonable(meta)
    if path.exists():
        with np.load(path, allow_pickle=False) as z:
            assert json.loads(str(z["meta"])) == meta, f"cached {path} was made with another request"
            return [z[f"query{i}"].copy() for i in range(len(meta["queries"]))]
    t0 = time.process_time()
    res = compute()["samples"]
    np.savez_compressed(path, meta=json.dumps(meta), cpu_s=time.process_time() - t0,
                        **{f"query{i}": a for i, a in enumerate(res)})
    print(f"  {path.parent.name}/{path.name}: {time.process_time() - t0:.1f} cpu-s", flush=True)
    return res


def frozen_scales(cal):
    ti = [TIMES.index(t) for t in SCORE_TIMES]
    g0 = cal[0][2][0, 0]                       # global (ports, 2) at t=0
    spread0 = np.sqrt(g0[:, 1])
    scales = {}
    for qi, sensor in enumerate(SENSORS):
        for p in range(len(PORT_PERMUTATION)):
            name = ROWS[PORT_PERMUTATION[p]]
            if sensor == "global":
                for slot, label, floor in ((0, "mean", spread0[p]), (1, "variance", g0[p, 1])):
                    raw = float(np.concatenate([c[qi][:, ti, p, slot].ravel() for c in cal]).std())
                    scales[f"{sensor}/{name}/{label}"] = dict(port=p, raw_std=raw, floor=float(FLOOR_FRAC * floor),
                                                              scale=_sig(max(raw, FLOOR_FRAC * floor, 1e-12)))
            else:
                raw = float(np.concatenate([c[qi][:, ti, p, :].ravel() for c in cal]).std())
                scales[f"{sensor}/{name}"] = dict(port=p, raw_std=raw, floor=float(FLOOR_FRAC * spread0[p]),
                                                  scale=_sig(max(raw, FLOOR_FRAC * spread0[p], 1e-12)))
    return scales


def score_groups(scales):
    groups = []
    for qi, sensor in enumerate(SENSORS):
        for p in range(len(PORT_PERMUTATION)):
            name = ROWS[PORT_PERMUTATION[p]]
            if sensor == "global":
                sel, sc = [], []
                for slot, label in ((0, "mean"), (1, "variance")):
                    for t in SCORE_TIMES:
                        sel.append(dict(query=qi, time_index=TIMES.index(t), port=p, slot=slot))
                        sc.append(scales[f"{sensor}/{name}/{label}"]["scale"])
                unit = f"global mean and variance of {name}; frozen calibration scales"
            else:
                k = (13, 19)[qi]
                sel = [dict(query=qi, time_index=TIMES.index(t), port=p, slot=j) for t in SCORE_TIMES for j in range(k)]
                sc = [scales[f"{sensor}/{name}"]["scale"]] * len(sel)
                unit = f"native {name} units; frozen calibration scale"
            groups.append(dict(id=f"{sensor}/{name}", selectors=sel, scales=sc, unit=unit))
    return groups


def build(out: Path, work: Path, dry: bool = False):
    out, work = out.resolve(), work.resolve()
    if (out / "manifest.json").exists():
        raise SystemExit("completed bundles are immutable; choose a new output directory")
    out.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    (out / "world" / "labkit").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(WORLD_SRC, out / "world" / "world.py")
    for src in LABKIT_SRC:
        shutil.copyfile(src, out / "world" / "labkit" / src.name)
    shutil.copyfile(OBS_SRC, out / "world" / "observables.py")
    write_json(out / "labworld.json", declaration())
    write_json(out / "apparatus.json", apparatus())
    state = prepare(work)
    if not (out / "preparation.npz").exists():
        np.savez_compressed(out / "preparation.npz", **state)
    oracle = oracle_from_dir(out)
    progs = programs()[:2] if dry else programs()
    # calibration ensemble (development seeds), then scales and groups, frozen before any truth
    (work / "calibration").mkdir(exist_ok=True)
    cal, cal_rows = [], []
    for k, (name, actions, n) in enumerate(calibration_plan()[:3] if dry else calibration_plan()):
        n = 1 if dry else n
        cal.append(ensemble(work / "calibration" / f"{name}.npz",
                            lambda: oracle.sample_truth(actions, queries(), n, truth_seed=CAL_SEED + k),
                            dict(actions=actions, queries=queries(), members=n, seed=CAL_SEED + k)))
        cal_rows.append(dict(id=name, actions=actions, members=n, seed=CAL_SEED + k))
    scales = frozen_scales(cal)
    groups = score_groups(scales)
    cases = []
    for i, (name, actions, kind, mech) in enumerate(progs):
        case = dict(id=f"c{i + 1:03d}", actions=actions, queries=queries())
        cases.append(dict(request=case, family=name, groups=groups, truth=f"truth/{case['id']}.npz"))
    suite = dict(
        schema_version="physim-suite-v1", scoring_version=scoring.VERSION, contract_version=R6.APPARATUS_PROTOCOL,
        forecast_members=64, truth_members=2, predictor_seed=20260913, aggregation="equal-case-mean",
        cases=cases,
        program_notes={name: dict(kind=kind, mechanism=mech) for name, _, kind, mech in progs},
        calibration=dict(plan=cal_rows, floor_frac=FLOOR_FRAC, score_times=SCORE_TIMES, scales=scales),
        truth_seeds=[TRUTH_SEED + i for i in range(len(cases))],
        known_limits=[
            "One prepared state and one apparatus; not a held-out generalization benchmark.",
            "Two grading truths per case; score scales are calibration-ensemble standard deviations.",
            "Native and ablated controls are privileged diagnostics, not learned agents.",
        ],
    )
    sp = out / "suite.json"
    if sp.exists():
        assert json.loads(sp.read_text()) == _jsonable(suite), "frozen suite changed"
    else:
        write_json(sp, suite, compact=True)    # frozen before any truth (compact: the bundle JSON cap is 2 MiB)
    (out / "truth").mkdir(exist_ok=True)
    for i, record in enumerate(cases):
        case, path = record["request"], out / record["truth"]
        if not path.exists():
            t0 = time.process_time()
            truth = oracle.sample_truth(case["actions"], case["queries"], n_samples=2, truth_seed=TRUTH_SEED + i)
            np.savez_compressed(path, request=json.dumps(case), **{f"query{q}": a for q, a in enumerate(truth["samples"])})
            print(f"  truth {case['id']} {record['family']}: {time.process_time() - t0:.1f} cpu-s", flush=True)
    write_manifest(out)
    bundle = LB.open_bundle(out, profile="evaluation")
    bundle.check_runtime()
    for record in bundle.suite["cases"]:
        bundle.truth(record)
    print(json.dumps(dict(bundle_id=bundle.manifest["bundle_id"], cases=len(cases)), indent=1))


def write_manifest(out: Path, checks: dict | None = None):
    if checks is not None:
        write_json(out / "checks.json", checks)
    decl = json.loads((out / "labworld.json").read_text())
    state = LB.read_state(out / "preparation.npz", decl)
    world_files = {p.relative_to(out).as_posix(): digest(p) for p in sorted((out / "world").rglob("*")) if p.is_file() and "__pycache__" not in p.parts}
    objects = {}
    objects["world"] = identified("world", dict(
        name=decl["name"], files=world_files, declaration_sha256=digest(out / "labworld.json"),
        implementation=LB.implementation_identity(),
        source=dict(world=str(WORLD_SRC.relative_to(LAB)), lab_repository="physim research/alife")))
    objects["preparation"] = identified("preparation", dict(
        world_id=objects["world"]["id"], file_sha256=digest(out / "preparation.npz"),
        state_sha256=LB.state_digest({k: np.asarray(v) for k, v in state.items()}),
        apparatus_sha256=digest(out / "apparatus.json"), noise_policy=R6.NOISE_POLICY, public_time=0,
        recipe=dict(PREP, script=Path(__file__).name)))
    suite = json.loads((out / "suite.json").read_text())
    objects["suite"] = identified("suite", dict(
        preparation_id=objects["preparation"]["id"], file_sha256=digest(out / "suite.json"),
        scoring_source_sha256=digest(scoring.__file__),
        truth_sha256={c["truth"]: digest(out / c["truth"]) for c in suite["cases"]}))
    files = []
    for p in sorted(out.rglob("*")):
        if not p.is_file() or p.name == "manifest.json" or "__pycache__" in p.parts:
            continue
        rel = p.relative_to(out).as_posix()
        role = "truth" if rel.startswith("truth/") else "world" if rel.startswith("world/") else p.stem
        profiles = ["evaluation"] if role in ("truth", "suite") else ["simulation", "evaluation"]
        files.append(dict(path=rel, bytes=p.stat().st_size, sha256=digest(p), role=role, profiles=profiles))
    manifest = dict(schema_version=LB.LAB_FORMAT,
                    bundle_id=identified("bundle", {k: v["id"] for k, v in objects.items()})["id"],
                    status="local-development-verified", licenses=dict(code="Apache-2.0", data="CC-BY-4.0"),
                    objects=objects, files=files)
    write_json(out / "manifest.json", manifest)
    return manifest


def checks(out: Path, work: Path):
    """checks.json: the packaged initial-persistence control scored through evaluation._forecast_suite (4 members),
    which evaluation.reference_demo reproduces; then the manifest (the bundle identity does not change)."""
    from physim import evaluation as EV

    bundle = LB.open_bundle(out, profile="evaluation")
    sensors = ["device0", "device1", "global"]
    init = bundle.make_oracle().sample_truth([], [dict(sensor=s, t=[0]) for s in sensors], n_samples=1, truth_seed=0)
    model = scoring.PersistencePredictor(dict(zip(sensors, [a[0, 0] for a in init["samples"]])), roster=bundle.roster)
    target = work / "checks_persistence"
    if target.exists():
        shutil.rmtree(target)
    report = EV._forecast_suite(
        bundle, target, lambda case, n, seed: (model.predict(case["actions"], case["queries"], n_samples=n, seed=seed),
                                               dict(kind="trusted-packaged-control")),
        members=4, predictor=dict(kind="trusted-packaged-control", name="initial_persistence"))
    value = dict(schema_version="physim-reference-checks-v1",
                 reference=dict(predictor="initial_persistence", forecast_members=4,
                                primary_joint_energy=report["primary_joint_energy"], absolute_tolerance=1e-10),
                 recipe_sha256=digest(__file__))
    manifest = write_manifest(out, value)
    print(json.dumps(dict(value["reference"], bundle_id=manifest["bundle_id"])), flush=True)


# ----------------------------------------------------------------------------- controls

def variant_oracle(bundle, name):
    world = bundle.world()
    devices = None
    if name in ("reference", "ignore_actions"):
        pass
    elif name == "wrong_probe_geometry":
        devices = LB.devices_from_apparatus(bundle.apparatus)
        for d in devices:
            d.center = (d.center + np.asarray([0.0, 3.0])) % d.L
    elif name == "numerical_null":
        world = dataclasses.replace(world, overrides={"dt": 0.01}, steps_per_tick=2, native_dt=0.01)
    elif name in ABLATION_OVERRIDES:
        ov, wrapper = ABLATION_OVERRIDES[name]
        if wrapper:
            os.environ["FV_BASE"] = str(bundle.root / "world" / "world.py")
            world = dataclasses.replace(world, path=str(ABLATIONS))
        world = dataclasses.replace(world, overrides=ov)
    else:
        raise ValueError(name)
    return bundle.make_oracle(world=world, devices=devices)


ABLATION_OVERRIDES = {
    "ablate_adv0": ({"adv": 0.0}, False),          # vortices do not advect each other (flow off)
    "ablate_kF0": ({"kF": 0.0}, False),            # fuel does not regrow
    "ablate_k0": ({"k": 0.0}, False),              # eating does not grow vorticity
    "ablate_mu0": ({"mu": 0.0}, False),            # weak vorticity does not decay
    "ablate_body_gain": ({"body_gain": 1.0}, True),  # no differential growth within a body (division hypothesis)
}
# Blunt ablations run on their targeted programs and the sham only (CPU); every other control on all cases.
LIMITED = {
    "ablate_k0": ("sham", "feed_vortex", "stir_cut", "feed_neck", "feed_and_follow"),
    "ablate_mu0": ("sham", "starve_vortex", "starve_neck", "stir_cut", "delayed_feed"),
}
CONTROLS = ["wrong_probe_geometry", "ablate_adv0", "ablate_kF0", "ablate_body_gain", "numerical_null",
            "ablate_k0", "ablate_mu0"]


def jobs(bundle):
    cases = bundle.suite["cases"]
    out = [("ignore_actions", -1)]
    for name in CONTROLS:
        for i, rec in enumerate(cases):
            if name in LIMITED and rec["family"] not in LIMITED[name]:
                continue
            out.append((name, i))
    out += [("reference", i) for i in range(len(cases))]
    return out


def run_job(bundle, work: Path, name: str, i: int, oracles: dict):
    d = work / "controls"
    d.mkdir(parents=True, exist_ok=True)
    if name == "ignore_actions":
        path, actions, members, seed = d / "ignore_actions.npz", [], 8, IGNORE_SEED
        q = queries()
    else:
        case = bundle.suite["cases"][i]["request"]
        path, actions, q = d / f"{name}_{case['id']}.npz", case["actions"], case["queries"]
        members = REF_MEMBERS if name == "reference" else CONTROL_MEMBERS
        seed = (NULL_SEED if name == "numerical_null" else FORECAST_SEED) + i
    if path.exists():
        return
    if name not in oracles:
        oracles[name] = variant_oracle(bundle, name)
    o = oracles[name]
    ensemble(path, lambda: o.sample_truth(actions, q, members, truth_seed=seed),
             dict(variant=name, actions=actions, queries=q, members=members, seed=seed,
                  suite_sha256=bundle.manifest["objects"]["suite"]["file_sha256"]))


def controls(out: Path, work: Path, worker: int, workers: int):
    bundle = LB.open_bundle(out, profile="evaluation")
    oracles = {}
    for j, (name, i) in enumerate(jobs(bundle)):
        if j % workers == worker:
            run_job(bundle, work, name, i, oracles)
    print(f"worker {worker} done", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["build", "checks", "controls", "report", "programs"])
    ap.add_argument("--out", type=Path)
    ap.add_argument("--work", type=Path)
    ap.add_argument("--worker", type=int, default=0)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    if a.cmd == "build":
        build(a.out, a.work or a.out.parent / "work", dry=a.dry)
    elif a.cmd == "checks":
        checks(a.out, a.work)
    elif a.cmd == "controls":
        controls(a.out, a.work, a.worker, a.workers)
    elif a.cmd == "programs":
        print(json.dumps([dict(id=p[0], kind=p[2], actions=p[1]) for p in programs()], indent=1))
    else:
        import fedvortex_report
        fedvortex_report.report(a.out, a.work)
