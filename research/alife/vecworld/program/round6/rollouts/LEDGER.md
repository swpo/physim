# Ledger of model spend: first rollouts of round 6

PILOT_NEVER_REUSE_AS_EXAM. Every model call is real money. One row per rollout, written before the rollout starts
(bound by its caps) and completed after it ends (cost from the usage the provider reported, as saved in the trace).
Hard ceiling of this workflow: $40. A rollout whose caps allow more than $20 is not started.

Prices: Prime's Models API, `GET https://api.pinference.ai/api/v1/models`, field `pricing` of the model's entry
(read without a credential on 11 Nov 2026; the entry is saved next to each rollout as `model_entry.json`).

| # | rollout | model | price in / out / cache read ($ per M tokens) | bound by caps | status | tokens in | tokens out | cost | running sum |
|---|---|---|---|---|---|---|---|---|---|
| 0 | preflight ping for qwen_ring_001 (one request, `tools/ping_model.py`) | qwen/qwen3.6-35b-a3b | 0.11 / 1.01 / 0.099 | 16 output tokens | done 10:59 UTC, HTTP 200 | 258 | 2 | $0.00003 (the provider's own `cost` field said 0) | $0.00003 |
| 1 | qwen_ring_001 | qwen/qwen3.6-35b-a3b | 0.11 / 1.01 / 0.099 | $1.22 (see below) | ENDED 11:12 UTC, complete (40 model calls, stop condition `max_turns`, graded) | 758,132 billed (101,524 at the input price + 656,608 cache reads); the caps saw 18,759 | 18,888 | $0.1025 (all input at the full price; $0.0952 with the cache-read price; the provider's own `cost` fields sum to $0.0951) | $0.1025 |

Total spent by this workflow so far: **$0.10** of the $40 ceiling.

Scripted, model-free runs (the reference table, the dry run) cost $0 and are not listed.

## How a rollout's caps bound its bill (read this before sizing the next rollout)

The pinned config and RUNBOOK_MAC.md step 3 give the bound `max_total_tokens x p_in + max_output_tokens x p_out`
($0.23 for row 1). That is not a bound on the bill. verifiers checks `max_total_tokens` against the trace's
`num_total_tokens`, which counts each fed-in token once over the whole rollout (v1/session.py:83-113,
v1/trace.py:482-509); the provider bills the whole context again at every turn. The bill is bounded by

    max_turns x min(context window, tokens fed so far) x p_in  +  (max_output_tokens + sampling.max_tokens) x p_out

Row 1: 40 x 262,144 x $0.11/M + 68,192 x $1.01/M = $1.15 + $0.07 = $1.22. The same arithmetic for a model at
$5 in / $20 out per million with a 400 k context and 40 turns gives $80 + $1.4: the turn cap, not the token cap,
is what sizes an expensive rollout. Cost after a rollout is computed from the per-call usage in the trace
(sum of prompt tokens, cached tokens and completion tokens over the calls), never from `num_input_tokens`.
