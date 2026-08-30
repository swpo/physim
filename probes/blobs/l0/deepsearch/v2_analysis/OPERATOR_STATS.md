# OPERATOR STATS — v2 final GPU campaign (era4, islands 1-6) vs v1

Attempts = screen-phase rows in final_gpu_harvest (4917 total).
`arch cands` = distinct candidates that hold >=1 cell in any island's
end-state archive (interest-matched). `union cells` = cells held in
UNION_FINAL_v2 (423). v1 = original local l0-deepsearch campaign
(metrics_v1 epoch, 164 evals; interest scale NOT comparable).

## era4 final campaign

| op | attempts | ok | ok% | arch cands | arch/att | union cells | I>=70 | I>=80 | best I | best cand |
|----|---------:|---:|----:|-----------:|---------:|------------:|------:|------:|-------:|-----------|
| mint_bilin | 615 | 609 | 99% | 100 | 16.3% | 85 | 240 | 66 | 89.33 | p3g9_022 |
| delete_bilin | 206 | 205 | 100% | 32 | 15.5% | 20 | 96 | 37 | 91.16 | p6g8_033 |
| merge_slow_tanh | 302 | 279 | 92% | 44 | 14.6% | 29 | 15 | 2 | 81.55 | p2g6_069 |
| merge_cross_edge | 731 | 694 | 95% | 101 | 13.8% | 89 | 82 | 5 | 81.66 | p5g4_063 |
| mutate | 1027 | 944 | 92% | 124 | 12.1% | 99 | 95 | 10 | 87.77 | p3g5_001 |
| add_chan | 413 | 398 | 96% | 46 | 11.1% | 42 | 89 | 22 | 88.74 | p2g7_039 |
| dup_act | 428 | 169 | 40% | 30 | 7.0% | 25 | 36 | 12 | 86.93 | p2g7_047 |
| merge_share_chan | 215 | 54 | 25% | 15 | 7.0% | 17 | 3 | 1 | 81.53 | p2g3_073 |
| immigrate | 980 | 408 | 42% | 8 | 0.8% | 8 | 0 | 0 | 48.84 | p4g3_082 |

## v1 local campaign (metrics_v1; 4-op alphabet, no mint/delete/add/dup/immigrate)

| op | attempts | ok% | archive holders | holder/att | best I (v1 scale) |
|----|---------:|----:|----------------:|-----------:|------------------:|
| mutate | 80 | 90% | 21 | 26.3% | 73.7 |
| merge_cross_edge | 39 | 97% | 8 | 20.5% | 68.8 |
| merge_share_chan | 24 | 21% | 3 | 12.5% | 54.5 |
| merge_slow_tanh | 21 | 86% | 1 | 4.8% | 72.7 |

## Reading

- **mint_bilin is the star of v2**: 16.3% of attempts become archive
  holders (best of any op), 99% survive the funnel+assay, it produced
  240 screens >=70 and 66 >=80 — 37% of all I>=70 rows from 12.5% of
  attempts. In v1 this operator did not exist (minted-vertex creation
  rate was structurally ZERO, per SCORECARD_V2_EVOLVE).
- **delete_bilin**: 100% ok (it can only simplify), 15.5% holder rate,
  and it authored the CAMPAIGN CHAMPION (91.16). Ablation-as-operator
  pays: 96 of 206 attempts scored >=70 (parents were already elite;
  ~half of deletions keep or raise interest).
- **mutate** remains the workhorse (1027 attempts, 12.1% holder rate) but
  its ceiling (87.8) is below mint/delete (89.3/91.2) — same law as v1
  where mutate held 21/35 cells but the peaks were merges.
- **merge_cross_edge** keeps its v1 role as cell-opener: 101 holder cands,
  ok 95%, second-most union cells (89). merge_slow_tanh low-volume
  high-leverage: it built the champion's pool founder (+16.3 jump).
  merge_share_chan stays fragile (25% ok, same-vacuum law) — unchanged v1->v2.
- **immigrate** is a diversity tax at final-campaign scale: 42% alive,
  0.8% holder rate, 0 rows >=70, but 8 union cells + 82 of 423 cells
  ultimately root in pod immigrants — it seeds future dynasties rather
  than scoring itself.
- **dup_act** stays the weakest structural op (39% ok, funnel-kill heavy;
  same as v1 local validation 3/10) yet 30 archive cands incl. an 86.9.
- Confirm economics: 769 seed2 (99.3% ok), 605 seed3 (100% ok);
  300/423 union cells are seed2-confirmed, 141 are 3-seed confirmed.
