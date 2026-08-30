# LINEAGE — v2 campaign: champion + top dynasties

Method: candidate names are pod-scoped (`p{island}g{gen}_{k}`) and REUSED
across eras, so every parent ref was resolved with a timestamp- and
structure-aware resolver: (1) earlier rows of the same campaign, (2) the
gpu_b_union1 breeding-pool holders, (3) earlier eras chronologically
(b1 pilot -> singlemode -> CPU pods -> local v2 -> local v1). Structural
checks per op: act/chan/bilin count deltas, vtag sub/superset, exact act0
parameter match. See `timeline.md` for the era map.

Union growth: union4_final_cpu 182 -> union5_prebatch 190 -> gpu_b_union1 362 -> UNION_FINAL_v2 423 cells.

## Dynasty census (all 423 cells traced to their seed root)

| root class | cells | share |
|------------|-------|-------|
| smoke_m0 / smoke_mint / smoke_elite (pod bootstrap seeds) | 245 | 58% |
| pod immigrants (fresh random genomes, parents=None) | 82 | 19% |
| ground truths (gt_m4, gt_pred, gt_xv, ...) | 36 | 9% |
| stage-2/3 elite seeds (rail_111_17, rh1_7000, ...) | 28 | 7% |
| local-v2 immigrants (ds2g12_019, ds2g12_022, ...) | 25 | 6% |
| local-v2 seeds (v2g10_*) | 7 | 2% |

Individual roots: smoke_m0 118 cells, smoke_elite 65, smoke_mint 62,
p0g1_077 (era1 random immigrant) 21, rh1_7000 19, gt_m4 16, ds2g12_019 13,
p2g4_088 13, ds2g12_022 12, gt_pred 11, p4g5_086 10, rail_111_17 8.

Pool founders (entry points into the final campaign) ranked by cells held:
p1g2_070 -> 41 cells (the CHAMPION dynasty), p1g2_009 -> 16, p4g6_004 -> 14,
p5g7_039 -> 13, p0g0_ds2g12_019 -> 13, p0g1_077 -> 13, p3g3_027 -> 12.

## 1. THE CHAMPION — p6g8_033, I=91.16, `3|grow|rotor|liquid|s2|g2`

10-hop spine through ALL FOUR campaign eras. It starts at smoke_m0 — the
TRIVIAL 1-species frozen ground truth, I=2.8 — a x32 interest amplification:

```
era4_final        91.16  p6g8_033               delete_bilin       3|grow|rotor|liquid|s2|g2
era4_final        87.30  p6g7_037               add_chan           3|grow|mobile|liquid|s2|g2
era4_final        88.04  p6g5_026               mint_bilin         3|switch|mobile|liquid|s2|g2
era4_final        81.47  p6g2_039               add_chan           3|grow|mobile|liquid|s1|g2
era4_final        83.31  p6g1_028               mint_bilin         3|switch|rotor|liquid|s2|g2
era3_b1           78.60  p1g2_070               merge_slow_tanh    3|grow|mobile|liquid|s2|g2  [+donor: blk_p0g0_ds2g12_019]
era2_singlemode   62.28  p6g1_043               add_chan           2|grow|rotor|liquid|s1|g0
era1_cpu          10.98  p5g6_005               mutate             2|constant|still|frozen|s1|g0
era1_cpu          10.62  p5g5_074               merge_share_chan   2|constant|still|frozen|s1|g0  [+donor: ref_iso_d0.65]
era1_cpu           2.80  smoke_m0               seed               1|constant|still|frozen|s1|g0
```

Donor branch of the era3 merge (p1g2_070 = merge_slow_tanh(p6g1_043 x blk_p0g0_ds2g12_019)):

```
block:pool_b1union  32.00  p0g0_ds2g12_019        seed               1|constant|still|frozen|s1|g2
era0_local_v2     32.00  ds2g12_019             immigrate          1|constant|still|frozen|s1|g2
```

Operator jumps along the spine (parent I -> child I):

| op | jump | delta | child |
|----|------|-------|-------|
| delete_bilin | 87.30 -> 91.16 | +3.87 | p6g8_033 |
| add_chan | 88.04 -> 87.30 | -0.74 | p6g7_037 |
| mint_bilin | 81.47 -> 88.04 | +6.57 | p6g5_026 |
| add_chan | 83.31 -> 81.47 | -1.84 | p6g2_039 |
| mint_bilin | 78.60 -> 83.31 | +4.72 | p6g1_028 |
| merge_slow_tanh | 62.28 -> 78.60 | +16.32 | p1g2_070 |
| add_chan | 10.98 -> 62.28 | +51.30 | p6g1_043 |
| mutate | 10.62 -> 10.98 | +0.35 | p5g6_005 |
| merge_share_chan | 2.80 -> 10.62 | +7.82 | p5g5_074 |

WHO MADE THE JUMPS: the two discontinuities that created this dynasty are
**add_chan +51.3** (11.0 -> 62.3, era2 singlemode: added a channel that woke
the frozen 2-species mutate-dead-end up into a growing rotor world) and
**merge_slow_tanh +16.3** (62.3 -> 78.6, era3 pilot: crossed it with a block
built from local-v2 immigrant ds2g12_019, I=32, a 1-act/3-chan miniature).
Inside era4 the ratchet is **mint_bilin** (+4.7 at g1 = vertex v6_1_028,
+6.6 at g5 = vertex v6_5_026) alternating with add_chan (structure-buying
dips), closed by a **delete_bilin ablation +3.9** at g8 that dropped
v6_5_026 again — the surviving champion carries exactly ONE minted vertex
(v6_1_028). So: merge/add_chan open the valley, mint climbs it, delete
prunes the scaffolding. seed2 confirm 79.67 (seed2_ok), T_used=20000 cap rider.

The champion dynasty (pool founder p1g2_070) holds **41 of 423 cells**, incl.
4 of the global top-6: 91.16, 88.60 (3|switch|rotor s2), 88.35 (3|grow|mobile
s2), 88.04 (3|switch|mobile s2), 86.88 (3|grow|rotor s3), 84.30.

## 2. Dynasty p1g2_009 — the 4-species mobile/rotor s3 family (best 89.33)

Root: **smoke_elite** = the ds3_014-class succession world (fossil vertex
fdr_ds3_014_0; v1 lineage: ds3_014 = merge_cross_edge(g0_jit_11 x
engine_10748), g0_jit_11 = mutate(rail_111_17), I=68.8 v1-epoch). 16 cells.

```
era4_final        89.33  p3g9_022               mint_bilin         4|grow|mobile|liquid|s3|g2
era4_final        88.02  p3g6_032               delete_bilin       4|grow|mobile|liquid|s3|g1
era4_final        87.04  p4g5_030               mint_bilin         4|grow|mobile|liquid|s3|g2
era4_final        86.91  p4g2_006               mutate             4|grow|mobile|liquid|s3|g2
era3_b1           77.31  p1g2_009               mutate             4|grow|mobile|liquid|s1|g2
era3_b1           75.77  p1g1_031               mint_bilin         4|grow|mobile|liquid|s1|g2
era1_cpu          77.99  p3g5_040               add_chan           4|switch|mobile|liquid|s1|g2
era1_cpu          67.00  p4g4_003               mutate             4|switch|rotor|liquid|s1|g2
era1_cpu          74.50  smoke_elite            seed               4|grow|rotor|liquid|s2|g2
```

Jump pattern: CPU era mutate/add_chan lifted 67 -> 78; era3 pilot minted
v1_1_031 (75.8) and mutate pushed to 77.3; era4 mutate recovered 86.9,
then **mint_bilin -> delete_bilin -> mint_bilin** (87.0 -> 88.0 -> 89.33)
walked the s3 (three-stage succession) axis up. Heads: p3g9_022 (89.33,
s3|g2), p2g7_039 (88.74 rotor s3, via add_chan), p3g6_032 (88.02 s3|g1).
NOTE: p2g7_039/p3g9_022 hold the ONLY s3 cells above 88 — this family owns
the deep-succession corner of the archive.

## 3. Dynasty p4g6_004 — the switch|mobile 4-species family (best 86.21)

Root: smoke_elite again, but through CPU-era mint p1g1_022 (v1_1_022). 14 cells.

```
era4_final        86.21  p5g3_040               add_chan           4|switch|mobile|liquid|s3|g2
era1_cpu          80.90  p4g6_004               mutate             4|switch|mobile|liquid|s2|g2
era1_cpu          73.50  p1g1_022               mint_bilin         4|grow|rotor|liquid|s1|g2
era1_cpu          74.50  smoke_elite            seed               4|grow|rotor|liquid|s2|g2
```

One era4 add_chan (+5.3) turned a CPU-era 80.9 elite into the 86.21
s3-switch head; mint_bilin then radiated it into rotor cells (p1g7_030
85.73). Pure two-op family: CPU mint+mutate, GPU add_chan+mint.

## 4. Dynasty p3g3_027 — the grow|rotor s3 mint-stack (best 85.20)

Root: smoke_elite; founder p3g3_027 is a CPU-era mint DIRECTLY on the seed
(I=81.3, already s3). 12 cells.

```
era4_final        85.20  p4g3_033               delete_bilin       4|grow|rotor|liquid|s3|g1
era4_final        82.73  p4g2_031               mint_bilin         4|grow|rotor|liquid|s3|g2
era4_final        82.00  p4g1_028               mint_bilin         4|grow|rotor|liquid|s3|g2
era1_cpu          81.33  p3g3_027               mint_bilin         4|grow|rotor|liquid|s3|g2
era1_cpu          74.50  smoke_elite            seed               4|grow|rotor|liquid|s2|g2
```

This family is the purest mint story: three stacked mint_bilin (fossil +
v3_3_027 + v3_1_028 + v4_2_031 = 4 bilinear vertices) then one delete_bilin
ablation (+2.5) that pruned back to 3. mint -> mint -> mint -> delete is
literally the whole era4 chain.

## Cross-dynasty facts

- 3 of the top-4 dynasties descend from smoke_elite = the ds3_014 fossil-vertex
  succession world — the v1-era flagship is the grandparent of most of the
  v2 leaderboard. The CHAMPION dynasty is the exception: it grew out of
  smoke_m0 (I=2.8) purely through operators, proving the pipeline can build
  complexity from nothing.
- Every top-4 dynasty chain contains >=1 mint_bilin, and 3 of 4 end in or
  pass through a delete_bilin ablation: minted vertices are used as
  SCAFFOLDING, kept only when load-bearing.
- Islands mix: champion spine hops isl5-CPU -> isl6-singlemode -> isl1-pilot
  -> isl6-final; dynasty 2 hops isl3/4-CPU -> isl1-pilot -> isl4/3-final.
  The every-2-gens union push (immigrate/merge pool) is what moved genomes
  across islands.
