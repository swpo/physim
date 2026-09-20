"""Streaming updates must not double count tokens or present estimates as bills."""

import importlib.util
import json
from pathlib import Path


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
