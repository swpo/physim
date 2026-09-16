"""Sequential, budget-accounted campaigns using stock Verifiers eval and task hooks.

Without --execute this only resolves configurations. Credentials stay in the
native Verifiers client; no token is read, written, or passed on a command line.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from physim.bundles import Bundle
from verifiers.v1.configs.cli.eval import EvalConfig

ROOT = Path(__file__).resolve().parents[2]
TARGET_USD = 50.0
CEILING_USD = 150.0


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def ledger(root):
    rows = []
    for attempt in sorted((root / "attempts").glob("*/attempt.json")):
        record = json.loads(attempt.read_text())
        receipts = []
        for artifact in sorted((attempt.parent / "artifacts").glob("*")):
            final, current = artifact / "spend_final.json", artifact / "spend_state.json"
            if final.exists() or current.exists():
                receipts.append(json.loads((final if final.exists() else current).read_text()))
        # Unknown spend must be reconciled before any subsequent paid run.
        if record.get("launched") and not receipts and record.get("status") != "zero_call_failure":
            raise RuntimeError(f"Missing spend receipt for {attempt.parent.name}; inspect before continuing")
        rows.append(
            dict(
                **record,
                accounted_cost_usd=sum(r["accounted_cost_usd"] for r in receipts),
                reported_cost_usd=sum(r["reported_cost_usd"] for r in receipts),
            )
        )
    return dict(
        target_usd=TARGET_USD,
        pause_ceiling_usd=CEILING_USD,
        attempts=rows,
        accounted_cost_usd=sum(r["accounted_cost_usd"] for r in rows),
        reported_cost_usd=sum(r["reported_cost_usd"] for r in rows),
    )


def configuration(root, attempt_dir, model, bundle, remaining):
    specs = model.get("specs") or {}
    pricing = model["pricing"]
    maximum = specs["max_output_tokens"]
    sampling = {"max_tokens": maximum}
    efforts = (model.get("reasoning") or {}).get("supported_efforts", [])
    if efforts:
        sampling["reasoning_effort"] = next(
            level for level in ("max", "xhigh", "high", "medium", "low") if level in efforts
        )
    else:
        sampling["extra_body"] = {"reasoning": {"enabled": True}}
    # No total turn/input/output-token or investigation cap. Provider context
    # and single-response maxima are model properties and explicitly retained.
    data = dict(
        model=model["id"],
        num_tasks=1,
        num_rollouts=1,
        max_concurrent=1,
        push=False,
        rich=None,
        serve=None,
        output_dir=str(attempt_dir / "runs"),
        run={"name": "rollout"},
        sampling=sampling,
        env={
            "taskset": {
                "id": "physim_r6_scaling",
                "task": {
                    "output_root": str(attempt_dir / "artifacts"),
                    "agent_image": "physim-agent:0.12.2",
                    "tools": {
                        "bundle": str(bundle),
                        "max_experiments": None,
                        "max_total_tu": None,
                        "max_validation_attempts": None,
                        "max_submission_attempts": None,
                        "predictor_limits": {
                            "cpu_seconds": 3600,
                            "wall_seconds": 3600,
                            "cpus": 4,
                            "memory_gib": 8,
                            "artifact_mib": 512,
                            "file_mib": 256,
                            "temporary_mib": 1024,
                        },
                    },
                    "spend": {
                        "limit_usd": remaining,
                        "input_usd_per_mtok": pricing["input_usd_per_mtok"],
                        "output_usd_per_mtok": pricing["output_usd_per_mtok"],
                        "cache_read_usd_per_mtok": pricing.get("cache_read_usd_per_mtok"),
                        "cache_write_usd_per_mtok": pricing.get("cache_write_usd_per_mtok"),
                        "context_window": specs["context_window"],
                        "max_response_tokens": maximum,
                    },
                },
            },
            "agent": {
                "max_turns": None,
                "max_input_tokens": None,
                "max_output_tokens": None,
                "max_total_tokens": None,
                "sampling": sampling,
                "timeout": {"setup": 180, "rollout": 604800, "finalize": 28800, "scoring": 86400},
                "harness": {"id": "bash", "edit": True, "search": False, "tool_timeout": 28800},
                "runtime": {
                    "type": "docker",
                    "image": "physim-agent:0.12.2",
                    "workdir": "/workspace",
                    "cpu": 4,
                    "memory": 8,
                    "allow": [],
                },
                "retries": {"max_retries": 0},
            },
            "retries": {"max_retries": 0},
        },
    )
    return EvalConfig.model_validate(data).model_dump(mode="json")


def completed_trace(attempt):
    paths = list((attempt / "runs").glob("*/traces.jsonl"))
    if len(paths) != 1:
        return None
    episodes = [json.loads(line) for line in paths[0].read_text().splitlines() if line.strip()]
    return episodes[-1]["traces"][-1] if episodes and episodes[-1].get("traces") else None


def execute(args):
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    lock = (root / ".campaign.lock").open("w")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    models = {r["id"]: r for r in json.loads((root / "catalog.json").read_text())["data"]}
    provenance = None
    if args.execute:
        provenance = json.loads((root / "provenance.json").read_text())
        for relative, expected in provenance["sources"].items():
            if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
                raise RuntimeError(f"Source changed after the campaign snapshot: {relative}; freeze a new snapshot")
    bundles = {w: (args.preparations / w / "bundle").resolve() for w in args.worlds.split(",")}
    for world, path in bundles.items():
        bundle = Bundle(path)
        bundle.check_runtime()
        if bundle.roster.protocol != "centered-pulse-v2":
            raise ValueError(f"{world} uses the old apparatus")
        validation = json.loads((path.parent / "native_validation.json").read_text())
        if not validation["ready"] or validation["references"] != bundle.references():
            raise ValueError(f"{world} has no matching completed validation")
    launched = 0
    for model_id in args.models.split(","):
        model = models[model_id]
        for repetition in range(args.rollouts):
            for world, bundle in bundles.items():
                key = f"{model_id.replace('/', '--')}-{world}-r{repetition + 1}"
                previous = [r for r in ledger(root)["attempts"] if r["key"] == key]
                if any(r["status"] == "complete" for r in previous):
                    continue
                for retry in range(len(previous), 3):
                    budget = ledger(root)
                    dump(root / "ledger.json", budget)
                    if budget["accounted_cost_usd"] >= TARGET_USD or launched >= args.max_new_runs:
                        print("Campaign paused between rollouts; see ledger.json", flush=True)
                        return
                    attempt = root / "attempts" / f"{key}-attempt{retry + 1}"
                    if attempt.exists():
                        raise RuntimeError(f"Inspect unfinished attempt before continuing: {attempt}")
                    config = configuration(root, attempt, model, bundle, CEILING_USD - budget["accounted_cost_usd"])
                    if not args.execute:
                        dump(root / "planned_configs" / f"{key}.json", config)
                        break
                    attempt.mkdir(parents=True)
                    dump(attempt / "eval.json", config)
                    dump(attempt / "provenance.json", provenance)
                    record = dict(
                        key=key,
                        model=model_id,
                        world=world,
                        repetition=repetition + 1,
                        attempt=retry + 1,
                        status="running",
                        launched=True,
                        started_utc=datetime.now(timezone.utc).isoformat(),
                        source_id=provenance["source_id"],
                        bundle_references=Bundle(bundle).references(),
                    )
                    dump(attempt / "attempt.json", record)
                    print(
                        f"Starting {key}, attempt {retry + 1}; campaign accounted ${budget['accounted_cost_usd']:.4f}",
                        flush=True,
                    )
                    with (attempt / "eval.log").open("w") as log:
                        run = subprocess.run(
                            [str(Path(sys.executable).with_name("eval")), "@", str(attempt / "eval.json")],
                            stdout=log,
                            stderr=subprocess.STDOUT,
                            cwd=ROOT,
                        )
                    launched += 1
                    trace = completed_trace(attempt)
                    if trace is None:
                        record.update(status="needs_inspection", exit_code=run.returncode)
                    else:
                        info = trace.get("info", {}).get("r6", {})
                        errors = trace.get("errors", [])
                        record.update(
                            status="complete" if trace.get("ok") else "error",
                            exit_code=run.returncode,
                            trace_id=trace["id"],
                            stop_condition=trace.get("stop_condition"),
                            errors=errors,
                            energy=info.get("primary_joint_energy"),
                            rewards=trace.get("rewards"),
                            limit_audit=info.get("limit_audit"),
                        )
                        if not trace.get("calls") and not trace.get("extra_usage"):
                            record["status"] = "zero_call_failure"
                        if trace.get("stop_condition") in {
                            "dollar_budget",
                            "context_length",
                            "max_turns",
                            "max_input_tokens",
                            "max_output_tokens",
                            "max_total_tokens",
                        }:
                            record["status"] = "limited"
                        if info.get("limit_audit", {}).get("length_finished_calls"):
                            record["status"] = "limited"
                        failures = info.get("grade", {}).get("failures", [])
                        artifact_path = Path(info.get("artifact_directory", attempt / "artifacts"))
                        state_path = artifact_path / "laboratory_state.json"
                        if state_path.exists():
                            for check in json.loads(state_path.read_text()).get("checks", []):
                                failures += check.get("validation", {}).get("checks", [])
                        if any(f.get("error_type") == "ExecutionLimitError" for f in failures):
                            record["status"] = "limited"
                    dump(attempt / "attempt.json", record)
                    budget = ledger(root)
                    dump(root / "ledger.json", budget)
                    print(
                        f"Finished {key}: {record['status']}; campaign accounted ${budget['accounted_cost_usd']:.4f}",
                        flush=True,
                    )
                    if record["status"] == "complete":
                        break
                    # The stock SDK already retries transient calls in-place.
                    # Whole-trajectory retries retain prior receipts and are only
                    # for captured provider faults, never low rewards/no predictor.
                    errors = record.get("errors", [])
                    if not errors or errors[-1].get("type") != "ProviderError":
                        print("Paused for limit/infrastructure inspection", flush=True)
                        return
                else:
                    print("Provider retry allowance exhausted; paused", flush=True)
                    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/evaluation-campaign-20260916")
    parser.add_argument("--preparations", type=Path, default=ROOT / "outputs/eval-preparation-20260916")
    parser.add_argument("--models", required=True)
    parser.add_argument("--worlds", default="bf,xv,p4g2_044")
    parser.add_argument("--rollouts", type=int, default=1)
    parser.add_argument("--max-new-runs", type=int, default=3)
    parser.add_argument("--execute", action="store_true")
    execute(parser.parse_args())
