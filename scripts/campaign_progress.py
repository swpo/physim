"""Append human-readable local progress; no inference calls or run control."""

import fcntl
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "outputs/evaluation-campaign-20260916"


def read(path):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def snapshot():
    total, reported_total, completed, active, finished = 0.0, 0.0, 0, [], []
    batch = read(ROOT / "batch.json")
    selected = set(batch.get("selected_models", []))
    selected_worlds = set(batch.get("worlds", ["bf", "xv", "p4g2_044"]))
    stage_completed = 0
    reconciled = {(r["key"], r["attempt"]): r for r in read(ROOT / "ledger.json").get("attempts", [])}
    for path in sorted((ROOT / "attempts").glob("*/attempt.json")):
        attempt = read(path)
        if not attempt:
            continue
        cost, reported, calls, experiments, validated = 0.0, 0.0, 0, 0, 0
        for artifact in (path.parent / "artifacts").glob("*"):
            final = artifact / "spend_final.json"
            spend = read(final if final.exists() else artifact / "spend_state.json")
            cost += spend.get("accounted_cost_usd", 0.0)
            reported += spend.get("reported_cost_usd", 0.0)
            calls += spend.get("model_calls", 0)
            lab = read(artifact / "laboratory_state.json")
            experiments += lab.get("usage", {}).get("experiments", 0)
            validated += sum(c.get("kind") == "validate" for c in lab.get("checks", []))
        terminal = reconciled.get((attempt["key"], attempt["attempt"]))
        if attempt["status"] != "running" and terminal and terminal["status"] == attempt["status"]:
            cost = terminal["accounted_cost_usd"]
            reported = terminal["reported_cost_usd"]
            calls = terminal.get("model_calls", calls)
        total += cost
        reported_total += reported
        amounts = f"${reported:.4f} provider-reported + ${cost - reported:.4f} reserve"
        label = f"{attempt['model']} / {attempt['world']}"
        if attempt["status"] == "complete":
            completed += 1
            stage_completed += attempt["model"] in selected and attempt["world"] in selected_worlds
            reward = attempt.get("rewards", {}).get("prediction_reward", {}).get("score")
            finished.append((path.parent.name, f"FINISHED {label}: reward={reward}; {amounts}"))
        elif attempt["status"] == "running":
            token_note = ""
            if (ROOT / "prime_agent.json").exists():
                sys.path.insert(0, str(Path(__file__).resolve().parent / "physim"))
                from prime_usage import summarize

                prices = {m["id"]: m["pricing"] for m in read(ROOT / "catalog.json").get("data", [])}
                native = summarize(path.parent / "diagnostics", prices)
                token_note = (
                    f"; native usage: {native['fresh_input_tokens']:,} fresh/write input + "
                    f"{native['cached_input_tokens']:,} cached input, {native['output_tokens']:,} output; "
                    f"${native['reported_cost_usd'] + native['estimated_unreported_cost_usd']:.4f} "
                    "reported + token-estimated cost"
                    + (
                        " (cache discount unknown; counted at full input price)"
                        if native["undiscounted_cache_estimate"]
                        else ""
                    )
                )
            active.append(
                f"{label}: {attempt['status']}, {calls} calls recorded, {experiments} experiments, "
                f"{validated} validation attempts, {amounts}{token_note}"
            )
        else:
            finished.append(
                (
                    path.parent.name,
                    f"PAST ATTEMPT {label}, attempt {attempt['attempt']}: {attempt['status']} "
                    f"({attempt.get('stop_condition', 'unknown')}); {amounts}. Retained for review; not a new error.",
                )
            )
    state = (
        f"Current batch {stage_completed}/{batch.get('expected_rollouts', len(selected) * len(selected_worlds))} complete; "
        f"{completed} completed overall | provider-reported ${reported_total:.4f} + "
        f"unconfirmed-cost reserve ${total - reported_total:.4f} = budget-accounted ${total:.4f} | "
        f"queue={batch.get('phase', 'unknown')}"
    )
    return state, active, finished, batch.get("phase")


def main(root=None):
    global ROOT
    if root is not None:
        ROOT = Path(root).resolve()
    with (ROOT / ".progress.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        lock.write(str(os.getpid()) + "\n")
        lock.flush()
        seen = set()
        with (ROOT / "progress.log").open("a", buffering=1) as output:

            def log(message):
                stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
                output.write(f"{stamp} | {message}\n")

            log(
                "Progress logging started. Costs/call counts come from receipts, which can lag during a long tool operation."
            )
            while True:
                state, active, finished, phase = snapshot()
                for key, message in finished:
                    if key not in seen:
                        log(message)
                        seen.add(key)
                log(state)
                for message in active:
                    log(message)
                if phase in {"complete_pending_review", "paused_for_review"}:
                    log("Queue has stopped; see batch.json and batch.log for details. Progress logging finished.")
                    return
                with (ROOT / ".batch.lock").open("a") as controller:
                    try:
                        fcntl.flock(controller, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    except BlockingIOError:
                        pass
                    else:
                        log(
                            "Batch controller is no longer holding its lock. Check batch.log; progress logging finished."
                        )
                        return
                time.sleep(60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT)
    main(parser.parse_args().output)
