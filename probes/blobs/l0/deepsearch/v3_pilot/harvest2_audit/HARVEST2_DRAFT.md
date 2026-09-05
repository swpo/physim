# HARVEST2 — audited final v3 continuation (draft)

**Scope:** two islands, creative generations 1–12, with generation-12 seed2/seed3 settlement complete. This is a local read-only analysis of the settled small files. No simulations, model evaluations, remote jobs, full archive extraction, raw-data rewrites, or web-page edits were performed by the main audit. Supplemental history notes pin selected source-text members from the already-local final archives.

## Measured verdict

The changed-configuration continuation added qualifying MAP-Elites descriptor bins and raised the best observed **partial-C9** same-genome confirmation from **0.8504 to 0.8895**. It did not show uniform improvement across islands or across selected confirmations. Screen success improved descriptively, but the selected-confirmation distribution and candidate-level validation yields did not improve uniformly.

This is **not** proof of biological cells, heterogeneous compartments, or a new biological organization level. Full C9 was not measured during the continuation. h9 remains exploratory; this harvest does not validate it. The operator mix, retry limits, objective weight, and parent archive changed together. These data do not identify their separate causal effects. They also do not test an unrun same-configuration continuation. The earlier forecast that the C9 ceiling could not improve under that counterfactual lacked evidence.

## 1. Sources, identity, and exclusions

The audit rehashes all ten critical settled files and matches the existing independent final-archive verification records. It does not rehash the two large archives. Their recorded SHA256 values and every small input hash are in `source_manifest.json`. Both final states are generation 12. The 2,324 baseline rows are exactly preserved in the final results and are not counted twice.

| Artifact owner | Raw final rows | Creative screens | Selected confirmation rows | C9fill raw / retained | Atlas imports |
| --- | --- | --- | --- | --- | --- |
| 1 | 1850 | 1054 | 705 | 88 / 88 | 3 |
| 2 | 1756 | 1045 | 626 | 82 / 80 | 3 |

Identity is the actual row tuple **(island, cand, phase, seed)**. Candidate-name prefixes are not island evidence. The 3,606 raw rows contain 3,605 distinct keys. One key has contradictory model payloads. Both variants are quarantined from primary summaries, leaving **3,604 retained rows**: 2,099 creative screens, 1,331 selected assay rows, 168 C9 backfill imports, and six atlas imports.

The conflicting key is `(2, p1g2_008_c9, c9fill, 958)`. Its two rows have:

- ghash `a19e1629a9d1fb98`, 4 activators / 8 channels, C9 0.4215, raw I 54.57172838379547;
- ghash `6aef37d09adb821c`, 2 activators / 5 channels, C9 0.4855, raw I 59.5337117778859.

Both donor entries already share the name `p1g2_008`. The backfill generator iterates archive entries without an identity-safe output name. Both rows declare `p1g2_008_c9.npz`. A single candidate-based path is therefore ambiguous. Row timestamps do not establish which genome the surviving film contains or prove overwrite timing. See `dedup_conflicts.json` and `history_evidence.json:c9fill_duplicate`. Both raw variants remain in `observations.csv` with `primary_included=False`.

### Eleven baseline seed3 rows are not replications of the named screen genome

All 2,318 generation-1–7 job/result pairs agree on the actual genome, parent list, and operator. However, eleven seed3 **jobs themselves** use a donor genome with the same base name as a new v3 candidate. Their physical model fields differ from the screen/seed2 model. These are not id, tag, provenance, or float-format-only differences.

`g0import` keeps donor names. New screens reuse `p{island}g{gen}_{index}`. `archive_seedk` takes the first archive entry whose candidate name matches after suffix stripping. `cmd_ingest2` then builds seed3 from that entry's genome, not the seed2 result's genome. The selected donor model matches each anomalous seed3 row exactly. See `pod_lib.py:291–306`, `pod_gen.py:375–393`, and the pinned source excerpts in `history_evidence.json`.

| Island | seed3 row | Screen ghash | Actual seed3 ghash | Physical fields that differ | Named screen op → actual model op |
| --- | --- | --- | --- | --- | --- |
| 1 | p1g2_021_s3 | cd3b802cf2dc17d5 | 67cf8460076bdd5b | acts, chans, bilin | mint_bilin → mint_bilin |
| 1 | p1g2_034_s3 | 158f0c237e4f658e | 65ee88a4e85ee72d | acts, chans, W, K, bilin | add_chan → delete_bilin |
| 1 | p1g3_035_s3 | 46505242674afd5a | a065779eaf3df961 | acts, chans, W, K, bilin | add_chan → delete_bilin |
| 2 | p2g2_023_s3 | 7fa13f78a42abf98 | 18fb4a511bd5fd41 | acts, chans, W, K, bilin | mint_bilin → mint_bilin |
| 2 | p2g2_038_s3 | 5c3b22eec22509f0 | ad835d9583d074b2 | chans, W, K, bilin | add_chan → add_chan |
| 2 | p2g2_070_s3 | 2ccd2e15c8fa6fb9 | 3403b1a691db96ea | acts, chans, W, K, bilin | merge_cross_edge → merge_cross_edge |
| 2 | p2g3_073_s3 | 97de45f90d6ebef4 | 6da2f3231522e927 | acts, chans, W, K, bilin | merge_cross_edge → merge_share_chan |
| 2 | p2g4_002_s3 | 583c31fd9c9b98d6 | bcc3072a07e51f96 | acts, chans, W, K, bilin | mutate → mutate |
| 2 | p2g4_015_s3 | a04fca4ed04a8fd9 | 04a0f0e5eb95cb51 | acts, chans, W, K, bilin | mutate → mutate |
| 2 | p2g4_030_s3 | 2d9a00b0dec7e567 | ca21e100b2dea0c3 | acts, chans, W, K, bilin | delete_bilin → mint_bilin |
| 2 | p2g7_039_s3 | 9e7b3a1d8d445359 | fa86cb8089d048d0 | acts, chans, W, K, bilin | add_chan → add_chan |

`confirmation_join_anomalies.json` records the exact keys, donor entries, job paths, model hashes, and sample numeric differences. These eleven runs remain valid observations of their actual models, but do not count as third-seed confirmations of the named v3 screens. Three meet the joint threshold at W9=.25; two meet it at W9=.40.

Strict physical-genome matching succeeds for **931/942 baseline selected assay rows** and **389/389 continuation selected assay rows**. This is a statement about these stored result/job identities, not a blanket validity claim for all runs. It does not establish same-initial-condition replication.

## 2. Common scores and metric modes

For each preserved row, compute only:

```text
I_w = (1-w) * interest_v2_preserved + 100*w*C9
w in {0.25, 0.40}
qualifying = status == "ok" AND C9 >= 0.4 AND I_w >= 60
```

The raw `interest` field is unchanged and retained in `observations.csv`. No old/new raw-interest difference is treated as like-for-like. The formula rescales stored measurements; it does not rerun the metric or the search. Partial C9 omits s9 and is not the same assay as full four-factor C9. Missing C9 is not assigned zero in metric means. Missing/failed screens still count in the screen-lane denominator.

There are 19 full-C9 rows: six atlas imports and 13 generation-1 creative screens. All continuation and C9fill measurements are partial. The following table separates full and partial observations. Mean scores are conditional on the shown measured rows; they are not means over all emitted lanes.

| Creative cohort | C9 mode | Measured n | Mean C9 | Median C9 | Max C9 | Mean I.25 | Mean I.40 | Q.25 / bins | Q.40 / bins |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| g1–7 | partial | 1114 | 0.2599 | 0.2920 | 0.7576 | 47.74 | 43.39 | 275 / 55 | 237 / 48 |
| g1–7 | full | 13 | 0.4487 | 0.4143 | 0.6979 | 63.56 | 59.83 | 6 / 4 | 4 / 3 |
| g8 | partial | 156 | 0.3016 | 0.3692 | 0.7000 | 49.56 | 45.68 | 49 / 21 | 38 / 17 |
| g9–12 | partial | 523 | 0.2870 | 0.3330 | 0.8185 | 48.63 | 44.64 | 137 / 47 | 121 / 41 |
| g8–12 | partial | 679 | 0.2903 | 0.3407 | 0.8185 | 48.84 | 44.88 | 186 / 50 | 159 / 45 |

The retained backfill imports are separate from creative progress: 168 partial-C9 rows, mean 0.3188, median 0.3719, maximum 0.6393. They yield 64 qualifying rows / 34 bins at W9=.25, and 59 / 32 at W9=.40. These counts exclude the two ambiguous variants. Atlas imports yield no joint-threshold successes.

Selected confirmations are also separate. Their means are selection-biased and are not estimates of the complete screen population. This table uses only correctly linked physical genomes:

| Cohort | Selected assay n | C9 measured n | Mean / median C9 | Max C9 | Mean I.25 / I.40 | Q.25 / Q.40 |
| --- | --- | --- | --- | --- | --- | --- |
| g1–7 | 931 | 930 | 0.2619 / 0.2797 | 0.8504 | 51.70 / 46.60 | 232 / 200 |
| g8 | 93 | 93 | 0.1844 / 0.0645 | 0.6824 | 43.12 / 38.19 | 17 / 16 |
| g9–12 | 296 | 296 | 0.2275 / 0.0983 | 0.8895 | 44.72 / 40.32 | 62 / 58 |
| g8–12 | 389 | 389 | 0.2172 / 0.0837 | 0.8895 | 44.33 / 39.81 | 79 / 74 |

The continuation's observed partial-C9 screen mean is higher than the baseline's, but its selected-confirmation mean is lower. The maximum and distribution tell different stories. Neither difference isolates an operator or configuration effect.

## 3. Screen-only generation tables and descriptor breadth

Below, `n` includes every emitted creative screen. C9 mean/median/max use only measured rows. `P/F` gives partial/full measurement counts. Generation 1's aggregate C9 statistic is mixed-mode; its full/partial split is above and in the CSV. Qualifying counts use the common score at each weight. Bins are exact **MAP-Elites descriptor bins**, not biological cells or heterogeneous compartments. Island-specific and mode-specific tables are in `screen_by_generation.csv`.

| Gen | n | ok / no_blobs / fail_g0a | P/F | C9 mean / median / max | Q.25 / bins | Q.40 / bins |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 200 | 157 / 28 / 15 | 144/13 | 0.2697 / 0.3343 / 0.6979 | 37 / 24 | 30 / 21 |
| 2 | 199 | 162 / 23 / 14 | 162/0 | 0.2747 / 0.2969 / 0.7576 | 42 / 22 | 36 / 21 |
| 3 | 196 | 171 / 17 / 8 | 171/0 | 0.2521 / 0.2840 / 0.7026 | 41 / 24 | 35 / 21 |
| 4 | 195 | 164 / 18 / 13 | 164/0 | 0.2558 / 0.2804 / 0.6314 | 38 / 23 | 33 / 22 |
| 5 | 193 | 158 / 22 / 13 | 158/0 | 0.2552 / 0.2922 / 0.7412 | 36 / 22 | 30 / 19 |
| 6 | 198 | 158 / 26 / 14 | 158/0 | 0.2641 / 0.2882 / 0.6485 | 46 / 27 | 41 / 25 |
| 7 | 195 | 157 / 22 / 16 | 157/0 | 0.2638 / 0.3053 / 0.6864 | 41 / 19 | 36 / 17 |
| 8 | 163 | 156 / 5 / 2 | 156/0 | 0.3016 / 0.3692 / 0.7000 | 49 / 21 | 38 / 17 |
| 9 | 142 | 132 / 7 / 3 | 132/0 | 0.2630 / 0.2628 / 0.7436 | 35 / 23 | 31 / 21 |
| 10 | 141 | 130 / 8 / 3 | 130/0 | 0.2917 / 0.3270 / 0.7360 | 31 / 20 | 27 / 17 |
| 11 | 138 | 130 / 4 / 4 | 130/0 | 0.3054 / 0.3728 / 0.8185 | 40 / 26 | 35 / 21 |
| 12 | 139 | 131 / 6 / 2 | 131/0 | 0.2881 / 0.3235 / 0.7916 | 31 / 21 | 28 / 19 |

Across screens only, baseline g1–7 has **59 / 51 qualifying bins** at common W9=.25/.40. Continuation g8–12 has **50 / 45**, including **12 / 14 bins** not seen qualifying in the baseline. The unions are **71 / 65**. In partial mode alone, the corresponding baseline counts are 55 / 48 and the unions are 67 / 62. These are observed-bin counts, not newly created archive entries.

The old **516 rows / 76 union bins** is reproducible at common W9=.25 when screens and selected assay rows are pooled. It is not 516 independent candidates or 76 verified archive incumbents. Excluding the three qualifying wrong-genome seed3 links leaves 513 correctly linked/screen qualifying observations, while the union remains 76 because those bins also have other observations. The corresponding correctly linked W9=.40 row count is 441, with 66 union bins. Screen-only baseline counts are 281 / 241 rows, not 516. Generation 1 alone has 102 pooled qualifying rows in 38 bins at W9=.25, not the full seven-generation 76-bin union.

## 4. Corrected candidate and operator rates

Definitions:

- **Screen success:** qualifying screen / all emitted creative screens.
- **Any-confirmed base:** at least one correctly linked same-genome seed2/seed3 assay qualifies. The screen need not qualify. Count each `(island, base candidate)` once.
- **Three-seed joint-threshold base:** screen, seed2, and seed3 all qualify, with matching physical genome and three distinct seeds. The CSV calls this `robust_three_seeds`; it is not a probability guarantee for new seeds.
- **Partial-only three-seed base:** the previous condition plus partial C9 on all three assays.

The all-base denominator measures observed validation yield. Unselected candidates have missing confirmation evidence, not proven failures. The selected and complete-pair denominators are shown separately. Selection is adaptive. Candidate names are distinct counting units, not independent random samples: the 2,099 creative candidates contain 1,929 distinct physical ghashes and share ancestry.

| Cohort | W9 | Screen / all | Selected / valid pairs | Any confirm / all | Any confirm / selected | Three-seed / all | Three-seed / pairs | Partial-only three-seed n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| g1–7 | 0.25 | 281/1376 (20.4%) | 496 / 435 | 148/1376 (10.8%) | 148/496 (29.8%) | 67/1376 (4.9%) | 67/435 (15.4%) | 66 |
| g1–7 | 0.40 | 241/1376 (17.5%) | 496 / 435 | 130/1376 (9.4%) | 130/496 (26.2%) | 55/1376 (4.0%) | 55/435 (12.6%) | 54 |
| g8 | 0.25 | 49/163 (30.1%) | 47 / 46 | 10/163 (6.1%) | 10/47 (21.3%) | 6/163 (3.7%) | 6/46 (13.0%) | 6 |
| g8 | 0.40 | 38/163 (23.3%) | 47 / 46 | 9/163 (5.5%) | 9/47 (19.1%) | 5/163 (3.1%) | 5/46 (10.9%) | 5 |
| g9–12 | 0.25 | 137/560 (24.5%) | 151 / 145 | 35/560 (6.2%) | 35/151 (23.2%) | 23/560 (4.1%) | 23/145 (15.9%) | 23 |
| g9–12 | 0.40 | 121/560 (21.6%) | 151 / 145 | 33/560 (5.9%) | 33/151 (21.9%) | 22/560 (3.9%) | 22/145 (15.2%) | 22 |
| g8–12 | 0.25 | 186/723 (25.7%) | 198 / 191 | 45/723 (6.2%) | 45/198 (22.7%) | 29/723 (4.0%) | 29/191 (15.2%) | 29 |
| g8–12 | 0.40 | 159/723 (22.0%) | 198 / 191 | 42/723 (5.8%) | 42/198 (21.2%) | 27/723 (3.7%) | 27/191 (14.1%) | 27 |

### Why 0.82 was not an operator hit rate

The old `merge_spatial_ic` numerator 92 combined **52 qualifying screens + 40 qualifying selected confirmation rows**, then divided by 112 screen lanes. The corrected W9=.25 screen rate is **52/112 = 46.4%**. At candidate level, **23/112 = 20.5%** have at least one qualifying same-genome confirmation, and **12/112 = 10.7%** meet the three-assay threshold (11 are partial-only). Among the 49 selected bases, the any-confirmed fraction is 23/49; among 44 valid complete pairs, the three-assay fraction is 12/44. At W9=.40, the counts are 45 screen successes, 21 any-confirmed bases, and 12 three-assay bases.

**Initial-condition caveat:** SIC screens use a composed `ic_npz`. The seed2 and seed3 builders omit `ic_npz` and use ordinary genome reseeds. All 182 stored SIC screens have `ic_merge=True`; all 130 SIC-origin confirmation rows lack that flag. Thus these are same-genome assays under a different initial-state construction, **not replications of the spatially composed phenotype**. This design difference is separate from the eleven wrong-genome substitutions.

The corrected baseline operator table at common W9=.25 follows. All numerators are one-count-per-base, except the explicitly screen-only column. Both weights, both islands, and all continuation cohorts are in `operator_rates.csv`.

| Origin operator | Screen success / all bases | Selected bases | Any-confirmed / all bases | Three-assay / all bases |
| --- | --- | --- | --- | --- |
| add_chan | 26/112 (23.2%) | 60 | 20/112 (17.9%) | 8/112 (7.1%) |
| delete_bilin | 19/56 (33.9%) | 21 | 7/56 (12.5%) | 5/56 (8.9%) |
| dup_act | 0/112 (0.0%) | 39 | 1/112 (0.9%) | 0/112 (0.0%) |
| immigrate | 0/280 (0.0%) | 8 | 0/280 (0.0%) | 0/280 (0.0%) |
| merge_cross_edge | 65/219 (29.7%) | 100 | 36/219 (16.4%) | 11/219 (5.0%) |
| merge_share_chan | 0/51 (0.0%) | 9 | 2/51 (3.9%) | 0/51 (0.0%) |
| merge_slow_tanh | 14/42 (33.3%) | 22 | 8/42 (19.0%) | 5/42 (11.9%) |
| merge_spatial_ic | 52/112 (46.4%) | 49 | 23/112 (20.5%) | 12/112 (10.7%) |
| mint_bilin | 57/168 (33.9%) | 72 | 26/168 (15.5%) | 11/168 (6.5%) |
| mutate | 48/224 (21.4%) | 116 | 25/224 (11.2%) | 15/224 (6.7%) |

SIC has the largest observed baseline screen success fraction, but the experiment did not randomly assign common parents and initial states to operators. The result is not a controlled causal validation. Continuation SIC has 28/70 screen successes at W9=.25, six any-confirmed bases, and four three-assay bases. Genome reuse is especially common in SIC: 112 baseline SIC candidates contain 43 distinct ghashes; 70 continuation SIC candidates contain 34. Different composed screens can share a genotype, while ordinary confirmation reseeds can repeat the same genotype/seed outcome under different candidate names.

## 5. Actual generator/configuration history

Use jobs, code, and campaign history rather than stale config comments. Requested counts are per island per generation. See `history_notes.md` and `history_evidence.json` for exact source lines and hashes.

| Setting | g1–7 | g8 only | g9–12 |
| --- | --- | --- | --- |
| W9 | .25 | .40 | .40 |
| mutate | 16 | 16 | 22 |
| mint_bilin | 12 | 16 | 18 |
| delete_bilin | 4 | 4 | 4 |
| add_chan | 8 | 8 | 8 |
| dup_act | 8 | 0 | 0 |
| SIC target slots | 8 | 24 | 12 |
| SIC retries per target | pilot generator | 60 | 12 |
| immigrate | 20 | 5 | 5 |
| merge_mix cross / slow / share | 12 / 8 / 4 | 14 / 6 / 0 | 14 / 6 / 0 |
| Actual classical merge target slots | 24 | 20 | 20 |
| Total requested creative slots | 100 | 93 | 89 |

`mix.merge=20` is not the generator's classical-merge loop bound. `merge_mix` supplies the loop plan, so the old plan totals 24, not 20. A slow-tanh target can fall back to a cross-edge child, and retry failure can drop a target. Requested and emitted counts therefore differ. Gen8 emitted 81/82 creative jobs across the two islands. Gens9–12 emitted 72/70, 69/72, 70/68, and 72/67.

The SIC target changes from 24 to 12 **at generation 9**, with retry cap 12. The final generator differs from the launch generator only in SIC retry cap 60→12 at line 203. `campaign9.sh` and both campaign logs pin the resume to generation 9. The settled `_midcourse` text saying “gens10–12” is stale. The gen8→gen9 mutate/mint increases are **+6 and +2**, not “+6 each.” Relative to the original pilot, their values are 16→22 and 12→18, respectively.

| Gen | SIC emitted isl1 | SIC emitted isl2 | SIC target per island |
| --- | --- | --- | --- |
| 8 | 22 | 23 | 24 |
| 9 | 2 | 1 | 12 |
| 10 | 2 | 7 | 12 |
| 11 | 5 | 4 | 12 |
| 12 | 3 | 1 | 12 |

The continuation emitted 70 SIC screens in total: 45 in gen8 and 25 in gens9–12, not 24 lanes per island for all five generations. `operator_emitted_by_generation.csv` records all actual screen operators. Broader changes also include C9 backfill, reblended parent selection, and C9 field propagation into new archive entries. Their joint effect cannot be separated from objective weight or operator mix using this continuation alone.

## 6. Archive reblend limitations — identified, not repaired

The final archives have 343 and 327 entries. Each still includes 100 legacy six-axis keys; the remaining keys have seven axes. This is not a count of biological compartments. The stored union contains 435 descriptor keys, which must not replace the qualifying-observation bin counts above.

All 496 surviving `_reblended_w9=.4` entries reproduce the historical script's numeric score and C9 join. However, that script selects the highest **stored-interest** row after name-suffix splitting, then copies its new blend/C9 annotation into an existing entry. It does not require the same physical genome, descriptor key, or seed, and does not update the archive key, genome, horizon, summary, or existing confirmation fields.

| Island | Marked entries | Different physical genome | Different descriptor key | Of these: seven-axis keys | Different winning row if ranked at common .40 |
| --- | --- | --- | --- | --- | --- |
| 1 | 243 | 11 | 173 | 73 | 13 |
| 2 | 253 | 18 | 179 | 79 | 14 |

### Initial contamination versus surviving entries

The initial join can be reconstructed without later-generation rows: use each original 269-entry gen7 archive and the preserved baseline-plus-C9fill result prefix. All 538 initial targets join; none is retained for lack of C9. The initial and surviving scopes differ as follows:

| Island | Scope | Entries | Wrong physical model | Different descriptor key | Exact-model screen references | Different seed from that screen |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | initial_gen7_archive | 269 | 11 | 183 | 169 | 118 |
| 1 | surviving_marked_final | 243 | 11 | 173 | 143 | 98 |
| 2 | initial_gen7_archive | 269 | 18 | 182 | 169 | 113 |
| 2 | surviving_marked_final | 253 | 18 | 179 | 153 | 106 |

The same 29 wrong-physical-model key/source pairs are present initially and survive at the end. The 42 replaced entries contain no wrong-model joins; their 13 descriptor mismatches explain the reduction from 365 to 352. This reconstruction supports the initial count rather than assuming the surviving count was the full initial impact.

**Seed limitation:** all 538 initial and all 670 final entries omit the target `seed` field. Therefore a universal wrong-target-seed count is not identifiable. The last two table columns compare the chosen source seed only to an exact name-and-physical-model matching historical screen, where one exists. Different source seeds are expected when intentionally choosing a best reseed; they are not automatically wrong seeds. Two island-2 cases also choose the wrong physical model. See `reblend_initial_vs_surviving.csv` for every initial and surviving target.

Of the 29 physical-genome mismatches, 27 are imported gen0 entries. Two are island-2 v3 entries (`p2g2_038`, `p2g7_039`) whose chosen seed3 model is a namesake donor. The 352 descriptor mismatches include all 200 legacy six-axis keys and 152 seven-axis keys. A different descriptor on a correctly matched reseed can be real behavioral variation; the problem is attaching that score to an unchanged archive key as if it measured the same bin/run.

The reblend ranking also mixes old stored weights with already-.40 backfill rows. For 27 surviving entries, selecting by common W9=.40 would choose a different row. This is a diagnostic only. It is not a silent archive repair. Numeric “single currency” does not establish model/run provenance.

The native seed3-ok counts are 103/99 in the final archives (74/73 in the baseline). Native `seed{k}_ok` means positive score ≥0.6× incumbent score, not the joint C9/interest threshold, and name-only matching is unsafe. These flags must not be presented as strict same-genome or same-IC confirmation counts. See `archive_reblend_diagnostics.csv` for every surviving entry and `history_evidence.json` for all 29 mismatched identities.

## 7. Confirmed maxima and image candidates

These maxima use explicit parents plus matching physical genomes. All are partial C9. “Confirmed” here means the row is a correctly linked selected reseed, not that every tested seed has the maximum or passes the joint threshold.

| Island | Cohort | Maximum-C9 selected row | C9 | Preserved I2 | Common I.25 | Common I.40 | Qualifies at .25/.40 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | g1–7 | p1g1_009_s3 | 0.8504 | 74.596 | 77.207 | 78.773 | True/True |
| 1 | g8–12 | p1g12_049_s3 | 0.8895 | 78.451 | 81.076 | 82.650 | True/True |
| 2 | g1–7 | p2g6_032_s2 | 0.8048 | 74.797 | 76.218 | 77.070 | True/True |
| 2 | g8–12 | p2g10_023_s2 | 0.7123 | 48.211 | 53.966 | 57.418 | False/False |

Island 2's continuation maximum C9=0.7123 does **not** meet I≥60 at either common weight. Its full-run maximum remains the older 0.8048 row. The best continuation island-2 C9 row that does meet both thresholds is `p2g8_020_s2` (0.6824).

The final overall joint-score maximum is `p1g12_049_s2`: preserved I2=81.38231987330606, C9=.8854, common I.25=83.17173990497955 and I.40=84.24539192398363. The final overall C9 maximum is its seed3 row `.8895`, not the old `.8504`.

Recommended image subjects include the following distinct base candidates. The CSV contains exact raw inputs, seed rows, archive/member paths, and threshold flags. A path is a locator, not evidence that a film has been visually reviewed here.

| Base candidate | Origin op | C9 screen / seed2 / seed3 | Three-assay pass at .25/.40 | Image role |
| --- | --- | --- | --- | --- |
| p1g11_043 | delete_bilin | 0.8185 / 0.0000 / 0.0000 | False/False | unstable_high_screen_control |
| p1g12_007 | mutate | 0.7916 / 0.5677 / 0.8867 | True/True | top_confirmed_C9_candidate |
| p1g12_037 | mint_bilin | 0.5299 / 0.8195 / 0.4901 | True/True | top_confirmed_C9_candidate |
| p1g12_049 | add_chan | 0.6737 / 0.8854 / 0.8895 | True/True | top_confirmed_C9_candidate |
| p2g10_023 | mint_bilin | 0.6486 / 0.7123 / 0.3989 | False/False | top_confirmed_C9_candidate |
| p2g6_032 | add_chan | 0.4320 / 0.8048 / 0.4952 | True/True | top_confirmed_C9_candidate |
| p2g8_020 | mint_bilin | 0.4717 / 0.6824 / 0.4573 | False/False | top_confirmed_C9_candidate |

Current final film-selection manifests also resolve to the following exact row identities. All six row indices match, none is a known wrong-genome confirmation, and all five confirmation items match their screen genome. The screen item is not itself a confirmation. Three manifests embed legacy job payloads; those three match their actual row models. Missing embedded jobs are not counted as checked by this particular manifest audit. Replay output is outside this audit; see `film_selection_identity_checks.json`.

| Island | Selected row | Phase | Seed | Actual origin op | Embedded job model checked |
| --- | --- | --- | --- | --- | --- |
| 1 | p1g12_049_s2 | seed2 | 958 | add_chan | not embedded |
| 1 | p1g12_007_s3 | seed3 | 959 | mutate | not embedded |
| 1 | p1g1_009_s3 | seed3 | 959 | mutate | True |
| 2 | p2g6_032_s2 | seed2 | 965 | add_chan | True |
| 2 | p2g11_036 | screen | 964 | mint_bilin | not embedded |
| 2 | p2g1_025_s2 | seed2 | 965 | mint_bilin | True |

`p1g12_049` is an `add_chan` child of `p1g11_043`; `p1g12_007` is a `mutate` child of the same parent. `p1g11_043` is a `delete_bilin` child of `p1g10_048`. The middle candidate's screen C9=.8185 falls to zero in both ordinary reseeds, so it is a useful instability control. Its descendants' high observations are not evidence of monotonic robust lineage improvement.

The old HARVEST image examples (`p1g1_009_s3`, `p2g6_032_s2`, `p1g3_005_s3`, `p1g2_051_s3`, `p1g2_052_s3`, `p1g4_050_s3`, `p2g7_049_s3`) are outside the eleven wrong-genome set. Four anomalous seed3 origin labels do change, as listed in section 1. Films of any affected row must use that row's actual job genome/seed/phase, not a suffix-inferred parent. SIC film captions must also distinguish composed screen IC from soup reseeds.

## 8. Corrections needed in posts 10/12 and the old harvest notes

No web pages or old harvest documents were edited by this audit. These corrections refer to the exact reviewed versions pinned in `interpretation_source_pins.json`. Concurrent edits may already address some items. Validation detected that post12 changed after review; its original hash and quoted line excerpts are retained rather than silently repinned. `VALIDATION.json` records interpretation drift separately from immutable data/code input checks.

### Post 12: `docs/blobs/breeding-spatial-economies.html`

- Lines 40–46, 115–120: call 76 a union of qualifying observed **descriptor bins** over screens and selected assays, not 76 archived biological/economy cells or independent candidates. Use screen-only rates and separate native archive flags from strict confirmation.
- Lines 63–65: replace the displayed additive equation with `(1-W9)*interest_v2 +100*W9*C9`.
- Lines 126–141: replace or label the pooled-generation table. It is not a screen-only trial series. Supply full/partial and denominator distinctions.
- Lines 143–170 and the associated chart: replace 0.82 and the whole mixed-row “hit-rate” table. Use screen success and one-count-per-base confirmation rates. State SIC's changed-IC confirmation design.
- Lines 173–179 and 211–233: retain the limited observation that the initial global maximum appeared early. Remove a fixed-ceiling forecast and the claim that all 76 bins appeared in one generation. Changed-config continuation is not a same-config counterfactual test, nor a grammar-ceiling proof.
- Lines 220–227: describe sic24 for gen8 only, then sic12+retry12 for gens9–12; mutate22/mint18; actual `merge_mix` planning and emitted counts. Do not carry the stale midcourse note forward.
- Label the actual new maxima and full-vs-partial limits. Do not imply that a proxy or a film proves heterogeneous compartments.

### `HARVEST.md` and `POST12_FACTS.json`

Correct `operator_hit_rate`, pooled `per_gen` labels, `continuation`, and the counterfactual ceiling prose. Keep the historical 516/76 figures only with their proper pooled-observation definition. “Strict economy class = 6” means **six qualifying full-C9 rows at W9=.25**, not six total class-economy rows: there are 18 total, including atlas imports and nonqualifying screens. The corresponding qualifying count at W9=.40 is four. No partial-C9 continuation row can satisfy the full-s9 spatial-class rule.

Do not call the reblended archive fully provenance-consistent just because its scalar scores use one formula. Add the contradictory C9fill key, the eleven wrong-genome seed3 jobs, and the 29 surviving reblend identity mismatches. None should be silently rewritten.

### Post 10: `docs/blobs/evolving-at-scale.html`

This audit does **not** re-audit the original v2 campaign's 423-bin, 9,409-evaluation, lineage, or I=91.16 claims. Do not replace those numbers with v3 data. Clarify “cells” as MAP-Elites descriptor bins where needed. Keep original v2 scores distinct from normalized v3 scores; 91.16 v2 and 84.2454 v3 are not directly comparable. Cross-links and new captions must not assume a reused candidate name uniquely identifies a v2/v3 model. C9fill imports and v3 descendants are not newly discovered v2 archive worlds. Original v2 provenance claims need their own source-genome audit before any numerical correction.

## 9. Reproduction and source pins

From the project root, in its own environment:

```sh
.venv/bin/python probes/blobs/l0/deepsearch/v3_pilot/harvest2_audit/audit.py
.venv/bin/python probes/blobs/l0/deepsearch/v3_pilot/harvest2_audit/write_report.py
.venv/bin/python probes/blobs/l0/deepsearch/v3_pilot/harvest2_audit/validate_audit.py
```

`audit.py` reads only small settled/reference JSON, logs, configs, and baseline job JSON. It does not depend on the ongoing metadata/film extraction. The optional `history_evidence.json` is a pinned supplement with source excerpts; the report uses it for the history section. Source-history pins can be checked with a selective text-member read, without extracting the archive to disk. Main assertions check final counts, small-file certificates, baseline row identity, all baseline job/result identities, and the eleven strict-genome mismatches.

Primary outputs:

- `observations.csv`: preserved raw scores, common-weight scores, phase/mode, identity, and inclusion flags for every raw row.
- `screen_by_generation.csv`, `cohort_phase_summary.csv`, `operator_emitted_by_generation.csv`: denominators, modes, per-generation screens, common-weight comparisons, and actual emitted operators.
- `candidate_confirmations.csv`, `operator_rates.csv`, `confirmation_origins.csv`: candidate-unit evidence and strict physical-genome rates.
- `dedup_conflicts.json`, `confirmation_join_anomalies.json`, `archive_reblend_diagnostics.csv`, `reblend_initial_vs_surviving.csv`: explicit unresolved/invalid joins and initial-versus-final reconstruction; no repair.
- `confirmed_top_rows.csv`, `image_shortlist.csv`, `film_selection_identity_checks.json`: exact candidate/phase/seed, film member locators, and checked selection identities.
- `audit_tables.json`, `source_manifest.json`, `history_notes.md`, `history_evidence.json`, `interpretation_source_pins.json`: machine-readable summaries and exact reviewed source pins.
- `VALIDATION.json`: independent checks of row identity, raw-score preservation, common-score arithmetic, candidate denominators, initial/final joins, film selections, and every small input hash.

Critical result/archive SHA256 pins:

| Source | SHA256 |
| --- | --- |
| island 1 settled results.json | b051be6572d441b25bd4d7696eae0d99583801ae1905c6ce7857f25285b71e26 |
| island 1 settled archive.json | 775161e0d7f8125cc9bfaefcbed290d1c492f4bef1714ab44a1877f6fbe05999 |
| island 1 settled state.json | 812bb47cd55514d7c2ca0b7068eec51d7d39f76b3844ac0a498a5341c06dff41 |
| isl1_final2.tgz (existing verified record) | 7ef7e373677750b16cef373623e1b6bbecd400cea312ba359a940fd5fe3f40c3 |
| island 2 settled results.json | 422f2ded50754aa71bd94da33c745f010e335f1b795b8ecda96a2856601afd5c |
| island 2 settled archive.json | eaa9b11e714f491a4b38244355ae178f5046ca077b94a49151f4e8308f8fe878 |
| island 2 settled state.json | e11d19e5db0dd984b0c56587b6211eff749928c9f79526f917d9b52d3b226357 |
| isl2_final2.tgz (existing verified record) | cb00bc78b38c7edf28cbb0a6128b721eec5a345810b26460f390992f72a68a81 |

The final deployed `pod_gen.py` SHA256 is `e1e52bac2847fcb8d0be99cc8f1d47cf7019de3914988e2e314959f7dd90dc3e`. The local launch generator is `1eb2277273338bd9fee441bcabc556eb2fc2ad8c5e0e7f55861311a55cbebdf7`. The final deployed `reblend_archive.py` is `8111730347b0fefcf0cb2d98b98a6420ea8cad26d8b41cffe3c4bed66ba3a160`. The final metric source is `2273a13f7de704234261c15f2886a57a1b68d017b196bf637e3c61db5fbd40c9`. Exact archive member names, config/log hashes, and source-line evidence are in `history_evidence.json` and `source_manifest.json`.
