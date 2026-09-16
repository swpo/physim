"""Regression checks for unbounded investigation and explicit predictor resources."""

from dataclasses import asdict
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from physim import taskset
from physim.blobround6_explore import ExperimentService
from physim.evaluation import _snapshot_inputs
from physim.sandbox import ExecutionLimitError, ExecutionLimits, Sandbox
from physim_r6.scaling import SpendConfig, spend_accounting


def test_unlimited_experiments_keep_accounting_and_request_validation():
    oracle = SimpleNamespace(sample_truth=lambda *args, **kw: {"samples": []})
    service = ExperimentService(oracle, max_experiments=None, max_total_tu=None)
    for _ in range(1001):
        service.experiment([], [{"sensor": "global", "t": [50]}])
    assert service.usage() == dict(experiments=1001, max_experiments=None, charged_tu=50050, max_total_tu=None)
    with pytest.raises(ValueError):
        service.experiment([], [{"sensor": "global", "t": [51]}])
    assert service.usage()["experiments"] == 1001


def test_null_caps_and_predictor_policy_round_trip_and_reach_prompt():
    config = taskset.R6ToolsConfig(
        max_experiments=None,
        max_total_tu=None,
        max_validation_attempts=None,
        max_submission_attempts=None,
        predictor_limits=ExecutionLimits(cpu_seconds=3600, wall_seconds=3600, cpus=4, memory_gib=8),
    )
    restored = taskset.R6ToolsConfig.model_validate_json(config.model_dump_json())
    assert restored == config
    prompt = taskset.public_prompt(config)
    assert "unlimited experiments" in prompt and "Validation attempts: unlimited" in prompt
    assert "3600 CPU seconds" in prompt and "8 GiB" in prompt
    assert "None" not in prompt


def test_predictor_configuration_reaches_validator(tmp_path):
    config = taskset.R6ToolsConfig(
        predictor_limits=ExecutionLimits(cpu_seconds=3600, wall_seconds=3600, cpus=4, memory_gib=8)
    )
    state = taskset.R6State(output=str(tmp_path))
    with (
        patch.object(taskset, "_snapshot", return_value={}),
        patch.object(taskset.E, "validate_predictor", return_value={"ok": True}) as validate,
    ):
        assert taskset._check(state, config, final=True)["accepted"]
        assert asdict(validate.call_args.kwargs["execution_limits"]) == asdict(config.predictor_limits)


def test_global_headroom_accepts_150_but_still_reserves_unknown_costs():
    config = SpendConfig(
        limit_usd=150, input_usd_per_mtok=1, output_usd_per_mtok=2, context_window=100000, max_response_tokens=10000
    )
    trace = SimpleNamespace(calls=[SimpleNamespace(usage=None)], extra_usage=[])
    assert spend_accounting(trace, config)["accounted_cost_usd"] == pytest.approx(0.12)
    with pytest.raises(ValueError):
        SpendConfig(**(config.model_dump() | {"limit_usd": 151}))


def test_grading_preserves_more_than_one_hundred_host_observations(tmp_path):
    source = tmp_path / "observations"
    source.mkdir()
    for i in range(101):
        (source / f"experiment_{i}.npz").write_bytes(b"host-generated fixture")
    rows = _snapshot_inputs(source, tmp_path / "frozen", observations=True)
    assert len(rows) == 101


def test_resource_kill_is_distinguishable_from_a_bad_predictor():
    box = object.__new__(Sandbox)
    box.name = "offline"
    box.limits = ExecutionLimits()
    with patch("physim.sandbox.docker"), patch.object(box, "invoke", return_value={"exit_code": 137, "output": ""}):
        with pytest.raises(ExecutionLimitError, match="possible resource limit"):
            box.prediction([], [], n_samples=1, seed=0)


def test_spend_hook_uses_native_verifiers_trace_boundary():
    import verifiers.v1 as vf
    from physim_r6.scaling import ScalingTask
    from verifiers.v1.session import hook_boundary

    assert hook_boundary(ScalingTask.dollar_budget, allow_trace=True) is vf.Trace
