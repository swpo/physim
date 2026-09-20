"""One-shot local queue for the approved evaluation batch.

Wait for the current rollout, then use the concurrent-world, spend-accounted
runner. No scheduler or assistant polling is involved. Ambiguous/limited runs
stop the queue for review; naturally completed model failures retain zero reward.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = ROOT / "outputs/evaluation-campaign-20260916"
MODELS = (
    "openai/gpt-5.6-terra",
    "anthropic/claude-sonnet-5",
)
DEFERRED_MODELS = ("deepseek/deepseek-v4.1-flash", "moonshotai/kimi-k2.6", "google/gemini-3.8-flash")
WORLDS = ("bf", "xv", "p4g2_044")


def records():
    return [json.loads(p.read_text()) for p in sorted((CAMPAIGN / "attempts").glob("*/attempt.json"))]


def blockers(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["key"]].append(row)
    problems = []
    for key, attempts in grouped.items():
        if any(row["status"] == "complete" for row in attempts):
            continue
        last = max(attempts, key=lambda row: row["attempt"])
        errors = last.get("errors", [])
        status_code = errors[-1].get("status_code") if errors else None
        retryable = (
            last["status"] == "error"
            and errors
            and errors[-1].get("type") == "ProviderError"
            and isinstance(status_code, int)
            and (status_code in {408, 409, 429} or 500 <= status_code < 600)
            and len(attempts) < 3
        )
        # A reviewed configuration interruption is replacement evidence, never
        # a best-of-N retry of a naturally completed model outcome.
        reviewed = last.get("configuration_review", {})
        retryable = retryable or (
            last["status"] == "limited"
            and last.get("stop_condition") == "context_length"
            and reviewed.get("cause") == "output_reservation"
            and reviewed.get("replacement_allowed") is True
            and len(attempts) < 3
        )
        retryable = retryable or (
            last["status"] == "limited"
            and last.get("stop_condition") == "dollar_budget"
            and reviewed.get("cause") == "automatic_budget_stop_removed"
            and reviewed.get("replacement_allowed") is True
            and len(attempts) < 3
        )
        transport_review = last.get("transport_review", {})
        retryable = retryable or (
            last["status"] == "error"
            and errors
            and errors[-1].get("type") == "HarnessError"
            and transport_review.get("cause") == "mcp_cancelled_error_masked_transport"
            and transport_review.get("replacement_allowed") is True
            and len(attempts) < 3
        )
        runtime_review = last.get("runtime_review", {})
        retryable = retryable or (
            last["status"] == "error"
            and errors
            and errors[-1].get("type") == "HarnessError"
            and runtime_review.get("cause") == "temporary_host_environment_package_files_removed"
            and runtime_review.get("replacement_allowed") is True
            and runtime_review.get("offline_smoke_passed") is True
            and len(attempts) < 3
        )
        if not retryable:
            problems.append({"key": key, "status": last["status"]})
    return problems


def main(execute=False, models=MODELS):
    if (CAMPAIGN / "HOLD.json").exists():
        raise RuntimeError("Campaign is held; review HOLD.json before preparing a new batch")
    if not models or len(set(models)) != len(models) or not set(models) <= set(MODELS):
        raise ValueError("Select a nonempty, unique subset of the approved models")
    expected = {f"{m.replace('/', '--')}-{w}-r1" for m in models for w in WORLDS}

    def selected_records():
        return [row for row in records() if row["key"] in expected]

    command = [
        sys.executable,
        str(ROOT / "scripts/physim/run_campaign.py"),
        "--models",
        ",".join(models),
        "--worlds",
        ",".join(WORLDS),
        "--rollouts",
        "1",
        "--max-new-runs",
        str(3 * len(models) * len(WORLDS)),
        "--concurrent-worlds",
        "3",
        "--execute",
    ]
    if not execute:
        print(
            json.dumps(
                {
                    "command": command,
                    "current_review_items": blockers(selected_records()),
                    "selected_models": models,
                    "deferred_models": DEFERRED_MODELS,
                    "target_usd": 50,
                    "automatic_target_pause": False,
                    "ceiling_usd": None,
                    "concurrent_worlds": 3,
                    "expected_rollouts": len(expected),
                },
                indent=2,
            )
        )
        return
    with (CAMPAIGN / ".batch.lock").open("a") as batch_lock:
        fcntl.flock(batch_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        source = Path(__file__).read_bytes()
        digest = hashlib.sha256(source).hexdigest()
        (CAMPAIGN / f"batch-controller-{digest}.py").write_bytes(source)

        def status(phase, **details):
            state = dict(
                phase=phase,
                updated_utc=datetime.now(timezone.utc).isoformat(),
                pid=os.getpid(),
                controller_sha256=digest,
                models=MODELS,
                selected_models=models,
                automatic_target_pause=False,
                ceiling_usd=None,
                concurrent_worlds=3,
                deferred_models=DEFERRED_MODELS,
                expected_rollouts=len(expected),
                worlds=WORLDS,
                **details,
            )
            tmp = CAMPAIGN / "batch.tmp.json"
            tmp.write_text(json.dumps(state, indent=2) + "\n")
            tmp.replace(CAMPAIGN / "batch.json")
            print(json.dumps(state), flush=True)

        status("waiting_for_current_rollout")
        # This is an OS lock wait, with no repeated assistant or model calls.
        with (CAMPAIGN / ".campaign.lock").open("a") as current:
            fcntl.flock(current, fcntl.LOCK_EX)
            problems = blockers(selected_records())
            if problems:
                status("paused_for_review", reasons=problems)
                return
        status("running_approved_batch")
        outcome = subprocess.run(command, cwd=ROOT)
        completed = {row["key"] for row in records() if row["status"] == "complete"}
        remaining = sorted(expected - completed)
        reports = []
        if outcome.returncode == 0:
            collected = subprocess.run([sys.executable, "scripts/campaign_results.py"], cwd=ROOT)
            reports.append({"step": "collect", "exit_code": collected.returncode})
            if collected.returncode == 0:
                data = json.loads((CAMPAIGN / "results.json").read_text())
                if data["models"]:
                    plotted = subprocess.run([sys.executable, "scripts/render_campaign_results.py"], cwd=ROOT)
                    reports.append({"step": "render", "exit_code": plotted.returncode})
        ready = not remaining and outcome.returncode == 0 and all(r["exit_code"] == 0 for r in reports)
        status(
            "complete_pending_review" if ready else "paused_for_review",
            remaining=remaining,
            runner_exit_code=outcome.returncode,
            reports=reports,
            visual_review_required=True,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--models", nargs="+", choices=MODELS, default=MODELS)
    args = parser.parse_args()
    main(args.execute, tuple(args.models))
