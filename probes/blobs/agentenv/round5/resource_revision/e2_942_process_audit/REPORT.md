# Fable E2 #942: process and resource audit

**One completed fresh-resource episode. Six accepted submissions. No resource stop.** Reported skill is **0.6544984435867794**. This is the mean of six instance skills in this episode, not a cohort or comparative benchmark mean. Elapsed wall time is **5 h 49 m 22.1 s**.

The agent built real, narrower empirical models: actuator response, replay uncertainty, and emission RMS/decorrelation/shrinkage. Its submitted path did **not** roll a learned general dynamics model forward. L3F uses recorded-history interpolation. L3S also uses saved observations, including **actual future global samples collected before ready** for its out-of-base window. These are permitted strategies, not evidence of misconduct. They limit what successful scores establish about theory learning.

## 1. Exact scope and completion

- Trace `ae982494a72144c186f58a687a99cd33`; task `physim-BLOB2v2r2-E2#942`; world/seed `p6g8_033` / `942`.
- Exact nested ID on line 1 of `~/v3work/ops/recovery_20260905/eval_fable_r2/E2/traces.jsonl`; episode `11107cb8a9b94145b5c2e05868dc10dc`.
- Both outer and nested `ok=true`. Nested `is_completed=true`, `stop_condition=agent_completed`, no trace errors, `score_status=scored`, and `readied=1`.
- Start **2026-09-05 21:32:29.603Z**; scoring end **2026-09-06 03:21:51.695Z**. Wall time is not a billing measurement.
- Actual resource policy is **v2r2**, with safety caps: sensor 1,000,000,000; adjustment 10,000,000; injection 1,000,000; simulated tu 10,000,000; fork spawns 100,000; logical open forks 10,000; log entries 1,000,000. Resident cache is separately limited to eight forks with `lru-replay`.
- All seven cap-hit counters are zero. `resource_truncated=false`; `resource_stop={}`. Tool timeouts and provider errors below are not resource stops.

No canceled E2 #943, unscored E1 #929, short diagnostic, or other cohort enters these totals. The paired notes use the existing E1 #928 audit, not a new E1 trace analysis. This work only read local files and computed audit statistics with the project's `.venv/bin/python`. No episode code, prediction generator, simulation, evaluation, world query, GPU/SSH operation, or live-process change was run.

## 2. Recorded tokens, not estimated dollars

The installed verifiers `Usage` schema separates cache reads from `prompt_tokens`. The Anthropic adapter puts provider input **plus cache creation** into prompt. Reasoning is a subset of completion, not an extra output bucket.

| Reported quantity | E2 total |
|---|---:|
| `prompt_tokens` (excluding cache reads, including cache writes) | **5,979,370** |
| `cached_input_tokens` (cache reads) | **213,938,314** |
| All input = prompt + cache reads | **219,917,684** |
| `completion_tokens` (all output) | **2,265,077** |
| `reasoning_tokens` (reported subset of output) | **97,241** |
| Input + output, without adding reasoning again | **222,182,761** |
| Cache writes separately / provider input excluding writes | **Unavailable** |
| Billed dollars | **Unavailable** |

These are **2,218 sampled response-bearing model calls**, including delegated branches, out of **2,258 request records**. All 2,218 have input/output/cache usage. Reasoning is present for 2,217; the remaining response has zero output. Two responses omit `finish_reason`: call 1919/node 4291 has one tool call and 68 output tokens; call 1922/node 4372 is empty with zero output. Neither is silently dropped.

The other **40 request records are error attempts**: **38 HTTP 429 `rate_limited`**, and **two HTTP 400 `content_policy_violation`** (calls 1923–1924). None records usage. There is no `retry_of` linkage, so these are not 40 known retry chains. No missing or partial tokens are imputed.

`extra_usage=[]` records no judge/off-graph usage. It does not prove zero auxiliary calls. `/v1/messages/count_tokens` is relayed without trace recording, so its request count and usage are unavailable. No prices or dollar estimates are inferred from tokens or duration.

Sources: `.venv/lib/python3.13/site-packages/verifiers/v1/types.py:107–167`; `v1/dialects/anthropic.py:146–160,273`; `v1/trace.py:349–350`; `v1/dialects/base.py:113–115`. Current installed definitions were inspected, not asserted to be an immutable historical source snapshot. [summary.json](summary.json) and [accounting_evidence.json](accounting_evidence.json) retain exact accounting and error-call indices.

## 3. Calls, graph copies, and environment turns

The graph has **5,150 nodes** and **2,558 tool-call occurrences**. The audit counts only tool IDs issued by sampled nodes referenced by completed calls: **2,336 distinct invocations**. There are **2,319 distinct results**, not 2,357: **38 result IDs recur with identical message content in copied context**. For example, result nodes 196/282 share `toolu_016JRSCB44y68beVAKtXqA5m`. This graph duplication is **not** another fork request or evidence of a state race. The audit validates identical copies and uses the earliest original result.

| Environment tool | Issued | Plain success replies | Other recorded outcomes |
|---|---:|---:|---|
| read | 421 | 339 | 2 malformed ports; 75 timeouts; 5 missing results |
| fork | 103 | 100 | 3 timeouts |
| reset | 110 | 101 | 1 unknown context; 8 timeouts |
| adjust | 78 | 58 | 10 first-step refusals; 1 partial refusal; 2 unknown contexts; 7 timeouts |
| inject | 33 | 33 | — |
| wait | 466 | 357 | 103 timeouts; 6 missing results |
| status | 82 | 12 | 70 timeouts |
| ready | 1 | 1 | — |
| submit | 6 | 6 | — |

Total: **1,300 environment requests**, **1,007 plain success replies**, 11 apparatus refusals, five explicit argument/context errors, **266 timeouts**, and **11 missing results**. The **1,023 non-timeout/non-missing replies happen to equal the 1,023 persisted environment turns**. This numerical equality is not a transaction reconciliation: timeout work may commit, and other updates may fail to compose.

Other tools include **Bash 665**, **Write 276**, **Agent 35**, **Read 22**, **TaskStop 16**, **TaskUpdate 9**, **Edit 8**, and **TaskCreate 5**. Bash has 43 explicit nonzero exits and six missing results; Write has one tool-error reply. An Agent acknowledgment is not proof that a delegated task completed. Model calls, tool invocations, persisted environment turns, and read frames are different quantities.

## 4. Persisted resources and independent E2 state evidence

| Final meter | Value |
|---|---:|
| Live simulation | **14,655 tu** |
| Sensor charge | **199,320 slot-tu** |
| Adjustment / injection charge | **219.229 / 559.7** |
| Log entries | **577** |
| Fork spawns / resets | **97 / 96** |
| Base / fork read frames | **500 / 895** |
| Environment turns | **1,023** |
| Peak logical open / resident forks | **12 / 8** |
| Cache evictions / reconstructions | **3 / 121** |

Read meters count frames, not calls. Sensor charge is selected sensor slots × 5 tu per frame, independent of selected port count. Globals are free. Adjustment charge includes the first refused step. Injection charge is `abs(amp)*(1+4*max(0,abs(amp)-0.5))*dur`, not money. Base reads and reconstruction/replay work do not add live `sim_tu`. Reconstructions include cold initial construction; 121 is not simply 121 evicted-fork reloads.

Naive sums of response-bearing operations give **190,965 sensor charge; 219.208 adjustment; 563.7 injection; 14,030 simulated tu; 566 log entries; 500/845 base/fork read frames; 100 fork replies; 101 reset replies**. These differ from the final persisted values above, even though ordinary reply count and persisted turns both equal 1,023. Timeouts and missing replies are excluded from these sums, not assigned zero execution. The exact differences and current-source formulas are preserved in `experiment_summary.json#/reply_accounting`.

E2 was examined independently. Its **100 successful fork replies return 96 distinct handles**. Three handles recur; one is reported at different anchors. In nodes 231, 244, and 254, distinct calls return `f0f5c36cbb60175bbc5c4d62144c3fe31`, first at 2500 and later at 1000. These are not E1's same-node duplicate-fork pattern and not the copied result nodes described above. Per-anchor protocols, clock observations, exact tool IDs, and reply-derived meter sums are in [EXPERIMENTS.md](EXPERIMENTS.md), [CONCURRENCY.md](CONCURRENCY.md), and [experiment_summary.json](experiment_summary.json).

A clock scan compares 773 pairs where the earlier response is in the later sampled node's ancestor context. It finds 18 nonadditive deltas, including six backward movements; not every excess advance is itself contradictory because timed-out work can intervene. One unambiguous example: wait node 1960/result 1968 (`toolu_014nZFu3wyWvqVKNtmmPCrrp`) reports 1250, then zero-window read node 1969/result 1977 (`toolu_01QwZ7fdvtTf9upR3GwmC4j7`) reports 1225. Five handles also acknowledge reset twice. These observations do not form a simple additive serial experiment ledger.

The native `_with_state` path performs whole-state GET → function → PUT (`.venv/lib/python3.13/site-packages/verifiers/v1/mcp/server.py:175–206,227–249`). Different forks still share that rollout state. Matched anomalous observations must be reported separately from that plausible shared-state mechanism. The trace lacks native GET/PUT transaction times, commit IDs, timeout completion records, and a full state history. It cannot establish the exact interleaving or attribute every missing/stale observation to one cause. Persisted meters are the reported accounting, not proof that every server operation was charged there. This integrity issue is separate from whether a scientific task distinguishes observation lookup from learned dynamics.

## 5. Scientific workflow and submitted methods

The agent captured the base record, delegated fork-divergence and post-base runs, scanned actuator channels, collected free global streams, scanned all 13 emission ports, tested doses, fitted narrower empirical predictors, and revised them. It used 35 Agent invocations. Parallel collection and later more serial batches are visible; so are failures and changed hypotheses. [SCIENTIFIC_PROCESS.md](SCIENTIFIC_PROCESS.md) gives calibration counts, data quality limits, abandoned alternatives, and exact message/artifact references.

| Instance | Actual submitted path; target time(s) | Raw instance CRPS | Skill |
|---|---|---:|---:|
| L1 | Empirical actuator-distance contraction of device-0 record toward a local mean; **752.6** after one command. | 0.024033 | 0.522456 |
| L2 | Post-ready local rebuild: 0.7 device-pooled mean + 0.3 global mean at **1458.66**, repeated across all 13 hidden slots. | 0.082542 | 0.126002 |
| L3F | Cubic recorded-device interpolation at **1814.02, 1889.02, 2189.02**; calibrated replay/interpolation sigma. All are inside base 2500. | 0.003990 | 0.956350 |
| L3S | Saved-global interpolation and window averaging over **2260.72–2460.72** and **2660.72–2860.72**. The second is outside base but covered by pre-ready future samples. | 0.000849 | 0.951778 |
| L4 | Record + empirical RMS-derived shrinkage toward a local mean, with response uncertainty; port **6**, amp **2.7998**, dur **10.5**. Times **839.94, 854.94, 879.94, 929.94, 1004.94, 1079.94**. | 0.066575 | 0.404015 |
| L4D | Same RMS/decorrelation/shrinkage method; port **11**, amp **0.8124**, dur **16.78**. Times **1371, 1421, 1496**. | 0.002930 | 0.966390 |

Artifact references below are line numbers in the exact embedded `app/models/predictor3.py` string: L1 79–94, L3F 105–116, L3S 44–76 and 118–128, emissions 130–214. **Final L2 is not the saved `predict_L2` function at 97–103**: Bash node 5114, `toolu_01KwioQiU29N3GXNPj1gg4YA`, overrides its payload using the device/global blend. This is a marginal hidden-sensor estimate, not recovered hidden geometry.

### Global coverage is not the device continuation

A pre-ready fresh-anchor-2500 capture planned at node 4013 (`toolu_01FArZ3E2DiK4KjzcSpJQaCG`) recorded **16 global observations at 2525, 2550, …, 2900**, every 25 tu. These bracket the entire revealed second L3S window. The final code line 74–75 averages **41 linearly interpolated global samples** over each 200-tu window. It does not learn a dynamics law to reach 2860.72.

The device continuation is different: retained `cont_r1` saves have 80 distinct frames from 2505 to 3000, with a **2800 → 2905 gap**; `cont_r3b` adds 40 frames at 2905–3100. The combined device record ends at 3100 but is **not uniformly sampled at 5 tu** past 2500. Do not conflate that gap with the global stream used for L3S. The source comment calling the extension deterministic is the agent's interpretation, not a certified property.

### Emission response is a real narrower model, not a passive-mean-only copy of E1

For E2, measured per-port RMS `M` gives `alpha=clip(1-M²/(2*v),0,1)` and `mean=alpha*record+(1-alpha)*local_mean`; response magnitude/spread also changes sigma (`predictor3.py:168–209`). This changes the **mean**, unlike E1's two drawn dose cases. It is a fitted magnitude/decorrelation model, not a signed spatial-response template or general simulator.

The distinction between the two drawn ports has data support, not just scores. At training anchor 1200, amp 1, dur 10, the logged all-port device-1 RMS versus base at lags 175/250 was about **0.2249/0.2118 for injection port 6**, versus **0.0117/0.0108 for port 11** (node 2364 → 2365, `toolu_01YYUePYZxCJ71Foe7dctYBd`). A separate audit calculation from retained literal sensor observations finds port-6 versus port-11 RMS **0.22694/0.22093** at those lags. These support a much larger late response in that measured comparison, not a pure causal effect or hidden-condition truth.

The drawn L4 amplitude 2.7998 is above the apparatus limit 1. Its scaling beyond measured effective amplitude is heuristic and bounded; this episode's L4 CRPS 0.066575 / skill 0.404015 is a conditional strong-dose result, **not direct training validation above amp 1**. The two off-anchor validation examples use lower doses and L4D lags, not strong-dose lag-250 truth. Port 11's smaller measured residuals and near-baseline shrinkage must not be generalized to all ports or inferred from the high L4D skill alone.

## 6. Ready → closed-book payloads

Ready: **03:13:08.486Z**, node **5090 → 5091**, `toolu_017NUVZLCyYuN5ApLCGKPHa4`. Reported ready meters are **14,655 simulated tu / 1,016 environment turns**.

- **No sampled world-tool request after ready**: no read, wait, adjust, fork, inject, or reset. The nine Bash commands, eight Read calls, and one Edit are local file/predictor operations. No world transport appears in the inspected submitted path.
- Node 5092 builds all payloads from revealed parameters and `predictor3`. Node 5114 replaces L2 locally. Node 5128 fixes emission-sigma broadcasting; 5131 rebuilds L4/L4D with shape assertions; 5135 rounds those two payloads to four decimals. These changes precede their first accepted submissions, with no post-ready experiments.
- Six accepts, one each, in order **L3S, L1, L2, L3F, L4D, L4**. No rejected submissions or resubmissions. Every submitted payload object equals its archived `app/models/sub_*_i1.json` object exactly; hashes and tool IDs are in `summary.json` and [TIMELINE.md](TIMELINE.md).
- Final status, node **5147 → 5148**, `toolu_012PuXHtRXzJWggvxMdsgkqj`, reports all six flags true, phase revealed, head 2500, and `contexts=[]`. Status does not expose resource meters; these come from final trace metadata.
- Six submits plus one status account for **1,016 → 1,023 turns**. Simulated tu stays **14,655**. Post-ready work has 26 sampled model responses, one further 429 attempt, and 43,248 recorded output tokens.

No pre-ready tool request has a *recorded* result timestamp after ready. Missing replies and timed-out work still leave a late-server-work gap: absence of a later recorded result is not proof that no background server request remained. Node/result timestamps are not native execution times. See the bounded late-work evidence in `CONCURRENCY.md`.

## 7. Cheaper controls, not investigator restrictions

[POST11_PAIR_NOTES.md](POST11_PAIR_NOTES.md) gives two recommendations motivated by both cases: (1) a model-free native state/phase-gate regression with deterministic event barriers; (2) declared record/continuation and no-emission forecast controls, separated from genuine learned-dynamics and active-dose tests. These are future designs, not tests executed here. Neither requires pressure or time caps on investigators, a new rollout now, or a production fix. A diagnostic wiring pass is not a scientific performance estimate.

## Evidence gaps and reproducibility

The embedded workspace has **51 files**, including final predictor/code/payloads and selected fork data. **Twenty of 21 base-read replies retain only persisted-output previews in this archive**; none of those 20 full output files is embedded. Bulk base arrays, calibration NPY files, global JSONLs, and selected continuation files used by the final predictor are absent. Some values and file-writing commands survive in messages, but not the full generator input set. This audit verifies the path and accepted artifact equality; it does not claim full independent regeneration or validate every fitted coefficient.

- Count with `.venv/bin/python probes/blobs/agentenv/round5/resource_revision/e2_942_process_audit/audit_counts.py`.
- Validate audit invariants with the sibling `validate_audit.py`; this is static checking, not environment testing.
- Full input SHA-256: `d73404e732b895d795ec41cd18ac2cbcb3c929f63ad2d44dbf0a3e65f1dd3459` (11,116,033 bytes).
- Selected canonical trace SHA-256: `a9e4fb4c1c610eba8dd233061a9f76a11f3cd64cccb62b7c7192acd5990588f9`.

The input hash is checked before and after analysis. Unknown billing, auxiliary usage, retry chains, state transactions, missing data, and untested extrapolation are left unknown. No raw trace or credential material is copied into these outputs.
