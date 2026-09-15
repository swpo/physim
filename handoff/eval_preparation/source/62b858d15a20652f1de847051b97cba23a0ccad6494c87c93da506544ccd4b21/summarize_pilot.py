"""Keep a compact, source-linked receipt for a completed stock Verifiers pilot."""

import argparse
import json
from pathlib import Path

from physim.bundles import digest


def summarize(source, trace_path):
    source, trace_path = Path(source).resolve(), Path(trace_path).resolve()
    episode = json.loads(trace_path.read_text())
    if not episode["ok"] or len(episode["traces"]) != 1:
        raise ValueError("Expected one successful episode; retain failed attempts separately")
    trace = episode["traces"][0]
    artifact = Path(trace["info"]["r6"]["artifact_directory"])
    if not artifact.is_relative_to(source):
        raise ValueError("Pilot artifact is outside the specified world output")
    state = json.loads((artifact / "laboratory_state.json").read_text())
    grade = json.loads((artifact / "grade.json").read_text())
    calls = trace["calls"]
    usage = {}
    for key in ("prompt_tokens", "completion_tokens", "cached_input_tokens", "reasoning_tokens", "cost"):
        values = [call.get("usage", {}).get(key) for call in calls]
        usage[key] = sum(value for value in values if value is not None) if any(v is not None for v in values) else None
    result = dict(
        ok=episode["ok"],
        submitted=state["submitted"],
        status=grade["status"],
        models=sorted({call["model"] for call in calls}),
        calls=len(calls),
        stop_condition=trace["stop_condition"],
        laboratory_usage=state["usage"],
        inference_usage=usage,
        observed_horizons=[
            max((max(q["t"], default=0) for q in e["request"]["queries"]), default=0) for e in state["experiments"]
        ],
        primary_joint_energy=grade["primary_joint_energy"],
        by_family=grade["by_family"],
        valid_cases=grade["valid_cases"],
        total_cases=grade["total_cases"],
        references=grade["references"],
        grade_id=grade["id"],
        checks=[dict(kind=c["kind"], ok=c["validation"]["ok"]) for c in state["checks"]],
        trace_path=str(trace_path.relative_to(source)),
        trace_sha256=digest(trace_path),
        artifact_path=str(artifact.relative_to(source)),
        grade_sha256=digest(artifact / "grade.json"),
        predictor_files=grade["predictor"]["files"],
        source_sha256=digest(__file__),
        interpretation="One bounded development rollout, not a model benchmark. Cost is the sum of provider-reported call costs.",
    )
    (source / "pilot_summary.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--trace", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(summarize(args.source, args.trace), indent=2))
