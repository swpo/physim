# V3 continuation generator and archive-history audit

Local audit only. No remote action, simulation, full tar extraction, archive rewrite,
web-page edit, deletion, or commit was run. Only this note and
`history_evidence.json` were written, as authorized by the parent.
Small source members from the two local final snapshots were streamed into memory.
The JSON file contains the measured member SHA256 values, line snippets, data-file
SHA256 values, job counts, join variants, and all identity-mismatch locators.
Array indices below are **zero-based**. Code line numbers are one-based.

## 1. Actual generator history

Counts are **requested creative-screen slots per island per generation**, not
successful offspring and not confirmation rows.

| Period | W9 | mutate | mint_bilin | delete | add_chan | dup_act | SIC | immigrate | classical merge targets | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Gens 1–7 | .25 | 16 | 12 | 4 | 8 | 8 | 8 | 20 | 12 cross + 8 slow + 4 share = 24 | 100 |
| Gen 8 | .40 | 16 | 16 | 4 | 8 | 0 | 24 | 5 | 14 cross + 6 slow + 0 share = 20 | 93 |
| Gens 9–12 | .40 | 22 | 18 | 4 | 8 | 0 | 12 | 5 | 14 cross + 6 slow + 0 share = 20 | 89 |

Evidence:

- Baseline configs: `~/v3work/harvest/isl{1,2}_snap/island_config.json:11-25`.
  Baseline job shards are `.../out/jobs/g{1..7}_w0.json`.
- Gen-8 launch configs: `~/v3work/v3bundle/island_config_cont_{1,2}.json:11-25`.
  These exact members also exist in `~/v3work/v3contbundle.tgz`.
  Final snapshot `setup_cont.sh:8` copies the continuation config into place.
- Final configs: `~/v3work/ops/recovery_20260905/v3cont-{1,2}/settled/island_config.json:11-25`.
- Final snapshots `~/v3work/isl{1,2}_final2.tgz::campaign9.sh:2,8-9`
  explicitly say **resume at gen 9 after sic12/retry12 respec**, and run
  `pod_run_batch.sh 9 12`. Their `campaign.log:4` records the resume at
  `2026-09-04T22:24:52Z` / `2026-09-04T22:24:57Z`.
- Initial continuation `v3contbundle.tgz::v3bundle/pod_gen.py:195-203` requests
  `mix.merge_spatial_ic` slots with **60 retries per slot**. The final snapshot
  `isl{1,2}/pod_gen.py:203` uses **12 retries per slot**. This is the **only diff**
  between these generator sources. It is a cap per target, not 12 attempts per gen.
- In that generator, `mix, mmix = cfg["mix"], cfg["merge_mix"]` is at line153.
  Unary targets are at166-170, SIC targets at196-203, classical merge targets at
  **231-235**, and immigrants at282-287. **`mix.merge` is not read.** Its old
  value20 does not override `merge_mix=12+8+4`. `slow_tanh` can be relabeled
  `cross_edge` at252-253. Retry exhaustion can produce fewer jobs than targets.

Corrections:

1. SIC24 was used for **gen8 only**, not all gens8–12. SIC12/retry12 began at **gen9**,
   not gen10. Final config `_midcourse` at line40 says `gens10-12`; that note is stale.
2. Gen8→gen9 reallocates **mutate +6, mint_bilin +2** (16/16→22/18), not +6 each.
3. Old classical merge targets were24, not `mix.merge=20`; total old targets were100,
   not96. Continuation classical merge targets were20.
4. `HARVEST.md:34` gives `immigrate 40/gen->10` in a recommendation. Actual per-island
   values were20→5. `POST12_FACTS.json:246` describes the initial continuation only.
   Its headline and per-gen tables are still the old gens1–7 harvest, not settled12.
5. W9 changed .25→.40 in commit `4239d7a53180e4cc5b43f755ab2f046304bc7160`.
   Pilot `git:3b07d0b:.../complexity/metrics_v3.py:86` has W9=.25, and pilot
   `v3_postpass.py:23` hard-codes `.75*iv2+25*C9`. Final
   `isl{1,2}/lib/metrics_v3.py:86,713-715` has W9=.40; final postpass:23-25 uses it.

### Emitted jobs, directly counted from retained screen shards

| Island | g1–7 total | g8 total / SIC | g9 total / SIC | g10 total / SIC | g11 total / SIC | g12 total / SIC |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 690 | 81 / 22 | 72 / 2 | 69 / 2 | 70 / 5 | 72 / 3 |
| 2 | 686 | 82 / 23 | 70 / 1 | 72 / 7 | 68 / 4 | 67 / 1 |

The cross-island totals are1376 screens for gens1–7,163 for gen8,560 for gens9–12.
SIC screens total112,45,25 in those periods. Thus gen9–12 emitted only25 SIC children
from96 requested SIC targets. Do not use requested slots as successful-lane counts.
The retained driver logs independently report mutate16/mint16 at gen8 and
mutate22/mint18 starting at gen9 (island1 lines98-114; island2 lines110-120).

## 2. Archive reblend: exact behavior and its limits

`probes/blobs/l0/deepsearch/v3_pilot/reblend_archive.py:13-18` keeps only rows with
`status == "ok"` and non-null C9. It strips `_s2`, `_s3`, `_c9` from candidate names
and selects **highest stored `interest`**, keeping the first tie. This includes
screens, seed2, seed3 and c9fill; it does not choose deepest confirmation or max C9.
Lines21-33 join each archive entry by candidate name and update only
`interest`, `C9`, `C9_factors`, `spatial_class`, `c9_partial`, `interest_v2`, and
`_reblended_w9`. They do **not** validate or update the archive key, candidate,
genome, ghash, T_used, summary, seed2/3 scores, or seed2/3 flags.

Both final `campaign.log:2` report269 reblended entries and0 kept at restore.
After continuation,243/253 entries retain `_reblended_w9=.4`.
This audit reproduced the script join without executing the script or writing archives.
Using only pre-gen8 eligible rows gives the same selections for these surviving entries.

| Diagnostic, surviving marked entries | Island1 | Island2 |
|---|---:|---:|
| Entries checked | 243 | 253 |
| Score and C9 match exact script selection | 243 | 253 |
| Selected phase: screen / seed2 / seed3 / c9fill | 54 / 46 / 55 / 88 | 57 / 59 / 55 / 82 |
| Selected source has different ghash **and structural genome** | **11** | **18** |
| No same-model eligible row even within candidate-name group | 9 | 10 |
| Same-model alternative exists, but script chose another model | 2 | 8 |
| Archive key differs from selected row.cell | 173 | 179 |
| Of these, legacy six-axis keys | 100 | 100 |
| Of these, pilot seven-axis keys | 73 | 79 |
| Seven-axis key spatial suffix differs from copied spatial_class | 16 | 12 |
| Retained T_used differs from selected source T_used | 84 | 93 |
| Retained summary differs from selected source summary | 198 | 206 |
| A row with higher recomputed W9=.4 score exists in the name group | 13 | 14 |

The last row is an alternative-join diagnostic, not a requested repair. Script selection
uses **old stored interest**, not recomputed new-W9 interest. All670 settled archive
entries have non-null C9 and their own numeric `.6*interest_v2+40*C9` identity holds.
That supports a common numeric weight, **not common run/genome/cell provenance**.
The29 identity mismatches are27 imported-gen0 entries and two island2 pilot cells.
The two pilot cells are `p2g2_038` and `p2g7_039`, whose selected seed3 sources
actually carry colliding donor genomes (next section).

### All29 selected-source / archive-genome mismatches

`results[i]` means the corresponding settled `results.json` element. Archive keys
are in the same settled directory. The JSON evidence contains full keys, hashes,
phases, C9, scores, and row cells. Structural comparison uses acts/chans/W/K/bilin,
not display IDs or provenance strings.

| Isl | Archive key | Archive cand | Archive ghash | Selected results index / cand / ghash |
|---|---|---|---|---|
| 1 | `4 / grow / mobile / liquid / s2 / g1` | `p1g7_025` | `07854843ba8e93b1` | 1051 / `p1g7_025` / `de1b14c1d5bc2426` |
| 1 | `4 / switch / rotor / liquid / s1 / g2` | `p1g7_030` | `d2ee337cb598d2ef` | 1053 / `p1g7_030` / `3e9e387b61a8cb22` |
| 1 | `4 / grow / rotor / liquid / s2 / g2` | `p1g2_020` | `07440dda3d77d9a9` | 318 / `p1g2_020_s2` / `94568c24e2971139` |
| 1 | `4 / grow / rotor / liquid / s2 / g1` | `p1g7_032` | `f0c0d4119fa77126` | 1054 / `p1g7_032` / `53ba29b19dcd90c2` |
| 1 | `3 / constant / rotor / flicker / s1 / g2` | `p1g6_065` | `6ffe5602270e02e4` | 876 / `p1g6_065` / `d760747f84c5546f` |
| 1 | `2 / switch / rotor / liquid / s1 / g2` | `p1g2_008` | `6aef37d09adb821c` | 216 / `p1g2_008` / `2e7f82f20c7a06c0` |
| 1 | `4 / oscillator / mobile / liquid / s2 / g0` | `p1g2_008` | `a19e1629a9d1fb98` | 216 / `p1g2_008` / `2e7f82f20c7a06c0` |
| 1 | `3 / grow / mobile / liquid / s1 / g0` | `p1g2_021` | `67cf8460076bdd5b` | 316 / `p1g2_021_s2` / `cd3b802cf2dc17d5` |
| 1 | `3 / grow / mobile / liquid / s2 / g0` | `p1g2_034` | `65ee88a4e85ee72d` | 110 / `p1g2_034` / `158f0c237e4f658e` |
| 1 | `4 / grow / mobile / liquid / s1 / g0` | `p1g7_023` | `ae859cef82a541f9` | 1068 / `p1g7_023` / `eb5e4ef733bd5672` |
| 1 | `4 / grow / drift / frozen / s1 / g2` | `p1g5_022` | `e0c477a1df493566` | 701 / `p1g5_022` / `4716b0ed967ab0c9` |
| 2 | `3 / grow / rotor / liquid / s3 / g2` | `p2g6_020` | `489530b94bd868b0` | 856 / `p2g6_020` / `1cd25e1fb85243c5` |
| 2 | `4 / grow / rotor / flicker / s3 / g2` | `p2g3_073` | `6da2f3231522e927` | 582 / `p2g3_073_s2` / `97de45f90d6ebef4` |
| 2 | `4 / grow / mobile / flicker / s2 / g2` | `p2g5_023` | `84ec665a3a51196b` | 676 / `p2g5_023` / `95a88a754c64494b` |
| 2 | `4 / grow / drift / liquid / s1 / g2` | `p2g4_020` | `36456c27fa9e9db9` | 538 / `p2g4_020` / `3868b359bed4a6eb` |
| 2 | `2 / grow / rotor / liquid / s1 / g2` | `p2g4_062` | `37e5bf4d92c4be41` | 579 / `p2g4_062` / `f78b00513c33a9a3` |
| 2 | `2 / grow / mobile / liquid / s1 / g2` | `p2g4_053` | `8f894fb7b2f207f4` | 526 / `p2g4_053` / `fa86cb8089d048d0` |
| 2 | `4 / switch / mobile / flicker / s1 / g2` | `p2g2_070` | `3403b1a691db96ea` | 311 / `p2g2_070_s2` / `2ccd2e15c8fa6fb9` |
| 2 | `3 / switch / rotor / flicker / s1 / g2` | `p2g4_041` | `794646053eadd329` | 543 / `p2g4_041` / `61edc1e3803867c8` |
| 2 | `3 / grow / rotor / flicker / s2 / g2` | `p2g6_031` | `84226d894db71e93` | 880 / `p2g6_031` / `b2edf1a5811fbe08` |
| 2 | `3 / grow / rotor / liquid / s1 / g0` | `p2g2_023` | `18fb4a511bd5fd41` | 303 / `p2g2_023_s2` / `7fa13f78a42abf98` |
| 2 | `4 / grow / rotor / frozen / s1 / g2` | `p2g6_001` | `b10ebb5bb2a75e70` | 820 / `p2g6_001` / `48e236252e0117e2` |
| 2 | `4 / grow / still / frozen / s2 / g2` | `p2g4_015` | `04a0f0e5eb95cb51` | 744 / `p2g4_015_s2` / `a04fca4ed04a8fd9` |
| 2 | `4 / oscillator / mobile / liquid / s2 / g0` | `p1g2_008` | `a19e1629a9d1fb98` | 1226 / `p1g2_008_c9` / `6aef37d09adb821c` |
| 2 | `3 / grow / still / frozen / s2 / g2` | `p2g4_069` | `ae9d1473551424c6` | 547 / `p2g4_069` / `929650f101dbb962` |
| 2 | `3 / grow / drift / liquid / s2 / g2` | `p2g2_041` | `6d69c834bff5afd0` | 153 / `p2g2_041` / `2c35048f8d3575ac` |
| 2 | `2 / switch / mobile / liquid / s2 / g2` | `p2g4_002` | `bcc3072a07e51f96` | 736 / `p2g4_002_s2` / `583c31fd9c9b98d6` |
| 2 | `2 / switch / still / liquid / s1 / g2 / structured` | `p2g2_038` | `5c3b22eec22509f0` | 496 / `p2g2_038_s3` / `ad835d9583d074b2` |
| 2 | `3 / switch / drift / liquid / s1 / g2 / structured` | `p2g7_039` | `9e7b3a1d8d445359` | 1139 / `p2g7_039_s3` / `fa86cb8089d048d0` |

## 3. Why11 baseline seed3 rows use the wrong named-parent genome

This is a **candidate namespace collision**, not a continuation-only defect.
`pod_gen_batch.py:83-86` retains donor candidates/genomes/hashes during g0 import.
`pod_gen.py:157-164` starts fresh candidates in the same `p{island}g{gen}_{k:03d}`
namespace. Imported six-axis archive cells appear before the newly appended
seven-axis v3 cells.

`pod_lib.py:294-305` strips the `_s2` / `_s3` suffix, loops archive entries in order,
and returns the **first candidate-name match**, with no model or ghash check.
`pod_gen.py:375-393` then builds the seed3 job from that returned archive cell's
`genome`, **not the seed2 result's genome**. Donor models therefore become the
supposed third seed of an unrelated fresh screen with the same name.
The packaged pre-continuation `pod_lib.py` differs from the final source only by
the five added C9 archive-copy lines; this confirmation-matching code is unchanged.

For each of the11 mismatches, the donor lookup below has exactly the seed3 model
and ghash, while the fresh screen and seed2 use the other model. The donor source is
`~/v3work/harvest/isl{1,2}_snap/out/archive_seed.json`. Both copies share SHA256
`b74a35ddf3ecc8d503bc67decda36cea9f456aea89afdaed644f050f2274a253`.
Every listed row is already in the baseline results, unchanged. The entire baseline
results arrays are exact prefixes of their settled arrays.

| Isl | Base cand | Screen / seed2 ghash | Seed3 = donor ghash | Donor key | Settled screen / s2 / s3 indices |
|---|---|---|---|---|---|
| 1 | `p1g2_021` | `cd3b802cf2dc17d5` | `67cf8460076bdd5b` | `3 / grow / mobile / liquid / s1 / g0` | 202 / 316 / 527 |
| 1 | `p1g2_034` | `158f0c237e4f658e` | `65ee88a4e85ee72d` | `3 / grow / mobile / liquid / s2 / g0` | 110 / 275 / 621 |
| 1 | `p1g3_035` | `46505242674afd5a` | `a065779eaf3df961` | `4 / switch / mobile / liquid / s2 / g1` | 355 / 505 / 676 |
| 2 | `p2g2_023` | `7fa13f78a42abf98` | `18fb4a511bd5fd41` | `3 / grow / rotor / liquid / s1 / g0` | 186 / 303 / 486 |
| 2 | `p2g2_038` | `5c3b22eec22509f0` | `ad835d9583d074b2` | `2 / grow / mobile / liquid / s2 / g2` | 190 / 406 / 496 |
| 2 | `p2g2_070` | `2ccd2e15c8fa6fb9` | `3403b1a691db96ea` | `4 / switch / mobile / flicker / s1 / g2` | 169 / 311 / 517 |
| 2 | `p2g3_073` | `97de45f90d6ebef4` | `6da2f3231522e927` | `4 / grow / rotor / flicker / s3 / g2` | 351 / 582 / 655 |
| 2 | `p2g4_002` | `583c31fd9c9b98d6` | `bcc3072a07e51f96` | `2 / switch / mobile / liquid / s2 / g2` | 520 / 736 / 917 |
| 2 | `p2g4_015` | `a04fca4ed04a8fd9` | `04a0f0e5eb95cb51` | `4 / grow / still / frozen / s2 / g2` | 561 / 744 / 918 |
| 2 | `p2g4_030` | `2d9a00b0dec7e567` | `ca21e100b2dea0c3` | `4 / grow / mobile / flicker / s1 / g2` | 550 / 759 / 933 |
| 2 | `p2g7_039` | `9e7b3a1d8d445359` | `fa86cb8089d048d0` | `4 / grow / rotor / liquid / s3 / g2` | 1044 / 1109 / 1139 |

These rows remain measured runs of the stored genomes. They are **not valid third-seed
replications of the named fresh v3 screen genome**. Candidate-only ancestry or
confirmation-rate joins must retain this qualification. No row or archive was repaired.

### Duplicate c9fill identity

Island2 c9fill jobs55 and64 in
`~/v3work/harvest2/v3cont-2/isl2/out/jobs/c9fill_w0.json` both name
`p1g2_008_c9`, seed958, but come from two donor cells:

- `2|switch|rotor|liquid|s1|g2`, ghash `6aef37d09adb821c`.
- `4|oscillator|mobile|liquid|s2|g0`, ghash `a19e1629a9d1fb98`.

Their settled result indices are1226 and1209 respectively. `gen_c9backfill.py:16-24`
emits one job per cell, without deduplicating newly emitted names or checking model
identity in the `have` name set. The worker's `done` set is loaded before the new
jobs are grouped (`pod_worker_batch.py:374-380`), so both pending names survive.
Reblend selects result1226 for both cells; one selected-source model is wrong.
Also, NPZ filenames use candidate names (`pod_worker_batch.py:128-129`), so these
jobs share one output path. This audit does not establish duplicate-NPZ provenance.

## 4. SIC confirmation does not preserve the composed IC

SIC screen jobs set `ic_npz` at `pod_gen.py:224-227`. Seed2 construction:316-319 and
seed3 construction:389-393 copy genome/seed/t0/parents but **omit `ic_npz`**.
The worker loads a composed IC only for `job.ic_npz` at384-404 and passes it to the
batch only if `_ic` exists at121-123. Thus SIC confirmations are ordinary genome
reseeds, not repeats of the composed initial state. Their t0 floor can also differ.

In settled results, all90/92 SIC screens have `ic_merge=True`. All69/61
SIC-origin seed2/seed3 rows lack it (130 confirms total). Inspected retained confirm
jobs also omit `ic_npz`. Same-genome evidence must not be labeled same-IC assay
replication. The source code explains this independently of the namespace issue.

## 5. Key source SHA256 pins

Full measured file/member pins and line snippets are in `history_evidence.json`.
Final snapshot container digests below come from existing local verification
certificates; this child did not rehash the multi-GB containers.

| Source | SHA256 |
|---|---|
| `v3contbundle.tgz` | `9232f8d972c9ab360ddc7817de03650fadc144d636f38cded25a5391e6ab1e32` |
| Initial `v3bundle/pod_gen.py` (retry60) | `1eb2277273338bd9fee441bcabc556eb2fc2ad8c5e0e7f55861311a55cbebdf7` |
| Final `isl{1,2}/pod_gen.py` (retry12) | `e1e52bac2847fcb8d0be99cc8f1d47cf7019de3914988e2e314959f7dd90dc3e` |
| Final/repo `pod_lib.py` | `174bf52683df0f600d3dbe36f59289d74519bf1c1eec113ac9c4b59b6bf74d4a` |
| Final/repo `reblend_archive.py` | `8111730347b0fefcf0cb2d98b98a6420ea8cad26d8b41cffe3c4bed66ba3a160` |
| Final `lib/metrics_v3.py` | `2273a13f7de704234261c15f2886a57a1b68d017b196bf637e3c61db5fbd40c9` |
| Final `lib/v3_postpass.py` | `705be884b017aaa8e333942008f399e997b1bb6f2bc70c1301727e98c9452f48` |
| `isl1_final2.tgz::campaign9.sh` | `0cc8f184e5ba8b22d6bbcb022680b81d96d056685bc70c6893e0be11c3dec010` |
| `isl2_final2.tgz::campaign9.sh` | `5b2bcdb89fa3f9264bee7970c915d65b08d2b1aa3f251fe5ec753f92b902710b` |
| Settled island1 archive | `775161e0d7f8125cc9bfaefcbed290d1c492f4bef1714ab44a1877f6fbe05999` |
| Settled island2 archive | `eaa9b11e714f491a4b38244355ae178f5046ca077b94a49151f4e8308f8fe878` |
| Settled island1 results | `b051be6572d441b25bd4d7696eae0d99583801ae1905c6ce7857f25285b71e26` |
| Settled island2 results | `422f2ded50754aa71bd94da33c745f010e335f1b795b8ecda96a2856601afd5c` |
| `HARVEST.md` | `a1b8a743aef23ae97b584c70d42d27a1da2c6c8c7481565fa2ea094386bddc35` |
| `POST12_FACTS.json` | `6e96debbab443f630864e7cd890bd10bb662534df9c04d6c2ded8b5b298d9de8` |
| `isl1_final2.tgz` (certificate) | `7ef7e373677750b16cef373623e1b6bbecd400cea312ba359a940fd5fe3f40c3` |
| `isl2_final2.tgz` (certificate) | `cb00bc78b38c7edf28cbb0a6128b721eec5a345810b26460f390992f72a68a81` |


## 6. Initial reblend reconstruction, before continuation selection

The restore-time input is the original gen7 archive, **269 cells per island**:
`~/v3work/harvest/isl{1,2}_snap/out/archive.json`. Its hashes are in the JSON pins.
The historical row pools are settled `results.json` filtered to `gen<=7`.
They are exact prefixes of1267/1227 rows: original1179/1145 rows plus88/82 c9fill
rows. No gen8–12 row is used. Applying the literal highest-stored-interest join
reblends269/269 on each island, with0 entries kept for lack of a complete join.
This is a read-only reconstruction, not execution of the archive-writing script.

| Diagnostic | Initial isl1 | Surviving marked isl1 | Initial isl2 | Surviving marked isl2 |
|---|---:|---:|---:|---:|
| Archive entries | 269 | 243 | 269 | 253 |
| Selected source: screen | 60 | 54 | 66 | 57 |
| Selected source: seed2 | 58 | 46 | 63 | 59 |
| Selected source: seed3 | 63 | 55 | 58 | 55 |
| Selected source: c9fill | 88 | 88 | 82 | 82 |
| Wrong physical genome **and** ghash | 11 | 11 | 18 | 18 |
| Archive key differs from selected row.cell | 183 | 173 | 182 | 179 |
| Key mismatches in imported six-axis entries | 100 | 100 | 100 | 100 |
| Key mismatches in pilot seven-axis entries | 83 | 73 | 82 | 79 |

All29 initial wrong-model key/source-index pairs are exactly the29 surviving pairs
listed in section2. The26/16 initial entries replaced during continuation have
**zero** wrong-model joins and10/3 key mismatches. Thus the final survivor-only
counts do not hide an additional initial wrong-model population.

### Target seed is unavailable; compare known screen seeds separately

The `seed` field is absent from all538 initial archive entries and all670 final
archive entries. Therefore universal archive **target-seed correctness is
unavailable**, including the imported donor targets. Do not call a source seed
wrong merely because it differs from an island default or a later config.

A narrower comparison is possible where a historical `phase=screen` row has the
**exact same candidate name and physical genome** as the archive entry. This
exists uniquely for169/169 initial pilot entries per island (all status ok), and
for none of the100/100 imported entries. Compare the selected source's seed with
that observed screen's seed, not with an invented target seed:

| Screen-referenced seed comparison | Initial isl1 | Surviving isl1 | Initial isl2 | Surviving isl2 |
|---|---:|---:|---:|---:|
| Comparable exact-candidate/same-model screen rows | 169 | 143 | 169 | 153 |
| Selected-source seed differs from that screen | 118 | 98 | 113 | 106 |
| Selected-source seed equals that screen | 51 | 45 | 56 | 47 |
| Different-seed comparisons also select a wrong model | 0 | 0 | 2 | 2 |

The two island2 wrong-model cases remain `p2g2_038` and `p2g7_039`.
If selected sources must also match the physical model, initial differing-seed
counts are118/169 and111/167; surviving counts are98/143 and104/151.
These mostly show confirmation-source reseeds. They are **not** universal
wrong-target-seed counts and do not, on their own, mean a run was erroneous.
The JSON `initial_reblend` section records the denominators, phases, source-pool
bounds, and initial/survivor/replaced/imported/pilot splits.
