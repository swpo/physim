"""Run one explicitly selected campaign stage, then stop for rollout review."""

import argparse
import fcntl
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/physim"))
from run_campaign import dump, ledger


def main(args):
    campaign = args.output.resolve()
    if (campaign / "HOLD.json").exists():
        raise RuntimeError("Campaign is held")
    models, worlds = args.models.split(","), args.worlds.split(",")
    with (campaign / ".batch.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        state = dict(
            phase="running_review_stage",
            stage=args.stage,
            pid=os.getpid(),
            updated_utc=datetime.now(timezone.utc).isoformat(),
            selected_models=models,
            worlds=worlds,
            expected_rollouts=len(models) * len(worlds),
            parallel_models=args.parallel_models,
            automatic_target_pause=False,
            ceiling_usd=None,
        )
        dump(campaign / "batch.json", state)
        logger = subprocess.Popen(
            [sys.executable, str(ROOT / "scripts/campaign_progress.py"), "--output", str(campaign)], cwd=ROOT
        )
        returncode = None
        try:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/physim/run_campaign.py"),
                    "--output",
                    str(campaign),
                    "--models",
                    args.models,
                    "--worlds",
                    args.worlds,
                    "--concurrent-worlds",
                    "3",
                    "--max-new-runs",
                    str(3 * len(models) * len(worlds)),
                    "--execute",
                    *(["--parallel-models"] if args.parallel_models else []),
                ],
                cwd=ROOT,
            )
            returncode = completed.returncode
        finally:
            record = ledger(campaign)
            dump(campaign / "ledger.json", record)
            state.update(
                phase="paused_for_review",
                runner_exit_code=returncode,
                updated_utc=datetime.now(timezone.utc).isoformat(),
            )
            dump(campaign / "batch.json", state)
            print(
                json.dumps(
                    {
                        "stage": args.stage,
                        "phase": state["phase"],
                        "reported_usd": record["reported_cost_usd"],
                        "reserve_usd": record["unreported_cost_reserve_usd"],
                    },
                    indent=2,
                ),
                flush=True,
            )
            # This local logger only reads receipts. It exits at the next tick.
            logger.wait(timeout=65)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--models", required=True)
    parser.add_argument("--worlds", default="bf,xv,p4g2_044")
    parser.add_argument("--parallel-models", action="store_true")
    main(parser.parse_args())
