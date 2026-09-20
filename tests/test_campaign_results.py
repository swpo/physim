"""Reward aggregation must not pool cases, select successes, or favor repeats."""

import importlib.util
from pathlib import Path

import pytest


def summarize(rows):
    spec = importlib.util.spec_from_file_location(
        "campaign_results", Path(__file__).resolve().parents[1] / "scripts/campaign_results.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.summarize(rows)


def test_equal_world_weight_and_completed_zero_reward():
    rows = [
        dict(model="test", world=w, repetition=n, reward=r, cost_usd=c)
        for w, n, r, c in (("bf", 1, 0.2, 2), ("bf", 2, 0.4, 4), ("xv", 1, 0.9, 6), ("p4g2_044", 1, 0, 12))
    ]
    result = summarize(rows)["models"][0]
    assert result["mean_reward"] == pytest.approx(0.4)
    assert result["mean_cost_usd"] == 7
    assert result["worlds"]["p4g2_044"]["rewards"] == [0]


def test_no_aggregate_for_missing_world_and_no_best_of_n():
    row = dict(model="test", world="bf", repetition=1, reward=0.5, cost_usd=1)
    assert summarize([row])["models"] == []
    with pytest.raises(ValueError, match="best-of-N"):
        summarize([row, dict(row, reward=0.8)])


def test_unknown_cost_retains_all_rewards_without_fabricating_plot_cost():
    rows = [
        dict(model="test", world=w, repetition=1, reward=r, cost_usd=c)
        for w, r, c in (("bf", 0.3, 2), ("xv", 0.9, 6), ("p4g2_044", 0, None))
    ]
    result = summarize(rows)
    assert result["models"] == []
    assert result["incomplete_models"] == []
    pending = result["pending_cost_models"][0]
    assert pending["mean_reward"] == pytest.approx(0.4)
    assert pending["mean_cost_usd"] is None
    assert pending["worlds"]["p4g2_044"]["rewards"] == [0]


def test_held_campaign_cannot_be_aggregated(tmp_path):
    (tmp_path / "HOLD.json").write_text('{"reason":"prompt review"}')
    with pytest.raises(ValueError, match="held"):
        spec = importlib.util.spec_from_file_location(
            "campaign_held_test", Path(__file__).resolve().parents[1] / "scripts/campaign_results.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.collect(tmp_path)
