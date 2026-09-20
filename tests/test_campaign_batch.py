"""Batch admission keeps technical replacement separate from natural outcomes."""

import importlib.util
from pathlib import Path


def blockers(rows):
    path = Path(__file__).resolve().parents[1] / "scripts/run_open_batch.py"
    spec = importlib.util.spec_from_file_location("campaign_batch", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.blockers(rows)


def test_configuration_replacement_requires_review_and_keeps_retry_bound():
    row = dict(key="kimi-bf", attempt=1, status="limited", stop_condition="context_length")
    assert blockers([row])
    reviewed = dict(row, configuration_review=dict(cause="output_reservation", replacement_allowed=True))
    assert blockers([reviewed]) == []
    assert blockers([dict(reviewed, stop_condition="max_turns")])
    assert blockers([dict(reviewed, attempt=i) for i in (1, 2, 3)])


def test_completed_zero_is_never_retried_and_unknown_failure_still_blocks():
    assert blockers([dict(key="one", attempt=1, status="complete", reward=0)]) == []
    assert blockers([dict(key="one", attempt=1, status="needs_inspection")])


def test_budget_interruption_replacement_requires_review_and_keeps_retry_bound():
    row = dict(key="terra-xv", attempt=2, status="limited", stop_condition="dollar_budget")
    assert blockers([row])
    reviewed = dict(row, configuration_review=dict(cause="automatic_budget_stop_removed", replacement_allowed=True))
    assert blockers([reviewed]) == []
    assert blockers([dict(reviewed, stop_condition="context_length")])
    assert blockers([dict(reviewed, attempt=i) for i in (1, 2, 3)])


def test_reviewed_transport_failure_can_use_remaining_attempt():
    row = dict(key="kimi-bf", attempt=2, status="error", errors=[dict(type="HarnessError")])
    assert blockers([row])
    row["transport_review"] = dict(cause="mcp_cancelled_error_masked_transport", replacement_allowed=True)
    previous = dict(key="kimi-bf", attempt=1, status="limited")
    assert blockers([previous, row]) == []
    assert blockers([previous, row, dict(row, attempt=3)])


def test_invalid_request_stops_instead_of_replaying_rollout():
    for code in (400, 401, None):
        row = dict(key="gemini-bf", attempt=1, status="error", errors=[dict(type="ProviderError", status_code=code)])
        assert blockers([row])
    for code in (429, 503):
        row = dict(key="one", attempt=1, status="error", errors=[dict(type="ProviderError", status_code=code)])
        assert blockers([row]) == []


def test_runtime_replacement_requires_review_and_smoke_without_loosening_other_errors():
    row = dict(key="terra-xv", attempt=1, status="error", errors=[dict(type="HarnessError")])
    review = dict(
        cause="temporary_host_environment_package_files_removed",
        replacement_allowed=True,
        offline_smoke_passed=True,
    )
    assert blockers([row])
    assert blockers([dict(row, runtime_review=review)]) == []
    for changed in (
        dict(cause="unknown"),
        dict(replacement_allowed=False),
        dict(offline_smoke_passed=False),
    ):
        assert blockers([dict(row, runtime_review=review | changed)])
    assert blockers([dict(row, runtime_review=review, errors=[dict(type="ProviderError")])])
    assert blockers([dict(row, runtime_review=review, attempt=i) for i in (1, 2, 3)])
