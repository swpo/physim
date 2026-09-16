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
