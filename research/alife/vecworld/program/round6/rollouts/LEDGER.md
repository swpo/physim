# Ledger of model spend: first rollouts of round 6

PILOT_NEVER_REUSE_AS_EXAM. Every model call is real money. One row per rollout, written before the rollout starts
(bound by its caps) and completed after it ends (cost from the usage the provider reported, as saved in the trace).
Hard ceiling of this workflow: $40. A rollout whose caps allow more than $20 is not started.

Prices: Prime's Models API, `GET https://api.pinference.ai/api/v1/models`, field `pricing` of the model's entry
(read without a credential on 11 Nov 2026; the entry is saved next to each rollout as `model_entry.json`).

| # | rollout | model | price in / out / cache read ($ per M tokens) | bound by caps | status | tokens in | tokens out | cost | running sum |
|---|---|---|---|---|---|---|---|---|---|
| 1 | qwen_ring_001 | qwen/qwen3.6-35b-a3b | 0.11 / 1.01 / 0.099 | $0.23 + one request (1.5 M total, 60 k out) | not started | | | | $0.00 |

Scripted, model-free runs (the reference table, the dry run) cost $0 and are not listed.
