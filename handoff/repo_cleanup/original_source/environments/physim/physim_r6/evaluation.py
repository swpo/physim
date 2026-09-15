"""R6 task validation and scoring, extracted unchanged from the v5 pilot.

No model client, conversation loop, retry policy, or harness lives here.
The checked-in worked example remains the private source of cases and truth.
"""
from datetime import datetime, timezone
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
WORKED = ROOT / "probes/blobs/agentenv/round6/worked_example"
HERE = WORKED / "rollout"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(WORKED / "p4g2_044"))
sys.path.insert(0, str(WORKED))
from isolation import Sandbox, SandboxError, IMAGE, docker
from origin import make_origin, file_digest
from contract import LIMITS
from physim import blobround6_eval as E

SUBMISSION_GATE_VERSION = "r6-gate-public-validation-v1"


def dump(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def read_prediction(sandbox, actions, queries, *, members=2, seed=11):
    case = dict(id="interface-check", actions=actions, queries=queries)
    shapes = E.validate_case(case, limits=LIMITS, allow_empty=True)
    data, execution = sandbox.prediction(actions, queries, n_samples=members, seed=seed)
    value = json.loads(data, parse_constant=E._reject_constant, object_pairs_hook=E._unique_object)
    arrays = E.validate_samples(value, shapes, members)
    return dict(samples=arrays), execution


def public_validation_cases():
    """Public API examples only; no case compiler, simulator or grading data."""
    mixed = [dict(sensor="device0", t=[0, .02]), dict(sensor="device1", t=[0]),
             dict(sensor="global", t=[0])]
    return [
        dict(name="mixed_sensors", actions=[], queries=deepcopy(mixed), n_samples=2, seed=11),
        dict(name="repeat_seed", actions=[], queries=deepcopy(mixed), n_samples=2, seed=11),
        dict(name="reordered_queries", actions=[], queries=list(reversed(deepcopy(mixed))), n_samples=2, seed=11),
        dict(name="empty_times", actions=[], queries=[dict(sensor="global", t=[]), dict(sensor="device1", t=[])], n_samples=2, seed=11),
        dict(name="empty_queries", actions=[], queries=[], n_samples=1, seed=11),
        dict(name="single_member_actions", actions=[
            dict(t=0, kind="inject", port=0, amp=1., dur=.02),
            dict(t=.02, kind="adjust", device=0, u=[.1, 0., 0.])],
            queries=[dict(sensor="device1", t=[0, .02, 5.02]), dict(sensor="global", t=[.02])], n_samples=1, seed=17),
        dict(name="default_members_repeated_sensor", actions=[], queries=[
            dict(sensor="global", t=[0]), dict(sensor="device0", t=[0, .02]),
            dict(sensor="device0", t=[.04])], n_samples=64, seed=23),
    ]


def validate_predictor(artifact, observations):
    """Run the public v5 gate; model code executes only inside Sandbox."""
    cases = public_validation_cases()
    report = dict(ok=False, gate=SUBMISSION_GATE_VERSION, checks=[],
                  checks_total=len(cases), experiments_used=0, integrated_tu=0,
                  scope="Public execution/interface checks only; no physical accuracy evaluation.")
    box = Sandbox(observations, artifact=artifact)
    baseline = None
    try:
        for case in cases:
            request = {k: v for k, v in case.items() if k != "name"}
            record = dict(name=case["name"], request=request,
                          expected_shapes=[[case["n_samples"], len(q["t"]), 12,
                                            {"device0":13, "device1":19, "global":2}[q["sensor"]]]
                                           for q in case["queries"]])
            try:
                prediction, execution = read_prediction(box, case["actions"], case["queries"],
                                                        members=case["n_samples"], seed=case["seed"])
                arrays = prediction["samples"]
                if case["name"] == "mixed_sensors":
                    baseline = arrays
                elif case["name"] == "repeat_seed" and not all(
                        np.array_equal(a, b) for a, b in zip(baseline, arrays)):
                    raise E.EvaluationError("repeated prediction calls with the same seed must reproduce output")
                record.update(ok=True, actual_shapes=[list(a.shape) for a in arrays],
                              wall_seconds=execution.get("wall_seconds"))
            except (SandboxError, E.EvaluationError, ValueError, TypeError) as exc:
                record.update(ok=False, error_type=type(exc).__name__, error=str(exc)[-3000:])
                report["checks"].append(record)
                report["failure"] = record
                break
            report["checks"].append(record)
        else:
            report["ok"] = True
    finally:
        box.close()
    report["checks_passed"] = sum(check["ok"] for check in report["checks"])
    return report


def grade(artifact, observations, output, *, members=64):
    # Predict every program and freeze those outputs BEFORE opening grader truths.
    from cases.build_cases import build_suite
    suite = build_suite("compact")
    saved, failures = [], []
    forecast_dir = output / "grading_predictions"
    forecast_dir.mkdir()
    for case in suite["public_cases"]:
        E.validate_plan(case, groups=suite["private"]["score_groups"][case["id"]],
                        n_samples=members, n_truth=2, limits=LIMITS)
        box = Sandbox(observations, artifact=artifact)
        try:
            predictor_seed = 20260908
            pred, execution = read_prediction(box, case["actions"], case["queries"], members=members,
                                               seed=predictor_seed)
            path = forecast_dir / (case["id"] + ".npz")
            np.savez_compressed(path, **{f"query{i}": value for i, value in enumerate(pred["samples"])})
            saved.append(dict(case_id=case["id"], file=path.name, sha256=file_digest(path),
                              request_digest=E.case_digest(case), predictor_seed=predictor_seed, execution=execution))
        except Exception as exc:
            failures.append(dict(case_id=case["id"], error=str(exc)[:3000]))
        finally:
            box.close()
    dump(forecast_dir / "manifest.json", dict(finalized_utc=datetime.now(timezone.utc).isoformat(),
                                              members=members, completed=saved, failures=failures,
                                              grader_truth_loaded=False))
    # Independent native truth was created before this pilot; no noise index pairing.
    truth_paths, truth_manifests = {}, []
    for dirname in ("native_validation", "native_supplemental"):
        directory = HERE.parent / "p4g2_044" / dirname
        manifest = json.loads((directory / "manifest.json").read_text())
        assert manifest["status"] == "COMPLETE"
        truth_manifests.append(dict(path=str(directory / "manifest.json"), sha256=file_digest(directory / "manifest.json")))
        for row in manifest["completed"]:
            path = directory / row["file"]
            assert file_digest(path) == row["sha256"]
            truth_paths[row["case_id"]] = path
    results = []
    cases = {case["id"]: case for case in suite["public_cases"]}
    for row in saved:
        cid, case = row["case_id"], cases[row["case_id"]]
        assert E.case_digest(case) == row["request_digest"]
        path = forecast_dir / row["file"]
        assert file_digest(path) == row["sha256"]
        with np.load(path, allow_pickle=False) as z:
            pred = dict(samples=[z[f"query{i}"] for i in range(len(case["queries"]))])
        with np.load(truth_paths[cid], allow_pickle=False) as z:
            assert json.loads(str(z["request"])) == case
            truth = dict(samples=[z[f"query{i}"] for i in range(len(case["queries"]))])
        score = E.score_case(case, pred, truth, groups=suite["private"]["score_groups"][cid],
                             n_samples=members, n_truth=2, limits=LIMITS)
        marginals = [np.asarray(q["crps_by_port_slot_mean_over_times"]) for q in score["marginal_crps"]]
        weights = [a.size * len(q["t"]) for a, q in zip(marginals, case["queries"])]
        results.append(dict(case_id=cid, family=suite["private"]["entries"][cid]["family"],
                            joint_energy=score["joint_energy_equal_group_mean"],
                            marginal_crps=float(np.average([a.mean() for a in marginals], weights=weights)), score=score))
    complete = len(results) == len(cases) and not failures
    report = dict(status="COMPLETE" if complete else "INVALID_PREDICTIONS", valid_cases=len(results), total_cases=len(cases),
                  primary_joint_energy=float(np.mean([r["joint_energy"] for r in results])) if complete else None,
                  marginal_crps=float(np.mean([r["marginal_crps"] for r in results])) if complete else None,
                  failures=failures, results=results, forecast_members=members, truth_members=2,
                  truth_policy="Reused independent native scheduler-validation realizations, never exposed to the model.",
                  truth_manifests=truth_manifests,
                  by_family={family: float(np.mean([r["joint_energy"] for r in results if r["family"] == family]))
                             for family in {r["family"] for r in results}})
    dump(output / "grade.json", report)
    return report
