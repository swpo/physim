# Matched fork-ID and state-update anomalies

This is a local, read-only audit of trace `0bdd699154ee4e1d96aac4e0961bc11d` only. No transport tests, model runs, or simulations were launched.

## What is directly established

Counts use tool invocations in **sampled nodes referenced by completed model calls**. The trace has 1,216 such nodes. Their 1,484 tool IDs are all unique. Context copies in other nodes are excluded. Tool replies are joined by `tool_call_id`, not by proximity or prose.

- 183 distinct `fork` invocations: 181 success-shaped replies and 2 timeouts.
- Those 181 replies name 145 distinct fork IDs. This equals the final persisted `fork_spawns=145` counter.
- 22 fork IDs recur. 15 IDs occur with more than one reported anchor. There are 36 extra success replies beyond the 145 distinct IDs.
- Repeated successful requests from the same anchor are not automatically “retries.” Replicate experiments can intentionally use the same arguments.

### Example A: different anchors, one sampled response, same ID

Model call **252**, sampled node **670**. Model request: `2026-09-05T21:59:31.116Z` to `22:00:15.074Z`. The response issued three fork tools. Two matched call/result pairs are:

| Distinct tool-call ID | Arguments | Result node | Returned bounded fields |
|---|---|---:|---|
| `toolu_019HrrsqkepWErgE3qaYePh4` | `{"t":"200"}` | 677 | `{"fork":"f19c4cdc7ec9b88627088165738ebdb58","anchor_t":200.0,"t":200.0}` |
| `toolu_015SsBeffHzq5ZLv394MsoxF` | `{"t":"600"}` | 678 | `{"fork":"f19c4cdc7ec9b88627088165738ebdb58","anchor_t":600.0,"t":600.0}` |

Result-node timestamps: `22:00:34.382Z` and `22:00:34.383Z`. These are graph-recording times, not server GET/PUT timestamps. The two calls are not copied contexts or the same retry ID. Node 680 explicitly notices: “Two forks got the same id.” Its “collision” explanation is the model's interpretation.

### Example B: four anchors, one sampled response, same ID

Model call **730**, sampled node **1892**, response at `2026-09-05T22:43:32.975Z`.

| Tool-call ID | Requested anchor | Result node |
|---|---:|---:|
| `toolu_01EZL11gDR2nUHJoKzPuyumZ` | 730 | 1905 |
| `toolu_01AiB9StHzubg9NzQKFVTnRp` | 1210 | 1906 |
| `toolu_01BDhDrfVraEy4uWUH55a5uX` | 1875 | 1907 |
| `toolu_019r6LxkdkvSqXn7eVc41XmU` | 2450 | 1908 |

All four results return fork ID `f81bc24bb761d97965b53d229a8203ecb`. Each returns its own requested `anchor_t` and `t`. All four result nodes are recorded at `22:44:40.363Z`.

### Independent symptom: advancing reads do not compose

Sampled node **93** issues five distinct base reads, all `window=1`, `stride=1`, devices/ports `all`. Results **94–98** report times **160, 165, 165, 165, 165**. Four returned reads have the same advanced time; these are not zero-window rereads.

The first two tool IDs are `toolu_01FmnN2rPNCrGmA659Dt5vpb` and `toolu_01AfN4V2FuJWcZW8KjVgHhr4`; the remaining IDs are `toolu_013eUSB3WWsFjPmoDkhFvfnH`, `toolu_019nL22dXbKup4FSLUfECJmw`, `toolu_01K8X86xsrYmfSaYhiWkRgXp`. Result-node timestamps are `2026-09-05T21:40:26.957Z`.

## Why a state-update race is strongly supported

The installed native code shows:

1. `verifiers/v1/mcp/server.py:175–206`: `_pull_state` sends GET; `_push_state` serializes the current state and sends whole-state PUT.
2. `server.py:227–249`: `_with_state` pulls, runs the tool, then pushes. Its docstring says: **“Updates replace the whole state, so concurrent writes are last-write-wins. Mutations that must compose need to run sequentially.”** No lock is visible in this wrapper.
3. `environments/physim/physim/servers/blob.py:243–258`: `_fork_record` increments the state-local fork counter and derives the ID from `nonce|counter`. The 128-bit ID check is against that call's state snapshot.

Two concurrent calls that pull the same state can therefore use the same counter and issue the same ID for different anchors. Their full-state writes can overwrite each other. This also fits the repeated advancing-read times, the 40 unknown-context replies, and the reply-sum/meter gaps.

**Evidence limit:** the trace has no server-side GET/PUT transaction log. The exact overlapping requests, ordering of writes, and winning state cannot be reconstructed. The evidence establishes repeated IDs on distinct issued calls and non-composing replies. It strongly supports lost updates in this transport/state path. It does **not** establish a random 128-bit hash collision or prove which individual scientific samples were corrupted. The inspected source is current local code, not an immutable historical snapshot.

## Retry and response accounting are separate

- Model requests: **1,239 = 1,216 completed + 23 errors**. Errors: 22 HTTP 429; 1 connection reset. No error record carries usage. There is no `retry_of` field, so the trace cannot prove the number of successful retry chains.
- Environment calls: **1,065** distinct tool IDs; **1,063** recorded results. Results comprise 962 success-shaped replies, 2 partial adjustments then refusal, 1 first-step refusal, 40 unknown-context errors, 4 malformed-port errors, and 54 timeouts. Two status calls have no result.
- The 1,009 non-timeout/non-missing environment replies exceed **891 persisted turns by 118**. Turn increments happen before validation in the inspected environment methods. Success/rejection counts therefore cannot recover final committed state.
- Reset replies: 150 successes, 140 distinct named IDs, versus 133 persisted resets.

Do not add repeated responses to the persisted resource meters. Do not silently deduplicate real tool requests just because their arguments or returned IDs match. `experiment_register.json` preserves bounded per-call evidence for all repeated fork IDs.
