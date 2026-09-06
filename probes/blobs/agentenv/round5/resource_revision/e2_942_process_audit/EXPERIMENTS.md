# E2 #942 — observed experiments and state accounting

Scope: trace `ae982494a72144c186f58a687a99cd33`, task `physim-BLOB2v2r2-E2#942` only. Source: `~/v3work/ops/recovery_20260905/eval_fable_r2/E2/traces.jsonl:1`. This is a static audit. No world tool, predictor, or simulation was run. These results do not import E1 conclusions.

References below use zero-based trace nodes. `Nn/tool_id/Rr` means sampled tool request node `n` and its first result node `r`. Workspace paths refer to strings embedded in this same trace, not a recovered full workspace.

## Counting rule and outcomes

Count each sampled call/node/tool ID once. There are 2,218 sampled model nodes, 2,336 distinct sampled tool IDs, and 1,300 probe requests. The graph has 2,357 tool-result nodes but only 2,319 result IDs. All 38 extra result nodes are identical context copies. They are not retries or new state operations.

| Tool | Issued | Success | Adjustment refusal* | Explicit error | Timeout | No result |
|---|---:|---:|---:|---:|---:|---:|
| read | 421 | 339 | 0 | 2 | 75 | 5 |
| fork | 103 | 100 | 0 | 0 | 3 | 0 |
| reset | 110 | 101 | 0 | 1 | 8 | 0 |
| adjust | 78 | 58 | 11 | 2 | 7 | 0 |
| inject | 33 | 33 | 0 | 0 | 0 | 0 |
| wait | 466 | 357 | 0 | 0 | 103 | 6 |
| status | 82 | 12 | 0 | 0 | 70 | 0 |
| ready | 1 | 1 | 0 | 0 | 0 | 0 |
| submit | 6 | 6 | 0 | 0 | 0 | 0 |

*Adjustments: 10 refusals applied zero steps; one applied one of 20 requested steps before refusal. All 69 structured adjustment replies concern device 0. They claim 212 accepted control steps and 51 read frames. “Success” is a returned reply, not proof of a surviving state write. Explicit errors are two malformed `ports` arguments and three unknown-context errors. No resource cap was recorded as hit.

## Recorded base coverage

There are 21 successful base reads. Their headers cover 500 distinct grid times, `t=5..2500` in steps of 5, without a repeated grid time. This is not 501 frames and does not include `t=0`.

Only the first base response is fully present. The other 20 responses are persisted-output previews whose referenced full files are absent from the workspace snapshot. Their headers and first frame times establish the 499 remaining grid positions; they do not recover the sensor arrays. The last request asked for 25 steps and returned 24 at the record boundary.

Endpoints: `N7/toolu_01MFmvD31hGcAXEWii5Gjkgx/R8` (`t=5`), and `N163/toolu_01PRRuvPKkKeNNm8GRBnqJ2G/R164` (`t=2385..2500`). The script uses those response headers, not an assumed 25 frames for the final chunk.

## Per-anchor overview

All 103 issued fork calls request a base anchor; none requests fork-from-fork. There are 100 success replies at 15 anchors. They return **96 distinct IDs**, not 100 independent experimental handles. Status reveals one additional ID with no successful fork response. One ID appears at both 1000 and 2500; anchor memberships therefore do not sum to a count of distinct handles.

`Adj` and `Inj` below exclude the multi-anchor ID. The maximum elapsed value is the largest reported `t-anchor` for unambiguous IDs, including status observations. It is not a verified continuous run length.

| Anchor | Fork replies | Distinct returned IDs | Status-only IDs | Adj steps | Inj replies | Max reported elapsed tu |
|---:|---:|---:|---:|---:|---:|---:|
| 600 | 2 | 2 | 0 | 0 | 0 | 225.0 |
| 700 | 4 | 4 | 0 | 3 | 0 | 5.0 |
| 800 | 4 | 4 | 0 | 0 | 1 | 870.0 |
| 1000 | 24 | 23 | 0 | 118 | 0 | 150.0 |
| 1080 | 1 | 1 | 0 | 0 | 0 | 30.0 |
| 1200 | 31 | 31 | 0 | 0 | 31 | 275.0 |
| 1300 | 4 | 4 | 0 | 9 | 0 | 15.0 |
| 1560 | 1 | 1 | 0 | 0 | 0 | 15.0 |
| 1600 | 7 | 7 | 0 | 4 | 0 | 475.0 |
| 1640 | 1 | 1 | 0 | 0 | 0 | 870.0 |
| 1800 | 1 | 1 | 0 | 0 | 1 | 250.0 |
| 1900 | 10 | 9 | 1 | 9 | 0 | 10.0 |
| 2040 | 1 | 1 | 0 | 0 | 0 | 15.0 |
| 2200 | 4 | 4 | 0 | 6 | 0 | 300.0 |
| 2500 | 5 | 4 | 0 | 0 | 0 | 700.0 |

Observed handle categories: 46 actuator, 33 emission, 9 unperturbed-read, 7 wait-only/global, 1 multi-anchor alias, and 1 status-only/no-measurement handle. These are request/reply categories, not a count of independent realized experiments.

- The actuator work includes one-step axis probes, multistep axis pushes, and multiaxis command sequences. The unambiguous 1000-anchor multistep group has six structured replies claiming 101 accepted steps. Five early adjustment replies use the ambiguous 1000/2500 handle and claim another 63 steps. Do not assign those five to a clean independent anchor experiment.
- The emission scan requests all ports 0–12 at anchor 1200 with `amp=1`, `dur=10`. There are 20 further injection replies for dose, duration, repeated-port, or changed-anchor checks. All 33 injection replies use distinct returned handles, but this alone does not establish persistence or statistical independence.
- The largest reported unambiguous live spans are 870 tu at anchors 800 and 1640, and 700 tu at anchor 2500. Status and a branch's own latest successful response do not always agree. For example the original 2500 continuation reports 3000 in its own latest successful read but 3200 in later status (`N3770/toolu_019tnSGHpTG3aG69ArTfCKxr/R3777`).

| Injection anchor | Amp | Dur tu | Replies | Ports in reply order |
|---:|---:|---:|---:|---|
| 1200 | 1 | 10 | 13 | 0, 4, 5, 1, 6, 2, 3, 7, 8, 10, 9, 11, 12 |
| 1200 | 0.1 | 10 | 3 | 2, 2, 6 |
| 1200 | 0.3 | 10 | 3 | 2, 6, 4 |
| 1200 | 0.55 | 10 | 5 | 2, 6, 6, 7, 2 |
| 1200 | 0.8 | 10 | 5 | 2, 4, 6, 6, 7 |
| 1200 | 0.55 | 5 | 1 | 2 |
| 1200 | 0.55 | 20 | 1 | 2 |
| 1800 | 0.55 | 10 | 1 | 2 |
| 800 | 0.8 | 10 | 1 | 6 |

Exact protocol examples and compact call-node lists are in `experiment_summary.json` under `injection_protocol_groups` and `adjustment_protocol_groups`. No raw sensor arrays are copied here.

Retained artifact check: `app/data/forks/act_u1n_adj.json:1` exactly matches `N773/toolu_01Mvdnti4kP2F7rtji27Rww7/R784` after JSON unwrapping (20 accepted steps) This cross-check confirms one retained result; it does not make the partial workspace complete.

## Reply-derived sums versus persisted meters

| Meter | Reply-derived | Persisted | Reply minus persisted |
|---|---:|---:|---:|
| sensor | 190965 | 199320 | -8355 |
| adjust | 219.208 | 219.229 | -0.021 |
| injection | 563.7 | 559.7 | +4 |
| sim_tu | 14030 | 14655 | -625 |
| log_entries | 566 | 577 | -11 |
| reads_base | 500 | 500 | +0 |
| reads_fork | 845 | 895 | -50 |
| fork_spawns | 100 | 97 | +3 |
| resets | 101 | 96 | +5 |
| turns | 1023 | 1023 | +0 |

The equality for `turns` is real: 1,023 non-timeout/non-missing probe replies equals the persisted counter. It is **not transaction exactness**. Several other counters disagree in both directions. The sums exclude timed-out and missing replies; exclusion does not mean those requests executed zero work. No exact allocation of lost writes, repeated work, or timeout work is possible.

Current source formulas: sensor = read frames × selected slots × 5; adjustment = `sum(abs(u))` × (applied steps plus the first refused step); injection = `abs(amp)*(1+4*max(0,abs(amp)-0.5))*dur`. Only live advancement contributes to `sim_tu`; base record reads and cold replay do not. Each advancing read/wait/accepted-adjustment call adds one log entry; an injection adds two. See `servers/blob.py:597-647,686-696,793-804,928-941` and `blobcore.py:146-149` under `environments/physim/physim/`.

Reproduce the machine summary from repository root:

```
.venv/bin/python -B probes/blobs/agentenv/round5/resource_revision/e2_942_process_audit/state_counts.py
```

See `CONCURRENCY.md` for the exact ID, clock, cache, and reveal-boundary limitations.
