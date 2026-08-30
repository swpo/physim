# CAP-RIDERS — worlds exiting at T=20000 with why=cap

Definition (assay_v2): the adaptive horizon doubles T while any extension
criterion fires (a_mem slow-channel memory, b_org organism dynamics, c_acf
long autocorrelation). `why=cap` = criteria STILL firing at T=20000 —
the assay was cut off, not converged. These worlds have unfinished dynamics.

## Counts

- 337 cap exits total in final harvest: **194 screens** + 82 seed2 + 61 seed3 confirms.
- (For scale: 337 of 5133 scored rows = 6.6%; horizon whys overall: static 3561, converged 1231, cap 337.)
- Screen cap-riders by island: isl3: 58, isl5: 33, isl6: 30, isl4: 29, isl2: 28, isl1: 16
  (island 3 = the 4|grow|mobile s3 dynasty's home).
- Cap-rider quality: mean I 75.5, median 76.4, max 89.33; **157/194 >= 70**, 54 >= 80.
  Cap-riding is an ELITE phenomenon: only 4% of all screens, but they populate the leaderboard top.
- **142/194 still RISING at exit** (I@20000 > I@10000) — measured interest is a lower bound for these.
- 21 union holder cells sit on a cap exit (incl. 89.33 / 88.35 / 88.02 / 85.15).
- NOTE: the 91.16 champion is NOT a cap-rider (why=converged at T=20000 after 3 extensions).

## Families (by dynasty pool founder)

| founder | cap screens | best I | dynasty |
|---------|------------:|-------:|---------|
| p1g2_009 | 56 | 89.3 | 4-species grow\|mobile s3 (smoke_mint root) |
| p1g2_070 | 37 | 88.3 | CHAMPION dynasty (smoke_m0 root) |
| p4g6_004 | 33 | 88.5 | switch\|mobile 4-species (smoke_elite root) |
| p6g1_071 | 24 | 79.2 | secondary isl6 family |
| p3g3_027 | 6 | 84.7 | grow\|rotor s3 mint-stack |
| others | 38 | <=81.5 | long tail |

The three top dynasties own 65% of all cap exits — the same lineages that
win cells are the ones that refuse to converge.

## Longer-horizon re-run candidates

106 distinct genomes (ghash-deduped) exit at cap with I>=70 AND
still rising (dI(10k->20k) > 0.5). Top 12 by rise rate:

| I@20k | dI 10k->20k | cand | isl | cell | union holder |
|------:|------------:|------|----:|------|--------------|
| 88.17 | +12.36 | p4g6_021 | 4 | `4\|grow\|mobile\|liquid\|s3\|g2` |  |
| 78.59 | +11.51 | p5g3_028 | 5 | `3\|switch\|rotor\|liquid\|s1\|g2` |  |
| 85.79 | +10.76 | p3g10_028 | 3 | `4\|grow\|mobile\|liquid\|s3\|g2` |  |
| 86.01 | +10.42 | p3g8_021 | 3 | `4\|grow\|mobile\|liquid\|s3\|g1` |  |
| 74.22 | +10.23 | p2g7_040 | 2 | `3\|switch\|rotor\|liquid\|s1\|g2` |  |
| 88.02 | +10.15 | p3g6_032 | 3 | `4\|grow\|mobile\|liquid\|s3\|g1` | YES |
| 81.51 | +9.55 | p3g4_057 | 3 | `4\|switch\|rotor\|liquid\|s2\|g2` |  |
| 89.33 | +8.81 | p3g9_022 | 3 | `4\|grow\|mobile\|liquid\|s3\|g2` | YES |
| 83.68 | +8.81 | p4g5_024 | 4 | `4\|grow\|mobile\|liquid\|s3\|g2` |  |
| 88.53 | +8.69 | p3g1_028 | 3 | `4\|grow\|rotor\|liquid\|s3\|g2` |  |
| 87.34 | +8.43 | p3g6_029 | 3 | `4\|grow\|mobile\|liquid\|s3\|g2` |  |
| 87.88 | +8.2 | p4g8_034 | 4 | `4\|grow\|mobile\|liquid\|s3\|g2` |  |

Full ranked list (106 genomes) in `cap_riders.json` -> `longer_horizon_rerun_candidates`.

Priority protocol (matches the deploy longH lane, cap 40000):
1. p4g6_021 (88.2, +12.4/decade, isl4 s3) — fastest riser among elites.
2. p3g9_022 (89.33 HOLDER, +8.8) — the #2 archive world; a T=40000 run
   likely crosses 90.
3. p3g6_032 (88.0 HOLDER, +10.2), p3g8_021 (86.0, +10.4), p3g10_028 (85.8,
   +10.8) — the isl3 s3 family, all same dynasty; run one per ghash.
4. p5g3_028 (78.6, +11.5, 3|switch|rotor s1) — outsider family, steepest
   slope outside the s3 clan.
5. p6g5_025 (72.4 HOLDER, +7.4, 2|grow|rotor s2) — only 2-species cap-rider
   holder; cheap and distinct.
