# E2 #942 — parallel-state evidence and limits

Scope and reference convention: `EXPERIMENTS.md`. All trace references are to `E2/traces.jsonl:1`, trace `ae982494a72144c186f58a687a99cd33`. This is an audit of recorded behavior, not a concurrency experiment.

## What the current native code does

Installed `.venv/lib/python3.13/site-packages/verifiers/v1/mcp/server.py:175-206,227-249` performs:

1. Whole-state GET and validation.
2. A per-call context-variable state binding.
3. The tool function.
4. A whole-state PUT if serialized state changed.

Its own docstring says concurrent writes are last-write-wins and mutations that must compose must run sequentially. There is no transaction-wide lock or version check in this wrapper. Context-variable isolation is not atomic update composition. The PUT is after normal function return; a client timeout does not by itself tell us whether the function or PUT completed.

Current `environments/physim/physim/servers/blob.py:243-259` derives the fork ID from the state nonce and incremented fork counter. `:883-886` marks a reset fork closed. `:479-484` derives displayed time from anchor and persisted step count. This makes duplicate IDs, repeated successful resets, and nonmonotone clocks relevant observations. It does not reveal which historical GET or PUT produced them. Current source hashes are in the JSON; these are not runtime transaction logs or proof of an unchanged historical deployment.

## Observed parallel surface is not the same as state-transaction timing

Node 222 issues eight distinct `Agent` calls for divergence and continuation work. Example IDs: `toolu_01TbaPSD7i1NHhVs21NLkEjn` (800 r1) and `toolu_013T2gvmPSag6izZSLhXCDid` (2500 r2). Their fork requests occur on different sampled nodes. There is **no same-node pair of fork calls** in this trace.

There are 16 sampled nodes containing multiple probe calls, with 43 calls in total. These include reset batches and reset/fork pairs. Node 1359 has two distinct successful reset calls (`toolu_01KqfE5hnwGw52SNDsYhfYcR`, `toolu_01LCYYgNrgoAaZfhqLwU4nWt`); node 1362 has six; node 3778 has nine. This proves issued fan-out, not the start/end order of state transactions.

Result copies must not be mistaken for duplicate requests. For example one `wait` result exists at both nodes 4290 and 4366 with the same tool ID and content. The later node is a context copy. The script counts its request once.

## Reused fork IDs: three distinct groups

- `f0f5c36cbb60175bbc5c4d62144c3fe31` returns from three different tool IDs: `N231/toolu_01Q98BPC1T8jfWZ4qkpSgrCp/R262` and `N244/toolu_011SN9GVFrck7dTPgo3nii27/R257` both report anchor 2500; `N254/toolu_013AyMjGdioaX3Bdddx5AXk1/R267` reports anchor 1000. These are distinct issued requests, not copied results. The 2500 branches then read this ID and receive `t=1050` and `t=1100` at nodes 259 and 264. This handle cannot be treated as three disjoint forks or assigned a single experimental anchor.
- `f6a7e9aacb8b9f80ae25bd4e8f9300885` returns at `N2000/toolu_01SdtgEDdvgThqB14zzDFhku/R2007`. Adjustment `N2008/toolu_01BZtxJefUNqUZzXhKC3zBAC/R2009` says unknown context. A new fork request returns the same ID at `N2012/toolu_01GZnxGEVirpmsWqnvjfk2Ua/R2013`. Both fork replies claim anchor 1000.
- `ffc9b8eedc2a9a4c45f7421f00bbc4c08` follows the same observed pattern at anchor 1900: successful fork `N2808/toolu_0153NWfK75if4oVXnqqtA7sL/R2815`, unknown-context adjustment `N2816/toolu_01QjJ8Kgjrcdgsas9xpkM842/R2819`, then successful same-ID fork `N2820/toolu_0166D8A96kzUETieCpehoUcM/R2823`.

Status also exposes `f98e5306cd9c3ac1ef3092c7999559561` at anchor 1900 without a successful spawning reply: `N2983/toolu_01VZsXJiUSwfCsP1JZNGy6eT/R2986` and `N3770/toolu_019tnSGHpTG3aG69ArTfCKxr/R3777`. Three fork requests at 1900 timed out (nodes 2539, 2551, 2575). The trace does not identify which, if any, created this status-only ID.

## Reset and clock anomalies

There are 101 successful reset replies for 96 unique IDs. Five IDs return success twice, despite no additional acknowledged creation of those IDs. For example `fd0ea22b9a76b67320448471ee5a08672` resets successfully at `N1498/toolu_016BVH7SoyYzJ86v7Z78YquL/R1504`, appears open in status at node 2010/result 2011, and resets successfully again at `N3778/toolu_01X8gyacBfwfMb3AW81StgXk/R3779`. All five pairs are retained in the JSON. The difference of five from persisted resets is not a proof of exactly five overwritten reset transactions.

The clock scan makes 773 comparisons in which the earlier response is actually present in the later sampled node's ancestor context. It finds 18 nonadditive deltas: 10 shortfalls, including 6 backwards movements. Two backwards movements involve the multi-anchor alias. Some larger-than-expected deltas have intervening timed-out requests and are not contradictions by themselves.

Examples on IDs with one reported anchor:

| Prior reply | Later reply | Returned times | Later operation |
|---|---|---|---|
| `N206/toolu_01Q37VzQTWNgn9CULmPLuEY6/R291` | `N294/toolu_01FHYyE9wmPsTPh9XpPvLvsm/R337` | 825 → 825 | read window 5; expected +25 |
| `N626/toolu_01EJyRcHuXYrMZ57bfhuGaFo/R641` | `N659/toolu_01GT9c623cJfmRzAyCRHezey/R668` | 1625 → 1625 | read window 5; expected +25 |
| `N1960/toolu_014nZFu3wyWvqVKNtmmPCrrp/R1968` | `N1969/toolu_01QwZ7fdvtTf9upR3GwmC4j7/R1977` | 1250 → 1225 | read window 0 |
| `N3239/toolu_01EhcN8HDXscxt33b6pb1Wg3/R3251` | `N3252/toolu_017VLyxUzZDWq2XvWAHoaAjV/R3271` | 1350 → 1300 | read window 0 |
| `N3399/toolu_01H61zMFfYmhPomYb6PvXfV1/R3406` | `N3407/toolu_01BEAtbXC6G6vNSB8gho3Bo2/R3420` | 1355 → 1370 | wait steps 4; expected +20 |

For these five pairs there is no intervening sampled request with the same context argument between the two request nodes. Other-context whole-state writes and older unresolved work are not excluded. The evidence rules out treating all replies as one simple additive serial history. It does not name a particular racing request or prove a causal interleaving.

## Logical handles, residents, and reveal boundary

Persisted logical-open peak: **12**. Successful status also shows 12 contexts at nodes 1355, 2983, and 3770. Persisted resident peak: **8**. Cache evictions: **3**; rebuilds: **121**. These are different measures. Source `servers/blob.py:224-241,310-338` evicts live cache entries without closing logical handles and counts cold reconstruction, including initial fork construction. “121 rebuilds” does not mean 121 evicted-handle reloads. Exact replay work and final resident count are not recorded.

The last data-capture delegation is `N4949/toolu_012D3RcmDsXFVjz8tuLbUxjT/R5076`, with `run_in_background=false`. It asks for final divergence tails, a 2500 continuation, and 15 waits from anchor 600. Its result is recorded before ready. The last world timeout is `N4969/toolu_01QTXqdimPJPu1mJFbVvcZh3/R4971` (a read), not a post-reveal world call.

The final sampled world request is reset `N5071/toolu_01HaqHnniA29uTczm9EdUidj/R5072`, at 03:09:52.573 UTC; its result node is recorded at 03:10:01.749. Ready is `N5090/toolu_017NUVZLCyYuN5ApLCGKPHa4/R5091`, sampled at 03:13:08.486. The request-node gap is 195.914 seconds. After ready there are six submit calls and one status call, **no sampled world calls**, and no earlier world result first recorded after ready.

Eleven earlier world requests have no result in the trace (latest at node 4291). There are also 266 tool timeouts. The trace does not certify that all old work was cancelled or finished. Tool-result timestamps are recorder observations, not GET/function/PUT transaction timestamps. Do not invent a race across ready from this uncertainty.

Final status `N5147/toolu_012PuXHtRXzJWggvxMdsgkqj/R5148` reports revealed phase and zero logical contexts. Source `servers/blob.py:949-977` closes open handles at ready and removes their cache entries. There is no final live-registry snapshot. One emitted handle, `f3c076bc05f9903053cee60035ad54459`, lacks an explicit reset acknowledgment; this does not contradict ready closing remaining handles.

**Bottom line:** parallel-state exactness is not established. The E2 trace directly records ID reuse, reopening/reset repetition, and clock inconsistencies, while current native source permits whole-state last-write-wins. The trace cannot provide a transaction-exact history, a unique causal race, or exact total server work.
