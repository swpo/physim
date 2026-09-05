"""Validate native resume bookkeeping on prepared COPIES only. Never launch an eval.

The caller must copy config.toml, traces.jsonl and eval.log to the staging
folders before running this script. load() prunes failed rows from those copies.
Original output directories are read-only inputs. The script records the original
six task keys and confirms the kept/owed counts before root authorizes retries.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from verifiers.v1.cli.eval.resume import load, load_resume_config
from verifiers.v1.cli.resume import task_key
from verifiers.v1.episode import WireEpisode

PROJECT = Path("/Users/spoho/Documents/prime/test/physim")
REPORT = PROJECT / "probes/blobs/agentenv/round5/recovery_20260905/native_resume_load_validation.json"
STAGING = Path("/Users/spoho/v3work/ops/recovery_20260905/eval_resume")
BASE = PROJECT / "outputs/physim--anthropic--claude-fable-5--claude_code"
RUNS = {
    "E2": "51d11a68-92fe-405f-aeb8-3b345bb69469",
    "E1": "588029cc-23dd-4b89-88e9-2813a3fa73b9",
}


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main() -> None:
    report = {
        "audit_utc": datetime.now(timezone.utc).isoformat(),
        "project_interpreter": str(PROJECT / ".venv/bin/python"),
        "native_api": "verifiers.v1.cli.eval.resume.load",
        "selected_keys_method": "native task_key(original task wire data), sorted by task data.idx",
        "copies_only": True,
        "eval_or_model_launched": False,
        "runs": {},
    }
    for menu, run_id in RUNS.items():
        original = BASE / run_id
        copied = STAGING / menu
        assert copied.resolve().is_relative_to(STAGING.resolve())
        assert copied.resolve() != original.resolve()
        original_hashes = {name: digest(original / name) for name in ("config.toml", "traces.jsonl", "eval.log")}
        rows = [json.loads(line) for line in (original / "traces.jsonl").read_text().splitlines() if line.strip()]
        rows.sort(key=lambda row: row["traces"][0]["task"]["data"]["idx"])
        selected_keys = [task_key(row["traces"][0]["task"]["data"]) for row in rows]
        assert len(selected_keys) == len(set(selected_keys)) == 3
        task_for_key = {
            task_key(row["traces"][0]["task"]["data"]): {
                "task_index": row["traces"][0]["task"]["data"]["idx"],
                "task_name": row["traces"][0]["task"]["data"]["name"],
                "world_seed": row["traces"][0]["task"]["data"]["world_seed"],
                "original_episode_id": row["id"],
                "original_trace_id": row["traces"][0]["id"],
            }
            for row in rows
        }
        episodes = [WireEpisode.model_validate(row) for row in rows]
        before = {
            "copy_trace_sha256": digest(copied / "traces.jsonl"),
            "original_hashes": original_hashes,
            "native_episode_checks": [
                {
                    **task_for_key[key],
                    "task_key": key,
                    "saved_outer_ok": row["ok"],
                    "saved_outer_errors": row["errors"],
                    "native_episode_ok": episode.ok,
                    "nested_trace_ok": [trace.ok for trace in episode.traces],
                    "nested_trace_errors": row["traces"][0]["errors"],
                }
                for key, row, episode in zip(selected_keys, rows, episodes)
            ],
        }
        assert before["copy_trace_sha256"] == original_hashes["traces.jsonl"], "Refuse a previously pruned or altered copy"
        config = load_resume_config(copied)
        assert config.num_tasks == 3 and config.num_rollouts == 1
        kept, owed = load(copied, selected_keys, config.num_rollouts)
        expected_kept = 2 if menu == "E2" else 0
        assert len(kept) == expected_kept
        assert sum(owed.values()) == 3 - expected_kept
        expected_owed_indices = [2] if menu == "E2" else [0, 1, 2]
        assert sorted(task_for_key[key]["task_index"] for key in owed) == expected_owed_indices
        assert all(episode.ok for episode in kept)
        after_hashes = {name: digest(original / name) for name in original_hashes}
        assert after_hashes == original_hashes, "Original files changed during validation"
        report["runs"][menu] = {
            "run_id": run_id,
            "copy_dir": str(copied),
            "original_dir": str(original),
            "before": before,
            "kept_count": len(kept),
            "kept_episode_ids": [episode.id for episode in kept],
            "kept_trace_ids": [trace.id for episode in kept for trace in episode.traces],
            "owed_count": sum(owed.values()),
            "owed": [{**task_for_key[key], "task_key": key, "num_rollouts": count} for key, count in owed.items()],
            "copy_trace_sha256_after_prune": digest(copied / "traces.jsonl"),
            "copy_trace_bytes_after_prune": (copied / "traces.jsonl").stat().st_size,
            "original_files_unchanged": after_hashes == original_hashes,
            "config_loaded_verbatim": True,
            "push": config.push,
            "resume_command_NOT_EXECUTED": f".venv/bin/eval --resume {copied}",
        }
    report["assertions_passed"] = True
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "report": str(REPORT),
        "assertions_passed": True,
        "runs": {menu: {key: data[key] for key in ("copy_dir", "kept_count", "owed_count", "original_files_unchanged")} for menu, data in report["runs"].items()},
    }, indent=2))


if __name__ == "__main__":
    main()
