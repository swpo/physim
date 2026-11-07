"""Credit-free, in-process proof of a lab bundle through PhySim's own task, validation and grading code.

    python prove_bundle.py local  --bundle BUNDLE --out OUT
    python prove_bundle.py oracle --bundle BUNDLE --out OUT --members M
    python prove_bundle.py debias --bundle BUNDLE --out OUT          (from oracle's frozen forecasts; no simulation)

local:
  1. taskset.required_bundle in both profiles; taskset.public_prompt (port lines must match the roster).
  2. One agent-style experiment through LaboratoryTools.experiment on an R6State (the copy into an agent container,
     _put_observation, is skipped: no runtime here): inject on device 1 for 10 tu, a device-0 move at t=1, readouts
     at t=0 on every sensor and up to 20 tu; its charge in tu is checked (20 tu = the last readout). Then an invalid
     port, which must be rejected without charge, and the usage tool.
  3. A simple predictor artifact, written as an agent would: predictor.py plus initial.npz, the experiment's t=0
     readouts (prepared-state readouts: the t=0 reading precedes any action's effect), repeated at every time and
     member (initial persistence). evaluation.validate_predictor runs the public validation cases on it.
  4. evaluation.grade grades it on the full suite, 64 members, exactly as a rollout's reward does, with LocalBox in
     place of the predictor container (LocalBox reads the frozen artifact archive like RuntimeSandbox and applies
     container_worker.py's output checks and JSON encoding, in this process).
oracle:
  evaluation.grade with OracleBox, whose predictions are the bundle's own native oracle (LabBundle.make_oracle) at M
  members per case, seeded by the grader's predictor seed (independent of the truth seeds). Forecasts are cached per
  request so a stopped run resumes.
debias:
  The scorer's energy is a V-statistic (ordered pairs including i=j), so an M-member forecast is penalized by
  0.5 E|X-X'| / M relative to the infinite ensemble. From the frozen forecasts and the truths, per group: cross term
  A and mean pairwise spread S (i != j); energy at K members = A - 0.5 (K-1)/K S. Reported at M (as graded), 4 (the
  suites' control ensembles) and 64 (a rollout's predictor).
No Prime sandbox, container or model call is made.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import asyncio
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import blobround6_eval as scoring  # noqa: E402
from physim import evaluation as EV  # noqa: E402
from physim import labbundle as LB  # noqa: E402
from physim import taskset as TS  # noqa: E402
from physim.artifact_store import archive_info, read_artifact_files, snapshot_artifact  # noqa: E402
from physim.rewards import DEFAULT_PRECISION, precision_reward  # noqa: E402
from physim.sandbox import ExecutionLimits  # noqa: E402

SLOTS = {"device0": 13, "device1": 19, "global": 2}

PREDICTOR = '''"""Initial persistence: the prepared state's t=0 readouts (from experiment_001), repeated."""
from pathlib import Path

import numpy as np

_DATA = np.load(Path(__file__).with_name("initial.npz"))
_INITIAL = {s: _DATA[s] for s in ("device0", "device1", "global")}


def predict(actions, queries, n_samples=64, seed=0):
    out = []
    for q in queries:
        x = _INITIAL[q["sensor"]]
        out.append(np.broadcast_to(x, (n_samples, len(q["t"])) + x.shape).copy())
    return {"samples": out}
'''


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=1, default=str, allow_nan=False) + "\n")


class LocalBox:
    """sandbox_factory stand-in: the frozen artifact's predictor.py run in this process (trusted local code only)."""

    def __init__(self, observations, *, artifact, limits=None):
        self.limits = limits or ExecutionLimits()
        self.dir = tempfile.TemporaryDirectory(prefix="local-predictor-")
        work = Path(self.dir.name) / "workspace"
        work.mkdir()
        info = archive_info(Path(artifact))
        if info is not None:
            for name, data in read_artifact_files(Path(artifact), info["files"]):
                (work / name).parent.mkdir(parents=True, exist_ok=True)
                (work / name).write_bytes(data)
        else:
            shutil.copytree(artifact, work, dirs_exist_ok=True)
        self.work = work

    def prediction(self, actions, queries, *, n_samples, seed, n_ports=12):
        started = time.monotonic()
        name = "local_predictor_" + hashlib.sha256(os.urandom(8)).hexdigest()[:12]
        spec = importlib.util.spec_from_file_location(name, self.work / "predictor.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.predict(json.loads(json.dumps(actions)), json.loads(json.dumps(queries)),
                                n_samples=n_samples, seed=seed)
        # container_worker.py's checks and encoding
        if type(result) is not dict or set(result) != {"samples"} or type(result["samples"]) is not list:
            raise ValueError("predict must return exactly {'samples': [array per query]}")
        if len(result["samples"]) != len(queries):
            raise ValueError("wrong number of query arrays")
        arrays = []
        for query, value in zip(queries, result["samples"]):
            array = np.asarray(value)
            expected = (n_samples, len(query["t"]), n_ports, SLOTS[query["sensor"]])
            if array.shape != expected or array.dtype.kind not in "iuf" or not np.isfinite(array).all():
                raise ValueError(f"array must have finite numeric shape {expected}, got {array.shape}")
            arrays.append(array.tolist())
        data = json.dumps(dict(samples=arrays), allow_nan=False, separators=(",", ":")).encode()
        return data, dict(exit_code=0, output="local in-process predictor", wall_seconds=time.monotonic() - started)

    def close(self):
        self.dir.cleanup()


class OracleBox:
    """sandbox_factory stand-in whose predictions are the bundle's native oracle (a trusted privileged control)."""

    bundle = None
    oracle = None
    cache = None
    cpu = 0.0

    def __init__(self, observations, *, artifact, limits=None):
        pass

    def prediction(self, actions, queries, *, n_samples, seed, n_ports=12):
        key = hashlib.sha256(json.dumps(dict(a=actions, q=queries, n=n_samples, s=seed), sort_keys=True).encode()).hexdigest()
        path = OracleBox.cache / f"{key[:24]}.npz"
        if path.exists():
            with np.load(path) as z:
                samples = [z[f"query{i}"] for i in range(len(queries))]
                cpu = float(z["cpu_s"])
        else:
            if OracleBox.oracle is None:
                OracleBox.oracle = OracleBox.bundle.make_oracle()
            t0 = time.process_time()
            samples = OracleBox.oracle.sample_truth(actions, queries, n_samples, truth_seed=seed)["samples"]
            cpu = time.process_time() - t0
            OracleBox.cpu += cpu
            np.savez_compressed(path, cpu_s=cpu, **{f"query{i}": a for i, a in enumerate(samples)})
            print(f"  oracle {n_samples} members, {max(max(q['t'], default=0) for q in queries)} tu: {cpu:.1f} cpu-s", flush=True)
        data = json.dumps(dict(samples=[a.tolist() for a in samples]), allow_nan=False, separators=(",", ":")).encode()
        return data, dict(exit_code=0, output="trusted native oracle", cpu_s=cpu)

    def close(self):
        pass


def check_prompt(config, bundle):
    text = TS.public_prompt(config)
    n = bundle.roster.n_ports
    expected = [f"`port` is an integer from 0 to {n - 1}.", f"Each measurement interface returns {n} channels.",
                f"shape `(1, number_of_requested_times, {n}, slots)`",
                f"(n_samples, number_of_requested_times, {n}, number_of_output_slots)"]
    missing = [e for e in expected if e not in text]
    leftover = [k for k in ("{n_ports}", "{last_port}", "{example_port}") if k in text]
    return dict(ok=not missing and not leftover, missing=missing, unreplaced=leftover, chars=len(text)), text


async def experiment(config, out: Path, n_ports: int):
    import verifiers.v1.mcp.server as S

    TS._put_observation = lambda state, path: None   # no agent runtime in this local check
    tools = TS.LaboratoryTools(config)
    state = TS.R6State(output=str(out), usage=dict(experiments=0, max_experiments=config.max_experiments,
                                                   charged_tu=0, max_total_tu=config.max_total_tu))
    (out / "observations").mkdir(parents=True, exist_ok=True)
    token = S._call_state.set(state)
    actions = [dict(t=0, kind="inject", device=1, port=1, amp=3.0, dur=10.0), dict(t=1, kind="adjust", device=0, u=[0.2, -0.1, 0.0])]
    queries = [dict(sensor="device0", t=[0, 5, 10]), dict(sensor="device1", t=[0, 10, 20]), dict(sensor="global", t=[0, 20])]
    try:
        t0 = time.process_time()
        good = json.loads(await tools.experiment(actions, queries))
        cpu = time.process_time() - t0
        bad = json.loads(await tools.experiment([dict(t=0, kind="inject", device=0, port=n_ports, amp=1.0, dur=1.0)],
                                                [dict(sensor="global", t=[1])]))
        usage = json.loads(await tools.usage())
    finally:
        S._call_state.reset(token)
    path = out / "observations" / Path(good["path"]).name
    with np.load(path, allow_pickle=False) as z:
        shapes = {k: list(z[k].shape) for k in z.files if k.startswith("query")}
        finite = all(np.isfinite(z[k]).all() for k in z.files if k.startswith("query"))
        initial = {q["sensor"]: z[f"query{i}"][0, 0] for i, q in enumerate(queries)}
    return dict(request=dict(actions=actions, queries=queries), admitted=good, rejected=bad, usage=usage,
                saved_shapes=shapes, finite=finite, recorded_experiments=len(state.experiments),
                rejected_requests=state.rejected_requests, charged_tu=good["usage"]["charged_tu"],
                charge_ok=good["usage"]["charged_tu"] == 20.0 and usage["charged_tu"] == 20.0 and usage["experiments"] == 1,
                cpu_s=cpu), initial, path


def local(bundle_dir: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    for name in ("lab", "artifact_src", "artifact", "naive_grade"):   # this step's outputs only (oracle's are kept)
        if (out / name).exists():
            shutil.rmtree(out / name)
    t0 = time.process_time()
    limits = ExecutionLimits()
    config = TS.R6ToolsConfig(bundle=bundle_dir.resolve(), max_experiments=1000, max_total_tu=50000)
    bundle = TS.required_bundle(config)
    sim = TS.required_bundle(config, profile="simulation")
    res = dict(bundle=str(bundle_dir), bundle_id=bundle.manifest["bundle_id"], type=type(bundle).__name__,
               n_ports=bundle.roster.n_ports, cases=len(bundle.suite["cases"]), simulation_profile_suite=sim.suite)
    res["prompt"], text = check_prompt(config, bundle)
    (out / "AGENT_SPEC.md").write_text(text)
    res["experiment"], initial, obs_file = asyncio.run(experiment(config, out / "lab", bundle.roster.n_ports))
    # cross-check: the experiment's t=0 readouts are the prepared-state readouts the packaged control uses
    ref = bundle.make_oracle().sample_truth([], [dict(sensor=s, t=[0]) for s in SLOTS], 1, truth_seed=0)["samples"]
    res["experiment"]["t0_equals_prepared_readouts"] = all(np.array_equal(initial[s], r[0, 0]) for s, r in zip(SLOTS, ref))
    art = out / "artifact_src"
    art.mkdir()
    (art / "predictor.py").write_text(PREDICTOR)
    np.savez(art / "initial.npz", **initial)
    frozen = out / "artifact"
    snapshot_artifact(art, frozen, limits)
    report = EV.validate_predictor(frozen, out / "lab" / "observations", roster=bundle.roster,
                                   execution_limits=limits, sandbox_factory=LocalBox)
    res["validation"] = dict(ok=report["ok"], checks_passed=report["checks_passed"], checks_total=report["checks_total"],
                             failure=report.get("failure"), gate=report["gate"])
    dump(out / "validation_report.json", report)
    grade = EV.grade(frozen, out / "lab" / "observations", out / "naive_grade", bundle=bundle, members=64,
                     run_context=dict(predictor="initial persistence artifact", harness="none (local)"),
                     execution_limits=limits, sandbox_factory=LocalBox, predictor_image="local-in-process")
    e = grade["primary_joint_energy"]
    res["naive"] = dict(predictor="initial persistence (artifact from experiment_001 t=0 readouts)", members=64,
                        status=grade["status"], valid_cases=grade["valid_cases"], total_cases=grade["total_cases"],
                        primary_joint_energy=e, reward_K2=precision_reward(e, DEFAULT_PRECISION) if e is not None else None,
                        checks_json=json.loads((bundle.root / "checks.json").read_text())["reference"]["primary_joint_energy"],
                        run_id=grade["id"])
    res["cpu_s"] = time.process_time() - t0
    dump(out / "local.json", res)
    print(json.dumps({k: res[k] for k in ("bundle_id", "prompt", "validation", "naive")}, default=str))
    print(json.dumps({k: res["experiment"][k] for k in ("charged_tu", "charge_ok", "rejected", "t0_equals_prepared_readouts", "cpu_s")}))


def oracle(bundle_dir: Path, out: Path, members: int):
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.process_time()
    bundle = LB.open_bundle(bundle_dir, profile="evaluation")
    bundle.check_runtime()
    OracleBox.bundle, OracleBox.cache = bundle, out / "oracle_cache"
    OracleBox.cache.mkdir(exist_ok=True)
    empty = out / "empty_artifact"
    empty.mkdir(exist_ok=True)
    (empty / "predictor.py").write_text("# the trusted native oracle predicts in OracleBox; no submitted code\n")
    obs = out / "no_observations"
    obs.mkdir(exist_ok=True)
    target = out / f"oracle_grade_m{members}"
    if target.exists():
        shutil.rmtree(target)
    grade = EV.grade(empty, obs, target, bundle=bundle, members=members,
                     run_context=dict(predictor="trusted native oracle", members=members),
                     execution_limits=ExecutionLimits(), sandbox_factory=OracleBox, predictor_image="local-in-process")
    e = grade["primary_joint_energy"]
    res = dict(bundle=str(bundle_dir), bundle_id=bundle.manifest["bundle_id"], members=members, status=grade["status"],
               valid_cases=grade["valid_cases"], failures=grade["failures"], primary_joint_energy=e,
               reward_K2=precision_reward(e, DEFAULT_PRECISION) if e is not None else None,
               by_family=grade["by_family"], simulation_cpu_s=OracleBox.cpu, cpu_s=time.process_time() - t0,
               run_id=grade["id"])
    dump(out / f"oracle_m{members}.json", res)
    print(json.dumps(res, default=str))
    debias(bundle_dir, out, members)


def debias(bundle_dir: Path, out: Path, members: int):
    bundle = LB.open_bundle(bundle_dir, profile="evaluation")
    grade_dir = out / f"oracle_grade_m{members}"
    grade = json.loads((grade_dir / "grade.json").read_text())
    by_case = {r["case_id"]: r for r in grade["results"]}
    rows = []
    for rec in bundle.suite["cases"]:
        case = rec["request"]
        with np.load(grade_dir / "grading_predictions" / f"{case['id']}.npz") as z:
            pred = [z[f"query{i}"] for i in range(len(case["queries"]))]
        truth = bundle.truth(rec)["samples"]
        A, S = [], []
        for g in rec["groups"]:
            def select(arrays):
                return np.column_stack([arrays[s["query"]][:, s["time_index"], s["port"], s["slot"]]
                                        for s in g["selectors"]]) / np.asarray(g["scales"])
            x, y = select(pred), select(truth)
            m = len(x)
            A.append(scoring._mean_rms_distance(x, y))
            S.append(scoring._mean_rms_distance(x, x) * m / (m - 1))
        A, S = np.asarray(A), np.asarray(S)
        e = {k: float(np.mean(A - 0.5 * (k - 1) / k * S)) for k in (members, 4, 64)}
        rows.append(dict(case=case["id"], family=rec["family"], graded=by_case[case["id"]]["joint_energy"], **{f"e{k}": v for k, v in e.items()}))
    agg = {k: float(np.mean([r[k] for r in rows])) for k in ("graded", f"e{members}", "e4", "e64")}
    res = dict(members=members, aggregate=agg, reward_K2={k: precision_reward(v, DEFAULT_PRECISION) for k, v in agg.items()},
               recomputed_matches_grade=bool(abs(agg["graded"] - agg[f"e{members}"]) < 1e-9), cases=rows)
    dump(out / f"debias_m{members}.json", res)
    print(json.dumps({k: res[k] for k in ("aggregate", "reward_K2", "recomputed_matches_grade")}))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["local", "oracle", "debias"])
    ap.add_argument("--bundle", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--members", type=int, default=2)
    a = ap.parse_args()
    {"local": lambda: local(a.bundle, a.out), "oracle": lambda: oracle(a.bundle, a.out, a.members),
     "debias": lambda: debias(a.bundle, a.out, a.members)}[a.cmd]()
