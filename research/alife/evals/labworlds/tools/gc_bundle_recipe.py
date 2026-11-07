"""A frozen grand-challenge (gc) lab-world suite folder as a PhySim LabBundle.

    python gc_bundle.py inputs --suite SUITE_DIR                       what the bundle takes from where (no writes)
    python gc_bundle.py build  --suite SUITE_DIR --out BUNDLE [--work WORK]
    python gc_bundle.py verify --bundle BUNDLE --case ID --out JSON     member 0 of one frozen truth re-simulated
                                                                        through the bundle's own oracle, bit for bit

The bundle has fedvortex_bundle.py's layout, manifest format (``physim-lab-bundle-v1``) and identity rules: world/
(the world file, the modules it imports, observables.py), labworld.json, apparatus.json, preparation.npz, suite.json
(``physim-suite-v1``, compact), truth/*.npz, checks.json (initial persistence, 4 members), manifest.json whose world /
preparation / suite objects bind every file by sha256 and the implementation by labbundle.implementation_identity().

Suite folders come in two schemas, both read from their frozen suite.json:

- ``gc-vortex-suite-v1/v2`` (scripts/physim/labworlds/gc_vortex, gc_suites/vortex/scripts2): declaration, sites,
  adjustment_matrix, preparation.file (relative to the world folder, sha256 checked), per-case truth_seed.
- ``labeval-v1+pmcips1+gc1...`` (labeval.py + pmcips.py + gc_phase_membrane / gc_cips / gc_rods): declaration,
  devices, adjust_mix, provenance.prepared (+ sha256), prepared_state_sha256, truth_seeds; groups, or
  groups_by_horizon with a per-case horizon (rods).

What a suite folder does not hold is taken from that world's scripts (``inputs`` prints it for one suite):
the world file (the declared path, sha256 checked against the suite), labkit (for worlds that import it), the
derived-channel functions (verbatim source of the function the declaration names, e.g. gcv.eat, gcrods.speed),
the device construction (gcv.device / pmcips.device: node permutation, centre convention, motion basis), the
identity port permutation and one FFT worker (every gc script builds ``LW.oracle(world, state, devices,
adjust_mix=MIX)`` and sets labkit's ops.WORKERS = 1), the preparation loader's keys (fields plus the declared
carry keys), and score-group unit labels where the suite stored none (gc_vortex/suite.py report()).

Two declaration items have no physim-lab-bundle-v1 key and are re-expressed:
- ``carry: null`` (phase_membrane) becomes ``[]``: with carry None LabStepper keeps the prepared state's non-field
  keys (none: pmgc.load_prep loads only the fields); with [] it keeps init's non-field keys (none: init returns only
  the fields). Same state either way.
- ``noise_bounds`` (CIPS: e, p in [0, 1]) is applied by a generated world.py that wraps the original world file and
  projects each bounded field onto its range at the start of every native step. LabStepper runs injection, noise,
  then step, so this is the same projection at the same point (``verify`` checks it bit for bit).

Truths are never regenerated: their arrays are copied from the suite folder's truth files into the bundle's truth
format (``request`` + ``query{i}``).
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import ast
import hashlib
import json
import re
import shutil
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path("/home/user/swpo/residency-environments")
ENV = REPO / "environments" / "physim"
SCRIPTS = REPO / "scripts" / "physim" / "labworlds"
sys.path.insert(0, str(ENV))
from physim import blobround6 as R6  # noqa: E402
from physim import blobround6_eval as scoring  # noqa: E402
from physim import labbundle as LB  # noqa: E402
from physim.bundles import digest, identified  # noqa: E402
from physim.devices import ProbeDevice  # noqa: E402

LAB = Path("/home/user/physim/research/alife")
LABKIT = [LAB / "labkit" / n for n in ("__init__.py", "ops.py", "world.py")]   # as fedvortex_bundle.LABKIT_SRC
PREDICTOR_SEED = 20260913                                                      # as the fed-vortex bundle
SLOTS = (13, 19)

# Where the derived channels named in a declaration ("module.function") are defined.
DERIVED_SOURCES = {"gcv": SCRIPTS / "gc_vortex" / "gcv.py", "gcrods": SCRIPTS / "gc_rods" / "gcrods.py"}

# Per world file (sha256 of the declared world.py): the scripts' device and loader conventions.
WORLDS = {
    "98b2f6bf27c2728c616e17b3b2ed6d06a83d7aabb6a3e5b28bb50937fc438b44": dict(
        world="c53 fed vortices with heredity and selection (SIDH)", devices="gcv", loader="gcv.load_state",
        scripts="scripts/physim/labworlds/gc_vortex (gcv.py, suite.py); gc_suites/vortex/scripts2 (gc2.py, suite2.py)"),
    "14049d3c46d89dda9ae17fc34dfe7365624d8bdc1fc45c158b69541ce13cc29f": dict(
        world="phase_membrane", devices="pmcips", loader="pmgc.load_prep",
        scripts="scripts/physim/labworlds/gc_phase_membrane (pmgc.py, suite.py), pmcips.py, labeval.py"),
    "150dd2c66b35ab3719e814af43ce04aa9dd43699eaff54e09faab9ccadf9a469": dict(
        world="CIPS-iso", devices="pmcips", loader="gccips.load_prep",
        scripts="scripts/physim/labworlds/gc_cips (gccips.py, suite.py), pmcips.py, labeval.py"),
    "464e9d2451587715fa79d1f926c2a61648c05419bd76db2df4cfbbf5aef516ba": dict(
        world="c34 Marangoni rods", devices="pmcips", loader="gcrods.load_prep",
        scripts="scripts/physim/labworlds/gc_rods (gcrods.py, suite.py), pmcips.py, labeval.py"),
}

# gc_vortex/suite.py report() and suite2.py report(): score_case requires a unit; the frozen groups have none.
VORTEX_UNITS = ("global mean and variance; frozen calibration scales", "native field units; frozen calibration scale")


class Inputs:
    """Everything a bundle needs, resolved from one suite folder (read only)."""

    def __init__(self, suite_dir: Path):
        self.dir = Path(suite_dir).resolve()
        self.src = json.loads((self.dir / "suite.json").read_text())
        s = self.src
        self.schema = s["schema_version"]
        self.vortex = self.schema.startswith("gc-vortex-suite")
        if not (self.vortex or self.schema.startswith("labeval-v1")):
            raise SystemExit(f"unsupported suite schema {self.schema}")
        d = s["declaration"]
        self.decl_src = d
        self.world_path = Path(d["path"])
        self.world_sha = s["world_sha256"]
        if digest(self.world_path) != self.world_sha:
            raise SystemExit("declared world file differs from the suite's world_sha256")
        if self.world_sha not in WORLDS:
            raise SystemExit("no device/loader convention recorded for this world file")
        self.conv = WORLDS[self.world_sha]
        self.fields = list(d["fields"])
        self.carry = list(d["carry"] or [])
        self.derived = list(d.get("derived") or [])
        self.observed = self.fields + [x["name"] for x in self.derived]
        # preparation
        if self.vortex:
            # relative to the world folder (gc_vortex ROOT): "prep/..." for suite/, "formation/prep/..." for formation/
            self.prep_path = (self.dir.parent / s["preparation"]["file"]).resolve()
            self.prep_sha = s["preparation"]["sha256"]
        else:
            self.prep_path = Path(s["provenance"]["prepared"]).resolve()
            self.prep_sha = s["provenance"]["prepared_file_sha256"]
        if digest(self.prep_path) != self.prep_sha:
            raise SystemExit(f"prepared state {self.prep_path} differs from the suite's sha256")
        self.loader_state = self._loader_state()
        if not self.vortex:
            if self._digest_state(self.loader_state) != s["prepared_state_sha256"]:
                raise SystemExit("prepared state differs from the suite's prepared_state_sha256")
        self.grid = list(self.loader_state[self.fields[0]].shape)
        self.L = float(self.grid[0] * d["dx"])
        self.mix = s["adjustment_matrix"] if self.vortex else s["adjust_mix"]
        self.devices = self._devices()
        self.cases = self._cases()

    # -- preparation: the loaders of the suites' scripts --
    def _loader_state(self):
        with np.load(self.prep_path) as z:
            loader = self.conv["loader"]
            if loader == "gcv.load_state":            # om, Y, a, b as float64, t
                st = {k: z[k].astype(np.float64) for k in ("om", "Y", "a", "b")}
                st["t"] = float(z["t"])
            elif loader == "pmgc.load_prep":          # the fields only
                st = {f: z[f].astype(np.float64) for f in self.fields}
            elif loader == "gccips.load_prep":        # the fields and t
                st = {f: z[f].astype(np.float64) for f in self.fields}
                st["t"] = float(z["t"])
            elif loader == "gcrods.load_prep":        # every array but t
                st = {k: z[k].astype(np.float64) for k in z.files if k not in ("t",)}
            else:
                raise ValueError(loader)
        return st

    @staticmethod
    def _digest_state(state):                         # labeval.digest_state
        h = hashlib.sha256()
        for k in sorted(state):
            v = state[k]
            if isinstance(v, np.ndarray):
                h.update(k.encode())
                h.update(np.ascontiguousarray(v).tobytes())
        return h.hexdigest()

    def preparation(self):
        """Bundle preparation: the fields and declared carry keys of the loader's state (what the native oracle uses)."""
        st = self.loader_state
        out = {f: np.asarray(st[f], np.float64) for f in self.fields}
        for k in self.carry:
            out[k] = np.asarray(st[k], np.float64)
        return out

    # -- devices: gcv.device / pmcips.device --
    def _devices(self):
        out = []
        for i in range(2):
            lattice, ds, rot, k = (("square", 3.0, 0.3, 13), ("hex", 6.0, 1.1, 19))[i]
            if self.conv["devices"] == "gcv":
                centre = list(map(float, self.src["sites"][i]))
                perm = np.random.default_rng(41031 + i).permutation(k)
                d = ProbeDevice(i, lattice, 3, ds, centre, self.L, rot, False, 0.0, False, np.asarray(perm))
            else:
                centre = np.asarray(self.src["provenance"]["sites"][f"device{i}"], float) + 0.5
                d = ProbeDevice(dev_id=i, lattice=lattice, n_rings=3, base_ds=ds, center=centre, L=self.L,
                                secret_rot=rot, reflect=False, motion_theta=0.0, motion_reflect=False,
                                node_perm=np.arange(k))
                rec = self.src["devices"][i]
                assert (rec["lattice"], rec["n_rings"], rec["base_ds"], rec["secret_rot"], rec["k"]) == \
                    (lattice, 3, ds, rot, k) and np.allclose(rec["center"], d.center, atol=0, rtol=1e-12), rec
            out.append(d)
        return out

    def apparatus(self):
        recs = []
        for d in self.devices:
            recs.append(dict(parameters=dict(dev_id=int(d.dev_id), lattice=d.lattice, n_rings=int(d.n_rings),
                                             base_ds=float(d.base_ds), center=[float(x) for x in d.center], L=float(d.L),
                                             secret_rot=float(d.secret_rot), reflect=bool(d.reflect), motion_theta=0.0,
                                             motion_reflect=False, node_perm=[int(x) for x in d.node_perm],
                                             dil_bounds=list(d.dil_bounds)),
                             dilation=float(d.dilation), motion_basis=np.asarray(d.Bm).tolist()))
        return dict(devices=recs, device_slots=list(SLOTS), port_permutation=list(range(len(self.observed))),
                    adjustment_matrix=[[float(x) for x in row] for row in self.mix], protocol=R6.APPARATUS_PROTOCOL)

    # -- declaration --
    def world_name(self):
        if self.vortex:
            return "c53-fed-vortex-selection-" + ("gc" if self.src.get("suite") is None else self.src["suite"])
        return self.src["world"]

    def bounded(self):
        """noise_bounds restricted to fields whose noise sd > 0 (LabStepper projects only those)."""
        b = self.decl_src.get("noise_bounds") or {}
        return {f: list(v) for f, v in b.items() if float(self.decl_src["noise"][f][1]) > 0}

    def declaration(self):
        d = self.decl_src
        return dict(
            name=self.world_name(), world_file="world.py", fields=self.fields, grid=self.grid,
            steps_per_tick=int(d["steps_per_tick"]), native_dt=float(d["native_dt"]),
            ports={f: dict(gain=float(p["gain"]), clip=list(p["clip"])) for f, p in d["ports"].items()},
            noise={f: [k, float(sd)] for f, (k, sd) in d["noise"].items()},
            noise_corr={f: float(v) for f, v in (d.get("noise_corr") or {}).items()},
            noise_intensity=list(d.get("noise_intensity") or []), overrides=dict(d["overrides"]), dx=float(d["dx"]),
            carry=self.carry, actuators=[dict(field=a["field"], sign=int(a["sign"])) for a in d["actuators"]],
            derived=[dict(name=x["name"], source="observables.py", function=x["fn"].split(".")[-1]) for x in self.derived],
            fft_workers=1,
        )

    def world_imports_labkit(self):
        return bool(re.search(r"^\s*(from labkit\b|import labkit\b)", self.world_path.read_text(), re.M))

    def observables_source(self):
        """observables.py: the declared derived functions, verbatim from the scripts that define them."""
        if not self.derived:
            return None
        parts, origins = [], []
        for x in self.derived:
            module, name = x["fn"].rsplit(".", 1)
            path = DERIVED_SOURCES[module]
            text = path.read_text()
            node = next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == name)
            parts.append(ast.get_source_segment(text, node))
            origins.append(f"{path.relative_to(REPO)}::{name}")
        head = ('"""Observe-only channels of this lab bundle\'s world, ``fn(module, state)``.\n\n'
                "Copied verbatim from " + ", ".join(origins) + ".\n\"\"\"\n")
        return head + "import numpy as np\n\n\n" + "\n\n\n".join(parts) + "\n", origins

    def wrapper_source(self):
        b = self.bounded()
        if not b:
            return None
        inner = self.world_path.name
        return f'''"""Bundle entry point for {inner} with the suite's declared noise bounds.

The suite declares LabWorld.noise_bounds = {json.dumps(b)}: right after its dynamics noise is added,
each bounded field is projected onto its range. The physim-lab-bundle-v1 declaration has no noise_bounds key, so
this file makes the same projection at the start of each native step. LabStepper runs injection, noise, then the
world's step, so the step sees the same doubles (gc_bundle.py verify checks a frozen truth member bit for bit).
Everything else is {inner}, loaded from this folder as a fresh module.
"""
import importlib.util
from pathlib import Path

import numpy as np

NOISE_BOUNDS = {{{", ".join(f"{f!r}: ({lo!r}, {hi!r})" for f, (lo, hi) in b.items())}}}

_spec = importlib.util.spec_from_file_location(__name__ + "_inner", Path(__file__).with_name({inner!r}))
_inner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_inner)
P = _inner.P
init = _inner.init
if hasattr(_inner, "ops"):
    ops = _inner.ops


def step(s):
    for f, (lo, hi) in NOISE_BOUNDS.items():
        s[f] = np.clip(s[f], lo, hi)
    return _inner.step(s)
'''

    # -- suite --
    def _cases(self):
        s = self.src
        out = []
        for i, c in enumerate(s["cases"]):
            req = c["request"]
            if self.vortex:
                groups = [dict(g, unit=VORTEX_UNITS[0] if g["id"].startswith("global") else VORTEX_UNITS[1])
                          if "unit" not in g else g for g in s["groups"]]
                family, seed = c["program"], c["truth_seed"]
            else:
                groups = s["groups_by_horizon"][str(c["horizon"])] if "groups_by_horizon" in s else s["groups"]
                family, seed = c["family"], s["truth_seeds"][i]
            tpath = self.dir / c["truth"]
            with np.load(tpath, allow_pickle=False) as z:
                meta = json.loads(str(z["meta"]))
                arrays = [z[f"query{q}"].copy() for q in range(len(req["queries"]))]
                extra = sorted(k for k in z.files if k not in ("meta", "cpu_s") and not k.startswith("query"))
            # the frozen truth file must be this case's: same request (or actions), seed and member count
            same_request = meta.get("request", dict(id=req["id"], actions=meta.get("actions"), queries=req["queries"])) == req
            assert meta["members"] == 2 and meta["seed"] == seed and same_request, (req["id"], meta)
            assert "times" not in meta or all(q["t"] == meta["times"] for q in req["queries"]), (req["id"], meta)
            for q, a in zip(req["queries"], arrays):
                assert a.shape == (2, len(q["t"]), len(self.observed), {"device0": 13, "device1": 19, "global": 2}[q["sensor"]])
                assert a.dtype == np.float64 and np.isfinite(a).all()
            out.append(dict(request=req, family=family, groups=groups, truth=f"truth/{req['id']}.npz", seed=seed,
                            arrays=arrays, source_truth=str(tpath), source_truth_sha256=digest(tpath), extra_keys=extra))
        return out

    def suite(self):
        return dict(
            schema_version="physim-suite-v1", scoring_version=scoring.VERSION, contract_version=R6.APPARATUS_PROTOCOL,
            forecast_members=64, truth_members=2, predictor_seed=PREDICTOR_SEED, aggregation="equal-case-mean",
            cases=[dict(request=c["request"], family=c["family"], groups=c["groups"], truth=c["truth"]) for c in self.cases],
            truth_seeds=[c["seed"] for c in self.cases],
            source=dict(suite_dir=str(self.dir), suite_json_sha256=digest(self.dir / "suite.json"), schema=self.schema,
                        scoring_version=self.src["scoring_version"]),
            known_limits=[
                "One prepared state and one apparatus; not a held-out generalization benchmark.",
                "Two grading truths per case (copied from the frozen suite); scales are calibration-ensemble standard deviations.",
            ],
        )

    def report(self):
        obs = self.observables_source()
        return dict(
            suite_dir=str(self.dir), schema=self.schema, world=self.conv["world"], world_name=self.world_name(),
            taken=dict(
                world_file=dict(path=str(self.world_path), sha256=self.world_sha, checked_against="suite.json world_sha256"),
                labkit=[str(p) for p in LABKIT] if self.world_imports_labkit() else [],
                derived_functions=obs[1] if obs else [],
                devices=("gcv.device: square-13 ds 3 rot 0.3 / hex-19 ds 6 rot 1.1 at suite sites, node_perm "
                         "default_rng(41031+i).permutation(k)" if self.conv["devices"] == "gcv" else
                         "pmcips.device: square-13 ds 3 rot 0.3 / hex-19 ds 6 rot 1.1 at provenance sites + 0.5, "
                         "node_perm arange(k) (cross-checked with suite.json devices)"),
                port_permutation="identity (LW.oracle default in every gc script)",
                fft_workers="1 (gcv.one_worker / pmcips.one_worker)",
                preparation=dict(path=str(self.prep_path), sha256=self.prep_sha, loader=self.conv["loader"],
                                 kept_keys=self.fields + self.carry,
                                 dropped_keys=sorted(set(np.load(self.prep_path).files) - set(self.fields) - set(self.carry))),
                group_units="gc_vortex/suite.py report() labels" if self.vortex else "suite.json",
                carry=("null -> [] (init returns only the fields)" if self.decl_src["carry"] is None else self.carry),
                noise_bounds_wrapper=self.bounded() or None,
                scripts=self.conv["scripts"],
            ),
            cases=len(self.cases), observed=self.observed,
            actuators=[f"{a['field']}{'+' if a['sign'] > 0 else '-'}" for a in self.decl_src["actuators"]],
            truths=[dict(case=c["request"]["id"], family=c["family"], seed=c["seed"], source=c["source_truth"],
                         sha256=c["source_truth_sha256"], extra_keys=c["extra_keys"]) for c in self.cases],
        )


def write_json(path, value, compact=False):
    text = json.dumps(value, separators=(",", ":"), allow_nan=False) if compact else json.dumps(value, indent=1, allow_nan=False)
    Path(path).write_text(text + "\n")


def write_manifest(out: Path, inputs: Inputs, checks: dict | None = None):
    """fedvortex_bundle.write_manifest with this suite's source and recipe records."""
    if checks is not None:
        write_json(out / "checks.json", checks)
    decl = json.loads((out / "labworld.json").read_text())
    state = LB.read_state(out / "preparation.npz", decl)
    world_files = {p.relative_to(out).as_posix(): digest(p) for p in sorted((out / "world").rglob("*"))
                   if p.is_file() and "__pycache__" not in p.parts}
    try:
        world_source = str(inputs.world_path.relative_to(LAB))
        repository = "physim research/alife"
    except ValueError:
        world_source = str(inputs.world_path.relative_to(REPO))
        repository = "swpo/residency-environments"
    objects = {}
    objects["world"] = identified("world", dict(
        name=decl["name"], files=world_files, declaration_sha256=digest(out / "labworld.json"),
        implementation=LB.implementation_identity(),
        source=dict(world=world_source, lab_repository=repository, world_sha256=inputs.world_sha)))
    objects["preparation"] = identified("preparation", dict(
        world_id=objects["world"]["id"], file_sha256=digest(out / "preparation.npz"),
        state_sha256=LB.state_digest({k: np.asarray(v) for k, v in state.items()}),
        apparatus_sha256=digest(out / "apparatus.json"), noise_policy=R6.NOISE_POLICY, public_time=0,
        recipe=dict(prepared=str(inputs.prep_path), prepared_file_sha256=inputs.prep_sha, loader=inputs.conv["loader"],
                    script=Path(__file__).name)))
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


def checks(out: Path, work: Path, inputs: Inputs):
    """checks.json as fedvortex_bundle.checks: initial persistence through evaluation._forecast_suite, 4 members."""
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
    return write_manifest(out, inputs, value), value


def build(suite_dir: Path, out: Path, work: Path):
    t0 = time.process_time()
    inputs = Inputs(suite_dir)
    out, work = out.resolve(), work.resolve()
    if (out / "manifest.json").exists():
        raise SystemExit("completed bundles are immutable; choose a new output directory")
    if out.exists():
        shutil.rmtree(out)
    (out / "world").mkdir(parents=True)
    work.mkdir(parents=True, exist_ok=True)
    wrapper = inputs.wrapper_source()
    shutil.copyfile(inputs.world_path, out / "world" / (inputs.world_path.name if wrapper else "world.py"))
    if wrapper:
        (out / "world" / "world.py").write_text(wrapper)
    if inputs.world_imports_labkit():
        (out / "world" / "labkit").mkdir()
        for src in LABKIT:
            shutil.copyfile(src, out / "world" / "labkit" / src.name)
    obs = inputs.observables_source()
    if obs:
        (out / "world" / "observables.py").write_text(obs[0])
    write_json(out / "labworld.json", inputs.declaration())
    write_json(out / "apparatus.json", inputs.apparatus())
    np.savez_compressed(out / "preparation.npz", **inputs.preparation())
    suite = inputs.suite()
    write_json(out / "suite.json", suite, compact=True)
    size = (out / "suite.json").stat().st_size
    if size > 2 * 1024 * 1024:
        raise SystemExit(f"suite.json is {size} bytes, over the 2 MiB bundle JSON cap")
    (out / "truth").mkdir()
    for c in inputs.cases:
        np.savez_compressed(out / c["truth"], request=json.dumps(c["request"]),
                            **{f"query{q}": a for q, a in enumerate(c["arrays"])})
    write_manifest(out, inputs)
    manifest, value = checks(out, work, inputs)
    bundle = LB.open_bundle(out, profile="evaluation")
    bundle.check_runtime()
    for rec, c in zip(bundle.suite["cases"], inputs.cases):
        t = bundle.truth(rec)["samples"]
        assert all(np.array_equal(a, b) for a, b in zip(t, c["arrays"])), "truth arrays changed in packing"
    sim = LB.open_bundle(out, profile="simulation")
    sim.check_runtime()
    report = inputs.report()
    report.update(bundle=str(out), bundle_id=manifest["bundle_id"], suite_json_bytes=size,
                  bytes=sum(r["bytes"] for r in manifest["files"]) + (out / "manifest.json").stat().st_size,
                  files=len(manifest["files"]) + 1, n_ports=bundle.roster.n_ports, checks=value["reference"],
                  opened=dict(evaluation=True, simulation=True, check_runtime=True), cpu_s=time.process_time() - t0)
    write_json(work / "build.json", report)
    print(json.dumps({k: report[k] for k in ("bundle", "bundle_id", "cases", "n_ports", "bytes", "suite_json_bytes", "checks")}, indent=1))
    return report


def verify(bundle_dir: Path, case_id: str, out: Path):
    """Member 0 of one frozen truth, re-simulated through the bundle's own oracle (LabBundle.make_oracle)."""
    bundle = LB.open_bundle(bundle_dir, profile="evaluation")
    bundle.check_runtime()
    i = next(k for k, r in enumerate(bundle.suite["cases"]) if r["request"]["id"] == case_id)
    rec = bundle.suite["cases"][i]
    seed = bundle.suite["truth_seeds"][i]
    t0 = time.process_time()
    member = bundle.make_oracle().sample_truth(rec["request"]["actions"], rec["request"]["queries"], 1, truth_seed=seed)["samples"]
    cpu = time.process_time() - t0
    truth = bundle.truth(rec)["samples"]
    same = [bool(np.array_equal(m[0], t[0])) for m, t in zip(member, truth)]
    res = dict(bundle=str(bundle_dir), bundle_id=bundle.manifest["bundle_id"], case=case_id, family=rec["family"],
               actions=len(rec["request"]["actions"]), horizon_tu=max(max(q["t"]) for q in rec["request"]["queries"]),
               truth_seed=seed, member=0, bit_identical=all(same), per_query=same,
               max_abs_diff=[float(np.abs(m[0] - t[0]).max()) for m, t in zip(member, truth)],
               members_differ=[bool(not np.array_equal(t[0], t[1])) for t in truth], cpu_s=cpu)
    write_json(out, res)
    print(json.dumps(res))
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["inputs", "build", "verify"])
    ap.add_argument("--suite", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--work", type=Path)
    ap.add_argument("--bundle", type=Path)
    ap.add_argument("--case")
    a = ap.parse_args()
    if a.cmd == "inputs":
        print(json.dumps(Inputs(a.suite).report(), indent=1))
    elif a.cmd == "build":
        build(a.suite, a.out, a.work or a.out.parent / "work" / a.out.name)
    else:
        verify(a.bundle, a.case, a.out)
