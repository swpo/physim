"""Streaming updates must not double count tokens or present estimates as bills."""

import importlib.util
import json
from pathlib import Path

import pytest


def test_streaming_usage_keeps_latest_per_request_and_separate_cost_bases(tmp_path):
    module_path = Path(__file__).resolve().parents[1] / "scripts/physim/prime_usage.py"
    spec = importlib.util.spec_from_file_location("prime_usage_test", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    native = dict(
        input_tokens=2,
        output_tokens=50,
        cache_creation_input_tokens=1000,
        cache_read_input_tokens=10000,
        cache_creation=dict(ephemeral_1h_input_tokens=1000, ephemeral_5m_input_tokens=0),
    )
    events = [
        dict(time_ns=1, model="sonnet", path="/v1/messages", usage=dict(native, output_tokens=1)),
        dict(time_ns=1, model="sonnet", path="/v1/messages", usage=native),
        dict(
            time_ns=2,
            model="gpt",
            path="/v1/responses",
            usage=dict(input_tokens=200, output_tokens=5, input_tokens_details=dict(cached_tokens=100), cost=0.001),
        ),
    ]
    (tmp_path / "native-usage.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events) + '{"partial":')
    prices = {k: dict(input_usd_per_mtok=2, output_usd_per_mtok=10) for k in ("sonnet", "gpt")}
    result = module.summarize(tmp_path, prices)
    assert result["calls_with_usage"] == 2
    assert result["fresh_input_tokens"] == 1102
    assert result["cached_input_tokens"] == 10100
    assert result["output_tokens"] == 55
    assert result["reported_cost_usd"] == 0.001
    assert abs(result["estimated_unreported_cost_usd"] - 0.006504) < 1e-10


@pytest.mark.parametrize("catalog_cache_rate, expected", [(None, 0.1044), (0.3, 0.1144), (0, 0.0844)])
def test_opus_cache_reads_use_model_rate_or_explicit_catalog_override(tmp_path, catalog_cache_rate, expected):
    module_path = Path(__file__).resolve().parents[1] / "scripts/physim/prime_usage.py"
    spec = importlib.util.spec_from_file_location("prime_usage_opus_test", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    event = dict(
        time_ns=1,
        model="anthropic/claude-opus-5.5",
        path="/v1/messages",
        usage=dict(
            input_tokens=100,
            output_tokens=1000,
            cache_read_input_tokens=100000,
            cache_creation_input_tokens=11000,
            cache_creation=dict(ephemeral_5m_input_tokens=8000, ephemeral_1h_input_tokens=3000),
            output_tokens_details=dict(thinking_tokens=600),
        ),
    )
    (tmp_path / "native-usage.jsonl").write_text(json.dumps(event) + "\n")
    prices = {
        event["model"]: dict(input_usd_per_mtok=4, output_usd_per_mtok=20, cache_read_usd_per_mtok=catalog_cache_rate)
    }
    result = module.summarize(tmp_path, prices)
    # All four price buckets count once; thinking is already part of output.
    assert result["estimated_unreported_cost_usd"] == pytest.approx(expected)
    assert result["reported_cost_usd"] == 0
