# SUMMARY — v2 deepsearch campaign analysis (UNION_FINAL_v2)

Analysis of the final GPU harvest (islands 1-6, batched JAX stepper) plus
full-campaign lineage across all eras. Deliverables in this directory:
`LINEAGE.md`, `OPERATOR_STATS.md`, `COMPLEXITY_TRAJECTORY.md`,
`CAP_RIDERS.md`, `timeline.md`, plus machine-readable jsons and
`film_candidates/` (5 ready-to-run genome payloads).

## The 10 headline numbers

1. **423 cells / 91.16 champion.** UNION_FINAL_v2 holds 423 of 2880
   possible descriptor cells (14.7%); top world p6g8_033
   `3|grow|rotor|liquid|s2|g2` at I=91.16 (seed2 confirm 79.7).
2. **x2.2 archive growth in the GPU eras**: union4_final_cpu 182 ->
   union5_prebatch 190 -> gpu_b_union1 362 -> FINAL 423; I>=80 cells
   4 -> 28 (x7); 241 of 423 cells did not exist at CPU handoff, and 131
   surviving CPU-era cells were improved.
3. **6291 evals in the final campaign** (4917 screens + 769 seed2 + 605
   seed3), 5129 ok; ~2061 lane-hours of assay compute across 6 islands
   in ~1.5 wall-days.
4. **230 of 423 cells (54%) carry minted bilinear vertices** — 133
   distinct minted vtags fixed in the union (of 651 seen). The v1 minted-
   vertex creation rate was structurally ZERO.
5. **mint_bilin is the best operator per attempt**: 16.3% of 615 attempts
   became archive holders, 66 screens >= 80 (6.6x mutate's I>=80 count from 60% of
   the attempts). delete_bilin: 100% ok, 15.5% holder
   rate, and it authored the champion.
6. **The champion rose x32 from the trivial seed**: smoke_m0 (I=2.8) ->
   10 hops through all 4 eras -> 91.16. Jump credits: add_chan +51.3,
   merge_slow_tanh +16.3, mint_bilin +4.7/+6.6, final delete_bilin +3.9.
7. **One dynasty holds 41/423 cells** (pool founder p1g2_070, champion
   family); top-4 dynasties hold 83 cells and ALL of the top-10 worlds.
   3 of the 4 descend from smoke_elite = the v1 ds3_014 fossil-vertex world.
8. **Succession axis exploded and owns the top**: s2 cells 18 -> 49, s3
   4 -> 12 (meanI 81.4 — highest of any axis value anywhere); ALL of the
   top-10 worlds are s2/s3. C7_roles mean rose 0.51 -> 0.56, C2_timescale
   0.35 -> 0.40 across checkpoints.
9. **194 screen cap-riders** (why=cap at T=20000; 6.6% of scored rows,
   mean I 75.5): 142 still rising at exit, 106 distinct elite genomes
   (I>=70, dI>0.5) queued as longer-horizon re-run candidates; 21 union
   holders sit on cap exits. 65% belong to the 3 top dynasties.
10. **box_limit is the elite norm**: 74% of flagged screens and 337/423
    union holders span the full L=128 box (L192 lane material).
    Battery integrity: 0 subsampled-mode rows in the harvest; 26
    battery_timeouts (isl3:10, isl6:9) were dropped as assay_error, never
    scored.

## 5 champion candidates for filming (genomes in film_candidates/)

| # | cand | cell | I | confirms | why film it |
|---|------|------|---|----------|-------------|
| 1 | p6g8_033 | `3\|grow\|rotor\|liquid\|s2\|g2` | 91.16 | s2 79.7 | THE champion. 42-organism 3-species rotor ecology (wind 8.0), 2-stage succession, memory 0.93, one load-bearing minted vertex. The x32-from-nothing story. |
| 2 | p3g9_022 | `4\|grow\|mobile\|liquid\|s3\|g2` | 89.33 | cap-rider | #2 world: 151-organism 4-species mobile swarm with FULL 3-stage succession (C8=1.0). Still rising at T=20000 (+8.8/decade) — film at 40000 and watch it become something else. |
| 3 | p5g3_040 | `4\|switch\|mobile\|liquid\|s3\|g2` | 86.21 | s2 75.9 AND s3 74.1 | Best 3-seed-CERTIFIED deep world: robust to seeds, s3 + memory 0.97. The one to show skeptics. |
| 4 | p4g3_033 | `4\|grow\|rotor\|liquid\|s3\|g1` | 85.20 | s2 80.4, s3 53.8 | 241-organism rotor STORM (wind 15.1): the most kinetic elite; mint-stack dynasty (3 vertices). |
| 5 | p4g2_044 | `4\|switch\|rotor\|liquid\|s2\|g2` | 82.47 | s2 80.8, s3 81.4 | Most seed-stable elite (81 +/- 1 across 3 seeds); minimal 21-organism 4-species rotor, NO minted vertices — clean architecture contrast to #1-#4. |

Alternates: p6g7_028 (88.6, 4 minted vertices, champion sibling),
p2g7_039 (88.7 rotor s3, cap-rider, unconfirmed).

## Campaign history in one line

182 (CPU pods, 08-26..28) -> 190 (single-mode GPU, 08-28) -> 362 (batched
pilot isl1, 08-29) -> **423 cells / 91.16 (batched islands 1-6, 08-29..30)**.
