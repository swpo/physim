# Experiment accounting — one completed run

Trace `0bdd699154ee4e1d96aac4e0961bc11d`; task `physim-BLOB2v2r2-E1#928`.

## Scope and interpretation

These tables describe calls and replies, not a clean randomized trial register. The trace has repeated fork IDs, unknown-context errors, and timeouts. A successful response does not prove its state change survived in the final state. The final environment meters are listed separately in REPORT.md and summary.json.

- 183 fork requests: 181 success-shaped replies, 2 timeouts, 145 distinct returned IDs. All sources were base anchors; none were nested forks.
- 62 reported anchor times. An ID reused at multiple anchors is marked ambiguous. IDs can therefore occur in more than one anchor row.
- 102 adjustment responses carry applied-step information: 99 fully accepted, 2 partly applied then refused, 1 refused at the first step. 9 other calls return unknown-context errors; 1 times out.
- 46 injection acknowledgments: amplitude 0.05–1.0; duration 5–20 tu. 18 other injections return unknown-context errors; 3 time out. No out-of-range emission was acknowledged.
- Base coverage: 58 success-shaped read responses, 505 reported frames but 500 distinct grid times, t=5..2500. Repeated t=165 (4 replies), 220 (2), 245 (2). The extra frames are not five extra base-time steps.
- Long unambiguous reported continuations include t=600→2500 (1900 tu, global-stat sweep) and t=2500→3105 (605 tu). No per-fork duration stop is recorded.

## Injection protocols with success-shaped responses

An anchor label with `AMBIGUOUS` lists every anchor reported for that fork ID. It does not identify which underlying state produced the response.

| Reported anchor(s) | Port | Amplitude | Duration (tu) | Replies |
|---|---:|---:|---:|---:|
| 1500 | 4 | 1 | 10 | 1 |
| 1600 | 0 | 1 | 10 | 1 |
| 1600 | 1 | 0.05 | 10 | 2 |
| 1600 | 1 | 0.3 | 10 | 1 |
| 1600 | 1 | 0.6 | 5 | 6 |
| 1600 | 1 | 0.6 | 10 | 1 |
| 1600 | 1 | 0.9 | 10 | 1 |
| 1600 | 1 | 1 | 10 | 1 |
| 1600 | 2 | 0.3 | 10 | 1 |
| 1600 | 2 | 0.6 | 10 | 1 |
| 1600 | 2 | 0.9 | 5 | 1 |
| 1600 | 2 | 0.9 | 10 | 1 |
| 1600 | 2 | 0.9 | 20 | 1 |
| 1600 | 2 | 1 | 10 | 1 |
| 1600 | 3 | 1 | 10 | 1 |
| 1600 | 4 | 1 | 10 | 1 |
| 1600 | 5 | 1 | 10 | 1 |
| 1600 | 6 | 1 | 10 | 1 |
| 1600 | 7 | 1 | 10 | 1 |
| 1600 | 8 | 1 | 10 | 1 |
| 1600 | 9 | 1 | 10 | 1 |
| 1600 | 10 | 1 | 10 | 1 |
| 1600 | 11 | 1 | 10 | 1 |
| 2100 | 1 | 1 | 10 | 1 |
| 2100 | 2 | 1 | 10 | 1 |
| 2100 | 4 | 1 | 10 | 1 |
| 2100 | 5 | 1 | 10 | 1 |
| 2100 | 8 | 1 | 10 | 1 |
| 2100 | 10 | 1 | 10 | 1 |
| 900 | 2 | 1 | 10 | 3 |
| AMBIGUOUS:900,1600 | 1 | 0.6 | 5 | 3 |
| AMBIGUOUS:900,1600 | 10 | 1 | 10 | 4 |
| AMBIGUOUS:900,1600,2200 | 2 | 1 | 10 | 1 |

## Per-anchor summary

Adjustment/injection columns include only IDs with one reported anchor. `Elapsed` is the largest observed response time minus that anchor, not a reconstructed physical history.

| Anchor | Fork replies / IDs | Multi-anchor IDs | Adjust replies / applied steps | Injection replies | Elapsed (tu) |
|---:|---:|---:|---:|---:|---:|
| 200 | 5 / 4 | 2 | 0 / 0 | 0 | 30 |
| 230 | 2 / 2 | 1 | 0 / 0 | 0 | 25 |
| 235 | 1 / 1 | 0 | 0 / 0 | 0 | 20 |
| 300 | 1 / 1 | 0 | 0 / 0 | 0 | 100 |
| 600 | 11 / 11 | 1 | 11 / 105 | 0 | 1900 |
| 605 | 1 / 1 | 0 | 0 / 0 | 0 | 95 |
| 615 | 1 / 1 | 0 | 0 / 0 | 0 | 0 |
| 620 | 2 / 2 | 1 | 1 / 1 | 0 | 5 |
| 640 | 1 / 1 | 0 | 3 / 3 | 0 | 15 |
| 660 | 1 / 1 | 0 | 1 / 1 | 0 | 5 |
| 730 | 1 / 1 | 1 | 0 / 0 | 0 | 0 |
| 750 | 1 / 1 | 0 | 2 / 2 | 0 | 10 |
| 780 | 1 / 1 | 0 | 2 / 2 | 0 | 10 |
| 800 | 1 / 1 | 0 | 2 / 2 | 0 | 10 |
| 875 | 1 / 1 | 0 | 0 / 0 | 0 | 0 |
| 900 | 13 / 9 | 6 | 0 / 0 | 3 | 75 |
| 905 | 1 / 1 | 0 | 3 / 3 | 0 | 15 |
| 920 | 1 / 1 | 0 | 1 / 1 | 0 | 5 |
| 950 | 1 / 1 | 0 | 3 / 3 | 0 | 15 |
| 1000 | 6 / 5 | 2 | 0 / 0 | 0 | 400 |
| 1005 | 2 / 2 | 0 | 0 / 0 | 0 | 120 |
| 1025 | 1 / 1 | 0 | 0 / 0 | 0 | 0 |
| 1040 | 1 / 1 | 0 | 1 / 1 | 0 | 5 |
| 1060 | 1 / 1 | 0 | 3 / 3 | 0 | 15 |
| 1100 | 1 / 1 | 0 | 1 / 1 | 0 | 5 |
| 1135 | 1 / 1 | 0 | 0 / 0 | 0 | 0 |
| 1150 | 1 / 1 | 0 | 2 / 2 | 0 | 10 |
| 1190 | 1 / 1 | 0 | 2 / 2 | 0 | 10 |
| 1200 | 1 / 1 | 0 | 2 / 2 | 0 | 10 |
| 1210 | 1 / 1 | 1 | 0 / 0 | 0 | 0 |
| 1250 | 1 / 1 | 0 | 2 / 2 | 0 | 10 |
| 1330 | 1 / 1 | 0 | 3 / 3 | 0 | 15 |
| 1340 | 1 / 1 | 0 | 1 / 1 | 0 | 5 |
| 1395 | 1 / 1 | 0 | 0 / 0 | 0 | 0 |
| 1400 | 1 / 1 | 0 | 3 / 3 | 0 | 15 |
| 1475 | 2 / 2 | 1 | 1 / 1 | 0 | 5 |
| 1480 | 1 / 1 | 0 | 3 / 3 | 0 | 15 |
| 1500 | 17 / 17 | 1 | 8 / 8 | 1 | 100 |
| 1550 | 1 / 1 | 0 | 1 / 1 | 0 | 5 |
| 1600 | 49 / 40 | 8 | 0 / 0 | 28 | 150 |
| 1620 | 2 / 2 | 1 | 2 / 2 | 0 | 10 |
| 1630 | 1 / 1 | 0 | 2 / 2 | 0 | 10 |
| 1655 | 1 / 1 | 0 | 0 / 0 | 0 | 0 |
| 1700 | 3 / 3 | 0 | 2 / 2 | 0 | 20 |
| 1705 | 1 / 1 | 0 | 0 / 0 | 0 | 15 |
| 1760 | 6 / 4 | 3 | 2 / 2 | 0 | 5 |
| 1770 | 1 / 1 | 0 | 1 / 1 | 0 | 5 |
| 1875 | 1 / 1 | 1 | 0 / 0 | 0 | 0 |
| 1900 | 1 / 1 | 0 | 1 / 1 | 0 | 5 |
| 1915 | 1 / 1 | 0 | 0 / 0 | 0 | 0 |
| 1920 | 1 / 1 | 0 | 3 / 3 | 0 | 15 |
| 2050 | 2 / 2 | 0 | 4 / 4 | 0 | 10 |
| 2060 | 1 / 1 | 0 | 2 / 2 | 0 | 10 |
| 2100 | 6 / 6 | 0 | 0 / 0 | 6 | 250 |
| 2125 | 1 / 1 | 0 | 0 / 0 | 0 | 0 |
| 2175 | 1 / 1 | 0 | 0 / 0 | 0 | 0 |
| 2200 | 6 / 5 | 2 | 9 / 9 | 0 | 15 |
| 2210 | 1 / 1 | 0 | 1 / 1 | 0 | 5 |
| 2280 | 1 / 1 | 0 | 3 / 3 | 0 | 15 |
| 2435 | 1 / 1 | 0 | 0 / 0 | 0 | 0 |
| 2450 | 1 / 1 | 1 | 0 / 0 | 0 | 0 |
| 2500 | 2 / 2 | 0 | 0 / 0 | 0 | 605 |

## Adjustment sequence register

`experiment_register.json → adjustment_sequences` preserves all 102 response-bearing commands, grouped by fork ID and ordered by sampled tool-call time. Each entry gives the exact u vector, device, requested/applied step counts, result, node, model-call index, tool-call ID and UTC timestamp. Multi-anchor IDs are explicitly flagged. These commands are observations of replies, not proof of an unbroken accepted state trajectory.

Initial range tests at anchor 600 include single-axis ±1 commands, five fully accepted 10-step blocks, one 50-step block, a u3=+1 request accepting 1/10 steps, u3=-1 accepting 0/10, and u3=+0.5 accepting 2/3. Later trials use continuous mixed commands and short sequences. The scientific notes explain the fitted artifact and which branch was used after reveal.

## Reconciliation

| Meter | Naive successful-reply sum | Persisted final meter | Difference |
|---|---:|---:|---:|
| sensor | 149070 | 145405 | +3665 |
| adjust | 229.865 | 219.721 | +10.144 |
| injection | 976.9 | 814.3 | +162.6 |
| sim_tu | 11860 | 11495 | +365 |
| log_entries | 562 | 514 | +48 |
| reads_base | 505 | 500 | +5 |
| reads_fork | 657 | 625 | +32 |

The reply tally gives 150 reset acknowledgments (140 distinct IDs), versus 133 persisted resets. All non-timeout/non-missing environment replies total 1009, versus 891 persisted environment turns. The trace does not preserve the authoritative per-operation commit history needed to allocate these gaps. Do not add the naive totals to the meters.
