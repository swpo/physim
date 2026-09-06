# Fable E1 #928: process and cost audit

**One completed fresh-resource run. Six accepted submissions. No resource stop.** The episode reward was **0.68066238**, the mean of this episode's six instance skills—not a cohort mean.

The main scientific result is narrower than the high forecast scores suggest: **L3F and L3E use recorded-history interpolation/counting. Both drawn dose instances use the undisturbed recorded mean, with dose-aware uncertainty.** A fitted port-2 response exists but was not used for either drawn dose mean. There is also strong evidence of non-composing concurrent state updates during exploration. This limits trust in the experiment history and prevents exact call-to-meter reconciliation.

## 1. Scope and completion

- Trace: `0bdd699154ee4e1d96aac4e0961bc11d`; task: `physim-BLOB2v2r2-E1#928`.
- World/seed: `p4g2_044` / `928`; resource policy: `v2r2`.
- Source: `~/v3work/ops/recovery_20260905/eval_fable_r2/E1/traces.jsonl`, exact nested ID on line 1. No other run or old capped success was included.
- Start: **2026-09-05 21:32:29.546Z**. Scoring finished: **2026-09-06 01:07:17.178Z**. Elapsed: **3 h 34 m 47.6 s**, not a billing estimate.
- `is_completed=true`, `ok=true`, `stop_condition=agent_completed`, `score_status=scored`. `resource_truncated=false`, empty `resource_stop`, and all seven cap-hit counters are zero.

Only local files were read. No new evaluation/model pilots, replay simulations, GPU work, SSH, or live process changes were used for this audit. Analysis ran through the project's `.venv/bin/python`.

## 2. Tokens and cost

The installed **verifiers v1 Usage** definition matters. `prompt_tokens` excludes cache reads. The Anthropic adapter combines provider `input_tokens` **plus cache-creation tokens** into that field. Reasoning tokens are already inside completion tokens; the adapter calls them a re-tokenized raw-thinking estimate, not an extra output charge.

| Reported quantity | Total |
|---|---:|
| `prompt_tokens`: non-cache-read input, including cache writes | **4,818,550** |
| `cached_input_tokens`: cache reads | **117,000,774** |
| All input: prompt + cache reads | **121,819,324** |
| `completion_tokens`: all output | **1,199,851** |
| `reasoning_tokens`: subset of output | **153,020** |
| Input + output, without double counting reasoning | **123,019,175** |
| Cache writes separately; uncached input excluding writes | **Unavailable** |
| Reported/billed dollars | **Unavailable** |

These totals cover **1,216 completed model calls**, including delegated branches. The trace has **1,239 model request records**: 1,216 completed, **22 HTTP 429 errors**, and **1 connection-reset error**. All 23 error records lack usage. Partial generation on the reset may be missing. No retry tokens or prices were imputed. There is no `retry_of` field, so error attempts are not counted as a known number of successful retry chains.

`extra_usage=[]` means no recorded judge/off-graph usage. It does **not** prove zero auxiliary requests: the installed adapter relays `/v1/messages/count_tokens` without recording those requests on the trace. Their count and usage are unavailable here.

Source definitions: `.venv/lib/python3.13/site-packages/verifiers/v1/types.py:107–167` and `v1/dialects/anthropic.py:146–160`. Repeated cached context is real reported token traffic, not unique scientific content. No dollar cost can be recovered from wall time or these merged buckets alone.

## 3. Tool and resource accounting

The 3,017-node message graph contains copied context. Counts below use the **1,216 sampled nodes referenced by completed calls**, and join results by unique tool ID. There are **1,484 distinct tool invocations**, **1,480 results**, and **22 Agent invocations**. All tool arguments parse as JSON; the four malformed calls below are port-format validation errors.

| Environment tool | Calls | Success-shaped replies | Other outcomes |
|---|---:|---:|---|
| read | 485 | 452 | 4 malformed ports; 8 unknown contexts; 21 timeouts |
| fork | 183 | 181 | 2 timeouts |
| reset | 160 | 150 | 5 unknown contexts; 5 timeouts |
| adjust | 112 | 99 | 2 partly applied then refused; 1 first-step refusal; 9 unknown contexts; 1 timeout |
| inject | 67 | 46 | 18 unknown contexts; 3 timeouts |
| status | 48 | 24 | 22 timeouts; 2 missing results |
| wait | 3 | 3 | — |
| ready | 1 | 1 | — |
| submit | 6 | 6 | — |

Thus **1,065 environment requests** produced 1,063 recorded results, including **54 timeouts** and **40 unknown-context errors**. A tool timeout is not a resource stop and does not establish whether server work committed.

Other tools: **Bash 324**, **Write 52**, **Agent 22**, **TaskUpdate 9**, **TaskCreate 5**, **TaskStop 4**, **Edit 3**. Bash has 13 explicit nonzero exits (9 two-minute command timeouts; 4 exit-code-1 results), one returned output with an embedded Python syntax error, and two missing results. Other non-environment calls have responses without explicit errors; Agent acknowledgments are not proof every worker finished successfully.

### Persisted environment meters

| Meter | Final value |
|---|---:|
| Live simulation | **11,495 tu** |
| Sensor charge | **145,405 slot-tu** |
| Adjustment charge | **219.721** |
| Injection charge | **814.3** |
| Log entries | **514** |
| Fork spawns / resets | **145 / 133** |
| Read frames: base / forks | **500 / 625** |
| Environment turns | **891** |
| Peak logical open / resident forks | **31 / 8** |
| Cache evictions / reconstructions | **44 / 168** |

Read meters count frames, not calls. Sensor charge is selected slots × 5 tu per read frame, independent of port count. Global statistics are free. Adjustment charge includes the first rejected step. Injection charge is `abs(amp)*(1+4*max(0,abs(amp)-0.5))*dur`, not dollars. Base reads and cold cache reconstruction do not add to `sim_tu`. The reconstruction counter includes cold initial construction; it is not simply 168 reloads after eviction.

### Important discrepancy: replies are not a committed experiment ledger

**181 successful fork replies name only 145 distinct IDs.** Twenty-two IDs recur; 15 have different reported anchors. A single sampled response at node 670 issues two distinct calls for anchors 200 and 600, and both replies return the same ID. Node 1892 does this for four anchors. Five advancing base reads in node 93 return times 160, 165, 165, 165, 165. These are real distinct tool IDs, not copied graph nodes.

The native state wrapper uses whole-state GET→tool→PUT and explicitly warns that concurrent writes are last-write-wins. These matched observations strongly support lost state updates, not a random 128-bit hash collision. The trace lacks transaction timestamps needed to prove the exact interleaving or identify every affected sample. See [CONCURRENCY.md](CONCURRENCY.md) for bounded call/result evidence.

Naively summing successful replies gives 11,860 simulated tu, 149,070 sensor charge, 229.865 adjustment charge, and 976.9 injection charge—**not** the final meters. It also gives 505/657 base/fork read frames and 562 log entries. The 1,009 non-timeout/non-missing environment replies exceed persisted turns by 118. Report the final meters as persisted accounting; do not claim they measure every piece of physical server work or silently reconcile the gaps away.

[EXPERIMENTS.md](EXPERIMENTS.md) gives per-anchor/protocol tables. The bounded [experiment_register.json](experiment_register.json) preserves exact response-bearing adjustment sequences, injection amplitudes/durations, and repeated-ID evidence. There were 62 reported anchors, all forked from base; no fork-from-fork experiments. Acknowledged emissions span amplitude 0.05–1.0 and duration 5–20 tu. Long reported trajectories include a 1,900-tu global sweep and a 605-tu post-base continuation.

## 4. What the agent investigated—and actually used

The run captured base data, probed actuator axes, compared fork continuations, scanned all 12 emission ports, tested dose scaling, fitted offline response/error models, and ran record-quality checks. It used 22 delegated tasks, often in parallel. Early “chaotic fork” interpretations changed after repeated/stale-context results. It stopped four workers after sustained timeouts, resumed data collection, and later ran major experiment batches serially. An anomalous port-2/anchor-900 data set was checked and its eight rows removed. The final response artifacts pooled anchors 1600/2100 instead.

Artifacts include `predict.py`, `predict_final.py`, `build_payloads.py`, L1 coefficients, replay sigmas, emission envelopes, a port-2 template, findings/playbook notes, and six payload files. **No custom dynamical simulator was used for these submissions.**

| Instance | Actual final method | Raw instance CRPS | Instance skill |
|---|---|---:|---:|
| L1 | Recorded device-0 values blended toward global means with fitted actuator response; cumulative command features and uncertainty. | 0.072269 | 0.2225 |
| L2 | Global nowcast/climatology choice per port; repeats marginal forecasts across hidden slots. No recovered hidden-sensor geometry. | 0.202600 | −0.0034 |
| L3F | Catmull–Rom record interpolation; circular interpolation for angle ports; empirical replay/interpolation sigma. | 0.000554 | 0.9964 |
| L3E | Interpolate port 4 on a 5-tu grid; count upward crossings over device-0 slots in 16 windows. | 0.123931 | 0.8856 |
| L4 | **Undisturbed recorded mean**, port-3 response envelope in sigma; amp 1.8696, dur 13.04. | 0.001939 | 0.9891 |
| L4D | **Undisturbed recorded mean**, port-1 envelope in sigma; amp 0.3295, dur 10.68. | 0.001284 | 0.9938 |

For L3F, `789.72 + 400 = 1189.72`; all four horizons are inside the readable base record. For L3E, `1694.78 + 800 = 2494.78`, also inside it. The actual code calls `record_at`, rather than rolling a learned dynamics law forward. **This is permitted pre-reveal recorded-history use, not observed post-ready access or proof of a leak.** It also is not proof of transferable theory learning.

The emission model has an empirical port-2 template and scale `amp**1.3*(dur/10)**0.85`. Only port 2 changes the mean. The drawn ports were **3 and 1**, so that fitted mean response was unused. For these instances, high dose skill is consistent with baseline history plus weak observed effects and calibrated uncertainty—not demonstrated strong-response extrapolation. L4D's uncertainty scale is floored at 1.0.

L1 used 81 reported command-step samples, with 60 fit / 21 calibration samples selected by every-fourth-sample holdout. This is not an independent anchor/trial holdout. Most raw fit inputs are absent from the archived workspace, so their full provenance cannot be independently replayed here. See [SCIENTIFIC_PROCESS.md](SCIENTIFIC_PROCESS.md) for source lines and evidence, including failed hypotheses and validation limits.

## 5. Ready → closed-book submission

The agent requested ready at **00:58:27Z**: node 2970, tool `toolu_01UJUVLKFPZJwjCTUQWafJko`. The next model request already contained the reveal. The ready counters were **11,495 simulated tu / 884 environment turns**.

After ready:

- **Zero world-tool calls.** All ten Bash commands inspect local files or run the saved offline predictors; no world transport appears in them.
- Two local predictor edits: sequentially clamp cumulative L1 u3 to `[0,1]`; increase the L3E sigma floor/scale. These were allowed offline changes, not new experiments.
- Six submissions, once each, in order **L3E, L1, L2, L3F, L4, L4D**. All returned `ok=true`; all submitted payload objects exactly match their archived payload files.
- One status call confirmed all six `submitted=true` and no open contexts.

The final seven environment turns are exactly six submits plus one status: **884 → 891**. Simulation stays at 11,495 tu. There were 19 completed post-ready model calls and one further 429 error; their recorded output totals 48,103 tokens. [TIMELINE.md](TIMELINE.md) lists exact submission IDs/times and annotated milestones.

## 6. A cheaper test ladder, without restricting the science

Recommendations only; **no new budgets or live changes were imposed here**. [NEXT_NATIVE_TEST.md](NEXT_NATIVE_TEST.md) specifies an event/barrier-based native GET/PUT reproduction, with no sleeps, models, or simulations. It was not executed during the active cohort. This future test design does not authorize another paid rollout.

1. **Deterministic native transport, lifecycle, and scripted controls first.** Test concurrent mutations through the actual MCP/state path, including different contexts that share rollout state—not only direct Python calls. Check unique forks, additive advances/meters, reset validity, eviction/reconstruction, timeout/retry behavior, and ready's phase gate. Add dependency/import checks, port-list serialization, large-output persistence, and six scripted shape-valid submissions. Add record-interpolation/no-emission controls so a high score does not silently stand in for learned dynamics.
2. **One short cheap-model wiring smoke.** Use it to check discovery of tools, files, accepted argument formats, reveal, and submission. Label it diagnostic—not a scientific performance estimate. Keep its diagnostic allowance separate from an investigator's exploration freedom.
3. **One frontier full pilot.** Let it investigate normally. Audit state integrity, artifacts, failures, usage, and prediction methods before multiplying runs.
4. **Predeclare a limited set of seeds/worlds.** Include cases that separate within-record interpolation from genuinely out-of-record prediction, and weak from active emission responses. Do not select only successful worlds or favorable ports after seeing scores.
5. **Broaden to a balanced model panel only after the interface is stable.** Keep versions and scientific conditions fixed, and report failures as well as successes.

Cheap-first has costs: a weak model can fail valid tools, make poor experimental choices, or never exercise long-context/parallel failure modes. A passing short smoke can miss this run's state-update race. A failing one does not establish a bad scientific environment. This is why deterministic native controls come first and a full frontier pilot still matters.

### Evidence gaps and files

The archive contains final models/code/payloads and four full persisted read outputs, but not all captured JSONL/NPZ data. Thirteen large base-read replies retain only previews here. No missing artifacts, auxiliary usage, transaction history, or retry cost was invented. Raw scores and all tier CRPS values remain **instance-specific**.

- Start here: this report.
- Process and evidence: `TIMELINE.md`, `SCIENTIFIC_PROCESS.md`, `CONCURRENCY.md`.
- Accounting: `summary.json`, `EXPERIMENTS.md`, `experiment_register.json`.
- Reproducible read-only counting: `audit_counts.py`, run with the project `.venv/bin/python`.
