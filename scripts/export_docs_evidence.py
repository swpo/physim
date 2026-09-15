"""Export bounded, public report fields from saved results. Never runs a model.

Source hashes identify the records used. No prompts, traces, credentials, local
artifact paths, or hidden truth data are included in the public snapshot.
"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKED = ROOT / "probes/blobs/agentenv/round6/worked_example"


def read(path):
    return json.loads(path.read_text())


def provenance(path):
    return {"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    keys = (
        "run",
        "model",
        "harness",
        "verifiers",
        "protocol",
        "stop",
        "sampling",
        "native_limits",
        "model_calls",
        "experiments",
        "charged_tu",
        "score_kind",
        "primary_joint_energy",
        "grade_status",
        "provider_reported_cost_usd",
        "calls_without_reported_cost",
        "trace_sha256",
    )
    profiles = []
    for name, label, experiments, time in (
        ("verifiers_scaling_v1", "Initial resource profile", 20, 750),
        ("verifiers_highlimits_v1", "Expanded resource profile", 100, 5000),
    ):
        path = WORKED / "rollout" / name / "summary.json"
        rows = [{k: row.get(k) for k in keys} for row in read(path)["rows"]]
        for row, original in zip(rows, read(path)["rows"]):
            row["cost_ceiling_usd"] = original.get("spend", {}).get("limit_usd")
        profiles.append(
            {
                "id": name,
                "label": label,
                "experiment_limit": experiments,
                "integrated_time_limit": time,
                "source": provenance(path),
                "rows": rows,
            }
        )
    control_path = WORKED / "p4g2_044/predictor_sanity/results.json"
    controls = read(control_path)
    out = {
        "schema_version": 1,
        "snapshot_date": "2026-09-10",
        "scope": "Selected native development profiles; every attempt in each selected profile is retained. Earlier harness-development pilots are excluded.",
        "world": "p4g2_044",
        "prepared_instances": 1,
        "cases": 15,
        "model_forecast_members": 64,
        "truths_per_case": 2,
        "profiles": profiles,
        "controls": {
            key: controls[key] for key in ("aggregate", "prediction_members", "truth_members_per_case", "scoring")
        },
        "control_source": provenance(control_path),
    }
    dest = ROOT / "docs_source/results.json"
    dest.write_text(json.dumps(out, indent=2, allow_nan=False) + "\n")
    print(f"Exported {sum(len(p['rows']) for p in profiles)} attempts and control aggregates.")


if __name__ == "__main__":
    main()
