"""Declarations and helpers for two lab-world evaluation candidates: phase_membrane and CIPS-iso.

- ``phase_membrane``: threads/autopoiesis/worlds/phase_membrane (128^2, dx 1). Noise by intensity
  (``LabWorld.noise_intensity``) with ell = 2 world units on every field: additive on phi, proportional on
  S, K, L. The native dt and the steps per tick are arguments (dt 1 is 1 step per tick; dt 0.5 is 2).
- ``cips_iso``: c40's CIPS layered-divide world with the isotropic enzyme drift stencil
  (``worlds/cips_iso.py``), 192^2, dt 0.1, 1 step per tick, proportional noise by intensity with ell = 2.

Run with OMP_NUM_THREADS=1. ``PHYSIM_PIN`` (optional) is a directory holding a pinned copy of the
``physim`` package; it is imported before labeval inserts the live tree, so the whole run uses one
version of labworld.py even if the working tree changes.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import dataclasses  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

_PIN = os.environ.get("PHYSIM_PIN")
if _PIN:
    sys.path.insert(0, _PIN)
    import physim  # noqa: E402,F401  (pins the package before labeval inserts the live tree)
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import labeval as E  # noqa: E402
from physim import labworld as LW  # noqa: E402
from physim.devices import ProbeDevice  # noqa: E402

if _PIN:
    assert Path(LW.__file__).resolve().is_relative_to(Path(_PIN).resolve()), LW.__file__

LAB = "/home/user/physim/research/alife"
PM_PATH = f"{LAB}/threads/autopoiesis/worlds/phase_membrane/world.py"
PM_FIELDS = ("S", "K", "L", "phi")
PM_FORMS = {"S": "proportional", "K": "proportional", "L": "proportional", "phi": "additive"}
CIPS_PATH = str(HERE / "worlds" / "cips_iso.py")
CIPS_ORIG = f"{LAB}/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py"
CIPS_FIELDS = ("e", "p", "F", "s")
CIPS_CLIPS = {"e": (0.0, 1.0), "p": (0.0, 1.0), "F": (0.0, None), "s": (0.0, None)}
ELL = 2.0


def one_worker(module):
    if hasattr(module, "ops") and hasattr(module.ops, "WORKERS"):
        module.ops.WORKERS = 1


def device(i, centre, L):
    """PhySim's two probe arrays: 13-node square (ds 3) and 19-node hex (ds 6), as in labeval."""
    lattice, ds, rot, k = (("square", 3.0, 0.3, 13), ("hex", 6.0, 1.1, 19))[i]
    return ProbeDevice(dev_id=i, lattice=lattice, n_rings=3, base_ds=ds, center=np.asarray(centre, float) + 0.5,
                       L=float(L), secret_rot=rot, reflect=False, motion_theta=0.0, motion_reflect=False,
                       node_perm=np.arange(k))


# ----------------------------------------------------------------------------- phase_membrane

def pm_world(intensity=0.01, dt=0.5, ell=ELL, gain=0.01, overrides=None, actuators=None):
    spt = int(round(1.0 / dt))
    assert abs(spt * dt - 1.0) < 1e-12, "one public tick is 1 native time unit"
    noise = {f: (PM_FORMS[f], float(intensity)) for f in PM_FIELDS}
    ov = {"dt": float(dt)}
    ov.update(overrides or {})
    return LW.LabWorld(path=PM_PATH, fields=PM_FIELDS, steps_per_tick=spt, native_dt=float(dt),
                       ports={f: LW.Port(gain=gain, clip=(0.0, None)) for f in PM_FIELDS}, noise=noise,
                       noise_corr={f: float(ell) for f in PM_FIELDS} if ell else {},
                       noise_intensity=PM_FIELDS, overrides=ov, dx=1.0, actuators=actuators)


# ----------------------------------------------------------------------------- CIPS-iso

CIPS_GAINS = {"e": 0.01, "p": 0.1, "F": 0.1, "s": 0.1}


def cips_world(intensity=0.01, ell=ELL, gains=None, dt=0.1, overrides=None, actuators=None, path=CIPS_PATH):
    g = dict(CIPS_GAINS, **(gains or {}))
    spt = int(round(0.1 / dt))
    assert abs(spt * dt - 0.1) < 1e-12, "one public tick is 0.1 native time units"
    ov = dict(overrides or {})
    if dt != 0.1:
        ov["dt"] = float(dt)
    return LW.LabWorld(path=path, fields=CIPS_FIELDS, steps_per_tick=spt, native_dt=float(dt),
                       ports={f: LW.Port(gain=float(g[f]), clip=CIPS_CLIPS[f]) for f in CIPS_FIELDS},
                       noise={f: ("proportional", float(intensity)) for f in CIPS_FIELDS},
                       noise_corr={f: float(ell) for f in CIPS_FIELDS} if ell else {},
                       noise_intensity=CIPS_FIELDS if intensity > 0 or ell else (),
                       overrides=ov, dx=1.0, sys_path=(LAB,), carry=("t",), actuators=actuators)


def load_state(path, fields):
    with np.load(path) as z:
        st = {f: z[f].astype(np.float64) for f in fields}
        if "t" in z.files:
            st["t"] = float(z["t"])
    return st


def native_module(world: LW.LabWorld):
    m = world.load()
    one_worker(m)
    return m


def jsonable(x):
    return E._jsonable(x)


def dump(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(jsonable(obj), indent=1) + "\n")


def replace(world, **kw):
    return dataclasses.replace(world, **kw)


# ----------------------------------------------------------------------------- programs

def _inj(t, device, port, dur, amp=3.0):
    return dict(t=float(t), kind="inject", device=int(device), port=int(port), amp=float(amp), dur=float(dur))


def _adj(t, device, u):
    return dict(t=float(t), kind="adjust", device=int(device), u=[float(v) for v in u])


# phase_membrane inject roster: port 0 S+ (feed), 1 S- (starve), 2 K+ (catalyst), 3 L+ (links)
PM_ACTUATORS = (LW.Actuator("S", 1), LW.Actuator("S", -1), LW.Actuator("K", 1), LW.Actuator("L", 1))
PM_SP, PM_SM, PM_K, PM_L = range(4)


def pm_programs():
    """(id, actions, mechanism note). device0: centre of a 168-px cell; device1: centre of the 550-px cell
    whose catalyst is already starved at its centre. Adjusts on one device are >= 5 tu apart (ADJUST_TICKS)."""
    rim = [_adj(5 * k, 0, [0, -1, 0]) for k in range(5)]
    return [
        ("sham", [], "no action"),
        ("probe_shift", [_adj(0, 0, [1, 0, 0])], "probe move only"),
        ("probe_wide", [_adj(0, 1, [0, 0, 1])], "probe dilation only"),
        ("K_d0", [_inj(0, 0, PM_K, 10)], "catalyst into the small cell: more links, tilt pushes the wall out"),
        ("L_d0", [_inj(0, 0, PM_L, 20)], "links at the small cell's centre: drift to the wall (adsorption), tilt"),
        ("L_rim", rim + [_inj(25, 0, PM_L, 20)], "probe walked 5 units toward the bath, links at the inner rim"),
        ("Sm_d0", [_inj(0, 0, PM_SM, 50)], "starve the small cell's centre: central starvation, split"),
        ("Sp_d0", [_inj(0, 0, PM_SP, 50)], "feed the small cell's centre (it starves and dissolves in the sham)"),
        ("Sm_d1", [_inj(0, 1, PM_SM, 50)], "starve the big cell's centre further"),
        ("Sp_d1", [_inj(0, 1, PM_SP, 50)], "feed the big cell's starved centre"),
        ("K_d1", [_inj(0, 1, PM_K, 10)], "re-seed catalyst at the starved centre"),
        ("L_d1", [_inj(0, 1, PM_L, 20)], "links at the starved centre: tilt holds the inside phase there"),
        ("move_during_pulse", [_inj(0, 0, PM_K, 10), _adj(2, 0, [1, 0, 0])], "standard composite"),
        ("two_sources", [_inj(0, 0, PM_K, 10), _adj(0, 1, [0, 1, 0]), _inj(0, 1, PM_K, 10)], "standard composite"),
    ]


# CIPS-iso inject roster: port 0 p+ (product), 1 F+ (feed), 2 F- (fuel cut), 3 s+ (amphiphile)
CIPS_ACTUATORS = (LW.Actuator("p", 1), LW.Actuator("F", 1), LW.Actuator("F", -1), LW.Actuator("s", 1))
CP_P, CP_FP, CP_FM, CP_S = range(4)


def cips_programs():
    """device0: neck of a dumbbell body that pinches about 20 tu into the window; device1: neck of a second
    dumbbell that pinches about 34 tu in."""
    return [
        ("sham", [], "no action"),
        ("probe_shift", [_adj(0, 0, [1, 0, 0])], "probe move only"),
        ("probe_wide", [_adj(0, 1, [0, 0, 1])], "probe dilation only"),
        ("p_d0", [_inj(0, 0, CP_P, 20)], "product at the neck: enzyme drifts up it, the pinch is held"),
        ("p_d1", [_inj(0, 1, CP_P, 20)], "product at the second neck"),
        ("Fp_d0", [_inj(0, 0, CP_FP, 20)], "feed the neck: catalysis burns the extra fuel"),
        ("Fp_d1", [_inj(0, 1, CP_FP, 20)], "feed the second neck"),
        ("Fm_d0", [_inj(0, 0, CP_FM, 50)], "local fuel cut at the neck: starvation"),
        ("Fm_d1", [_inj(0, 1, CP_FM, 50)], "local fuel cut at the second neck"),
        ("s_d0", [_inj(0, 0, CP_S, 20)], "amphiphile at the neck: adsorbs to the interface"),
        ("move_during_pulse", [_inj(0, 0, CP_FM, 10), _adj(2, 0, [1, 0, 0])], "standard composite"),
        ("two_sources", [_inj(0, 0, CP_FM, 10), _adj(0, 1, [0, 1, 0]), _inj(0, 1, CP_FM, 10)], "standard composite"),
    ]


# ----------------------------------------------------------------------------- suites
#
# The suite format is labeval's (labeval.run): suite.json frozen before any truth, with the same keys and the
# same score groups and scales (labeval.frozen_scales / score_groups), truths at 71000 + case index (2 members),
# forecasts at 81000 + case index, ignore_actions at 80999, calibration at 51000 + k. Additions, all as extra keys:
#   programs       the world's own program list (labeval.build_programs is not used: its pulse programs index
#                  ports by field, which an explicit actuator roster does not)
#   calibration    sham x2 plus every single-inject program x1 (labeval: sham x4 plus every single pulse x1)
#   case_controls  the controls run on each case (labeval runs every control on every case); every case has
#                  independent_native, ignore_actions, wrong_probe_geometry and initial_persistence
#   band_native    a second independent native ensemble on the listed cases (seeds 91000 + i, labeval's band seeds)
#   numerical_null its own seeds 61000 + i (labeval's shares the forecast seeds with independent_native)
#   members        forecast members per control ensemble (labeval: 8)
from physim import blobround6 as R6  # noqa: E402
from physim import blobround6_eval as scoring  # noqa: E402

SCHEMA = "labeval-v1+pmcips1"
NULL_SEED = 61000
BASE_CONTROLS = ("independent_native", "ignore_actions", "wrong_probe_geometry", "initial_persistence")


@dataclasses.dataclass
class SuitePlan:
    spec: E.LabSpec
    programs: list                    # (id, actions, note)
    subsets: dict                     # control name -> list of program ids (base controls: every case)
    members: int = 4

    def controls(self):
        return list(BASE_CONTROLS) + ["band_native"] + [f"ablate_{a}" for a in self.spec.ablations] + ["numerical_null"]

    def case_controls(self, pid):
        return [c for c in self.controls() if c in BASE_CONTROLS or pid in self.subsets.get(c, ())]


def _cases(plan):
    return [dict(id=f"c{i + 1:03d}", actions=copy_actions(a), queries=E.queries()) for i, (_, a, _) in enumerate(plan.programs)]


def copy_actions(a):
    return json.loads(json.dumps(a))


def calibrate(plan, out: Path):
    cal_dir = out / "calibration"
    cal_dir.mkdir(parents=True, exist_ok=True)
    oracle = E.make_oracle(plan.spec, "native")
    todo = [(pid, a, 2 if pid == "sham" else 1) for pid, a, _ in plan.programs
            if pid == "sham" or (len(a) == 1 and a[0]["kind"] == "inject")]
    samples, rows = [], []
    for k, (pid, a, n) in enumerate(todo):
        req = dict(id=pid, actions=copy_actions(a), queries=E.queries())
        samples.append(E.cached(cal_dir / f"{pid}.npz", lambda: oracle.sample_truth(
            req["actions"], req["queries"], n, truth_seed=E.CAL_SEED + k), meta=dict(request=req, members=n,
                                                                                     seed=E.CAL_SEED + k)))
        rows.append((pid, n, E.CAL_SEED + k))
    return samples, rows


def freeze(plan, out: Path):
    """Calibrate, freeze scales and groups, write suite.json (before any truth). Returns the suite dict."""
    out.mkdir(parents=True, exist_ok=True)
    spec = plan.spec
    cal, cal_rows = calibrate(plan, out)
    scales = E.frozen_scales(spec, cal)
    groups = E.score_groups(spec, scales)
    cases = _cases(plan)
    suite = dict(
        schema_version=SCHEMA, world=spec.name, scoring_version=scoring.VERSION, protocol=R6.APPARATUS_PROTOCOL,
        declaration=jsonable(spec.world.declaration()), world_sha256=E.file_sha(spec.world.path),
        prepared_state_sha256=E.digest_state(spec.state, spec.world.fields),
        devices=[dict(lattice=d.lattice, n_rings=d.n_rings, base_ds=d.base_ds, center=d.center.tolist(),
                      secret_rot=d.secret_rot, k=int(d.k)) for d in spec.devices],
        provenance=spec.provenance, ablations=spec.ablations, numerical_null=spec.null,
        calibration=dict(plan=cal_rows, floor_frac=E.FLOOR_FRAC, score_times=E.SCORE_TIMES, scales=scales),
        programs=[dict(id=pid, note=note) for pid, _, note in plan.programs],
        cases=[dict(request=c, family=pid, truth=f"truth/{c['id']}.npz") for c, (pid, _, _) in zip(cases, plan.programs)],
        groups=groups, truth_members=E.N_TRUTH, truth_seeds=[E.TRUTH_SEED + i for i in range(len(cases))],
        forecast_members=plan.members, forecast_seeds=[E.FORECAST_SEED + i for i in range(len(cases))],
        band_seeds=[E.BAND_SEED + i for i in range(len(cases))], null_seeds=[NULL_SEED + i for i in range(len(cases))],
        ignore_actions_seed=E.IGNORE_SEED, geometry_shift=list(E.GEOMETRY_SHIFT), controls=plan.controls(),
        case_controls={c["id"]: plan.case_controls(pid) for c, (pid, _, _) in zip(cases, plan.programs)},
    )
    suite = jsonable(suite)
    sp = out / "suite.json"
    if sp.exists():
        assert json.loads(sp.read_text()) == suite, "frozen suite changed; use a new output directory"
    else:
        sp.write_text(json.dumps(suite, indent=1) + "\n")
    return suite


def run_suite(plan, out: Path, controls=None, cases=None):
    """Truths and control ensembles (cached; resumable), then scores per case. ``controls``/``cases`` restrict
    what is simulated in this call (the frozen suite says what exists)."""
    suite = json.loads((out / "suite.json").read_text())
    spec, m = plan.spec, plan.members
    assert jsonable(spec.world.declaration()) == suite["declaration"]
    assert E.file_sha(spec.world.path) == suite["world_sha256"]
    (out / "truth").mkdir(exist_ok=True)
    rost = E.roster(spec)
    oracles = {}

    def oracle(v):
        if v not in oracles:
            oracles[v] = E.make_oracle(spec, v)
        return oracles[v]

    native = oracle("native")
    q0 = native.sample_truth([], [dict(sensor=s, t=[0]) for s in E.SENSORS], 1, truth_seed=0)["samples"]
    persistence = scoring.PersistencePredictor(dict(zip(E.SENSORS, [a[0, 0] for a in q0])), roster=rost)
    ign_req = dict(id="ignore", actions=[], queries=E.queries())
    ignore = None
    for i, entry in enumerate(suite["cases"]):
        case = entry["request"]
        if cases and case["id"] not in cases and entry["family"] not in cases:
            continue
        cdir = out / "controls" / case["id"]
        cdir.mkdir(parents=True, exist_ok=True)
        truth = E.cached(out / entry["truth"], lambda: native.sample_truth(
            case["actions"], case["queries"], E.N_TRUTH, truth_seed=E.TRUTH_SEED + i),
            meta=dict(request=case, members=E.N_TRUTH, seed=E.TRUTH_SEED + i))
        preds = {}
        for name in suite["case_controls"][case["id"]]:
            if controls and name not in controls:
                if (cdir / f"{name}.npz").exists():
                    preds[name] = E.cached(cdir / f"{name}.npz", None, meta=_meta(case, name, i, m))
                continue
            if name == "ignore_actions":
                if ignore is None:
                    ignore = E.cached(out / "ignore_actions.npz", lambda: native.sample_truth(
                        [], E.queries(), m, truth_seed=E.IGNORE_SEED), meta=dict(request=ign_req, members=m,
                                                                                 seed=E.IGNORE_SEED))
                preds[name] = ignore
                continue
            if name == "initial_persistence":
                preds[name] = persistence.predict(case["actions"], case["queries"], n_samples=m)["samples"]
                continue
            variant, seed = _variant_seed(name, i)
            o = oracle(variant)
            preds[name] = E.cached(cdir / f"{name}.npz", lambda: o.sample_truth(
                case["actions"], case["queries"], m, truth_seed=seed), meta=_meta(case, name, i, m))
        scores = {}
        for name, pred in preds.items():
            scores[name] = scoring.score_case(case, {"samples": pred}, {"samples": truth}, groups=suite["groups"],
                                              n_samples=m, n_truth=E.N_TRUTH, roster=rost)
        old = json.loads((cdir / "scores.json").read_text()) if (cdir / "scores.json").exists() else {}
        old.update(scores)
        (cdir / "scores.json").write_text(json.dumps(old, indent=1, allow_nan=False) + "\n")


def _variant_seed(name, i):
    if name == "independent_native":
        return "native", E.FORECAST_SEED + i
    if name == "band_native":
        return "native", E.BAND_SEED + i
    if name == "numerical_null":
        return "numerical_null", NULL_SEED + i
    return name.removeprefix("ablate_"), E.FORECAST_SEED + i


def _meta(case, name, i, m):
    variant, seed = _variant_seed(name, i)
    return dict(request=case, members=m, seed=seed, variant=variant)


def report(out: Path, title=None):
    """Aggregate (case-bootstrap 90% intervals), per-group and per-case ratios to independent_native, with the
    native-vs-native band (band_native / independent_native) as the yardstick. A control 'separates' when its
    interval lies above the band's upper bound; a group is not to be relied on for a control when the control's
    group interval reaches into the band's group interval."""
    suite = json.loads((out / "suite.json").read_text())
    fam = {c["request"]["id"]: c["family"] for c in suite["cases"]}
    S = {c: json.loads((out / "controls" / c / "scores.json").read_text()) for c in fam
         if (out / "controls" / c / "scores.json").exists()}
    ref, band = "independent_native", "band_native"
    gids = [g["id"] for g in suite["groups"]]
    controls = suite["controls"]

    def agg(k, cs):
        return np.array([S[c][k]["joint_energy_equal_group_mean"] for c in cs])

    def grp(k, cs, g):
        return np.array([next(x["energy_score"] for x in S[c][k]["joint_energy"] if x["id"] == g) for c in cs])

    def have(k):
        return [c for c in S if k in S[c] and ref in S[c]]

    res = dict(world=suite["world"], members=suite["forecast_members"], truths=suite["truth_members"],
               cases_scored=len(S), aggregate={}, groups={}, per_case={}, not_to_rely_on={})
    bc = have(band)
    band_ci = E._boot(agg(band, bc), agg(ref, bc)) if bc else [1.0, 1.0]
    band_g = {g: E._boot(grp(band, bc, g), grp(ref, bc, g)) for g in gids} if bc else {}
    for k in controls:
        cs = have(k)
        if not cs or k == ref:
            continue
        num, den = agg(k, cs), agg(ref, cs)
        ci = E._boot(num, den)
        res["aggregate"][k] = dict(n_cases=len(cs), ratio=float(num.mean() / den.mean()), ci90=ci,
                                   cases_worse=int((num > den).sum()),
                                   separated=bool(ci[0] > band_ci[1]) if k != band else None)
        res["groups"][k] = {}
        for g in gids:
            gn, gd = grp(k, cs, g), grp(ref, cs, g)
            gci = E._boot(gn, gd)
            res["groups"][k][g] = dict(ratio=float(gn.mean() / gd.mean()), ci90=gci)
            if k not in (band, "numerical_null") and band_g and gci[0] <= band_g[g][1]:
                res["not_to_rely_on"].setdefault(k, []).append(g)
    res["band_aggregate_ci90"] = band_ci
    for c in S:
        r = S[c][ref]["joint_energy_equal_group_mean"]
        row = {"family": fam[c], "ref_score": r}
        for k in controls:
            if k in S[c] and k != ref:
                row[k] = S[c][k]["joint_energy_equal_group_mean"] / r
                gr = {x["id"]: x["energy_score"] for x in S[c][k]["joint_energy"]}
                g0 = {x["id"]: x["energy_score"] for x in S[c][ref]["joint_energy"]}
                row[k + "_sensors"] = {s: float(np.mean([gr[g] for g in gids if g.startswith(s + "/")]) /
                                                np.mean([g0[g] for g in gids if g.startswith(s + "/")])) for s in E.SENSORS}
        res["per_case"][c] = row
    (out / "report.json").write_text(json.dumps(jsonable(res), indent=1) + "\n")
    L = [f"# {title or suite['world']}: frozen suite, controls vs independent_native", "",
         f"{len(S)} cases; {suite['forecast_members']} members per control ensemble, {suite['truth_members']} truths per case; "
         f"PhySim score_case joint energy, equal-group mean over {len(gids)} groups. Ratio = control / independent_native "
         f"(means over the cases the control ran on); 90% case-bootstrap interval. Band = band_native / independent_native, "
         f"all cases: {band_ci[0]:.2f}-{band_ci[1]:.2f}. 'sep' = interval above the band's upper bound.", "",
         "| control | cases | ratio | 90% interval | cases worse | sep |", "|---|---|---|---|---|---|"]
    for k, a in res["aggregate"].items():
        sep = "band" if k == band else ("null" if k == "numerical_null" else ("yes" if a["separated"] else "NO"))
        L.append(f"| {k} | {a['n_cases']} | {a['ratio']:.2f} | {a['ci90'][0]:.2f}-{a['ci90'][1]:.2f} | "
                 f"{a['cases_worse']}/{a['n_cases']} | {sep} |")
    L += ["", "Per group: ratio to independent_native over the cases each control ran on.", "",
          "| control | " + " | ".join(gids) + " |", "|---" * (len(gids) + 1) + "|"]
    for k in res["groups"]:
        L.append(f"| {k} | " + " | ".join(f"{res['groups'][k][g]['ratio']:.2f}" for g in gids) + " |")
    L += ["", "Groups not to rely on (control's group interval reaches the band's group interval):", ""]
    for k, gs in res["not_to_rely_on"].items():
        L.append(f"- {k}: {', '.join(gs)}")
    cols = [k for k in controls if k != ref]
    L += ["", "Per case: aggregate ratio to independent_native (blank: not run on that case).", "",
          "| case | program | " + " | ".join(cols) + " |", "|---" * (len(cols) + 2) + "|"]
    for c, row in res["per_case"].items():
        L.append(f"| {c} | {row['family']} | " + " | ".join(f"{row[k]:.2f}" if k in row else "" for k in cols) + " |")
    abl = [k for k in cols if k.startswith("ablate_") or k == "numerical_null"]
    L += ["", "Per case and sensor for the mechanism controls and the null: device0 / device1 / global.", "",
          "| case | program | " + " | ".join(abl) + " |", "|---" * (len(abl) + 2) + "|"]
    for c, row in res["per_case"].items():
        L.append(f"| {c} | {row['family']} | " + " | ".join(
            "/".join(f"{row[k + '_sensors'][s]:.1f}" for s in E.SENSORS) if k in row else "" for k in abl) + " |")
    (out / "report.md").write_text("\n".join(L) + "\n")
    return res


# ----------------------------------------------------------------------------- the two evaluation specs

PM_PREP = os.environ.get("PM_PREP", "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/"
                         "scratchpad/evalpilot/out/prep_s0")          # .npz and .json (labeval's phase_membrane)
CIPS_PREP = os.environ.get("CIPS_PREP", "/home/user/evalwork/pm_cips_eval/cips_prep/prep_s5_t3100")
CIPS_SITES = {"device0": [20.2, 153.8], "device1": [16.1, 101.8]}   # necks of the two dumbbells (pixel indices)

PM_ABLATIONS = {"a2": {"a": 2.0}, "chi0": {"chi": 0.0}, "DS2": {"DS": 0.4}}
CIPS_ABLATIONS = {"chi0": {"chi": 0.0}, "kF0": {"kF": 0.0}, "chis0": {"chi_s": 0.0}, "d0": {"d": 0.0},
                  "DF10": {"DF": 20.0}}


def pm_spec(intensity=0.01, dt=0.5, null_dt=0.25):
    world = pm_world(intensity, dt, actuators=PM_ACTUATORS)
    with np.load(PM_PREP + ".npz") as z:
        state = {f: z[f].astype(np.float64) for f in PM_FIELDS}
    info = json.loads(Path(PM_PREP + ".json").read_text())
    devices = [device(0, info["sites"]["centre"], 128), device(1, info["sites"]["other"], 128)]
    return E.LabSpec(name="phase_membrane_iso_noise", world=world, state=state, devices=devices, main_port=PM_K,
                     ablations=dict(PM_ABLATIONS),
                     null={"overrides": {"dt": null_dt}, "steps_per_tick": int(round(1 / null_dt)), "native_dt": null_dt},
                     provenance=dict(prepared=PM_PREP + ".npz", prep_info=info,
                                     prepared_file_sha256=E.file_sha(PM_PREP + ".npz")))


def cips_spec(intensity, gains=None, null_dt=0.05):
    world = cips_world(intensity, gains=gains, actuators=CIPS_ACTUATORS)
    with np.load(CIPS_PREP + ".npz") as z:
        state = {f: z[f].astype(np.float64) for f in CIPS_FIELDS}
        state["t"] = float(z["t"])
    devices = [device(0, CIPS_SITES["device0"], 192), device(1, CIPS_SITES["device1"], 192)]
    info = json.loads(Path(CIPS_PREP + ".json").read_text())
    return E.LabSpec(name="cips_iso", world=world, state=state, devices=devices, main_port=CP_FM,
                     ablations=dict(CIPS_ABLATIONS),
                     null={"overrides": {"dt": null_dt}, "steps_per_tick": int(round(0.1 / null_dt)), "native_dt": null_dt},
                     hook=one_worker,
                     provenance=dict(prepared=CIPS_PREP + ".npz", prep_info=info, sites=CIPS_SITES,
                                     prepared_file_sha256=E.file_sha(CIPS_PREP + ".npz")))
