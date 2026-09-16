"""Campaign admission and receipt accounting without model calls."""

import importlib.util
from pathlib import Path

import pytest


@pytest.fixture
def runner():
    path = Path(__file__).resolve().parents[1] / "scripts/physim/run_campaign.py"
    spec = importlib.util.spec_from_file_location("campaign_runner_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_resolved_campaign_has_unlimited_investigation_and_large_predictor(runner, tmp_path):
    model = dict(
        id="offline/test",
        specs=dict(context_window=100000, max_output_tokens=65000),
        pricing=dict(input_usd_per_mtok=1, output_usd_per_mtok=2),
        reasoning=dict(supported_efforts=["max", "high", "low"]),
    )
    config = runner.configuration(tmp_path, tmp_path, model, tmp_path / "bundle", 135)
    agent = config["env"]["agent"]
    assert all(agent[key] is None for key in ("max_turns", "max_input_tokens", "max_output_tokens", "max_total_tokens"))
    tools = config["env"]["taskset"]["task"]["tools"]
    assert all(
        tools[key] is None
        for key in ("max_experiments", "max_total_tu", "max_validation_attempts", "max_submission_attempts")
    )
    assert tools["predictor_limits"]["cpu_seconds"] == 3600
    assert agent["sampling"]["reasoning_effort"] == "max"
    assert config["env"]["taskset"]["task"]["spend"]["limit_usd"] == 135


def test_ledger_uses_final_receipt_once_and_keeps_retry_spend(runner, tmp_path):
    for i, cost in enumerate((0.5, 17.0)):
        attempt = tmp_path / "attempts" / str(i)
        runner.dump(attempt / "attempt.json", dict(key="one", launched=True, status="error" if i == 0 else "complete"))
        runner.dump(
            attempt / "artifacts" / "trace" / "spend_final.json", dict(accounted_cost_usd=cost, reported_cost_usd=cost)
        )
        runner.dump(
            attempt / "artifacts" / "trace" / "spend_state.json",
            dict(accounted_cost_usd=cost - 0.1, reported_cost_usd=cost - 0.1),
        )
    ledger = runner.ledger(tmp_path)
    assert ledger["accounted_cost_usd"] == 17.5
    assert ledger["target_usd"] == 50 and ledger["pause_ceiling_usd"] == 150


def test_missing_receipt_blocks_more_spending(runner, tmp_path):
    runner.dump(
        tmp_path / "attempts" / "interrupted" / "attempt.json", dict(key="one", launched=True, status="running")
    )
    with pytest.raises(RuntimeError, match="Missing spend receipt"):
        runner.ledger(tmp_path)
