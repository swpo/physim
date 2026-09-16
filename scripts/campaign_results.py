"""Collect completed campaign evidence with equal weighting of the three worlds."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean

WORLDS = ("bf", "xv", "p4g2_044")


def summarize(rows, worlds=WORLDS):
    grouped = defaultdict(lambda: defaultdict(list))
    seen = set()
    for row in rows:
        key = (row["model"], row["world"], row["repetition"])
        if key in seen:
            raise ValueError(f"Multiple eligible outcomes for {key}; never select best-of-N")
        seen.add(key)
        if row["world"] not in worlds or not 0 <= row["reward"] <= 1:
            raise ValueError("Unexpected world or invalid reward")
        grouped[row["model"]][row["world"]].append(row)
    complete, incomplete = [], []
    for model, by_world in sorted(grouped.items()):
        if set(by_world) != set(worlds):
            incomplete.append(dict(model=model, completed_worlds=sorted(by_world)))
            continue
        means = {
            world: dict(
                reward=mean(r["reward"] for r in by_world[world]),
                cost_usd=mean(r["cost_usd"] for r in by_world[world]),
                repetitions=len(by_world[world]),
                rewards=[r["reward"] for r in by_world[world]],
            )
            for world in worlds
        }
        complete.append(
            dict(
                model=model,
                mean_reward=mean(v["reward"] for v in means.values()),
                mean_cost_usd=mean(v["cost_usd"] for v in means.values()),
                worlds=means,
            )
        )
    return dict(models=complete, incomplete_models=incomplete)


def collect(root):
    rows, excluded, receipts = [], [], []
    for file in sorted((root / "attempts").glob("*/attempt.json")):
        attempt = json.loads(file.read_text())
        if attempt["status"] != "complete":
            excluded.append(dict(attempt=file.parent.name, status=attempt["status"]))
            continue
        artifact = file.parent / "artifacts" / attempt["trace_id"]
        spend_path = artifact / "spend_final.json"
        spend = json.loads(spend_path.read_text())
        audit = json.loads((artifact / "limit_audit.json").read_text())
        if audit["truncated"] or audit["length_finished_calls"]:
            raise ValueError(f"Attempt marked complete despite a binding limit: {file.parent.name}")
        if spend["calls_missing_cost"]:
            raise ValueError(f"Reconcile unreported provider cost before plotting: {file.parent.name}")
        reward = attempt["rewards"]["prediction_reward"]["score"]
        energy = attempt.get("energy")
        expected = 0 if energy is None else 1 / (1 + energy)
        if not math.isclose(reward, expected, abs_tol=1e-12):
            raise ValueError("Reward differs from the published mapping")
        row = dict(
            model=attempt["model"],
            world=attempt["world"],
            repetition=attempt["repetition"],
            reward=reward,
            energy=energy,
            cost_usd=spend["reported_cost_usd"],
            stop_condition=attempt["stop_condition"],
            usage=audit["usage"],
            source_id=attempt["source_id"],
            bundle_references=attempt["bundle_references"],
            attempt=file.parent.name,
        )
        rows.append(row)
        receipts.append(dict(path=str(file), sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
        receipts.append(dict(path=str(spend_path), sha256=hashlib.sha256(spend_path.read_bytes()).hexdigest()))
    return dict(
        **summarize(rows),
        rows=rows,
        excluded_attempts=excluded,
        sources=receipts,
        aggregation="Mean reward and cost within each world, then equal mean over BF, XV, and p4g2_044.",
        cost="Reported inference dollars per eligible rollout. Retry/failed-attempt costs remain in the campaign ledger.",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", type=Path, default=Path("outputs/evaluation-campaign-20260916"))
    args = parser.parse_args()
    result = collect(args.campaign.resolve())
    target = args.campaign / "results.json"
    target.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({k: result[k] for k in ("models", "incomplete_models", "excluded_attempts")}, indent=2))
