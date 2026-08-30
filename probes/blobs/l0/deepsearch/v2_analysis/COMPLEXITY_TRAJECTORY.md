# COMPLEXITY TRAJECTORY — era4 final GPU campaign

## Per-generation screen population (islands 1-6 pooled; ok rows only for I/C stats)

`s2+%` = share of ok rows in succession cells (s2/s3); `g2%` = memory-grade-2
cells; `box%` = box_limit-flagged (pattern spans the full L=128 box).

| gen | n | ok% | meanI | p90 I | maxI | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | s2+% | g2% | box% | T2500/5k/10k/20k |
|----:|--:|----:|------:|------:|-----:|----|----|----|----|----|----|----|----|-----:|----:|-----:|------------------|
| 1 | 576 | 77% | 43.4 | 73.1 | 88.5 | 0.44 | 0.28 | 0.38 | 0.74 | 0.50 | 0.56 | 0.55 | 0.05 | 8 | 64 | 69 | 294/69/41/42 |
| 2 | 576 | 75% | 46.0 | 74.7 | 86.9 | 0.47 | 0.31 | 0.42 | 0.78 | 0.53 | 0.54 | 0.57 | 0.08 | 14 | 69 | 73 | 276/61/56/39 |
| 3 | 576 | 77% | 46.1 | 76.0 | 86.3 | 0.46 | 0.32 | 0.42 | 0.78 | 0.50 | 0.60 | 0.58 | 0.07 | 12 | 69 | 72 | 280/59/53/51 |
| 4 | 576 | 78% | 44.7 | 75.0 | 85.4 | 0.45 | 0.32 | 0.41 | 0.77 | 0.48 | 0.55 | 0.57 | 0.07 | 11 | 64 | 73 | 283/78/43/44 |
| 5 | 576 | 80% | 43.2 | 72.3 | 88.3 | 0.44 | 0.28 | 0.39 | 0.73 | 0.49 | 0.57 | 0.53 | 0.05 | 8 | 63 | 75 | 311/60/42/46 |
| 6 | 576 | 76% | 43.9 | 73.5 | 88.6 | 0.45 | 0.30 | 0.38 | 0.75 | 0.48 | 0.55 | 0.55 | 0.07 | 12 | 62 | 75 | 290/58/41/47 |
| 7 | 576 | 74% | 47.5 | 78.3 | 88.7 | 0.49 | 0.31 | 0.41 | 0.76 | 0.53 | 0.61 | 0.62 | 0.08 | 13 | 63 | 78 | 270/53/47/55 |
| 8 | 444 | 76% | 45.9 | 75.9 | 91.2 | 0.47 | 0.29 | 0.41 | 0.75 | 0.52 | 0.58 | 0.57 | 0.07 | 11 | 65 | 75 | 231/38/28/40 |
| 9 | 281 | 77% | 45.1 | 75.2 | 89.3 | 0.46 | 0.29 | 0.42 | 0.76 | 0.46 | 0.58 | 0.56 | 0.06 | 10 | 56 | 78 | 150/31/12/24 |
| 10 | 141 | 75% | 48.7 | 73.2 | 85.8 | 0.51 | 0.30 | 0.43 | 0.85 | 0.54 | 0.57 | 0.62 | 0.07 | 8 | 73 | 76 | 66/22/7/11 |
| 11 | 19 | 58% | 42.0 | 57.3 | 69.6 | 0.39 | 0.29 | 0.37 | 0.64 | 0.38 | 0.54 | 0.62 | 0.05 | 9 | 64 | 64 | 8/1/1/1 |

Population-level screen stats are FLAT (meanI 43-48, C-components stable):
the search does not drift the whole population upward, it ratchets the
ARCHIVE. Best-of-gen: 88.5 (g1, inherited pool elites) -> plateau -> 88.6
(g6) -> 88.7 (g7) -> **91.2 (g8, champion)** -> 89.3 (g9). Gen-11 is a
19-row tail shard (island 6 only).

## Archive/union composition across the campaign checkpoints

Interest distribution of union holders:

| checkpoint | cells | meanI | medI | p90 | max | >=70 | >=80 |
|------------|------:|------:|-----:|----:|----:|-----:|-----:|
| union4_final_cpu | 182 | 44.4 | 42.7 | 69.0 | 81.9 | 17 | 3 |
| union5_prebatch | 190 | 44.3 | 42.0 | 69.0 | 81.9 | 18 | 4 |
| gpu_b_union1 | 362 | 46.5 | 45.0 | 74.2 | 88.5 | 46 | 22 |
| UNION_FINAL_v2 | 423 | 47.0 | 45.7 | 73.2 | 91.2 | 50 | 28 |

The GPU-batched eras did the heavy lifting: cells x2.2 (190->423), >=70
count x2.8 (18->50), >=80 count x7 (4->28).

## Did the staging / memory / roles axes move?

Cell-key axis occupancy (share of cells):

| axis | union4_cpu | union5 | gpu_b_union1 | FINAL | verdict |
|------|-----------|--------|--------------|-------|---------|
| stages s2 | 18 (10%) | 18 (9%) | 40 (11%) | **49 (12%)** | s2 nearly x3 in count; meanI 65.1 |
| stages s3 | 4 (2%) | 4 (2%) | 11 (3%) | **12 (3%)** | x3 count; s3 meanI **81.4** — deep succession = elite |
| mem g1 | 24 (13%) | 26 (14%) | 68 (19%) | **87 (21%)** | partial-memory band widened most |
| mem g2 | 103 (57%) | 106 (56%) | 177 (49%) | 197 (47%) | count +91 but share fell (g0/g1 exploration) |
| phase flicker | 19 (10%) | 20 (11%) | 64 (18%) | **82 (19%)** | flicker graph-phase x4.3 — new territory of the batched eras |
| phase gas | 7 (4%) | 7 (4%) | 16 (4%) | 25 (6%) | x3.6 |
| growth oscillator | 19 (10%) | 20 (11%) | 63 (17%) | **75 (18%)** | x3.9 |
| growth relaxation | 1 (1%) | 1 (1%) | 6 (2%) | **12 (3%)** | x12 — rarest class got occupied |
| spp 3 / 4 | 54/54 | 57/56 | 112/106 | 128/119 | stable ~58% multi(3+)-species |

C-component means over union holders (u4 -> FINAL):
C7_roles 0.510 -> **0.559** (n>0.5: 94 -> 248), C2_timescale 0.349 -> **0.398**
(n>0.5: 48 -> 142), C8_succession 0.071 -> 0.086 (n>0.5: 4 -> 12),
C5_memory 0.499 -> 0.456 (dilution by new low-memory cells; n>0.5 still
111 -> 249), C3_motion flat 0.39.
VERDICT: yes — roles and timescale-separation moved up, succession cells
tripled (and own the top of the leaderboard), memory stayed the largest
occupied axis but its SHARE diluted as exploration filled g0/g1 bands.

## Interest by stage / memory grade (FINAL union)

| group | n | meanI | maxI |
|-------|--:|------:|-----:|
| s1 | 362 | 43.4 | 85.7 |
| s2 | 49 | 65.1 | **91.2** |
| s3 | 12 | **81.4** | 89.3 |
| g0 | 139 | 38.3 | 76.9 |
| g1 | 87 | 45.5 | 88.0 |
| g2 | 197 | **53.8** | 91.2 |

Succession stage is the strongest single predictor of interest in the
final archive.

## box_limit & battery flags

- box_limit-flagged screens (era4): **2783 / 3762** flagged rows (74%) —
  most live worlds span the whole L=128 box; 337/423 union holders are
  box_limited. The L192 confirm lane (cap 2/gen per island) exists for
  exactly these; box-limit is the norm at elite level, not an anomaly.
- battery_mode=subsampled rows: **0** in the final harvest (the x4-stride
  retry never SUCCEEDED-with-flag); instead **26 assay_error rows** =
  `battery_timeout(300s; subsample x4 retry also timed out)` (isl3: 10,
  isl6: 9, isl4: 4, isl1: 2, isl5: 1, isl2: 0). These are dropped, not
  scored — no subsampled metrics contaminate the archive.
