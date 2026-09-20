"""Token-derived streaming cost estimates, separate from native billed costs."""

import json
from pathlib import Path


def summarize(directory, prices):
    path = Path(directory) / "native-usage.jsonl"
    latest = {}
    if path.exists():
        for line in path.read_text().splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue  # a concurrently appended final line
            latest[event["time_ns"]] = event
    result = dict(
        calls_with_usage=len(latest),
        fresh_input_tokens=0,
        cached_input_tokens=0,
        output_tokens=0,
        reported_cost_usd=0.0,
        estimated_unreported_cost_usd=0.0,
        undiscounted_cache_estimate=False,
    )
    for event in latest.values():
        u = event["usage"]
        p = prices[event["model"]]
        base = p["input_usd_per_mtok"]
        output = p["output_usd_per_mtok"]
        if event["path"] == "/v1/messages":
            writes = u.get("cache_creation_input_tokens") or 0
            cached = u.get("cache_read_input_tokens") or 0
            fresh = (u.get("input_tokens") or 0) + writes
            generated = u.get("output_tokens") or 0
            creation = u.get("cache_creation") or {}
            long = creation.get("ephemeral_1h_input_tokens", writes)
            short = creation.get("ephemeral_5m_input_tokens", 0)
            # Anthropic's documented multipliers; retain the raw native buckets.
            estimate = (
                (fresh - writes) * base
                + long * 2 * base
                + short * 1.25 * base
                + cached * 0.1 * base
                + generated * output
            ) / 1e6
        else:
            cached = (u.get("prompt_tokens_details") or u.get("input_tokens_details") or {}).get("cached_tokens") or 0
            fresh = (u.get("prompt_tokens", u.get("input_tokens", 0)) or 0) - cached
            generated = u.get("completion_tokens", u.get("output_tokens", 0)) or 0
            cache_rate = p.get("cache_read_usd_per_mtok")
            if cache_rate is None:
                cache_rate = base
                result["undiscounted_cache_estimate"] |= bool(cached and u.get("cost") is None)
            estimate = (fresh * base + cached * cache_rate + generated * output) / 1e6
        result["fresh_input_tokens"] += fresh
        result["cached_input_tokens"] += cached
        result["output_tokens"] += generated
        if u.get("cost") is not None:
            result["reported_cost_usd"] += u["cost"]
        else:
            result["estimated_unreported_cost_usd"] += estimate
    return result
