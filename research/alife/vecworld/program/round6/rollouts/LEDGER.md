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
| 2 | preflight ping for astra_ring_001 (two streamed requests with tools, as the bash harness sends them: `tools/ping_stream.py`) | openai/gpt-6-astra | 10 / 50 / none listed | 2 x 2,048 output tokens ($0.21) | done 11:47 UTC, both answered, usage in the stream | 396 (182 + 214; 0 cached) | 24 (19 + 5; 0 reasoning) | $0.0052 (the provider's own `cost` fields: 0.0028 + 0.0024; the listed price gives the same) | $0.1077 |
| 3 | astra_ring_001 | openai/gpt-6-astra | 10 / 50 / none listed | $19.02 (22 turns, 70,000 total tokens, 16,384 per reply; see "Row 3" below) | ENDED 12:09 UTC, complete (14 model calls, stop condition `frozen` after an accepted submit, graded) | 193,826 billed (21,636 uncached + 172,190 cache reads); the caps saw 10,135 | 10,782 (5,242 of them reasoning) | $2.4774 (all input at the listed $10; the provider's own `cost` fields sum to $1.0188, so cache reads are billed below the listed input price, at a rate the Models API does not list) | $2.5851 |
| 4 | qwen_ring_002_cut (rehearsal of the round-4 pin from a request, `RUNBOOK_MAC.md` step 3; meant to be interrupted on purpose; its config asked for `reasoning_summary = "auto"`, ruling E14) | qwen/qwen3.6-35b-a3b | 0.11 / 1.01 / 0.099 | $2.0303 (`cap_usd` 2 + one worst-case call of $0.0303: the spend stop's bound, section "Rows 4 to 6" below) | ENDED BY ITSELF 17:27 UTC at its first model call: the route answered HTTP 400, `Unsupported request for this model (reasoning).` The run counts as failed and was graded on the baseline its box started with (skill -0.062, the null policy's score); nothing was interrupted | 0 (no usage reported) | 0 | $0.0303 as COUNTED by the spend stop (an error reply counts as one worst-case call); the provider reported no usage for the refused request, so the bill is probably $0 | $2.6154 |
| 5 | qwen_ring_002_cutb (rehearsal of the round-4 pin; default settings; INTERRUPTED ON PURPOSE after a few turns: the tool and vf-eval killed between two model calls, then the runbook's clean-up) | qwen/qwen3.6-35b-a3b | 0.11 / 1.01 / 0.099 | $2.0303 (`cap_usd` 2 + one worst-case call) | CUT 17:45 UTC after 4 model calls (25 s), on purpose; cleaned up and closed by the runbook's own commands (`--stage close`: cut, count complete); not graded | 25,875 billed (7,399 at the input price + 18,476 cache reads) | 166 | $0.0028 as counted by the spend stop (per call: usage at the listed prices, or the provider's own `cost` field where that was higher) | $2.6182 |
| 6 | qwen_ring_002 (rehearsal of the round-4 pin: ONE full rollout from a request, default settings and caps, to its natural end) | qwen/qwen3.6-35b-a3b | 0.11 / 1.01 / 0.099 | $2.0303 (`cap_usd` 2 + one worst-case call) | ENDED 18:41 UTC, complete (143 model calls, all streamed with usage; stop condition `agent_completed`: the agent stopped by itself after 38.5 of its 60 minutes; graded from the final collection, 0.786 of the oracle; packed, key scan clean: `qwen_ring_002/`) | 7,280,288 billed (681,239 at the input price + 6,599,049 cache reads) | 74,233 (0 reasoning) | $0.8050 as counted by the spend stop (per call: usage at the listed prices with the cache-read price, or the provider's own `cost` field where that was higher, 65 of 143 calls; $0.8758 with all input at the full price) | $3.4232 |
| 7 | qwen_ring_003 (rehearsal of the round-4 SECOND-PASS pin `841b4a1e1`, from a request: 30 turns, 15 minutes, `cap_usd` 0.5; the second pass's byte bounds and request-key allow-list in an ordinary run) | qwen/qwen3.6-35b-a3b | 0.11 / 1.01 / 0.099 | $0.5193 (`cap_usd` 0.5 + one worst-case call: 100,000 x $0.11/M + 8,192 x $1.01/M) | ENDED 21:24 UTC, complete (24 model calls, all streamed with usage, none refused; stop condition `agent_timeout`: the 15-minute wall time; graded from the final collection, the box's baseline: -0.029, the null policy's score; packed, key scan clean: `qwen_ring_003/`) | 254,533 (47,499 at the input price + 207,034 cache reads) | 5,792 (0 reasoning) | $0.0318 as counted by the spend stop (per call: usage at the listed prices with the cache-read price, or the provider's own `cost` field where that was higher) | $3.4550 |
| 8 | qwen_ring_004 (rehearsal of the round-5 pin `c48eb6dc2`, from a request: 60 turns, 18 minutes, `cap_usd` 1.0; the round-5 bounds and the new disclosures in an ordinary run) | qwen/qwen3.6-35b-a3b | 0.11 / 1.01 / 0.099 | $1.0193 (`cap_usd` 1.0 + one worst-case call: 100,000 x $0.11/M + 8,192 x $1.01/M) | ENDED 00:45 UTC 12 Nov, complete (60 model calls, all streamed with usage, none refused; stop condition `max_turns` after 790 s of 1,080; graded from the final collection: 0.316 of the oracle, no failed item; packed, key scan clean: `qwen_ring_004/`) | 1,696,119 (29,690 at the input price + 1,666,429 cache reads) | 33,274 (0 reasoning) | $0.2026 as counted by the spend stop (per call: usage at the listed prices with the cache-read price, or the provider's own `cost` field where that was higher) | $3.6576 |
| 9 | qwen_ring_005 (rehearsal of the round-5 SECOND-PASS pin `19b6beb83`, from a request: 40 turns, 15 minutes, `cap_usd` 0.5; the changed box run line and request routing in an ordinary run) | qwen/qwen3.6-35b-a3b | 0.11 / 1.01 / 0.099 | $0.5193 (`cap_usd` 0.5 + one worst-case call: 100,000 x $0.11/M + 8,192 x $1.01/M) | ENDED 01:59 UTC 12 Nov, complete (40 model calls, all streamed with usage, none refused; stop condition `max_turns` after 367 s of 900; graded from the final collection: the agent's predictor raised on the first public example, so all 64 items were scored with the null policy, 0.006 of the oracle; no infrastructure failure; packed, key scan clean: `qwen_ring_005/`) | 788,804 (82,151 at the input price + 706,653 cache reads) | 18,080 (0 reasoning) | $0.0978 as counted by the spend stop (per call: usage at the listed prices with the cache-read price, or the provider's own `cost` field where that was higher) | $3.7554 |

Total spent by this workflow so far: **$2.59** of the $40 ceiling by the listed prices ($0.1025 + $0.0052 + $2.4774, with the $0.00003 ping); **$1.12** by the provider's own cost fields ($0.0951 + $0.0052 + $1.0188).
With the three rehearsal rows 4 to 6 (counted by the spend stop of the round-4 pin; the provider's bill for them is not read here): **$3.42** ($2.5851 + $0.0303 + $0.0028 + $0.8050). The rehearsal's own standing go had a ceiling of $5, against which the tool counted rows 0 to 3 as spent elsewhere; after row 6 it stands at $3.42 of $5. With row 7 (the rehearsal job of the second-pass pin, $0.0318 counted): **$3.455**. With row 8 (round 5, $0.2026): **$3.6576**. With row 9 (round 5, second pass, $0.0978): **$3.7554**.

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

## Row 3 (astra_ring_001): the bound made exact, and what it costs the rollout

Price of `openai/gpt-6-astra` from the same Models API field: $10 in, $50 out per million tokens, no cache-read
price listed (all input is counted at $10), context window 1,050,000 tokens. The two-request ping (row 2) was
billed at exactly these prices (the provider's `cost` fields: $0.0028 = (182 x $10 + 19 x $50) / 1e6 and
$0.0024 = (214 x $10 + 5 x $50) / 1e6). With the pinned caps the formula above gives 40 x 1,050,000 x $10/M = $420.

What does bound the context of a call is `max_total_tokens`, for every call but the last:

- verifiers refuses a turn when `num_total_tokens` has reached the cap (session.py:83-113), and after every call
  `num_total_tokens >= that call's prompt tokens + completion tokens` (trace.py:178-189 and 482-509: a call's new
  input is its prompt beyond the previous call's prompt + completion, clamped at zero; reasoning tokens count as
  completion tokens).
- So a call that is followed by another has prompt + completion < M, and all completions before the last call
  sum to less than M. The last call may exceed M by the tool results of one reply (the harness cuts each result
  at 20,000 bytes, harnesses/utils/compaction.py:18) and its reply is at most `sampling.max_tokens`.

      bill <= [ (T - 1) x p_in + (p_out - p_in) ] x M  +  p_in x (M + D)  +  p_out x R
            = (10 T + 40) x M / 1e6  +  50 x R / 1e6  +  10 x D / 1e6        for $10 in, $50 out

  with T = `max_turns`, M = `max_total_tokens`, R = `sampling.max_tokens`, D = tokens of tool output returned by
  the last reply's tool calls.

Turns and total tokens therefore share ONE budget: at $20 and R = 16,384, (T + 4) x M <= 1.92 million.

| turns T | largest M under $20 | what it means |
|---|---|---|
| 150 | 12,400 | the task statement alone is 3,400 tokens |
| 40 | 43,600 | rollout qwen_ring_001 used 37,647 in its 40 turns with no reasoning tokens, and had not finished |
| 30 | 56,400 | |
| 22 | 73,700 | **chosen: T = 22, M = 70,000** (about 3,000 tokens of conversation per turn) |
| 16 | 95,900 | |

Chosen caps (coordinator's rulings of 11:42 UTC: no hidden cut; the bill bounded by turns x context at $20 or
less; the limits told to the agent): T = 22, M = 70,000, R = 16,384. Bound: $18.20 + $0.82 = **$19.02**, plus
$0.01 per 1,000 tokens of D: under $20 unless the last reply returns more than 98,000 tokens of tool output (at
least 10 results, each at the 20,000-byte limit). The caps do not exclude that case; if a single reply filled the
whole context window the last call alone would cost $10.50. Both limits are told to the agent in one sentence of
the system message (`configs/astra_ring_001.system_prompt.txt`). `max_output_tokens` is set to 70,000 so that it
cannot end the run before the total does; it is no part of the bound.

## Rows 4 to 6 (rehearsal of the round-4 pin): the bound is the spend stop's

From round 4 on a model rollout is started from a request (`../vfport/RUNBOOK_MAC.md`, step 3) and has a spend stop
in vf-eval (`../vfport/physim2_env/spend.py`): a call is sent only while what was counted so far, plus one
worst-case call for every call still under way, is below `cap_usd`, and no call's prompt can exceed
`max_context_tokens`. The bound on the bill is therefore

    cap_usd + one worst-case call = cap_usd + max_context_tokens x p_in + max_output_tokens_per_turn x p_out

For `qwen/qwen3.6-35b-a3b` at the prices listed on 11 Nov 2026 with the default caps (context 200,000, reply 8,192)
one worst-case call is 200,000 x $0.11/M + 8,192 x $1.01/M = $0.0303, and with `cap_usd` = 2 the bound is $2.0303.
The crude bound that the turn cap alone would give (150 turns x a full context window) is $5.57. The standing go
of the rehearsal has a ceiling of $5, of which the tool counts the $2.5851 of rows 0 to 3 as spent elsewhere.
